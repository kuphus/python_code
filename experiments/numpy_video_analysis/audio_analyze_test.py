import wave

with wave.open('test_audio@1591699628.2682886.wav') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    print('sampling rate:', framerate, 'Hz')
    print('length:', frames, 'samples')
    print('channels:', channels)
    print('sample width:', width, 'bytes')


    for i in range(frames):
        print(i, w.readframes(i))

