# fastx_subseq.py
This script can extract FASTA/Q subseq **extremely fast** but **consumes memory** a lot.

## Methods
### Commands:
```Bash
$ python fastx_subseq.py INPUT SEQ_NAME_LIST     # No detailed information printed.
```
or
```Bash
$ python fastx_subseq.py INPUT SEQ_NAME_LIST -v  # If the option "-v" exsists, the script will print detailed process infomation.
```
All extracted sequences will be put in a generated fold named `extract_sequences` in **current work directory**. Make sure you have permission.

### Formats:
`INPUT` is supposed to be a file in [FASTA format](https://en.wikipedia.org/wiki/FASTA_format) or [4-line FASTQ format](https://en.wikipedia.org/wiki/FASTQ_format).  
And `SEQ_NAME_LIST` is a plain text, containing sequence names, one per line (no space), such as:
```Bash
$ head SEQ_NAME_LIST
E00247:343:HYMLVCCXX:8:1101:11363:40583
E00247:343:HYMLVCCXX:8:1101:1813:43941
E00247:343:HYMLVCCXX:8:1101:23023:68658
E00247:343:HYMLVCCXX:8:1101:23409:33041
E00247:343:HYMLVCCXX:8:1101:2656:67058
```

### Note:
If few subseqs need to be extracted from a FASTA file, I suggest to use [samtools](https://github.com/samtools/samtools):
```Bash
$ samtools faidx INPUT_FASTA                          # Build an index for your FASTA file first.  
$ samtools faidx INPUT_FASTA SEQ_NAME > OUTPUT_FASTA  # Extract the subseq.
```

## License
[MIT License](https://github.com/yangwu91/fastx_subseq/blob/master/LICENSE)