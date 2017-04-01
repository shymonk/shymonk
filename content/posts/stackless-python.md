Title: Stackless Python 探秘
Date: 2016-06-01 22:00
Category: Python
Tags: stackless, python


提到stackless python， 相信很多人早已对其有所耳闻。作为Python解释器的另一种实现，其设计思路对整个Python世界产生了
深远影响。坦白的讲，我并没有大规模stackless python 的应用经验，本文意在对其背后实现原理进行探索。如果你和我一样对它感到好奇，欢迎深入阅读。


# stackless历史

- 1998年， 作者Christian Tismer便开始了Stackless Python 1.0版本的开发。作为雏形版本， Tismer 首次在Python中加入了`continuation` 这一抽象概念的实现。
- 2000年，以Stackless Python为背景的[PEP 0219](https://www.python.org/dev/peps/pep-0219/) 出现了。根据PEP的描述，Tismer希望Stackless 相关的代码能够成为Python核心的一部分。然而，他的这一提议在Python开发者当中备受争议。出于代码简洁性的考虑，一些开发者认为 stackless相关代码虽然功能强大但是晦涩难懂并且难以维护，加之其对于Jython并不兼容。最终，这一提议没有成为现实。
- 2002年，Stackless Python 2.0版本诞生。在这一版本中，Tismer彻底重写了代码并放弃了原有的`continuation` 实现。取而代之的是一种新的"一次性"`continuation` - `tasklets` 。
- 2004年，Stackless Python 3.0版本诞生。它包含2.0版本的全部功能并加入了一个重要概念： `soft-switching` 用于将程序的执行状态序列化（Pickling of Program State）。

其实，早在1999年stackless PEP被提出之前，Python核心开发者Sam Rushing便开发了一个直接通过切换`C-Stack` 实现的协程模块。然而，与stackless 一样，Python开发人员一致认为其不应该合并到Python核心代码中。理由很简单：由于各硬件平台和编译器对于`C-Stack` 的处理不尽相同，对于Python这样一种跨平台语言来说，添加平台依赖的代码将大大增加其移植的难度。
经过多年的发展，如今的Stackless Python已经摆脱了当初的麻烦。作为一个与`CPython`完全兼容的Package 被广大Python用户所使用。正如Tismer所说，"现在的Stackless只提供最干净的概念——`Microthreads`， 至于那些对稀奇古怪事物不感兴趣的人根本不会真正认识Stackless，只是碰巧它更快。"


# 为什么使用stackless?

关于stackless，不得不提到[协程(coroutine)](https://en.wikipedia.org/wiki/Coroutine)。对于大规模并发程序，传统的并发接口线程(Thread)和进程(Process)都有着较大的系统资源开销。与其相比，协程是一种更为自然并且低开销的并发解决方案。它被广泛应用于模拟器、游戏、异步IO以及其他事件驱动的编程模型中。然而，Python2.2之前的版本并没有实现对协程的支持，stackless的诞生正是为了解决这个问题。

# 并发模型

![coroutine concurrency model]({filename}/images/concurrency-model.png)

并发系统从本质上讲，是一系列独立的执行单元（`routine`）在调度器的调度之下交替执行。与线程相比，协程并发模型与其最大不同之处在于：

> 协程由应用程序实现调度，线程由操作系统实现调度

由于协程作为执行单元并发执行时，会因为主动放弃执行权限而被挂起，调度系统必须同时维护多个函数执行上下文，以实现非本地跳转（non-local jump）。


# stackless是如何工作的?

## Stackfull Python

为了更好的理解`stackless`，我们以下面这段代码为例，先简要介绍`stackfull`的`C-Python`解释器栈结构以及它是如何工作的。

```
def a(x):
    b(x + 1)

def b(x):
    c(x * x)

def c(x):
    print 'x=', x

a(42)
```

在Python shell中执行上面这段代码时，解释器中`C-stack`和`Python-stack`结构如下图。

![standard 'stackfull' python]({filename}/images/stackfull-python.png)

Python虚拟机以`eval_code2`作为解释函数执行`a`时，首先通过`PyFrame_New`构造`a`的栈帧`frame-a`并返回`eval_code2`，然后执行`a`对应的Python代码。由于`a`嵌套调用`b`，此时解释器递归调用`eval_code2`并重复之前过程执行`b`，从而形成`C-stack`和由`PyFrameObject`构成的`python-stack`。

## 范式转换

对于`stackfull`的标准Python而言，实现协程并发的核心在于将`Python-Stack` 与 `C-Stack`解耦，这种改变Python解释器执行过程的方法也被称作**范式转换**。要点可以归纳为以下三个方面：

1.函数栈帧执行时机    解释器执行`Python`函数的标准范式是：为函数的`PyCodeObject`构造一个函数栈帧`PyFrameObject`并附带所有参数，最后通过`eval_code2`解释执行相应的函数体直到其返回。

然而，以正确的调用顺序执行所有的函数栈帧并不意味着我们必须在当前`C-stack`嵌套层级中执行`eval_code2`。如果我们能够避免与`C-stack`相关的所有后续操作，就可以在函数栈帧执行前实现`C-stack`的退栈操作，从而达到解耦的目的。

2.参数生命周期
在标准python中，函数参数的引用由其上层调用者持有。这意味着只有下层函数返回后，其参数元组的引用才能被上层函数销毁。

现在，让我们换一种思维方式。很明显，函数参数应该与函数栈帧有着相同的生命周期，参数元组的引用也应该同函数栈帧一起被销毁。所以，我们在`PyFrameObject`结构中添加对参数元组的引用，就可以实现范式的转换。

3.系统状态
在标准python中，执行一个函数栈帧后的返回值会存在两种情况：

1. 返回`PyObject`代表函数正常执行。
2. 返回`NULL`代表函数抛出异常。

基于这两种基本系统状态，添加一个特殊的返回值类型`Py_UnwindToken`作为第三种系统状态，这样我们便可以在下层栈帧被执行之前实现`C-stack`退栈操作。

由于`Py_UnwindToken`与其他Python对象兼容，这一范式的转换对于大部分相关代码并不可见，我们只需要对执行栈帧的C函数做出修改即可。

Return Value   | 系统状态
:------------- | :-------
NULL           | 函数执行异常
Py_UnwindToken | 调度函数栈帧
Other PyObject | 作为正常结果返回

# 参考资料
- <http://archive.is/TwQEJ>
- <https://web.archive.org/web/20131005114137/http://www.onlamp.com/pub/a/python/2000/10/04/stackless-intro.html>
- <http://www.onlamp.com/pub/a/python/2002/02/14/pythonnews.html>
- <https://web.archive.org/web/20120508092636/http://islab.org/stackless/2007/stackless.html>
- <https://ep2013.europython.eu/conference/talks/the-story-of-stackless-python>
- <https://www.python.org/dev/peps/pep-0219/>
- <https://www.python.org/dev/peps/pep-0342/>
