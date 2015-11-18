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

![demo commit graph](https://raw.githubusercontent.com/mkfifo/open-source-stats/master/resources/oos-demo.png )

you can also just view the above graph from running `make view`

colouring values
----------------

HELP WANTED

I am not a designer...

I want to make the graph bars colours to show percentages,
I also would like the right-most bar to be coloured to show it being 'in progress'

in site/graph.js at the top we have

    /* FIXME we need to decide on these colour graduations
     * the idea is:
     *     colour_range[0] is for  0 ..  9 %
     *     colour_range[1] is for 10 .. 19 %
     *     colour_range[2] is for 20 .. 29 %
     *     ...
     *     colour_range[8] is for 80 .. 89 %
     *     colour_range[9] is for 90 ..100 %
     */
    var colour_range = [
        /* 0 =  0 ..   9 % */
        [  0, 191, 255],

        /* 1 = 10 ..  19 % */
        [  0, 154, 205],

        /* 2 = 20 ..  29 % */
        [ 30, 144, 255],

        /* 3 = 30 ..  39 % */
        [ 24, 116, 205],

        /* 4 = 40 ..  49 % */
        [ 72, 118, 255],

        /* 5 = 50 ..  59 % */
        [ 58,  95, 205],

        /* 6 = 60 ..  69 % */
        [ 16,  78, 139],

        /* 7 = 70 ..  79 % */
        [ 39,  64, 139],

        /* 8 = 80 ..  89 % */
        // FIXME this is my favourite colour
        // so I want things around this
        [  0,   0, 255],

        /* 9 = 90 .. 100 % */
        [ 25,  25, 112],
    ];

    // default colour should never actually be used
    var colour_default = [0, 0, 0];
    // ongoing colour is for the current month, to show that the number is not yet final
    var colour_ongoing = [138, 43, 226];


this defines our colour range


colour chart
------------

if you change the above colouring values and then run `make generate` your browser of choice should open to a page showing this graph

![colour chart](https://raw.githubusercontent.com/mkfifo/open-source-stats/master/resources/colour_chart.png )

I am not yet happy with these colours, I would love help tweaking them!

I particularly like this blue
![ideal blue](https://raw.githubusercontent.com/mkfifo/open-source-stats/master/resources/ideal_blue.png )


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


