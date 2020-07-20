

import argparse
import glob
import os

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--handle', type=str, required=True, 
                    help='provide unique identifier  to select a subset of directories.')    
parser.add_argument('--max', type=int, required=False,
                    default = 24, help='the maximum number of jobs to include in the list')
parser.add_argument('--append', type=bool, required=False,
                    default = False, help='make true to append to the existing file. False (default) will overwrite the existing file')
args = parser.parse_args()

if args.append:
    write_mode = "a"
else:
    write_mode = "w"

checklist = ['21990443','21990445','21990447','21990449']

stitchlist = []
counter = 0
with open('/media/recnodes/recnode_2mfish/stitch_list.txt', write_mode) as output:
    for vidfile in glob.glob('/media/recnodes/recnode_2mfish/*'+ args.handle + '*.21990443'):
        STATUS = 'ok'
        for checknum in checklist:
            #check that all corners are present
            if not os.path.exists(vidfile.rsplit('.',1)[0] + '.' + checknum+'/metadata.yaml'):
                STATUS = 'not ok'
                continue
            #must be greater than 1mb (black videos or bad recordings are less than 1mb)
            if not os.path.getsize(vidfile.rsplit('.',1)[0] + '.' + checknum+'/000000.mp4') > 1000:
                STATUS = 'not ok'
                continue
        #dont add if already done
        if os.path.exists(vidfile.rsplit('.',1)[0] + '.stitched/metadata.yaml'):
            STATUS = 'not ok'
        
        if STATUS == 'ok':
            counter +=1
            if counter <= args.max:
                output.writelines('scp -r ' + vidfile.split('/')[-1][:-1] +'* dbath@130.183.23.251:/ptmp/dbath \n')
                print "appended: ", vidfile.rsplit('.',1)[0].split('/')[-1]
            else:
                continue
