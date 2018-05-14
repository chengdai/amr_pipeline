import glob
import subprocess
import argparse

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def identify_taxonomy(f, metaphlan2, threads, bowtie2, out_path):
    print 'Finding taxonomic composition for file: {0}'.format(f.split('/')[-1])
    fastq_read_1 = f + '_quality_controlled_paired_1.fastq'
    fastq_read_2 = f + '_quality_controlled_paired_2.fastq'
    fastq_unpaired_1 = f + '_quality_controlled_unmatched_1.fastq'
    fastq_unpaired_2 = f + '_quality_controlled_unmatched_2.fastq'

    out_file = out_path + f.split('/')[-1] + '_taxonomy.txt'
    
    command = '{0} {1},{2},{3},{4} --nproc {5} --input_type fastq --ignore_viruses --ignore_eukaryotes --bowtie2_exe {6} --no_map  -t rel_ab_w_read_stats -o {7}'.format(metaphlan2, fastq_read_1, fastq_read_2, fastq_unpaired_1, fastq_unpaired_2, threads, bowtie2, out_file)
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for Metaphlan2 identification of taxonomy.')
    parser.add_argument('--fastq_folder',
                        help='path to folder containing quality controlled fastq files')
    parser.add_argument('--out',
                        help='folder for all MetaPhlan2 output files')
    parser.add_argument('--bowtie2',
                        help='path to Bowtie2 software')
    parser.add_argument('--metaphlan',
                        help='path to MetaPhlan2 software')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to use for MetaPhlan2')
    args = parser.parse_args()

    #Get all fastq file in folder (NOTE: fastq files should be QC'ed)
    fastq_folder = args.fastq_folder
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(fastq_folder + '*.fastq*')])
    out_path = args.out

    #metaphlan parameters
    bowtie2 = args.bowtie2
    metaphlan2 = args.metaphlan
    threads = args.threads

    for file_prefix in files:
        identify_taxonomy(file_prefix, metaphlan2, threads, bowtie2, out_path)

main()
