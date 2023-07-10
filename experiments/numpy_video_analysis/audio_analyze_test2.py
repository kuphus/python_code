import numpy as np
import soundfile as sf



rms = [np.sqrt(np.mean(block**2)) for block in
       sf.blocks('test_empty.wav', blocksize=1024, overlap=512)]
average = sum(rms) / len(rms)
#print(rms)
print(average)
if(average > 0.001):
    print('there is sound')
else:
    print('no sound to be found')
