from pytube import YouTube
import sys

try: 
    yt = YouTube(sys.argv[1]) 
except: 
    print("Connection Error") 
    sys.exit()


stream = yt.streams.first()
if not stream:
    print("Erro")
    sys.exit()

try:
    stream.download(sys.argv[2])
except:
     stream.download()