#!/usr/bin/python3

# can set to 'hex' or 'rgb'
mode = "hex"

# list of input hex or rgb colours
#
# in hex mode each entry should be:
#   "E1F5FE"
#
# in rgb mode each should be ANY of
#   [r, g, b]
#   "r g b"
#   "r, g, b,"
#
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

def hex_to_rgb(hex):
    r = hex[0:2]
    g = hex[2:4]
    b = hex[4:6]
    return [ int(r,16), int(g,16), int(b,16) ]

def rgb_str_to_list(rgbstr):
    parts = rgbstr.split()
    return parts

headers = [
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

def pretty_print(output):
    if len(output) != 10:
        print("Error: pretty_print output must be 10 elems")
        exit(1)

    # print open
    print("var colour_range = [")

    for i in range(0, 10):
        print("    ", headers[i])
        print("    ", output[i])
        print("")

    # print close
    print("];\n")


if __name__ == "__main__":
    if len(colours) != 10:
        print("Error: colour list must have 10 elems")
        exit(1)

    output = []

    for c in colours:
        if mode == 'hex':
            c = hex_to_rgb(c)
            if len(c) != 3:
                print("Error: hex list must have 3 elems")
                exit(1)
        elif mode == 'rgb':
            if type(c) == type([]):
                if len(c) != 3:
                    print("Error: rgb list must have 3 elems")
                    exit(1)
                # this is good!
                pass
            elif type(c) == type(""):
                # must convert to []
                c = rgb_str_to_list(c)
            else:
                print("Unsupported type for rgb")
                exit(1)
        else:
            print("Unsupported mode")
            exit(1)

        output.append(c)

    pretty_print(output)

