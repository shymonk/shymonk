Title: How To Customize Save In Django Admin Inline Form
Date: 2014-10-01 23:00:00 UTC+08:00


# Background

This is a common case in django ORM.

    from django.db import models
    
    class Author(models.Model):
        name = models.CharField(max*length=255)
    
    class Book(models.Model):
        name = models.CharField(max*length=255)
        author = models.ForeignKey(Author)

As a CMS, we are also required to provide a feature to create Author and
several Books for him together. So, the `admin` class is here:

    from django import forms
    
    class AuthorAdmin(object):
        form = [AuthorForm,]
        inlines = [BookInline,]
        form_layout = (
            ...
        )
    
    class BookInline(object):
        model = Book
        form = BookForm
        form_layout = (
            ...
        )
    
    class AuthorForm(forms.ModelForm):
        model = Author
    class BookForm(forms.ModelForm):
        model = Book

With this `BookInline`, you can get all things done without doubt.
But let't think about a special case:

> Assume that there's another Model `Press`, every author belongs to
> a press.
> 
> class Press(models.Model):
>     &#x2026;
> 
> When creating a author and add/update book to him, you also need
> to create/update the same one for the press, synchronously. May be
> it is a obvious bad design, but just a example.

So, how to do that?

# HowTo

Straightforward to say, you should customize `FormSet` for `BookInline`
and override these two methods:

-   `save_new_objects`
-   `save_existing_objects`

So, the `BookInline` will becomes

    from django.forms.models import BaseInlineFormSet
    
    class BookInline(object):
        model = Book
        form = BookForm
        fromset = BookFormSet
        form_layout = (
            ...
        )
    
    class BookInlineFormSet(BaseInlineFormSet):
        def save_new_objects(self, commit=True):
            saved_instances = super(BookInlineFormSet, self).save_new_objects(commit)
            if commit:
                # create book for press
            return saved_instances
    
        def save_existing_objects(self, commit=True):
            saved_instances = super(BookInlineFormSet, self).save_existing_objects(commit)
            if commit:
                # update book for press
          return saved_instances

# Why

## Traps

Inertia of thinking, we can override `save` function of `BookForm`
like this:

    class BookForm(models.ModelForm):
        ...
    
        def save(self, commit=True):
            instance = super(BookForm, self).save(commit)
            # do anything you want to sync book for Press

In fact that is a **mistake** I've made before, because `save` function of
`BookForm` instance is called with `commit=False`, it means book
instance is lacking attribute values. So, it can't be copied or do
anything else. I will give some hints to show that how django does it.

    # django/forms/models.py
    
    class BaseInlineFormSet(BaseModelFormSet):
        ...
        def save_new(self, form, commit=True):
            # Use commit=False so we can assign the parent key afterwards, then
            # save the object.
            obj = form.save(commit=False)
            pk_value = getattr(self.instance, self.fk.rel.field_name)
            setattr(obj, self.fk.get_attname(), getattr(pk_value, 'pk', pk_value))
            if commit:
                obj.save()
            # form.save_m2m() can be called via the formset later on if commit=False
            if commit and hasattr(form, 'save_m2m'):
                form.save_m2m()
            return obj

Moreover, it is worth mention that although `obj's` Foreignkey is saved above,

    setattr(obj, self.fk.get_attname(), getattr(pk_value, 'pk', pk_value))

you can not access it directly as following at downstream

    def save_new_objects(self, commit=True):
        saved_instances = super(BookInlineFormSet, self).save_new_objects(commit)
        if commit:
            book = saved_instances[0]
            author = book.author  # wrong way
        return saved_instances

Because django probably already **cached** a invalid author before.
In order to get a "fresh" author, use the primary key value of the
related object as stored in the db field instead.

    def save_new_objects(self, commit=True):
        saved_instances = super(BookInlineFormSet, self).save_new_objects(commit)
        if commit:
            book = saved_instances[0]
            author = Author.objects.get(pk=book.author_id)  # correct way
        return saved_instances

About caching ForeignKey in django, see [django doc](https://docs.djangoproject.com/en/dev/topics/db/queries/#one-to-many-relationships) for more details.
