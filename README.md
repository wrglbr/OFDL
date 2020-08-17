
# OFDL
Onlyfans media downloader with graphical user interface using Python's tkinter as well as command line interface using PyInquirer.

Downloads media files from Onlyfans (images, videos, highlights)

Before logging in, press F12 (or inspect/inspect element and go to the network tab) to bring up the "developer tools" and then log in. Type "init?" in the search bar and copy the text after the word "cookie:" but don't copy the "referer:". So when copying the cookie you should highlight: sc_is_visitor_unique, ref_src, sess, auth_id and auth_hash. Also copy the user-agent:

<img src="https://github.com/Hashirama/OFDL/blob/master/of2.png">

Paste the cookie and user-agent to the application and press OK:

<img src="https://github.com/Hashirama/OFDL/blob/master/of.png" width="500">

 It should then retrieve the users you're subscribed to. 
 
 # Requirements

Written using Python 3.7, but 3.6 works too (tested) and theoretically any version from Python 3 onwards should do it.

The additional packages tkinter, PyInquirer and requests are required. You can install them using pip.

<pre><code>pip install tkinter</code></pre>
<pre><code>pip install requests</code></pre>
<pre><code>pip install PyInquirer</code></pre>

Then run the script OFDL.py by double clicking it, start it from a Python runtime environment or from the command line using 

<pre><code>python OFDL.py --cli</code></pre>

Note that your python alias should point to a Python 3 runtime environment.

# Note

onlyfans.sqlite3.db is a file that stores information on all the downloaded files. It exists to prevent the same files being downloaded again. If you do update the application, store this file in the same directory as the OFDL.py file before running the script for the first time.
