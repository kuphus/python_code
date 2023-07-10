import subprocess


audio = 'Stereo Mix (Conexant ISST Audio)'
filename = 'test.wav'
length = 5
cmd = subprocess.run(['ffmpeg', '-f', 'dshow', '-i', f'audio="{audio}"', '-t', str(length), filename], capture_output=True)  #, check=True
#print(cmd.returncode)
#if cmd.returncode != 0:
#    print(cmd.stderr)
