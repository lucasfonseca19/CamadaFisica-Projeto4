from time import process_time_ns
import logmaker as logmaker
import numpy as np



a = b'\xAA\xBB\xCC\xDD'
b = np.array(a)
print(list(bytes(b)))