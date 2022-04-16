import numpy as np

a = b'\xAA\xBB\xCC\xDD'
array = np.asarray(a)

print(len(list(bytes(array))))