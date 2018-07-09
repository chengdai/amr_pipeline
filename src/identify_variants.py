import glob, os, shutil, subprocess, argparse, datetime

'''NOTE: When in doubt, call "python [FILENAME.py] -h" to get a description of the necessary parameters'''

def force_mkdir(dir, force):
    if not os.path.exists(dir):
        print 'Creating folder: {0}'.format(dir)
        os.makedirs(dir)
    elif os.path.exists(dir) and force == 'True':
        print '{0} currently exists, removing existing files'.format(dir)
        shutil.rmtree(dir, ignore_errors=True)
        os.makedirs(dir)
    else:
        print '{0} currently exists, ignoring'

def align_to_homolog_genes(f, diamond, dmnd, threads, temp_folder):
    print '\nAligning to homolog genes for file: {0} [{1}]'.format(f.split('/')[-1], datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"))

    report_out_file = temp_folder + f.split('/')[-1].split('.')[0] + '_homolog_matches.txt'
    header_out_file = temp_folder + f.split('/')[-1].split('.')[0] + '_homolog_matches_header.txt'

    command = "{0} -q {1} -d {2} -f 6 -o {3} -k 1 --id 90 --query-cover 80 -p {4} && awk '{{print $1}}' {3} > {5}".format(diamond, f, dmnd, report_out_file, threads, header_out_file)

    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

    return header_out_file

def extract_reads(f, header_file, temp_folder, subset):
    print '\nExtracting aligned reads from file {0} using {1}  [{2}]'.format(f.split('/')[-1], header_file.split('/')[-1], datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"))

    subset_fasta_file = temp_folder + f.split('/')[-1].split('.')[0] + '_homolog_subset.fa'

    command = "python {0} --input {1} --headers {2} --out {3}".format(subset, f, header_file, subset_fasta_file)

    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

    return subset_fasta_file

def identify_variants(f, usearch, udb, threads, out_path):
    print '\nFinding variants for file: {0} [{1}]'.format(f.split('/')[-1], datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"))

    report_out_file = out_path + f.split('/')[-1].split('_homolog_subset.fa')[0] + '_variants.txt'

    command = "{0} {1} -db {2} -target_cov 1.0 -maxgaps 0 -id 1.0 -maxaccepts 0 -maxrejects 0 -maxhits 1 -threads {3} -userout {4} -userfields query+target+id+evalue+qcov+tcov+ql+tl+bits".format(usearch, f, udb, threads, report_out_file)

    final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (stdout, stderr) = final.communicate()
    print stdout
    print stderr

def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Specify arguments for alignment of ARG variants.')
    parser.add_argument('--fasta_folder',
                        help='path to folder containing quality controlled fasta files')
    parser.add_argument('--dmnd',
                        help='path to the diamond db for the reference homolog sequences')
    parser.add_argument('--udb',
                        help='path to the usearch db for the reference marker sequences')
    parser.add_argument('--out',
                        help='folder for all marker alignment output files')
    parser.add_argument('--temp',
                        help='folder for all intermediate files')
    parser.add_argument('--diamond', default='diamond',
                        help='path to diamond software [Default = diamond]')
    parser.add_argument('--usearch', default='usearch',
                        help='path to usearch software [Default = usearch]')
    parser.add_argument('--subset', default='subset_fasta.py',
                        help='path to subset_fasta.py script [Default = subset_fasta.py]')
    parser.add_argument('--threads', default= 1.0,
                        help='number threads to use for alignment. [Default = 1]')
    parser.add_argument('--force', default= 'False',
                        help='force the creation of a directory. NOTE: data in existing directories will be deleted. [Default = False]')
    args = parser.parse_args()

    #Get all fasta file in folder (NOTE: fasta files should be QC'ed)
    fasta_folder = args.fasta_folder
    files = glob.glob(fasta_folder + '*.fasta*')
    out_path = os.path.normpath(os.path.expanduser(args.out)) + '/'
    temp_folder = os.path.normpath(os.path.expanduser(args.temp)) + '/'

    diamond = args.diamond + ' blastx'
    dmnd = args.dmnd
    usearch = args.usearch + '  -usearch_local'
    udb = args.udb
    subset = args.subset
    threads = args.threads
    force = args.force

    print '\nCreating temporary directory [{0}]'.format(datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"))
    force_mkdir(temp_folder, force)

    print '\nCreating output directory [{0}]'.format(datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"))
    force_mkdir(out_path, force)

    for f in files:
       header_out_file = align_to_homolog_genes(f, diamond, dmnd, threads, temp_folder)
       subset_fasta_file = extract_reads(f, header_out_file, temp_folder, subset)
       identify_variants(subset_fasta_file, usearch, udb, threads, out_path)

main()

