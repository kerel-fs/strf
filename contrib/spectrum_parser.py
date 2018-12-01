from datetime import datetime
import numpy as np
import glob
import os
import re
from pathlib import Path


def read_spectrum(path):
    # Get the number of files
    filenames = glob.glob(os.path.join(path, '*.bin'))
    datestr = Path(filenames[0]).stem.split('_')[0]

    # Read first file to get the number of channels and number of "samples"
    filename = os.path.join(path, '{:s}_{:06}.bin'.format(datestr, 0))
    with open(filename, 'rb') as f:
        header = parse_header(f.read(256))

    zs = []
    headers = []
    for i_file in range(len(filenames)):
        filename = os.path.join(path, '{:s}_{:06}.bin'.format(datestr, i_file))
        # i_sub = 0
        with open(filename, 'rb') as f:
            next_header = f.read(256)
            while(next_header):
                headers.append(parse_header(next_header))
                zs.append(np.fromfile(f, dtype=np.float32, count=400))
                next_header = f.read(256)
    return np.transpose(np.vstack(zs)), headers


def write_spectra(path, zs, headers):
    nsub = int(headers[0]['nsub'])

    for i in range(int(np.ceil(len(headers)/nsub))):
        filename = headers[0]['utc_start'].strftime('%Y-%m-%dT%H:%M:%S_{:06d}.bin'.format(i))
        write_spectrum_file(os.path.join(path, filename),
                            np.transpose(zs[:,i * nsub:(i + 1) * nsub]),
                            headers[i * nsub:(i + 1) * nsub])


def write_spectrum_file(path, z, headers):
    with open(path, 'wb') as f:
        # write_spectrum(f, zs[:, 0], headers[:nsub])
        for z, header in zip(z, headers):
            f.write(write_header(header))
            f.write(z.astype('float32').tobytes())


def parse_header(header_b):
    # TODO. Support files with the additional fields
    #       - NBITS
    #       - MEAN
    #       - RMS
    # "HEADER\nUTC_START    %s\nFREQ         %lf Hz\nBW           %lf Hz\nLENGTH       %f s\nNCHAN        %d\nNSUB         %d\n"

    header_s = header_b.decode('ASCII').strip('\x00')

    regex = r"^HEADER\nUTC_START    (.*)\nFREQ         (.*) Hz\nBW           (.*) Hz\nLENGTH       (.*) s\nNCHAN        (.*)\nNSUB         (.*)\nEND\n$"
    match = re.fullmatch(regex, header_s, re.MULTILINE)

    utc_start = datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S.%f')

    return {'utc_start': utc_start,
            'freq': float(match.group(2)),
            'bw': float(match.group(3)),
            'length': float(match.group(4)),
            'nchan': int(match.group(5)),
            'nsub': int(match.group(6))}


def write_header(header):
    header_tmpl = 'HEADER\n' \
                  'UTC_START    {utc_start:%Y-%m-%dT%H:%M:%S.}{utc_start_ms:03d}\n' \
                  'FREQ         {freq:.6f} Hz\n' \
                  'BW           {bw:.6f} Hz\n' \
                  'LENGTH       {length:.6f} s\n' \
                  'NCHAN        {nchan}\n' \
                  'NSUB         {nsub}\nEND\n'
    header_str = header_tmpl.format(**header,
                                    utc_start_ms=int(header['utc_start'].microsecond/1e3))
    return header_str.encode('ascii').ljust(256, b'\x00')
