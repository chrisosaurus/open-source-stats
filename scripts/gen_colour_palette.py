#!/usr/bin/python3
import sys
import os

# this script allows the loading of palettes from files
# when invoked you must specify a palette
#       google-blue.hex
#       google-light-blue.hex
#       old-blue.rgb
#
# a hex file must be made up with one rgb hex file per line, like so:
#
#    chris@Ox1b open-source-stats(master)-> cat palettes/google-light-blue.hex
#    E1F5FE
#    B3E5FC
#    81D4FA
#    4FC3F7
#    29B6F6
#    03A9F4
#    039BE5
#    0288D1
#    0277BD
#    01579B
#
# a rgb file takes 3 values per line (r, g and then b)
# these values must be whitespace separated, commas are ignored
# leading and trailing whitespace are ignored:
#
#     chris@Ox1b open-source-stats(master)-> cat palettes/old-blue.rgb
#     227, 242, 253
#     187, 222, 251
#     144, 202, 249
#     100, 181, 246
#      66, 165, 245
#      33, 150, 243
#      30, 136, 229
#      25, 118, 210
#      21, 101, 192
#      13,  71, 161
#

def hex_to_rgb_list(hex):
    r = hex[0:2]
    g = hex[2:4]
    b = hex[4:6]
    return [
        "%3d" %(int(r,16)),
        "%3d" %(int(g,16)),
        "%3d" %(int(b,16))
    ]

def rgb_str_to_list(rgbstr):
    parts = rgbstr.split()
    out = []
    for part in parts:
        part = "%3d" %(int(part))
        out.append(part)
        print(part)
    return out

def parse_palette(path):
    colours = []
    if not os.path.exists(path):
        print("Error: failed to find palette at '" + path + "'")
        exit(1)

    mode = path[-3:]
    if mode != 'hex' and mode != 'rgb':
        print("Error: unsupported palette format '" + mode + "'")
        exit(1)

    lines = []
    with open(path, "r") as f:
        lines = f.readlines()

    if len(lines) != 10:
        print("Error: palette did not specify exactly 10 colours")
        exit(1)

    colours = []

    for line in lines:
        line = line.lstrip(" ")
        line = line.rstrip("\n")
        line = line.rstrip(" ")
        line = line.replace(",", " ")
        colour = None
        if mode == "rgb":
            colour = rgb_str_to_list(line)
        elif mode == "hex":
            colour = hex_to_rgb_list(line)
        else:
            print("Error: unsupported format")
            exit(1)
        colours.append(colour)

    if len(colours) != 10:
        print("Error: failed to parse 10 colour lines")
        exit(1)

    return colours


# example output:
#
#    var colour_range = [
#         /* 0 =  0 ..   9 % */
#         [225, 245, 254]
#
#         /* 1 = 10 ..  19 % */
#         [179, 229, 252]
#
#         /* 2 = 20 ..  29 % */
#         [129, 212, 250]
#
#         /* 3 = 30 ..  39 % */
#         [79, 195, 247]
#
#         /* 4 = 40 ..  49 % */
#         [41, 182, 246]
#
#         /* 5 = 50 ..  59 % */
#         [3, 169, 244]
#
#         /* 6 = 60 ..  69 % */
#         [3, 155, 229]
#
#         /* 7 = 70 ..  79 % */
#         [2, 136, 209]
#
#         /* 8 = 80 ..  89 % */
#         [2, 119, 189]
#
#         /* 9 = 90 .. 100 % */
#         [1, 87, 155]
#
#    ];

header = '''
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
'''

comments = [
    "/* 0 =  0 ..   9 % */",
    "/* 1 = 10 ..  19 % */",
    "/* 2 = 20 ..  29 % */",
    "/* 3 = 30 ..  39 % */",
    "/* 4 = 40 ..  49 % */",
    "/* 5 = 50 ..  59 % */",
    "/* 6 = 60 ..  69 % */",
    "/* 7 = 70 ..  79 % */",
    "/* 8 = 80 ..  89 % */",
    "/* 9 = 90 .. 100 % */",
]

footer = '''
// default colour should never actually be used
var colour_default = [0, 0, 0];
// ongoing colour is for the current month, to show that the number is not yet final
var colour_ongoing = [138, 43, 226];
'''

def pretty_print(f, output):
    if len(output) != 10:
        print("Error: pretty_print output must be 10 elems")
        exit(1)

    lines = []

    # print header
    lines.append(header)
    lines.append("\n")

    # print open
    lines.append("var colour_range = [")

    for i in range(0, 10):
        lines.append("    ")
        lines.append(comments[i])
        lines.append("\n")
        lines.append("    ")
        lines.append("[")
        for o in output[i]:
            o += ","
            lines.append(o)
        lines.append("],\n")

    # print close
    lines.append("];\n")

    # print footer
    lines.append(footer)
    lines.append("\n")

    f.writelines(lines)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Error: must specify palette file")
        exit(1)
    if len(args) > 2:
        print("Error: too many args, only take palette file")
        exit(1)
    palette = args[1]

    if not os.path.exists(palette):
        expanded_palette = os.path.join("palettes", palette)
        if not os.path.exists(expanded_palette):
            print("Error: failed to find palette, checked at '" + palette + "' and '" + expanded_palette + "'")
            print("Please see palettes/ for a list of available palettes")
            exit(1)
        palette = expanded_palette

    colours = parse_palette(palette)

    if len(colours) != 10:
        print("Error: colour list must have 10 elems")
        exit(1)

    target = "site/colours.js"
    with open(target, "w") as f:
        pretty_print(f, colours)


