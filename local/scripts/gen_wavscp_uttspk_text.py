import os
import random
import re
import numpy as np
from pydub import AudioSegment

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################



def save_duration(input_wav_scp_path, output_path, is_val=False):

    if not os.path.exists(output_path):
        os.makedirs("/".join(output_path.split("/")[:-1]))
    
    with open(input_wav_scp_path,'r') as f:
        with open(output_path,'w') as d:
            counter = 0
            for line in f.readlines():
                line = line.strip()
                id = line.split()[0]
                if is_val:
                    path = line.split()[1].replace('/home/rdi/kaldi-master-19-jun-2018-GPU-compiled/egs/Dr-Sherif/','waves/')
                else:
                    path = line.split()[1]
                try:
                    dur = AudioSegment.from_file(path).duration_seconds
                    d.write(id + ' ' + path + ' ' + str(dur) + '\n')
                    counter +=1
                    print('computing duration of wav file num: ',counter,end='\r')
                except:
                    d.write(id + ' ' + path + ' invalid\n')




################# Training Data Preprocessing #################
def preprocess_training_data(train_dir = 'data/train', threshold=12, coll_only=False, 
    durations_path='local/data/durations/train_wavs_durations.txt', long_utt_path='local/data/durations/train_long_utterances.txt'):
    text = {}
    waves_dict = {}

    with open('local/data/train/text', 'r') as f:
        for line in f:
            line = line.strip().split(" ", 1)
            if len(line) > 1:
                sent = line[1].strip()
                sent = re.sub(' SIL','',sent)
                text[line[0]] = sent.strip()

    total_dur = 0
    long_utt_dur = 0
    with open(durations_path,'r') as f:
        with open(long_utt_path, 'w') as out:
            counter = 0
            for line in f:
                line = line.strip()
                id = line.split()[0]
                path = line.split()[1]
                dur = int(float(line.split()[2]))
                if (coll_only and 'Colloquial-Waves' in path) or not coll_only:
                    total_dur += dur
                    if dur <= threshold:
                        waves_dict[id] = (id, path)
                        counter +=1
                        print('num of selected wavs: ', counter, end='\r')
                    else:
                        out.write(line + '\n')
                        long_utt_dur += dur
    
    hours, rem = divmod(total_dur, 3600)
    minutes, seconds = divmod(rem, 60)

    print('Train : total num of waves is',len(waves_dict))
    print('Train : total duration is {:0>2}:{:0>2}:{:0>2}'.format(int(hours),int(minutes),int(seconds)) )

    hours, rem = divmod(long_utt_dur, 3600)
    minutes, seconds = divmod(rem, 60)
    print('Train : long utterances duration is {:0>2}:{:0>2}:{:0>2}'.format(int(hours),int(minutes),int(seconds)) )

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)

    with open(train_dir + '/wav.scp', 'w') as wavscp:
        with open(train_dir + '/text', 'w') as text_out:
            with open(train_dir + '/utt2spk', 'w') as utt2spk:
                selected_waves = 0
                for wave_id in text.keys():
                    if wave_id in waves_dict:
                        selected_waves += 1
                        name = waves_dict[wave_id][0]
                        path = waves_dict[wave_id][1]
                        wavscp.write(name + " " + path + '\n')
                        text_out.write(name + " " + text[wave_id] + '\n')
                        utt2spk.write(name + " " + name + '\n')
    
    print('Train : total num of selected waves is',selected_waves)



################# Validation Data Preprocessing #################
def preprocess_validate_data(dev_dir = 'data/coll_dev_10', threshold=12,
    durations_path='local/data/durations/val_wavs_durations.txt', long_utt_path='local/data/durations/val_long_utterances.txt'):
    text = {}
    waves_dict = {}
    with open('local/data/coll_dev_10/text', 'r') as f:
        for line in f:
            line = line.strip().split(" ", 1)
            if len(line) > 1:
                sent = line[1].strip()
                sent = re.sub(' SIL','',sent)
                text[line[0]] = sent.strip()

    total_dur = 0
    with open(durations_path, 'r') as f:
        with open(long_utt_path, 'w') as out:
            counter = 0
            for line in f:
                line = line.strip()
                id = line.split()[0]
                path = line.split()[1]
                dur = int(float(line.split()[2]))
                total_dur += dur
                if dur <= threshold:
                    waves_dict[id] = (id, path)
                    counter += 1
                    print('num of selected wavs: ', counter, end='\r')
                else:
                    out.write(line + '\n')
    
    hours, rem = divmod(total_dur, 3600)
    minutes, seconds = divmod(rem, 60)

    print('Val : total num of waves is',len(waves_dict))
    print('Val : total duration is {:0>2}:{:0>2}:{:0>2}'.format(int(hours),int(minutes),int(seconds)) )

    if not os.path.exists(dev_dir):
        os.makedirs(dev_dir)

    with open(dev_dir + '/wav.scp', 'w') as wavscp:
        with open(dev_dir + '/text', 'w') as text_out:
            with open(dev_dir + '/utt2spk', 'w') as utt2spk:
                selected_waves = 0
                for wave_id in text.keys():
                    selected_waves += 1
                    name = waves_dict[wave_id][0]
                    path = waves_dict[wave_id][1]
                    wavscp.write(name + " " + path + '\n')
                    text_out.write(name + " " + text[wave_id] + '\n')
                    utt2spk.write(name + " " + name + '\n')
    print('Val : total num of selected waves is', selected_waves)




def main():
    #save_duration('local/data/train/wav.scp', 'local/data/durations/train_wavs_durations.txt')
    #save_duration('local/data/coll_dev_10/wav.scp', 'local/data/durations/val_wavs_durations.txt', is_val=True)
    #preprocess_training_data()
    #preprocess_validate_data()
    #preprocess_training_data(train_dir='data/train_coll', threshold=12, coll_only=True, 
    #    durations_path='local/data/durations/train_wavs_durations.txt', long_utt_path='local/data/durations/train_coll_long_utterances.txt')
    

if __name__=="__main__":
    main()

          