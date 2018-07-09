import glob
import multiprocessing
import subprocess
import argparse
import random

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def quantify_read_resistomes(f):
    print 'Finding resistomes for file: {0}'.format(f.split('/')[-1])
    fasta_read_1 = f + '_quality_controlled_paired_1.fasta'
    fasta_read_2 = f + '_quality_controlled_paired_2.fasta'
    fasta_unpaired_1 = f + '_quality_controlled_unmatched_1.fasta'
    fasta_unpaired_2 = f + '_quality_controlled_unmatched_2.fasta'
    
    out_file = out_path + f.split('/')[-1] + '_shortbred.txt'
    
    command = '{0} --markers {1} --wgs {2} {3} {4} {5} --results {6} --id {7}  --threads 20 --usearch ../tools/usearch-v10.0.240 --tmp {8}quantification_{9}'.format(shortbred, markers, fasta_read_1, fasta_read_2, fasta_unpaired_1, fasta_unpaired_2, out_file, id, temp, random.randint(1,100000))
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr
    
def quantify_genome_resistomes(f):
    print 'Finding resistomes for file: {0}'.format(f.split('/')[-1])
    
    out_file = out_path + f.split('/')[-1] + '_shortbred.txt'
    
    command = '{0} --markers {1} --genome {2} --results {3} --id {4}  --threads 20 --usearch ../tools/usearch-v10.0.240 --tmp {5}quantification_{6}'.format(shortbred, markers, f, out_file, id, temp, random.randint(1,1000))
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

    
def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for ShortBRED quantification identification of ARGs.')
    parser.add_argument('--fasta_folder',
                        help='path to folder containing quality controlled fasta files')
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
    parser.add_argument('--temp_folder', default= './temp_files/',
                        help='path to hold the temp files')
    parser.add_argument('--fasta_content', default= 'reads',
                        help='designates whether the fasta file contains metagenomic reads or draft genomes. Viable options are "reads" and "genome" (default = "reads")')
    args = parser.parse_args()

    global shortbred, out_path, markers, shrotbred, id, temp

    #Get all fasta file in folder (NOTE: fasta files should be QC'ed)
    fasta_folder = args.fasta_folder
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(fasta_folder + '*.fasta*')])
    if len(files) == 0:
        print 'ERROR: No fasta files found, please check if the folder is correct or if filetype is correct'
        return
    out_path = args.out

    #shortbred parameters
    markers = args.ref_markers
    shortbred = args.shortbred
    id = float(args.id)
    try:
        assert (id >= 0.0) and (id <= 1.0)
    except:
        print 'ERROR: invalid identity threshold - please ensure it is between 0 and 1'
        return
    temp = args.temp_folder
    fasta_content = args.fasta_content
    
    if fasta_content == 'reads':
        #multiprocessing
        threads = args.threads
        p = multiprocessing.Pool(int(threads))
        p.map_async(quantify_read_resistomes, files)
        p.close()
        p.join()
    elif fasta_content == 'genome':
        #multiprocessing
        threads = args.threads
        p = multiprocessing.Pool(int(threads))
        p.map_async(quantify_genome_resistomes, files)
        p.close()
        p.join()
    else:
        print 'ERROR: Invalid option for fasta_content. Please select "reads" or "genome"'
        return

main()
