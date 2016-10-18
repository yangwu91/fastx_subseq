#!/usr/bin/env python

print "\n# Warning: This script is memeory-consuming! #"
import sys, re, os
#import my_lib.ProcessingBar.ProcessingBar as PB
from copy import deepcopy

if __name__ == '__main__':
	try:
		input_fastx, seqname_listfile = sys.argv[1], sys.argv[2]
	except IndexError:
		print 'Require arguements!'
		quit()
	with open(input_fastx, 'r') as inputfile:
		print 'Initializing...'
		mate_pattern=re.compile(r'[-/\_.]([12])$')
		firstline=inputfile.readline().strip().split()[0]
		sig=firstline[0]
		if len(re.findall(mate_pattern, firstline))==0:# and len(re.findall(mate_pattern, firstline.split()[0]))==0:
			mate=False
		else:
			mate=True
	with open(input_fastx, 'r') as inputfile:
		fastqa_dict={}
		if sig=='@':	
			while True:
				fastqa1=inputfile.readline().strip()
				fastqa2=inputfile.readline().strip()
				fastqa3=inputfile.readline().strip()
				fastqa4=inputfile.readline().strip()
				if fastqa1=='' or fastqa2=='' or fastqa3=='' or fastqa4=='':
					break
				fastqa_name=fastqa1.split()[0]
				if mate:
					pair_num=int(re.findall(mate_pattern, fastqa_name)[0])
					if fastqa_dict.has_key(fastqa_name[1:-2]):
						fastqa_dict[fastqa_name[1:-2]].update({pair_num:[fastqa1, fastqa2, fastqa3, fastqa4]})
					else:
						fastqa_dict[fastqa_name[1:-2]]=deepcopy({pair_num:[fastqa1, fastqa2, fastqa3, fastqa4]})
				else:
					if fastqa_dict.has_key(fastqa_name[1:]):
						fastqa_dict[fastqa_name[1:]].update({2:[fastqa1, fastqa2,fastqa3,fastqa4]})
					else:
						fastqa_dict.update({fastqa_name[1:]:{1:[fastqa1, fastqa2, fastqa3, fastqa4]}})			
		elif sig=='>':
			all_fasta=inputfile.read().strip().strip('>').split('\n>')
			for e in all_fasta:
				e=e.strip().split('\n', 1)
				fastqa1=e[0]
				fastqa2=e[-1].replace('\n', '')
				fastqa_name=fastq1.split()
				if mate:
					pair_num=int(re.findall(mate_pattern, fastqa1)[0])
					if fastqa_dict.has_key(fastqa_name[:-2]):
						fastqa_dict[fastqa_name[:-2]].update({pair_num:['>'+fastqa1, fastqa2]})
					else:
						fastqa_dict[fastqa_name[:-2]]=deepcopy({pair_num:['>'+fastqa1, fastqa2]})
				else:
					if fastqa_dict.has_key(fastqa1):
						fastqa_dict[fastqa_name].update({2:['>' + fastqa1, fastqa2]})
					else:
						fastqa_dict[fastqa_name]=deepcopy({1:['>' + fastqa1, fastqa2]})
		else:
			print 'It seems not a standard FASTA/FASTQ file. Please check your input.'
			quit()	
	with open(seqname_listfile, 'r') as inputfile:
		print 'Extracting...'
		os.system(r'mkdir -p ./extract_sequences/ && rm -f ./extract_sequences/%s' % os.path.split(input_fastx)[-1])
		for seqname in inputfile:
			seqname=seqname.strip().split()[0]
			if seqname[0]=='>' or seqname[0]=='@':
				seqname=seqname[1:]
			pair_num=re.findall(mate_pattern, seqname)
			with open('./extract_sequences/%s' % os.path.split(input_fastx)[-1], 'a') as outputfile:
				try:
					if len(pair_num)==0:
						for fastqa in fastqa_dict.get(seqname).values():
							outputline='\n'.join(fastqa) + '\n'
							outputfile.write(outputline)
					else:
						outputline='\n'.join(fastqa_dict.get(seqname).get(pair_num[0])) + '\n'
						outputfile.write(outputline)
				except:
					with open('./extract_sequences/no-hits.list', 'a') as outputfile:
						outputfile.write(seqname + '\n')
						print 'Not found: %s' % seqname
	print 'All done.'	

