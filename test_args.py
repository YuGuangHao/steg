#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from argparse import ArgumentParser

def main():
    arg_parser = ArgumentParser(description="An image steganography utility that produces outputs compatible with StegSolve.jar analysis\nDefault steganography method: hide data by rows, in RGB order", add_help=False)
    arg_parser.add_argument("-h", "--help", action="store_true", help="Print this help message and exit")
    arg_parser.add_argument("-v", "--version", action="store_true", help="Print version info and exit")
    arg_parser.add_argument("-i", "--ifile", help="Specify input file")
    arg_parser.add_argument("-s", "--source", help="Specify data source file")
    arg_parser.add_argument("-o", "--ofile", help="Specify output filename")
    advanced_args = arg_parser.add_argument_group(title="Advanced Usage", description="Specify a specific steganography method")
    advanced_args.add_argument("--order", choices=["RGB", "RBG", "BRG", "BGR", "GBR", "GRB"], default="RGB", help="Set order, default RGB")
    advanced_args.add_argument("--column", action="store_true", help="Hide information column by column")
    advanced_args.add_argument("--row", action="store_true", help="Hide information row by row")
    try:
        args = arg_parser.parse_args()
        print(args.ofile)
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()