import glob
import os
import subprocess
import argparse

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def classify_reads(f, centrifuge, db, threads, out_path):
    print 'Finding taxonomic composition for file: {0}'.format(f.split('/')[-1])
    fastq_read_1 = f + '_quality_controlled_paired_1.fastq'
    fastq_read_2 = f + '_quality_controlled_paired_2.fastq'
    fastq_unpaired_1 = f + '_quality_controlled_unmatched_1.fastq'
    fastq_unpaired_2 = f + '_quality_controlled_unmatched_2.fastq'
    
    classification_out_file = out_path + f.split('/')[-1] + '_classification.txt'
    report_out_file = out_path + f.split('/')[-1] + '_report.tsv'
    
    centrifuge_kreport = centrifuge + '-kreport'
    kreport_out_file = out_path + f.split('/')[-1] + '_kreport.txt'
    
    command = '{0} -x {1} -1 {2} -2 {3} -U {4},{5} -S {6} --report-file {7} -q -p {8} && {9} -x {1} {6} > {10} && pigz -p {8} --best {6}'.format(centrifuge, db, fastq_read_1, fastq_read_2, fastq_unpaired_1, fastq_unpaired_2, classification_out_file, report_out_file, threads, centrifuge_kreport, kreport_out_file)
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for centrifuge classification of reads.')
    parser.add_argument('--fastq_folder',
                        help='path to folder containing quality controlled fastq files')
    parser.add_argument('--indexed_db',
                        help='path to basename of the index for the reference genomes')
    parser.add_argument('--out',
                        help='folder for all centrifge output files')
    parser.add_argument('--centrifuge', default='centrifuge',
                        help='path to centrifuge software')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to use for alignment')
    args = parser.parse_args()

    #Get all fastq file in folder (NOTE: fastq files should be QC'ed)
    fastq_folder = args.fastq_folder
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(fastq_folder + '*.fastq*')])
    out_path = args.out

    #centrifuge parameters
    db = args.indexed_db
    centrifuge = args.centrifuge
    threads = args.threads

    for file_prefix in files:
	classify_reads(file_prefix, centrifuge, db, threads, out_path)

main()
