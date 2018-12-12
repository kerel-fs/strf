#!/usr/bin/env python3
import os
import argparse

from spectrum_parser import read_spectrum, write_spectra


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modify the freq stored in strf .bin files.')
    parser.add_argument('path',
                        type=str,
                        help='Path to the directory with the input files $PATH/x_???.bin')
    parser.add_argument('new_path',
                        type=str,
                        help='Output Path')
    parser.add_argument('new_freq', type=float, help='new frequency to be written')
    args = parser.parse_args()

    # Load all spectra
    z, headers = read_spectrum(args.path)

    # Modify freqency
    for h in headers:
        h['freq'] = args.new_freq

    # Create output directory
    if not os.path.exists(args.new_path):
        os.makedirs(args.new_path)

    # Save pectra with modified headers
    write_spectra(args.new_path, z, headers)
