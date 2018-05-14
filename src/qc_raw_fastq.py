import glob
import argparse
import subprocess

#run kneaddata on each file
def quality_control(file_prefix, human_ref, out_path, bowtie2, trimmomatic, threads):
    print 'Preprocessing file: {0}'.format(file_prefix.split('/')[-1])
    fastq_read_1 = file_prefix + '_1_sequence.fastq.gz'
    fastq_read_2 = file_prefix + '_2_sequence.fastq.gz'

    out_prefix = file_prefix.split('/')[-1] + '_quality_controlled'

    trimmomatic_options = '\"ILLUMINACLIP:' + '/'.join(trimmomatic.split('/')[:-1]) + 'adapters/NexteraPE-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:50\"'

    command = 'kneaddata --input {0} --input {1} -db {2} --bowtie2 {3} --trimmomatic {4} --trimmomatic-options {5} --threads {6} --output {7} --output-prefix {8} && rm {7}*contam* && rm {7}*trimmed* && mv {7}*log {7}log_files/'.format(fastq_read_1, fastq_read_2, human_ref, bowtie2, trimmomatic, trimmomatic_options, threads, out_path, out_prefix)
    print command
    #final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    #(stdout, stderr) = final.communicate()
    #print stdout
    #print stderr


def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for ShortBRED quantification identification of ARGs.')
    parser.add_argument('--raw_fastq_folder',
                        help='path to folder containing raw fastq reads')
    parser.add_argument('--out',
                        help='folder for all MetaPhlan2 output files')
    parser.add_argument('--human_ref',
                        help='path to human genome reference genome')
    parser.add_argument('--bowtie2_folder',
                        help='path to folder containing Bowtie2 software')
    parser.add_argument('--trimmomatic_folder',
                        help='path to folder containing Trimmomatic software')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to employ')
    args = parser.parse_args()

    fastq_folder = args.raw_fastq_folder
    files = set([f.split('_1_')[0] for f in glob.glob(fastq_folder + '*_1_*')])
    out_path = args.out
    human_ref = args.human_ref
    bowtie2 = args.bowtie2_folder
    trimmomatic = args.trimmomatic_folder
    threads = args.threads

    for file_prefix in files:
        quality_control(file_prefix, human_ref, out_path, bowtie2, trimmomatic, threads)

main()
