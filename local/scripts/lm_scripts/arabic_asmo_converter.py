import os
import glob
from multiprocessing import Pool, cpu_count
from os import listdir, makedirs

def conv_asmo(line):
    out_line = ''
    line = line.strip()
    for letter in line:
        if letter == 'ء':
            out_line += 'A'
        elif letter == 'آ':
            out_line += 'B'
        elif letter == 'أ':
            out_line += 'C'
        elif letter == 'ؤ':
            out_line += 'D'
        elif letter == 'إ':
            out_line += 'E'
        elif letter == 'ئ':
            out_line += 'F'
        elif letter == 'ا':
            out_line += 'G'
        elif letter == 'ب':
            out_line += 'H'
        elif letter == 'ة':
            out_line += 'I'
        elif letter == 'ت':
            out_line += 'J'
        elif letter == 'ث':
            out_line += 'K'
        elif letter == 'ج':
            out_line += 'L'
        elif letter == 'ح':
            out_line += 'M'
        elif letter == 'خ':
            out_line += 'N'
        elif letter == 'د':
            out_line += 'O'
        elif letter == 'ذ':
            out_line += 'P'
        elif letter == 'ر':
            out_line += 'Q'
        elif letter == 'ز':
            out_line += 'R'
        elif letter == 'س':
            out_line += 'S'
        elif letter == 'ش':
            out_line += 'T'
        elif letter == 'ص':
            out_line += 'U'
        elif letter == 'ض':
            out_line += 'V'
        elif letter == 'ط':
            out_line += 'W'
        elif letter == 'ظ':
            out_line += 'X'
        elif letter == 'ع':
            out_line += 'Y'
        elif letter == 'غ':
            out_line += 'Z'
        elif letter == 'ف':
            out_line += 'a'
        elif letter == 'ق':
            out_line += 'b'
        elif letter == 'ك':
            out_line += 'c'
        elif letter == 'ل':
            out_line += 'd'
        elif letter == 'م':
            out_line += 'e'
        elif letter == 'ن':
            out_line += 'f'
        elif letter == 'ه':
            out_line += 'g'
        elif letter == 'و':
            out_line += 'h'
        elif letter == 'ى':
            out_line += 'i'
        elif letter == 'ي':
            out_line += 'j'
        elif letter == ' ':
            out_line += ' '
        elif letter == '-':
            pass
        elif letter == '_':
            pass	
        else:
            out_line += letter
    return out_line




def split_file_chunk(file_path ,chunk_size=268435456):
    
    head, tail = os.path.split(file_path)
    dir = os.path.join(head, tail.split(".")[0]+"_split")
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_number = 1
    with open(file_path) as f:
        chunk = f.readlines(chunk_size)
        while chunk:
            with open(dir + "/" + tail.split(".")[0]+ "_" + str(file_number) + ".txt", 'w') as chunk_file:
                for line in chunk:
                    chunk_file.write(line.strip()+'\n')
            
            print("Chunk: " + str(file_number))
            file_number += 1
            chunk = f.readlines(chunk_size)




def convert_file(in_file):
    '''
    Inputs: 
    in_file: Path to ASMO file to be converted
    '''

    mis_converted_chars = set()
    head, tail = os.path.split(in_file)


    root_dir = head.split('/')[0]
    data_set_type = head.split('/')[3]
    file_number = tail.split('.')[0].split('_')[-1]
    
    dir = 'local/data/lang_model/lm_corpus_clean_split_asmo'

    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except:
            pass
    
    file_path = dir + '/' + data_set_type + '_' + str(file_number) + '.txt'
    head, tail = os.path.split(in_file)
    file_number = tail.split('.')[0].split('_')[-1]

	#check if the converted file has been created before or not
    num_written_lines = 0
    if os.path.exists(file_path):
        print(f'***{tail} is resuming***')
        with open(file_path, 'r') as f:
            for line in f:
                num_written_lines += 1
        
        with open(file_path, 'a') as f:
            with open(in_file, 'r') as data:
                count = 0
                for line in data:
                    count += 1
                    if count > num_written_lines:
                        asmo_line = conv_asmo(line)
                        f.write("%s\n" % asmo_line)
    else:
        print(f'***{tail} is starting***')
        with open(file_path, 'w') as f:
            with open(in_file, 'r') as data:
                for line in data:
                    asmo_line = conv_asmo(line)
                    f.write("%s\n" % asmo_line)
    print(tail+' has been finished')




def merge_splits(files, output_file_path):

    with open(output_file_path,'w') as out:
        for file_ in files:
            with open(file_,'r') as f:
                for line in f:
                    out.write(line)




def main():

    split_file_chunk('local/data/lang_model/lm_corpus_clean.txt')
    
    files_names = glob.glob(os.path.join("local/data/lang_model/lm_corpus_clean_split", "*.txt"))    
    p = Pool(processes=cpu_count())
    p.map(convert_file,files_names)

    merge_splits(files_names, 'local/data/lang_model/lm_corpus_clean_asmo.txt')
    

    
if __name__ == "__main__":
    main()