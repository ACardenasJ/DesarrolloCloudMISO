# import required modules
from os import path
import subprocess

#from pydub import AudioSegment
# py -m venv venv
# ./venv/Scripts/activate
# pip install pydub
# pip install ffmpeg-python
# assign files
input_file = "./kwest.mp3"
input_file_mp3 = "./kwest.mp3"
output_file_wav = "./sounds/sound_wav.wav"
output_file_ogg = "./sounds/sound_ogg.ogg"
output_file_aac = "./sounds/sound_aac.m4a"

# convert mp3 file to wav file
# sound = AudioSegment.from_mp3(input_file_mp3)
# sound.export(output_file_wav,format="wav")

# wma_version = AudioSegment.from_file(input_file_mp3, "mp3")
# sound.export(output_file_ogg,format="ogg")

# wma_version = AudioSegment.from_file(input_file_mp3, "mp3")
# sound.export(output_file_aac,format="aac")

#AAC
bashCommand = "ffmpeg  -i kwest.mp3 -c:a aac -vn ./sounds/KW.m4a"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

#WAV
bashCommand = "ffmpeg -i kwest.mp3 -acodec pcm_u8 -ar 22050 ./sounds/KW.wav"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

#OGG
bashCommand = " ffmpeg -y -i kwest.mp3  -strict -2 -acodec vorbis -ac 2 -aq 50 ./sounds/KW.ogg"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

#WMA
bashCommand = " ffmpeg -i kwest.mp3 ./sounds/KW.wma"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
