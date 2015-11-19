Sometimes we have to map a hostname to loopback address 127.0.0.1
by some reasons of development. This is a simple guide to show how
to do that on MacOS 10.10 Yosemite.

# Everythings starts with [hosts file](https://en.wikipedia.org/wiki/Hosts_(file))

Add the following line in `/etc/hosts`.

    127.0.0.1 test.domain.com

If your local port goes with `80`, this is all that you need to do.
But mostly we start a develop web server with `Non-80` port such as
`localhost:8080`. So port forwarding comes.

# Port Forwarding

From OS X 10.10, well-known [ipfw](https://en.wikipedia.org/wiki/Ipfirewall#cite_note-2) has been removed completely. So we
use [pf](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/pf.conf.5.html) which is the new recommanded way to do port forwarding.

First, add an anchor file `/etc/pf.anchors/com.custom` to contain the
port forwarding rule.

    rdr pass on lo0 inet proto tcp from any to 127.0.0.1 port 80 -> 127.0.0.1 port 8080

Then, add two lines to /etc/pf.conf to load your new rule.
It is important where these lines go.
Add this line right after rdr-anchor "com.apple/\*":

    rdr-anchor "custom"

Add this line directly after `load anchor "com.apple"` from `/etc/pf.anchors/com.apple":

    load anchor "pow" from "/etc/pf.anchors/com.custom"

Next, reload the rules into pf by running

    sudo pfctl -f /etc/pf.conf

Finally, enable `pf` by running

    sudo pfctl -e

Now, input `test.domain.com` into your browser address bar, it will works.
