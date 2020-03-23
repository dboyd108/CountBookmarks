# CountBookmarks

Purpose: To count the number of bookmarks in each folder and subfolder of a bookmarks file exported by a web browser. The output file that this program generates can be imported into a spreadsheet and sorted by either of its bookmark count columns to determine the relative size of all bookmark folders.

Inputs: This program requires a command line argument specifying the fully qualified name of a bookmarks file in HTML format and, optionally, a command line argument (-d) indicating that debugging output is to be included in the log file.

Outputs: For each folder of the bookmarks file, the folder's name, a count of the bookmarks local to that folder, and a count of the total number of bookmarks in that folder and all of its subfolders are written, in CSV format, to a file named CountBookmarks.csv, in the current working directory. To allow for commas in bookmark folder names, this output file uses semicolons for field separators instead of commas. Select semicolon as the field separator when importing this file into a spreadsheet. This program also generates a log file, CountBookmarks.log, in the current working directory.

Command Syntax: python CountBookmarks.py [-d] File
Command Options: -d: Include debugging output in the log file, CountBookmarks.log.
Command Example: python CountBookmarks.py "/home/yourname/Downloads/your bookmarks.html"

Compatible Browsers: This program is compatible with the Google Chrome, Mozilla Firefox, Microsoft Edge, and Microsoft Internet Explorer browsers. It may also work with non-Google, Chromium-based browsers and Apple Safari.

Browsers Tested (Version):
 - Google Chrome (80.0.3987.132 (Official Build) (64-bit))
 - Mozilla Firefox (74.0 (64-bit))
 - Microsoft Edge (44.18362.449.0)
 - Microsoft Internet Explorer (11.719.18362.0)

Development and Test Environments:

Operating System (Version):
 - Windows 10 Home (1909)
 - Ubuntu Linux (18.04 LTS)
Programming Language (Version):
 - Python (3.8.2)
 - Python (3.6.9)
Python Environment on Ubuntu Linux:
 - See https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-18-04
