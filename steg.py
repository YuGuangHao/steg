#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import time
from PIL import Image
from argparse import ArgumentParser

ORDER = ""
R_C = ""
IFILE = ""
SFILE = ""
OFILE = ''.join(time.ctime()[11:19].split(':')) + ".png"
QR_MODE = False
IMAGE = None
QR_IMAGE = None
DAT = []

def add_and_process_args():
    global ORDER, R_C, IFILE, OFILE, SFILE, QR_MODE
    arg_parser = ArgumentParser(
        description="An image steganography utility that produces outputs compatible with StegSolve.jar analysis. Default steganography method: hide data by rows, in RGB order",
        add_help=False)
    arg_parser.add_argument("-h", "--help", action="store_true", help="Print this help message and exit")
    arg_parser.add_argument("-v", "--version", action="store_true", help="Print version info and exit")
    arg_parser.add_argument("-i", "--ifile", help="Specify input file")
    arg_parser.add_argument("-s", "--source", help="Specify data source file")
    arg_parser.add_argument("-o", "--ofile", help="Specify output filename, default: current_time.png")
    advanced_args = arg_parser.add_argument_group(title="Advanced Usage",
                                                  description="Specify a specific steganography method")
    advanced_args.add_argument("--plane_order", choices=["RGB", "RBG", "BRG", "BGR", "GBR", "GRB", "R", "G", "B", "RG", "GR", "RB", "BR", "GB", "BG"], default="R",
                               help="Set order, default R")
    advanced_args.add_argument("--method", choices=["column", "row"], default="row", help="Specify the method that you hide")
    advanced_args.add_argument("--qrcode", action="store_true",
                               help="Specify the source file as a QR code. If this option is selected, the QR code will be steganographically embedded into the layers of the image, rather than the data of the QR code itself. Note: Once this option is enabled, steganography can only be performed in a single channel.")
    args = arg_parser.parse_args()
    if args.help:
        arg_parser.print_help()
        sys.exit(0)
    if args.version:
        print("VERSION 0.0.1\nAuthor: sawd6")
        sys.exit(0)
    if not args.ifile:
        arg_parser.print_usage()
        print("\033[31mERROR: You haven't specify the IFILE yet!\033[0m")
        sys.exit(1)
    else:
        if args.ifile[-4:] != '.png' and args.ifile[-4:] != '.PNG':
            print("\033[31mPlease specify PNG file!\033[0m")
            sys.exit(1)
        else:
            IFILE = args.ifile
    if args.ofile:
        OFILE = args.ofile if args.ofile[-4:] == '.png' or args.ofile[-4:] == '.PNG' else args.ofile + '.png'
    else:
        print(f"\033[33mYou didn't specify the output filename so defaulting to {OFILE}\033[0m")
    if not args.source:
        arg_parser.print_usage()
        print("\033[31mPlease specify the source file!\033[0m")
        sys.exit(1)
    else:
        SFILE = args.source
    if args.qrcode:
        if len(args.plane_order) != 1:
            arg_parser.print_help()
            print("\033[31mPlease check the --plane_order!\033[0m")
            sys.exit(1)
        else:
            ORDER = args.plane_order
            QR_MODE = True
            if args.method == "column":
                # print("\033[33mYou selected column! Things may get different...\033[0m")
                R_C = args.method
    else:
        ORDER = args.plane_order
        R_C = args.method

def init_check():
    global DAT, IMAGE, QR_IMAGE
    try:
        IMAGE = Image.open(IFILE).convert('RGB')
        image_size = IMAGE.width * IMAGE.height * 3
    except Exception as e:
        print("\033[31m", e, "\033[0m")
        sys.exit(1)
    if QR_MODE:
        try:
            QR_IMAGE = Image.open(SFILE).convert('L')
        except Exception as e:
            print("\033[31m", e, "\033[0m")
            sys.exit(1)
        if QR_IMAGE.width * QR_IMAGE.height > image_size / 3:
            print("\033[31mThe QRCode you input is tooo BIG!\033[0m")
            sys.exit(1)
        for y in range(QR_IMAGE.height):
            for x in range(QR_IMAGE.width):
                DAT.append('0' if QR_IMAGE.getpixel((x, y)) == 0 else '1')
    else:
        try:
            with open(SFILE, 'rb') as sfile:
                sfile_data = sfile.read()
        except Exception as e:
            print("\033[31m", e, "\033[0m")
            sys.exit(1)
        if len(sfile_data) * 8 > image_size / 3 * len(ORDER):
            print("\033[31mThe file you input is tooo BIG!\033[0m")
            sys.exit(0)
        for i in sfile_data:
             DAT += list(format(i, '08b'))

def process(r_g_b):
    global DAT
    if len(DAT) == 0:
        return r_g_b
    result = list(format(r_g_b, '08b'))
    result[-1] = DAT.pop(0)
    return int(''.join(result), 2)

def steg_by_row():
    # print("row", ORDER)
    global IMAGE
    if QR_MODE:
        if QR_IMAGE.width > IMAGE.width:
            print("\033[31mYour QRCode Image's is tooo wide!\033[0m")
            sys.exit(1)
        flag = True
        for y in range(QR_IMAGE.height):
            for x in range(QR_IMAGE.width):
                r, g, b = IMAGE.getpixel((x, y))
                match ORDER:
                    case 'R':
                        r = process(r)
                    case 'G':
                        g = process(g)
                    case 'B':
                        b = process(b)
                IMAGE.putpixel((x, y), (r, g, b))

                if len(DAT) == 0:
                    flag = False
            if not flag:
                break
    else:
        flag = True
        for y in range(IMAGE.height):
            for x in range(IMAGE.width):
                r, g, b = IMAGE.getpixel((x, y))
                for i in ORDER:
                    if i == 'R': r = process(r)
                    elif i == 'G': g = process(g)
                    elif i == 'B': b = process(b)

                IMAGE.putpixel((x, y), (r, g, b))

                if len(DAT) == 0:
                    flag = False
            if not flag:
                break

def steg_by_col():
    global IMAGE
    if QR_MODE:
        if QR_IMAGE.width > IMAGE.height:
            print("\033[31mYour QRCode Image is tooo wide!\033[0m")
            sys.exit(1)
        print("\033[1;33mWarning! Something strange may happen...\033[0m")
        flag = True
        for x in range(QR_IMAGE.width):
            for y in range(QR_IMAGE.height):
                r, g, b = IMAGE.getpixel((x, y)) # changed here
                match ORDER:
                    case 'R':
                        r = process(r)
                    case 'G':
                        g = process(g)
                    case 'B':
                        b = process(b)
                IMAGE.putpixel((x, y), (r, g, b))

                if len(DAT) == 0:
                    flag = False
            if not flag:
                break
    else:
        flag = True
        for x in range(IMAGE.width):
            for y in range(IMAGE.height):
                r, g, b = IMAGE.getpixel((x, y))
                for i in ORDER:
                    if i == 'R': r = process(r)
                    elif i == 'G': g = process(g)
                    elif i == 'B': b = process(b)

                IMAGE.putpixel((x, y), (r, g, b))

                if len(DAT) == 0:
                    flag = False
            if not flag:
                break

def main():
    global IMAGE
    add_and_process_args()
    init_check()
    if R_C == "column":
        steg_by_col()
    else:
        steg_by_row()
    IMAGE.save(OFILE)

if __name__ == "__main__":
    main()
