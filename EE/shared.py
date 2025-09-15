import threading
import multiprocessing
import numpy as np

cap_resolution = (1280, 960)
img_resolution = (960, 960)

therds_stop = threading.Event()
process_stop  = multiprocessing.Event()
