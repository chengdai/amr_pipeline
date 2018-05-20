import glob
import multiprocessing
import subprocess
import argparse
import random

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def concat(f):
    print 'Finding blast outputs for file with prefix: {0}'.format(f.split('/')[-1])
    blast_1, blast_2, blast_3, blast_4 = glob.glob(f + '*')
    out_file = out_path + f.split('/')[-1] + suffix
    
    command = 'cat {0} {1} {2} {3} > {4}'.format(blast_1, blast_2, blast_3, blast_4, out_file)
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for concatenating all of the output files from blast.')
    parser.add_argument('--blast_folder',
                        help='path to folder containing blast result files')
    parser.add_argument('--suffix',
                        help='the common of the files to get all of the blast output files')
    parser.add_argument('--out',
                        help='folder to store the concatenated output files')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to employ')
    args = parser.parse_args()

    global blast_folder, out_path, suffix

    #Get all blast file in folder
    blast_folder = args.blast_folder
    suffix = args.suffix
    files = set([f.split('_quality_controlled_')[0] for f in glob.glob(blast_folder + '*' + suffix)])

    if len(files) == 0:
        print 'No files found, please check if the parameters are correct'
	return None
    out_path = args.out

    #multiprocessing
    threads = args.threads
    p = multiprocessing.Pool(int(threads))
    p.map_async(concat, files)
    p.close()
    p.join()

main()

