#!/usr/bin/env python3
import argparse

from spectrum_parser import read_spectrum, write_spectra


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot RF observations')
    parser.add_argument('path',
                        type=str,
                        help='Path to the directory with the input files $PATH/x_???.bin')
    args = parser.parse_args()

    z, headers = read_spectrum(args.path)
    write_spectra('./out/', z, headers)
