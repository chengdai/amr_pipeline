import glob
import multiprocessing
import subprocess
import argparse
import random

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def quantify_resistomes(f):
    print 'Finding resistomes for file: {0}'.format(f.split('/')[-1])
    fastq_read_1 = f + '_quality_controlled_paired_1.fastq'
    fastq_read_2 = f + '_quality_controlled_paired_2.fastq'
    fastq_unpaired_1 = f + '_quality_controlled_unmatched_1.fastq'
    fastq_unpaired_2 = f + '_quality_controlled_unmatched_2.fastq'
    
    out_file = out_path + f.split('/')[-1] + '_shortbred.txt'
    
    command = '{0} --markers {1} --wgs {2} {3} {4} {5} --results {6} --id {7}  --threads 20 --usearch ../tools/usearch-v10.0.240 --tmp ./temp_files/quantification_{8}'.format(shortbred, markers, fastq_read_1, fastq_read_2, fastq_unpaired_1, fastq_unpaired_2, out_file, id, random.randint(1,1000))
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for ShortBRED quantification identification of ARGs.')
    parser.add_argument('--fastq_folder',
                        help='path to folder containing quality controlled fastq files')
    parser.add_argument('--ref_markers',
                        help='path to ARG markers')
    parser.add_argument('--out',
                        help='folder for all ShortBRED output files')
    parser.add_argument('--shortbred',
                        help='path to shortbred software')
    parser.add_argument('--id', default= 0.99,
                        help='minimum identity for alignment')
    parser.add_argument('--threads', default= 1.0,
                        help='number file sets to analyze')
    args = parser.parse_args()

    global shortbred, out_path, markers, shrotbred, id

    #Get all fastq file in folder (NOTE: fastq files should be QC'ed)
    fastq_folder = args.fastq_folder
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(fastq_folder + '*.fastq*')])
    out_path = args.out

    #shortbred parameters
    markers = args.ref_markers
    shortbred = args.shortbred
    id = args.id

    #multiprocessing
    threads = args.threads
    p = multiprocessing.Pool(int(threads))
    p.map(quantify_resistomes, files)
    p.close()
    p.join()

main()
