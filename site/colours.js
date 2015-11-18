
/* FIXME we need to decide on these colour graduations
 * the idea is:
      *     colour_range[0] is for  0 ..  9 %
 *     colour_range[1] is for 10 .. 19 %
 *     colour_range[2] is for 20 .. 29 %
 *     ...
 *     colour_range[8] is for 80 .. 89 %
 *     colour_range[9] is for 90 ..100 %
 *
 * currently using the light blue palette from
 *  http://www.google.com/design/spec/style/color.html#color-color-palette
 *
 *  FIXME I do really like this blue...
 *  [  0,   0, 255],
 */

var colour_range = [    /* 0 =  0 ..   9 % */
    [225,245,254,],
    /* 1 = 10 ..  19 % */
    [179,229,252,],
    /* 2 = 20 ..  29 % */
    [129,212,250,],
    /* 3 = 30 ..  39 % */
    [ 79,195,247,],
    /* 4 = 40 ..  49 % */
    [ 41,182,246,],
    /* 5 = 50 ..  59 % */
    [  3,169,244,],
    /* 6 = 60 ..  69 % */
    [  3,155,229,],
    /* 7 = 70 ..  79 % */
    [  2,136,209,],
    /* 8 = 80 ..  89 % */
    [  2,119,189,],
    /* 9 = 90 .. 100 % */
    [  1, 87,155,],
];

// default colour should never actually be used
var colour_default = [0, 0, 0];
// ongoing colour is for the current month, to show that the number is not yet final
var colour_ongoing = [138, 43, 226];

