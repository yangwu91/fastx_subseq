# fastx_subseq.py
This script can extract FASTA/Q subseq **extremely fast** but **consumes memory** a lot.

## Methods
### In Bash:
```Bash
$ pypy fastx_subseq.py -f FASTX -l SEQ_NAME_LIST # No detailed information printed.
```
or
```
$ pypy fastx_subseq.py -f FASTX -l SEQ_NAME_LIST -o OUT_DIR -v

# Warning: This script is memeory-consuming! #
Initializing...
Extracting...
    [================================================================================]  Processing 100.0%... 
All done.
```
All extracted sequences will be put in a generated fold named `extract_sequences` in **current work directory**. Make sure you have permission.
### Imported as a Python module:
An example:
```Python
import sys
sys.path.append('/path/to/fastx_subseq/')  # If necessary.
from fastx_subseq import Fastx
f = Fastx(FASTX, verbose=True)             # To process verbosely, set "verbose=True" (default).
f.ExtractInfo()                            # To extract the FASTX's info (consumes memory).
f.FetchSeq(SEQ_NAME_LIST, OUT_DIR)         # To fetch sequences.
f.ReleaseMemory()                          # Recommended."""
```
For more details:
```Python
>>> from fastx_subseq import Fastx
>>> help(Fastx)
```

### Formats:
`FASTX` is supposed to be a file in [FASTA format](https://en.wikipedia.org/wiki/FASTA_format) or [4-line FASTQ format](https://en.wikipedia.org/wiki/FASTQ_format).  
And `SEQ_NAME_LIST` is a plain text, containing sequence names, one per line (no space), such as:
```Bash
$ head SEQ_NAME_LIST
E00247:343:HYMLVCCXX:8:1101:11363:40583
E00247:343:HYMLVCCXX:8:1101:1813:43941
E00247:343:HYMLVCCXX:8:1101:23023:68658
E00247:343:HYMLVCCXX:8:1101:23409:33041
E00247:343:HYMLVCCXX:8:1101:2656:67058
```
`OUT_DIR` refers to a customized output directory (default: "./extracted_sequences/").

### Note:
If few subseqs need to be extracted from a FASTA file, [samtools](https://github.com/samtools/samtools) is suggested:
```Bash
$ samtools faidx INPUT_FASTA                          # Build an index for your FASTA file first.  
$ samtools faidx INPUT_FASTA SEQ_NAME > OUTPUT_FASTA  # Extract the subseq.
```

## License
[MIT License](https://github.com/yangwu91/fastx_subseq/blob/master/LICENSE)