<h1>CountBookmarks</h1>

<strong>Purpose:</strong> To count the bookmarks in each folder and subfolder of a bookmarks file exported by a web browser. The output file that this program generates can be imported into a spreadsheet and sorted to show the relative size of all your bookmark folders.<br/>

<strong>Inputs:</strong> This program requires a command line argument specifying the fully qualified name of a bookmarks file in HTML format and, optionally, a command line argument (-d) indicating that debugging output is to be included in the log file.<br/>

<strong>Outputs:</strong> For each folder of the bookmarks file, the folder's name, the number of bookmarks local to that folder, and the total number of bookmarks in that folder and all of its subfolders are written to file CountBookmarks.csv, in the current working directory. To allow for commas in bookmark folder names, this output file uses semicolons for field separators instead of commas. Select semicolon as the field separator when importing this file into a spreadsheet. This program also generates a log file, CountBookmarks.log, in the current working directory.<br/>

<strong>Command Syntax:</strong> python CountBookmarks.py [-d] File<br/>
<strong>Command Options: -d:</strong> Include debugging output in the log file.<br/>
<strong>Command Example:</strong> python CountBookmarks.py "/home/yourname/Downloads/your bookmarks.html"<br/>

<strong>Compatible Browsers:</strong> This program is compatible with the Google Chrome, Mozilla Firefox, Microsoft Edge, and Microsoft Internet Explorer browsers. It may also work with non-Google, Chromium-based browsers and Apple Safari.<br/>
<hr />
<h2>Development and Test Environments</h2>

<strong>Browsers</strong><br/>
<ul>
<li>Google Chrome 80.0.3987.132 (Official Build) (64-bit)</li>
<li>Mozilla Firefox 74.0 (64-bit)</li>
<li>Microsoft Edge 44.18362.449.0</li>
<li>Microsoft Internet Explorer 11.719.18362.0</li>
</ul>

<strong>Operating Systems</strong>
<ul>
<li>Windows 10 Home 1909</li>
<li>Ubuntu Linux 18.04 LTS</li>
</ul>

<strong>Programming Languages</strong>
<ul>
<li>Python 3.8.2</li>
<li>Python 3.6.9</li>
</ul>

<strong>Python Environment on Ubuntu Linux</strong>
<ul>
<li>See https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-18-04</li>
</ul>
<hr />
<strong>License:</strong> https://www.apache.org/licenses/LICENSE-2.0
