# Automover

Little tool that allows you to automatically move files from one directory to another and cleans up afterwards:
- First make it executable:
<pre>chmod 777 automover.py</pre>
- To run it use:
<pre>sudo ./automover.py src_path dest_path </pre>
- Use case: 
1) Step: <pre>automover.py src_path=your/downloads/directory/ dest_path=somewhere/lecture/xy/slides </pre>
2) Step: download zipped lecture slides of your favourite lecture
3) Step: The .zip will be extracted (automover searches for them recursively in all directories of the zip) and your pdf's will be moved into your slides folder
4) Step: Profit


<pre><font color="#55FF55"><b>[julian@manjaro</b></font><font color="#FFFFFF"><b> Automover</b></font><font color="#55FF55"><b>]$</b></font> ./automover.py -h
usage: automover.py [-h] [-v] src_path dest_path

Automatic file mover/zip archive extractor.

positional arguments:
  src_path       The src_path of the dir_path you want to track
  dest_path      The dest_path to move the file to.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity

Made by Julian Hohenadel 2019</pre>
