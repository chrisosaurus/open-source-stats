open-source-stats
=================

This is a proof of concept for a website dedicated to presenting statistics on open source projects and their contributors.

This is an early work in progress.

demo
----

`make view` will open a browser with the current demo

![demo commit graph](resources/oos-demo.png )


full demo
----

If you want to see a full length demo including git cloning, data generation, and display you can run `make demo`

    chris@Ox1b open-source-stats(master)-> make demo
    ./scripts/demo.sh
    db 'oos.sqlite' already exists, deleting
    creating database 'oos.sqlite'
    success
    name is 'github.com_CausalityLtd_ponyc.git'
    fetching to 'repos/github.com_CausalityLtd_ponyc.git'
    name is 'github.com_rust-lang_rust.git'
    fetching to 'repos/github.com_rust-lang_rust.git'
    output generated to `site/index.html`, attempting to open in browser
    Created new window in existing browser session.

this will create a new db with a fresh schema, clone/update the testing project (here we use ponyc)
it then generates the statistics, and then opens the testing site in a browser showing those generated stats.

this will then open your browser of choice showing a page with the colouring graphs along with the graphs for the current
testing projects.

colour chart
------------

HELP WANTED

I am not a designer...

I want to make the graph bars colours to show percentages,
I also would like the right-most bar to be coloured to show it being 'in progress'

if you run `make generate` your browser should open to a page showing

![colour chart](resources/colour_chart.png )

These colours are currently based on the 'light blue' palette from http://www.google.com/design/spec/style/color.html#color-color-palette

the section below `colouring values` includes instructions on how to play with these colours

colouring values
----------------

HELP WANTED

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
        [225, 245, 254],

        /* 1 = 10 ..  19 % */
        [179, 229, 252],

        /* 2 = 20 ..  29 % */
        [129, 212, 250],

        /* 3 = 30 ..  39 % */
        [79, 195, 247],

        /* 4 = 40 ..  49 % */
        [41, 182, 246],

        /* 5 = 50 ..  59 % */
        [3, 169, 244],

        /* 6 = 60 ..  69 % */
        [3, 155, 229],

        /* 7 = 70 ..  79 % */
        [2, 136, 209],

        /* 8 = 80 ..  89 % */
        [2, 119, 189],

        /* 9 = 90 .. 100 % */
        [1, 87, 155],

    ];

    // default colour should never actually be used
    var colour_default = [0, 0, 0];
    // ongoing colour is for the current month, to show that the number is not yet final
    var colour_ongoing = [138, 43, 226];


this defines our colour range

you can generate the data for the colour_range block by looking at the script `scripts/gen_colour_palette.py`

it has the following at the top:

    mode = "hex"

    colours = [
        "E1F5FE",
        "B3E5FC",
        "81D4FA",
        "4FC3F7",
        "29B6F6",
        "03A9F4",
        "039BE5",
        "0288D1",
        "0277BD",
        "01579B",
    ]

this also supports an rgb mode:

    mode = "rgb"

which allows the following 3 rgb formats:

    # [r, g, b]
    colours = [
        [225, 245, 254],
        [179, 229, 252],
        [129, 212, 250],
        [79, 195, 247],
        [41, 182, 246],
        [3, 169, 244],
        [3, 155, 229],
        [2, 136, 209],
        [2, 119, 189],
        [1, 87, 155],
    ]


    # "r, g, b"
    colours = [
        "225, 245, 254",
        "179, 229, 252",
        "129, 212, 250",
        "79, 195, 247",
        "41, 182, 246",
        "3, 169, 244",
        "3, 155, 229",
        "2, 136, 209",
        "2, 119, 189",
        "1, 87, 155",
    ]

    #"r g b"
    colours = [
        "225 245 254",
        "179 229 252",
        "129 212 250",
        "79 195 247",
        "41 182 246",
        "3 169 244",
        "3 155 229",
        "2 136 209",
        "2 119 189",
        "1 87 155",
    ]


in all cases the output of this is

    var colour_range = [
         /* 0 =  0 ..   9 % */
         [225, 245, 254]

         /* 1 = 10 ..  19 % */
         [179, 229, 252]

         /* 2 = 20 ..  29 % */
         [129, 212, 250]

         /* 3 = 30 ..  39 % */
         [79, 195, 247]

         /* 4 = 40 ..  49 % */
         [41, 182, 246]

         /* 5 = 50 ..  59 % */
         [3, 169, 244]

         /* 6 = 60 ..  69 % */
         [3, 155, 229]

         /* 7 = 70 ..  79 % */
         [2, 136, 209]

         /* 8 = 80 ..  89 % */
         [2, 119, 189]

         /* 9 = 90 .. 100 % */
         [1, 87, 155]

    ];

which is suitable for placing into `site/graph.js`

you can run this via `make palette`

if you then update `site/graph.js` and run `make generate` you should have the colour chart open
in your browser


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


