import pandas, numpy, scipy, glob, argparse

def parse_readcount_metadata(readcount_metadata_file):
    #Create dictionary that stores number of reads in a sample, N, for each sample
    readcount_dict = {}
    with open(readcount_metadata_file, 'r') as readcount_f:
        for line in readcount_f:
            f_name, num_reads = line.strip().split()
            readcount_dict[f_name.split('_quality_controlled')[0]] = readcount_dict.get(f_name.split('_quality_controlled')[0], 0) + int(num_reads)
    return readcount_dict

def get_gene_variant_pos(row):
    return row.name.split('|')[1]
def get_gene(row):
    return row.name.split('|')[3]
def get_variant(row):
    return row.name.split('|')[4]

def variant_read_count(file_name, readcount_dict, suffix):
    base_file_name = file_name.split('/')[-1].split(suffix)[0]
    resistome_out_file = base_file_name + '_resistomes.txt'
    drug_class_out_file = base_file_name + '_antibiotic_classes.txt'

    df = pandas.read_table(file_name, sep = '\t', header = None)
    df.columns = ['query','target','id','evalue','qcov','tcov','ql','tl','bits']

    hits = df.groupby('target').count()['query']
    adjusted_marker_length = int(df['tl'].mean())*3
    
    N = readcount_dict[base_file_name]
    normalized = ((hits*(10**9))/(float(adjusted_marker_length)*N)).to_frame()
    normalized.columns = [base_file_name]
    return normalized

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for generating an single AMR variant abundance table for all samples.')
    parser.add_argument('--merged_blast_folder',
                        help='path to folder merged alignment results files')
    parser.add_argument('--suffix',
                        help='common suffix of the files')
    parser.add_argument('--out_prefix',
                        help='folder to output consolidated abundance table')
    parser.add_argument('--readcount_metadata',
                        help='path to file containing the read counts of fastq files of a sample')
    args = parser.parse_args()

    folder = args.merged_blast_folder
    suffix = args.suffix
    files = glob.glob(folder + '*' + suffix)
    read_count_metadata = args.readcount_metadata
    out_prefix = args.out_prefix

    readcount_dict = parse_readcount_metadata(read_count_metadata)

    abundance_table = variant_read_count(files[0], readcount_dict, suffix)
    for f in files[1:]:
        abundance_table = abundance_table.join(variant_read_count(f, readcount_dict, suffix), how = 'outer')
    abundance_table.sort_index().fillna(0).to_csv(out_prefix + '_amr_abundance.txt', sep = '\t')
main()
