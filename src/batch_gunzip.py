from multiprocessing import Pool
import glob
import subprocess
import argparse

def gunzip(file_name):
    '''
	For multi-processing gunzipping of .gz files without installation of GNU parallel. 
	If you have GNU parallel installed, please use: parallel --jobs <int cores> gunzip {} ::: *.fastq.gz
    '''
    command = 'gunzip {0}'.format(file_name)
    
    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    return None

def main():
    parser = argparse.ArgumentParser(description='Specify arguments for batch gunzipping.')
    parser.add_argument('--gz_folder',
                        help='path to folder containing gz files')
    parser.add_argument('--wildcard_command', default = '*.gz',
                        help='wildcard command to use for locating gz files')
    args = parser.parse_args()
    folder = args.gz_folder
    wildcard = args.wildcard_command
    gzipped_files = glob.glob(folder + wildcard)
    pool = Pool()
    pool.map(gunzip, gzipped_files)
    
main()
