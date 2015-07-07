# Schematic:

        ssh       ssh
    A ------> B ------> C
        ^          ^
     using A's   using B's
     ssh key     ssh key

# Preconditions:

A is running ssh-agent;
A can access B;
B can access C;
A's ssh public key is present in `B:~/.ssh/authorized_keys`
B's ssh public key is present in `C:~/.ssh/authorized_keys`

# HowTo

## Method 1 (Use ssh -t)

    A$ ssh -t B ssh C

## Method 2 (Use ProxyCommand)

    A$ vim ~/.ssh/config
    
    Host C
    ProxyCommand ssh -o 'ForwardAgent yes' B 'ssh-add && nc %h %p'

If your ssh private key on B is in a non-standard location(not `~/.ssh/id_rsa`), add its path after ssh-add.
You should now be able to access C from A:

    A$ ssh C
    C$

# Debug

Use multiple -v option to debugging connection, authentication, and configuration problems.

    A$ ssh -vvv C

# Example

    $ cat ~/.ssh/config
    Host sshproxy
    HostName 192.168.10.10
    User root
    
    Host target
    HostName 192.168.0.170
    User root
    ProxyCommand ssh -o 'ForwardAgent yes' sohuzk 'ssh-add && nc %h %p'
    
    $ ssh target 'tail -f /var/log/example.log'
