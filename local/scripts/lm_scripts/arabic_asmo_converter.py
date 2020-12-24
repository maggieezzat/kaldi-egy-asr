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



def conv_arab(line):
	words = line.strip().split(' ')
	temp_line=''
	for word in words:
		if word == 'L191':
			arab_word = '0'
		elif word == 'L192':
			arab_word = '1'
		elif word == 'L193':
			arab_word = '2'
		elif word == 'L194':
			arab_word = '3'
		elif word == 'L195':
			arab_word = '4'
		elif word == 'L196':
			arab_word = '5'
		elif word == 'L197':
			arab_word = '6'
		elif word == 'L198':
			arab_word = '7'
		elif word == 'L199':
			arab_word = '8'
		elif word == 'L200':
			arab_word = '9'
		elif word == 'L201':
			arab_word = '،'
		elif word == 'L202':
			arab_word = ':'
		elif word == 'L203':
			arab_word = '؛'
		elif word == 'L204':
			arab_word = '-'
		elif word == 'L205':
			arab_word = '+'
		elif word == 'L206':
			arab_word = '*'
		elif word == 'L207':
			arab_word = '('
		elif word == 'L208':
			arab_word = ''
		elif word == 'L209':
			arab_word = '='
		elif word == 'L210':
			arab_word = '%'
		elif word == 'L211':
			arab_word = '!'
		elif word == 'L212':
			arab_word = '/'
		elif word == 'L213':
			arab_word = '"'
		elif word == 'L214':
			arab_word = '؟'
		elif word == 'L215':
			arab_word = '.'
		elif word == ' ':
			arab_word = ' '
		elif word == 'L342':
			pass
		else:
			arab_word = word
		temp_line += (arab_word + ' ') 
		
		out_line = ''
		for letter in temp_line:
			if letter == 'A':
				out_line += 'ء'
			elif letter == 'B':
				out_line += 'آ'
			elif letter == 'C':
				out_line += 'أ'
			elif letter == 'D':
				out_line += 'ؤ'
			elif letter == 'E':
				out_line += 'إ'
			elif letter == 'F':
				out_line += 'ئ'
			elif letter == 'G':
				out_line += 'ا'
			elif letter == 'H':
				out_line += 'ب'
			elif letter == 'I':
				out_line += 'ة'
			elif letter == 'J':
				out_line += 'ت'
			elif letter == 'K':
				out_line += 'ث'
			elif letter == 'L':
				out_line += 'ج'
			elif letter == 'M':
				out_line += 'ح'
			elif letter == 'N':
				out_line += 'خ'
			elif letter == 'O':
				out_line += 'د'
			elif letter == 'P':
				out_line += 'ذ'
			elif letter == 'Q':
				out_line += 'ر'
			elif letter == 'R':
				out_line += 'ز'
			elif letter == 'S':
				out_line += 'س'
			elif letter == 'T':
				out_line += 'ش'
			elif letter == 'U':
				out_line += 'ص'
			elif letter == 'V':
				out_line += 'ض'
			elif letter == 'W':
				out_line += 'ط'
			elif letter == 'X':
				out_line += 'ظ'
			elif letter == 'Y':
				out_line += 'ع'
			elif letter == 'Z':
				out_line += 'غ'
			elif letter == 'a':
				out_line += 'ف'
			elif letter == 'b':
				out_line += 'ق'
			elif letter == 'c':
				out_line += 'ك'
			elif letter == 'd':
				out_line += 'ل'
			elif letter == 'e':
				out_line += 'م'
			elif letter == 'f':
				out_line += 'ن'
			elif letter == 'g':
				out_line += 'ه'
			elif letter == 'h':
				out_line += 'و'
			elif letter == 'i':
				out_line += 'ى'
			elif letter == 'j':
				out_line += 'ي'
			elif letter == ' ':
				out_line += ' '
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



def conv_arab_file(in_file, out_file, is_text=False):

    with open(out_file, 'w') as out:
        with open(in_file, 'r') as f:
            for line in f:
                if is_text:
                    line = line.strip().split(" ", 1)
                    fname = line[0]
                    text = line[1]
                    text = text.split()
                    out_line = ""
                    for word in text:
                        if word != "<UNK>":
                            out_line += conv_arab(word)
                        else:
                            out_line += word + " "
                    out.write(fname + " " + out_line.strip() + '\n')




def main():

    pass
    
if __name__ == "__main__":
    main()