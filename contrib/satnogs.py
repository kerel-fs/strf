import numpy as np
from datetime import datetime, timedelta


def read_ts_waterfall_file(fname):
    with open(fname) as f:
        cfreq = float(np.fromfile(f, dtype="float32", count=1)[0])
    
        # Read number of channels
        nchan = int(np.fromfile(f,dtype='float32',count=1)[0])
    
        # Read channel frequencies
        freq = np.fromfile(f,dtype='float32',count=nchan)/1000.0
    
        tv_sec = np.fromfile(f, dtype='uint32', count=1)[0]
        tv_usec = np.fromfile(f, dtype='uint32', count=1)[0]
        timestamp = datetime.utcfromtimestamp(tv_sec)
        timestamp += timedelta(microseconds=int(tv_usec))

        # Read entire file
        data = np.fromfile(f,dtype='float32').reshape(-1,nchan+1)
    return cfreq, nchan, freq, timestamp, data
