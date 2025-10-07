import threading
import queue

therds_stop = threading.Event()
hsv_frame_queue = queue.Queue(maxsize=1)
