import glob
import subprocess
import argparse

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def identify_taxonomy(f, threads, bowtie2, out_path, crAssphage_genome):
    print 'Finding taxonomic composition for file: {0}'.format(f.split('/')[-1])
    fastq_read_1 = f + '_quality_controlled_paired_1.fastq'
    fastq_read_2 = f + '_quality_controlled_paired_2.fastq'
    fastq_unpaired_1 = f + '_quality_controlled_unmatched_1.fastq'
    fastq_unpaired_2 = f + '_quality_controlled_unmatched_2.fastq'

    out_file = out_path + f.split('/')[-1] + '_crAssphage.sam'
    
    command = '{0} -x {1} -1 {2} -2 {3} -U {4},{5} -S {6} -p {7} -k 1 --no-unal'.format(bowtie2, crAssphage_genome, fastq_read_1, fastq_read_2, fastq_unpaired_1, fastq_unpaired_2, out_file, threads)
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for bowtie2 identification of crAssphage.')
    parser.add_argument('--fastq_folder',
                        help='path to folder containing quality controlled fastq files')
    parser.add_argument('--out',
                        help='folder for all bowtie2 output files')
    parser.add_argument('--bowtie2', default='bowtie2',
                        help='path to Bowtie2 software')
    parser.add_argument('--crassphage',
			help='path to crAssphage reference genome index (prefix)')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to use for bowtie2')
    args = parser.parse_args()

    #Get all fastq file in folder (NOTE: fastq files should be QC'ed)
    fastq_folder = args.fastq_folder
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(fastq_folder + '*.fastq*')])
    out_path = args.out

    #metaphlan parameters
    bowtie2 = args.bowtie2
    threads = args.threads
    crAssphage_genome = args.crassphage
    for file_prefix in files:
        identify_taxonomy(file_prefix, threads, bowtie2, out_path, crAssphage_genome)

main()
