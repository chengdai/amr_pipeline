import pandas
import argparse

def generate_new_header_dict(blast_result):
    df = pandas.read_table(blast_result, sep ='\t', header = None)
    df.columns = ['query']
    df['new_header'] = 1
    print 'Number of sequences to subsets: {0}'.format(len(set(df['query'].values)))
    return df.set_index('query')['new_header'].to_dict()

def subset_reads(fasta_file, out_file, new_header_dict):
    out = open(out_file, 'w')
    with open(fasta_file) as in_file:
        write = False
        for line in in_file:
            if line[0] == ">":
                if new_header_dict.get(line.strip()[1:], None) != None:
                    write = True
                    out.write(line)
                else:
                    write = False
            elif line[0] != ">" and write == True:
                out.write(line)
    out.close()
    return None
                
def main():
    parser = argparse.ArgumentParser(description='Specify arguments for filtering and renaming the reference fasta headers.')
    parser.add_argument('--input',
                        help='path to input fasta file to be filtered and altered')
    parser.add_argument('--out',
                        help='filename for altered fasta')
    parser.add_argument('--headers',
                        help ='headers to subset the fasta files by')
    args = parser.parse_args()
    
    fasta_file = args.input
    out_file = args.out
    headers = args.headers
    
    new_header_dict = generate_new_header_dict(headers)
    subset_reads(fasta_file, out_file, new_header_dict)
    
main()
