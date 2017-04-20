#!/usr/bin/env pypy

import sys, re, os, commands
import gc # garbage collector
from copy import deepcopy
from subprocess import check_call as CC
from ProcessingBar import Bar
#from glob import glob # support wildcard
from datetime import datetime
from Argv import ArgvToDict as ATD

class Fastx:
	"""An example:
	
	import sys
	sys.path.append('/path/to/fastx_subseq/')  # If necessary.
	from fastx_subseq import Fastx 
	f = Fastx(FASTX_file, verbose=True)        # To process verbosely, set "verbose=True" (default).
	f.ExtractInfo()                            # To extract the FASTX's info (consumes memory).
	f.FetchSeq(query_list, outdir)             # To fetch sequences.
	f.ReleaseMemory()                          # Recommended."""
	
	global mate_p
	mate_p = re.compile(r'[-/._ ]([123])(:N:0:0)?$')
	
	global fastx_name_p
	fastx_name_p = re.compile(r'^[@>](.+)[-/._ ][123](:N:0:0)?$')
	
	def __init__(self, infastx, verbose=True):
		self.infastx = infastx
		self.verbose = verbose
		self.fastx_dict = {}
		if self.verbose:
			print '    Initializing...'	

	def __CheckFastx(self, level=5):
		fmt = ''
		assert type(level) == int and level >= 1
		with open(self.infastx, 'r') as inf:
			n, fasta_num, fastq_num, mate_num = 0, 0, 0, 0
			next_sig = '+'
			for i in xrange(level):
				line = inf.readline().strip()
				if len(line) == 0:
					break
				if i % 2 == 0:
					n += 1
					sig = line[0]
					if sig == '@' and next_sig == '+':
						fastq_num += 1
						next_sig = '@'
					elif sig == '+' and next_sig == '@':
						fastq_num += 1
						next_sig = '+'
					elif sig == '>':
						fasta_num += 1
					mate_sig = re.findall(mate_p, line)
					if len(mate_sig) == 1:
						mate_num += 1
		if fmt == '':
			# 1. format
			if n == fastq_num:
				fmt = 'fastq'
			# 2. paired or not
				if mate_num == (level+3)/4:
					self.mate = True
				else:
					self.mate = False
			elif n == fasta_num:
				fmt = 'fasta'
			# 2. paired or not
				if mate_num == n:
					self.mate = True
				else:
					self.mate = False				
			else:
				fmt = 'error0'
		return fmt
	
	def __FastqInfo(self):
		with open(self.infastx, 'r') as inputfile:
			while True:
				fastq1 = inputfile.readline().strip()
				fastq2 = inputfile.readline().strip()
				fastq3 = inputfile.readline().strip()
				fastq4 = inputfile.readline().strip()
				if fastq1 == '' or fastq2 == '' or fastq3 == '' or fastq4 == '':
					break
				fastq_name = re.findall(fastx_name_p, fastq1)[0][0]
				if self.mate:
					pair_num = int(re.findall(mate_p, fastq1)[0][0])
					if self.fastx_dict.has_key(fastq_name):
						self.fastx_dict[fastq_name].update({pair_num: [fastq1, fastq2, fastq3, fastq4]})
					else:
						self.fastx_dict[fastq_name] = deepcopy({pair_num: [fastq1, fastq2, fastq3, fastq4]})
				else:
					if self.fastx_dict.has_key(fastq_name):
						self.fastx_dict[fastq_name].update({2: [fastq1, fastq2,fastq3,fastq4]})
					else:
						self.fastx_dict.update({fastq_name: {1: [fastq1, fastq2, fastq3, fastq4]}})					

	def __FastaInfo(self):
		with open(self.infastx, 'r') as inputfile:
			all_fasta = inputfile.read().strip().strip('>').split('\n>')
			for contig in all_fasta:
				contig = contig.strip().split('\n', 1)
				fasta1 = contig[0]
				fasta2 = contig[-1].replace('\n', '')
				fasta_name = re.findall(fastx_name_p, ('>'+fastq1))[0][0]
				if self.mate:
					pair_num = int(re.findall(mate_p, fasta1)[0][0])
					if self.fastx_dict.has_key(fasta_name):
						self.fastx_dict[fasta_name].update({pair_num: ['>'+fasta1, fasta2]})
					else:
						self.fastx_dict[fasta_name] = deepcopy({pair_num: ['>'+fasta1, fasta2]})
				else:
					if self.fastx_dict.has_key(fasta_name):
						self.fastx_dict[fasta_name].update({2: ['>' + fasta1, fasta2]})
					else:
						self.fastx_dict[fasta_name] = deepcopy({1: ['>' + fasta1, fasta2]})			

	def ExrtactInfo(self, returned=False, checklevel=5):
		assert type(returned) == bool
		fmt = self.__CheckFastx(checklevel)
		if fmt == 'fastq':
			self.__FastqInfo()
		elif fmt == 'fasta':
			self.__FastaInfo()
		else:
			self.fastx_dict = {}
			print self.__ErrorCode(fmt)
		if returned:
			return self.fastx_dict
		
	def FetchSeq(self, seqname_list, outdir='./extracted_sequences'):
		total_job = int(commands.getoutput('wc -l < %s' % seqname_list))
		CC(r'mkdir -p %s' % outdir, shell=True)
		outf_name = '%s/%s' % (outdir, os.path.split(self.infastx)[-1])
		if os.path.isfile(outf_name):
			CC('rm -f %s' % outf_name, shell=True)		
		with open(seqname_list, 'r') as inf:
			if self.verbose:
				print '    Fetching to "%s"...' % outdir
			n, pre_process = 0, -1
			for seqname in inf:
				n += 1
				seqname = seqname.strip().split()[0]
				if len(seqname) > 0 and seqname[0] <> '#':		
					if seqname[0] == '>' or seqname[0] == '@':
						seqname = seqname[1:]
					pair_num = re.findall(mate_p, seqname)
					fastx_dict_values = self.fastx_dict.get(seqname)		
					if fastx_dict_values != None:
						with open(outf_name, 'a') as outf:
							if len(pair_num) == 0:
								for fastx in fastx_dict_values.itervalues():
									outf.write('\n'.join(fastx) + '\n')
							else:
								outf.write('\n'.join(fastx_dict_values.get(pair_num[0])) + '\n')
					else:
						with open('%s/NoHits-%s.list' % (outdir, os.path.split(self.infastx)[-1]), 'a') as outf:
							outf.write(seqname + '\n')
							#print 'Not found: %s' % seqname
					if self.verbose:
						process = int(1000.0*n/total_job)/10.0
						if pre_process < process: # reduce redundant output
							Bar(n, total_job, bar_size = 80, left_indentation = 4)
						pre_process = process
			print ''	

	def ReleaseMemory(self):
		"""For inputting multiple files at the same time, this method is recommended."""
		del self.fastx_dict
		gc.collect()
		
	def __ErrorCode(code):
		error_code = {
              'error0': '    It seems not a standard FASTA/FASTQ file. Please check your input.',
		      'error1': "    Discordant paired numbers were found in reads' names."
		}
		default_error = '    Unknown error. Aborted.'
		return error_code.get(code, default_error)

