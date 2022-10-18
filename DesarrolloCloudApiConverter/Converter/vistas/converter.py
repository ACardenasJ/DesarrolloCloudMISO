# import required modules
from os import path
import subprocess

input_file = "./kwest.mp3"
input_file_mp3 = "./kwest.mp3"
output_file_wav = "./sounds/sound_wav.wav"
output_file_ogg = "./sounds/sound_ogg.ogg"
output_file_aac = "./sounds/sound_aac.m4a"




#MP3 to WAV
bashCommand = "ffmpeg -i kwest.mp3 -acodec pcm_u8 -ar 22050 ./sounds/KW.wav"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#MP3 to WMA
bashCommand = "ffmpeg -i kwest.mp3 ./sounds/KW.wma"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#WAV to MP3
bashCommand = "ffmpeg -i kwest.wav -vn -ar 44100 -ac 2 -b:a 192k ./sounds/KW.mp3"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#WAV to WMA
bashCommand = "ffmpeg -i kwest.wav ./sounds/KW.wma"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#WMA to MP3
bashCommand = "ffmpeg -i kwest.wma -f mp3 -ab 192 ./sounds/KW.mp3"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#WMA to WAV
bashCommand = "ffmpeg -i kwest.wma ./sounds/KW.wav"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#MP3 to AAC
bashCommand = "ffmpeg  -i kwest.mp3 -c:a aac -vn ./sounds/KW.m4a"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#MP3 to OGG
bashCommand = " ffmpeg -y -i kwest.mp3  -strict -2 -acodec vorbis -ac 2 -aq 50 ./sounds/KW.ogg"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()