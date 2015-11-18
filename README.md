open-source-stats
=================

This is a proof of concept for a website dedicated to presenting statistics on open source projects and their contributors.

This is an early work in progress.

demo
----

to see a running demo you can invoke `make demo`

    [chris@heimdall open-source-stats]$ make demo
    db 'oos.sqlite' already exists, deleting
    creating database 'oos.sqlite'
    success
    name is 'github.com_CausalityLtd_ponyc.git'
    fetching to 'repos/github.com_CausalityLtd_ponyc.git'
    Created new window in existing browser session.

this will create a new db with a fresh schema, clone/update the testing project (here we use ponyc)
it then generates the statistics, and then opens the testing site in a browser showing those generated stats.

which shows the following graph:

![demo commit graph 2015-11-18](https://raw.githubusercontent.com/mkfifo/open-source-stats/master/resources/oos-demo-2015-11-18.png )

you can also just view the above graph from running `make view`

deps
----

 * python3
 * sqlite3
 * libgit2
 * python cffi
 * pygit2

license
-------

This works is licensed under the GPL version 3


