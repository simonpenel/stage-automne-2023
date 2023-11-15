import argparse

parser = argparse.ArgumentParser(description='Reads hmm_search tab output file and writes another file with tab separator instead of whitespaces')

parser.add_argument('-i', '--input', type=str, required=True, help='HMM_search -domtblout file path')
parser.add_argument('-o', '--output', type=str, required=True, help='Processed file path')
parser.add_argument('-s', '--synthesis', type=str, required=True, help='1 line only for each query (best match and whole domain alignment coordinates)\
                                                                        synthetic file path')
args = parser.parse_args()

with open(args.input) as reader, open(args.output, 'w') as writer:
    for line in reader.readlines():
        if line.startswith('#'):
            del(line)
        else:
            for elt in line.split(maxsplit=23):
                writer.write(f"{elt.strip()}\t")
            writer.write('\n')

with open(args.output) as reader, open(args.synthesis, 'w') as writer:
    seq_ID = ''
    newline = ''
    for line in reader.readlines(): 
        current_seq_ID = line.split('\t')[0]
        if current_seq_ID != seq_ID:
            seq_ID = current_seq_ID
            writer.write(newline + '\n')
            newline = ''
            for elt in line.split(maxsplit=23):
                newline += f"{elt.strip()}\t"
        else:
            line_data = line.split(maxsplit=23)
            newline_data = newline.split('\t')
            evalue = line_data[12]
            start = line_data[17]
            end = line_data[18]
            newline_data[12] = str(min(float(evalue), float(newline_data[12])))
            newline_data[17] = str(min(int(start), int(newline_data[17])))
            newline_data[18] = str(max(int(end), int(newline_data[18])))
            newline = '\t'.join(newline_data)    
    writer.write(newline + '\n')
        



        