def HelpMsg():
	print '''
Commands:
pypy fastx_subseq.py -f FASTA/Q -l query_list -v
# Support wildcard. 
# Mutiple input files could be seperated by a comma without space.
'''

# Main Sub
if __name__ == '__main__':
	args = ATD(argv_list = sys.argv, required = ['-f', '-l'], optional = {'-v':False, '-h':False, '-o':'./extracted_sequences'})
	#print args
	if args.get('-h') or args == {}:
		HelpMsg()
		quit()
	infastx, seqname_list, verbose, outdir = args.get('-f'), args.get('-l'), args.get('-v'), args.get('-o')
	if verbose:
		print "\n# Warning: This script is memeory-consuming! #"
	i = 0
	if type(infastx) != list:
		infastx = [infastx, ]
	for in_file in infastx:
		i += 1
		if verbose:
			start_time = datetime.now()
			print '(%s/%s) Extracting from "%s":' % (str(i), str(len(infastx)), os.path.split(in_file)[-1])
		fastx = Fastx(in_file, verbose)
		fastx.ExrtactInfo()
		fastx.FetchSeq(seqname_list, outdir)
		if verbose:
			end_time = datetime.now()
			print '    Done in %ss.' % (end_time-start_time).seconds
		fastx.ReleaseMemory()
	print 'All done.\n'
