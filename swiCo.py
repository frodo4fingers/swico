#!/usr/bin/env python
# encoding: UTF-8

import sys, re, os, shutil
import time, datetime
from PIL import Image
# from dominant_colour import most_frequent_colour as mfc
from dominant_colour import average_colour as ac


def rgb2hex(rgb):
    return "#%02x%02x%02x" % rgb


def backUpStuff(stuff, verbose):
    """
        will save a copy from given file with timestamp
    """
    stamp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")

    newstuff = (stuff + ".bak_" + stamp)
    shutil.copy(stuff, newstuff)
    if verbose:
        print("backed %s up as %s" % (stuff, newstuff))


def getActiveTheme(path_r, verbose):
    """
        function just to read out the rc.xml to know what is what
    """

    names = []
    with open(path_r, "r") as rc:
        for line in rc:
            # i actually dont know if every rc.xml has this structure...
            # goal is to have the line right under <theme> where the theme itself
            # is written
            if "<name>" in line or "<theme>" in line:
                names.append(line)
                if len(names) == 2:
                    break

        rc.close()

    if "theme" in names[0] and "name" in names[1]:
        theme = (re.split("\W+", names[1]))[2]
    else:
        print("ERROR: something went wrong catching the current theme")

    if verbose:
        print("found %s as current theme" % (theme))

    return theme


def getCurrentWallpaper(path_n, verbose):
    """
        read the bg-saved.cfg and receive the path of current wallpaper
    """

    with open(path_n, "r") as config:

        for line in config:
            if "file=" in line:
                wallpaper = line.split("=")[1].replace("\n", "")
                break

    if verbose:
        print("found %s as wallpaper" % (wallpaper))
    return wallpaper


def getColor(wallpaper, verbose):
    """
        get colors with dominant_colour from ZeevG
        https://github.com/ZeevG/python-dominant-image-colour
    """

    # return rgb2hex(mfc(Image.open(wallpaper)))
    return rgb2hex(ac(Image.open(wallpaper)))


def editThemerc(path, fg, bg, verbose):
    """
        will edit the colors of obmenu
    """
    # back this up before something goes wrong
    backUpStuff(path, verbose)

    item = [
        "menu.border.color:",
        "menu.items.active.bg.color:",
        "menu.items.active.bg.colorTo:",
        "menu.items.active.bg.border.color:",
        "menu.items.bg.color:"
    ]

    with open(path, "r") as current_file:
        with open(path + "_tmp", "w") as new_file:

            for line in current_file:

                if item[0] in line:
                    new_file.writelines(item[0] + " " + bg + "\n")

                elif item[1] in line:
                    new_file.writelines(item[1] + " " + bg + "\n")

                elif item[2] in line:
                    new_file.writelines(item[2] + " " + bg + "\n")

                elif item[3] in line:
                    new_file.writelines(item[3] + " " + bg + "\n")

                elif item[4] in line:
                    new_file.writelines(item[4] + " " + fg + "\n")

                else:
                    new_file.writelines(line)

            new_file.close()
        current_file.close()
    os.rename(path + '_tmp', path)


def editDmenu(path, fg, bg, verbose):
    """
        will edit the colors of dmenu in rc.xml
    """
    # back this up before something goes wrong
    backUpStuff(path, verbose)

    with open(path, "r") as current_file:
        with open(path + "_tmp", "w") as new_file:

            for line in current_file:
                if "dmenu_run" in line:
                    # rewrite the whole line is much easier
                    # " "*8 is the whitespace in order to maintain the xml structure
                    new_file.writelines(" "*8 + "<command>dmenu_run -p 'WHAT' -sb '%s' -nb '%s' -nf '%s'</command>\n" % (bg, fg, bg))

                    if verbose:
                        print("changed colors in dmenu")

                else:
                    new_file.writelines(line)

            new_file.close()
        current_file.close()
    os.rename(path + '_tmp', path)


def editGTKrc(path, fg, bg, verbose):
    """
        edit selected color in gtk source
    """
    # back this up before something goes wrong
    backUpStuff(path, verbose)

    with open(path, "r") as current_file:
        with open(path + "_tmp", "w") as new_file:

            for line in current_file:
                if "# Background, base." in line:

                    new_file.writelines('gtk_color_scheme = "bg_color:#d4d4d4\\nselected_bg_color:%s\\nbase_color:#F7F7F7" # Background, base.\n' % (bg))

                    if verbose:
                        print("changed colors in gtkrc")

                else:
                    new_file.writelines(line)

            new_file.close()
        current_file.close()
    os.rename(path + '_tmp', path)


def removeBackUps(pathThemerc, pathDMenu, pathGTKrc, verbose):
    """
        remove all the backed up files that were produced during the changes of
        wallpaper or color
    """

    for item in (pathThemerc, pathDMenu, pathGTKrc):
        path = item
        path = path.split("/")[:-1]
        path = "/".join(path)
        path = path + "/"

        filelist = [f for f in os.listdir(path) if ".bak_" in f]
        for f in filelist:
            os.remove(path + f)

        if verbose:
            print("deleted %i items in %s" % (len(filelist), path))


def main(argv):
    """
        here to handle stuff
    """

    import argparse

    parser = argparse.ArgumentParser(description="this script is able to change the colors of ObMenu, DMenu and pcmanfm (at least at my laptop) out of the obmenu itself", epilog="running on antergos/arch linux with openbox", prog="swico")

    parser.add_argument("-b",
        dest="background",
        help="selected item color",
        # change here for default selected color
        default="#D54836")

    parser.add_argument("-f",
        dest="foreground",
        help="foreground color",
        # change here for default foreground color
        default="#f7f7f7")

    parser.add_argument("-i",
        dest="image",
        help="take selescted color from wallpaper",
        action="store_true")

    parser.add_argument("--remove",
        dest="remove",
        help="remove all backed up files",
        action="store_true")

    parser.add_argument("--path_n",
        dest="path_n",
        help="path to bg-saved.cfg of nitrogen to get current set wallpaper and path",
        default="/home/frodo/.config/nitrogen/bg-saved.cfg")

    parser.add_argument("--path_r",
        dest="path_r",
        help="path to rc.xml to get the used theme",
        default="/home/frodo/.config/openbox/rc.xml")

    parser.add_argument("--path_t",
        dest="path_t",
        help="path to .themes to get stuff started",
        default="/home/frodo/.themes/")

    parser.add_argument("-v",
        dest="verbose",
        help="console output",
        action="store_true")

    args = parser.parse_args()

    if args.image:
        wallpaper = getCurrentWallpaper(args.path_n, args.verbose)

        fg = args.foreground
        bg = getColor(wallpaper, args.verbose)

    else:
        fg = args.foreground
        bg = args.background

    theme = getActiveTheme(args.path_r, args.verbose)

    if args.remove:
        removeBackUps(args.path_t + theme + "/openbox-3/themerc", args.path_r, args.path_t + theme + "/gtk-2.0/gtkrc", args.verbose)

        sys.exit()

    editThemerc(args.path_t + theme + "/openbox-3/themerc", fg, bg, args.verbose)
    editDmenu(args.path_r, fg, bg, args.verbose)
    # editGTKrc(args.path_t + theme + "/gtk-2.0/gtkrc", fg, bg, args.verbose)

    os.system("openbox --reconfigure")



if __name__ == "__main__":
    main(sys.argv[1:])
