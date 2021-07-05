from decouple import config

# Path to TLE
# Filename convention: {TLE_DIR}/{observation_id}.txt
TLE_DIR = config('SATNOGS_TLE_DIR')

# absulute frequency measurement storage
# Filename convention: {OBS_DIR}/{observation_id}.txt
OBS_DIR = config('SATNOGS_OBS_DIR')

# SATTOOLS/STRF/STVID sites.txt file
SITES_TXT = config('SATNOGS_SITES_TXT')
