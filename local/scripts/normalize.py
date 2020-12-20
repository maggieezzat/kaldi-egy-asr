import sys
import shutil
def normalize(input_file):
    output_string = ""
    with open(input_file, 'r') as f:
        for line in f:
            for i, word in enumerate(line.split()):
                if (i == 0):
                    output_string += word
                else:
                    output_string += " " + word.replace("i", "j").replace("I", "g").replace("E", "G").replace("C", "B").replace("B", "G")
            output_string += "\n"

    text_file = open("normalized_output.txt", "w")
    text_file.write(output_string)
    text_file.close()
    
    shutil.copyfile(input_file, "input_safe.txt") #copy src to dst
    shutil.copyfile("normalized_output.txt", input_file) #copy src to dst

if __name__ == "__main__":
    input_file = sys.argv[1]
    normalize(input_file)