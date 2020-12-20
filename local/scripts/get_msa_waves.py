
#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

#get the waves from msa dataset only
with open('local/data/wav_all.scp', 'r') as f:
    with open('local/data/wav_msa.scp', 'w') as out:
        for line in f:
            if "Waves/msa/waves/" in line:
                line = line.strip().split()
                id = line[0]
                name = line[1].split("/")[-1]
                out.write(id + " " + name + '\n')
