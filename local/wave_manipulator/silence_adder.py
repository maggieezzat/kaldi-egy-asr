
from wave_manipulator import wave_manipulator as wm
import glob
import os
import sys

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################


input_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.exists(output_path):
    os.makedirs(output_path)

files = glob.glob(os.path.join(input_path, "*.wav"))
print(os.path.join(input_path, "*.wav"))
total = len(files)
print(total, " files")
i=0
for _file in files:
    i+=1
    print("Processing File: " + str(i) + "/" + str(total), end='\r')
    try:
        dummy = wm(_file)
        dummy.add_silence_beginning_and_end(400, 400)
        dummy.export_file(os.path.join(output_path, os.path.basename(_file)))
    except:
        raise Exception("Bad file: " + _file)
