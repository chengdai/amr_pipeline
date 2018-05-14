import glob
import os
import subprocess
import argparse

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def identify_protein_variants(f, usearch, db, threads, out_path):
    print 'Finding variants for file: {0}'.format(f.split('/')[-1])

    report_out_file = out_path + f.split('/')[-1].split('.')[0] + '_protein_snp.txt'
    
    command = "{0} {1} -db {2} -target_cov 1.0 -id 1.0 -maxhits 1 -threads {3} -userout {4} -userfields query+target+id+evalue+qcov+tcov+ql+tl+bits".format(usearch, f, db, threads, report_out_file)

    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for usearch local alignment of ARGs.')
    parser.add_argument('--fasta_folder',
                        help='path to folder containing quality controlled fasta files')
    parser.add_argument('--db',
                        help='path to basename of the db for the reference markers')
    parser.add_argument('--out',
                        help='folder for all usearch output files')
    parser.add_argument('--usearch', default='usearch',
                        help='path to usearch software')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to use for alignment')
    args = parser.parse_args()

    #Get all fasta file in folder (NOTE: fasta files should be QC'ed)
    fasta_folder = args.fasta_folder
    files = glob.glob(fasta_folder + '*.fasta*')
    out_path = args.out

    #usearch parameters
    db = args.db
    usearch = args.usearch + '  -usearch_local'
    threads = args.threads

    for f in files:
        identify_protein_variants(f, usearch, db, threads, out_path)

main()