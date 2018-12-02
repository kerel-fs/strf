#!/usr/bin/env python3
import sys
import numpy as np
from satnogs import read_ts_waterfall_file
from spectrum_parser import write_header, parse_header, write_spectra_file
from datetime import timedelta

# Get filename
fname=sys.argv[1]

cfreq, nchan, freq, utc_start, data = read_ts_waterfall_file(fname)

tc_usec = utc_start.microsecond
cfreq = 437.375e6

# Get time
t=data[:,:1]

# Get spectra
spec=data[:,1:]

# Get extrema
fmin,fmax=np.min(freq),np.max(freq)
tmin,tmax=np.min(t),np.max(t)
nsub = 60
nfiles = int(np.ceil(spec.shape[0]/nsub))
timestamp = utc_start
for file_nr in range(nfiles):
    ts = t[file_nr * nsub:(file_nr + 1) * nsub][:,0]
    specs = spec[file_nr * nsub:(file_nr + 1) * nsub,:]
    
    j = 0
    t0 = 0
    headers = []
    for j in range(int(np.ceil(len(ts)))):
        t1 = ts[j]
        header = {'utc_start': timestamp,
                  'freq': cfreq,
                  'bw': np.ceil(fmax-fmin),
                  'length': t1-t0,
                  'nchan': nchan,
                  'nsub': nsub}
        headers.append(header)
        timestamp += timedelta(seconds=float(t1-t0))
        t0 = t1
    
    # for spectrum, header in zip(specs, headers):
    #     print(spectrum, header)
    filename = utc_start.strftime('%Y-%m-%dT%H:%M:%S_{:06d}.bin'.format(file_nr))
    write_spectra_file('./out_satnogs/', filename, np.transpose(specs), headers)
