import sys
def Bar(i, total_job, bar_size=80):
	odds_process=bar_size*i/total_job
	print '\r    ['+odds_process*'='+(1-odds_process/bar_size)*'>'+(bar_size-1-odds_process)*' '+']'+'  Processing '+'%.1f' % (100.0*i/total_job)+'%...',
	sys.stdout.flush()