

import argparse
import glob
import os

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--handle', type=str, required=True, 
                    help='provide unique identifier  to select a subset of directories.')    

args = parser.parse_args()

checklist = ['21990443','21990445','21990447','21990449']

stitchlist = []
with open('/u/dbath/stitch_list.txt', "w") as output:
    for vidfile in glob.glob('/ptmp/dbath/*'+ args.handle + '*.21990443'):
        STATUS = 'ok'
        for checknum in checklist:
            if not os.path.exists(vidfile.rsplit('.',1)[0] + '.' + checknum+'/metadata.yaml'):
                STATUS = 'not ok'
                continue
        if os.path.exists(vidfile.rsplit('.',1)[0] + '.stitched/metadata.yaml'):
            STATUS = 'not ok'
        
        if STATUS == 'ok':
            output.writelines('_'.join(vidfile.rsplit('.',1)[0].split('_')[-2:])+'\n')
            print "appended: ", vidfile.rsplit('.',1)[0].split('/')[-1]
    
