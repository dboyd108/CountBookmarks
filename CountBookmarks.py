#
# Name: CountBookmarks.py
# Purpose: To count the number of bookmarks in each folder and subfolder of a bookmarks file exported by a web browser. The output file that this
#          program generates can be imported into a spreadsheet and sorted by either of its bookmark count columns to determine the relative size
#          of all bookmark folders.
#
# Inputs: This program requires a command line argument specifying the fully qualified name of a bookmarks file in HTML format and, optionally,
#         a command line argument (-d) indicating that debugging output is to be included in the log file.
# Outputs: For each folder of the bookmarks file, the folder's name, a count of the bookmarks local to that folder, and a count of the total number of bookmarks in that
#          folder and all of its subfolders are written, in CSV format, to a file named CountBookmarks.csv, in the current working directory. To allow for commas in
#          bookmark folder names, this output file uses semicolons for field separators instead of commas. Select semicolon as the field separator when importing this
#          file into a spreadsheet. This program also generates a log file, CountBookmarks.log, in the current working directory.
#
# Command Syntax: python CountBookmarks.py [-d] File
# Command Options: -d: Include debugging output in the log file, CountBookmarks.log.
# Command Example: python CountBookmarks.py "/home/yourname/Downloads/your bookmarks.html"
#
# Compatible Browsers: This program is compatible with the Google Chrome, Mozilla Firefox, Microsoft Edge, and Microsoft Internet Explorer browsers.
#                      It may also work with non-Google, Chromium-based browsers and Apple Safari.
# Browsers Tested (Version):
#  - Google Chrome (80.0.3987.132 (Official Build) (64-bit))
#  - Mozilla Firefox (74.0 (64-bit))
#  - Microsoft Edge (44.18362.449.0)
#  - Microsoft Internet Explorer (11.719.18362.0)
#
# Development and Test Environments:
# Operating System (Version):
#  - Windows 10 Home (1909)
#  - Ubuntu Linux (18.04 LTS)
# Programming Language (Version):
#  - Python (3.8.2)
#  - Python (3.6.9)
# Python Environment on Ubuntu Linux:
#  - See https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-18-04
#
# Author: David Boyd
# Date: 03-21-20
#

#
# Process Overview: This program looks for DT (definition term) start tags that are immediately followed by H3 tags (for folder names) or A tags (for bookmark links),
#                   and for DL (definition list) start and end tags which represent, potentially nested, bookmark folders.
#

# ------------------------------------------------------------------------------------------- IMPORTS

import sys
import logging
import functools
from html.parser import HTMLParser
from collections import deque 

# ------------------------------------------------------------------------------------------- GLOBAL DECLARATIONS

tag_stack = deque() 
folder_name_stack = deque() 
local_bookmarks_count_stack = deque()
offspring_bookmarks_count_stack = deque() 

nesting_level_counter = -1 # nesting level 0 is the top level of the folder name hierarchy (i.e. while parsing within a highest level DL tag, the nesting level should be 0)
localandchild_bookmarks_counter = 0

log_file = "CountBookmarks.log"
output_file = "CountBookmarks.csv"
output_buffer = "Folder Name;Local Bookmarks;Total Bookmarks\n"

print = functools.partial(print, flush=True) # suppress print buffering
logging.basicConfig(filemode="w", filename=log_file, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger('__name__')

# ------------------------------------------------------------------------------------------- FUNCTION

def BuildBookmarkFolderName(NestingLevel):
    global folder_name_stack
    temp_folder_name_stack = deque()

    logger.debug("BuildBookmarkFolderName: NestingLevel: " + str(NestingLevel))
    logger.debug("BuildBookmarkFolderName: folder_name_stack: " + str(folder_name_stack)) 
    foldername = ""

    # assemble the hierarchical folder name
    i = 0
    while i <= NestingLevel:

       if len(folder_name_stack) <= 0: # the folder name stack is empty
          print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
          logger.critical("BuildBookmarkFolderName: Critical error: len(folder_name_stack) <= 0")
          print("Exiting CountBookmarks...")
          logger.critical("BuildBookmarkFolderName: Exiting CountBookmarks to avoid popping an empty folder_name_stack...")
          raise SystemExit() # abort this program

       temp_foldername = folder_name_stack.pop()
       foldername = temp_foldername + foldername
       temp_folder_name_stack.append(temp_foldername)
       i += 1

    # restore folder_name_stack
    i = 0
    while i <= NestingLevel:

       if len(temp_folder_name_stack) <= 0: # the temp_folder_name_stack is empty
          print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
          logger.critical("BuildBookmarkFolderName: Critical error: len(temp_folder_name_stack) <= 0")
          print("Exiting CountBookmarks...")
          logger.critical("BuildBookmarkFolderName: Exiting CountBookmarks to avoid popping an empty temp_folder_name_stack...")
          raise SystemExit() # abort this program

       folder_name_stack.append(temp_folder_name_stack.pop())
       i += 1

    return foldername

# ------------------------------------------------------------------------------------------- BEGIN CLASS BookmarksHTMLParser

class BookmarksHTMLParser(HTMLParser):

# ------------------------------------------------------------------------------------------- METHOD OF CLASS BookmarksHTMLParser

    def handle_starttag(self, tag, attrs):
        global tag_stack
        global offspring_bookmarks_count_stack 
        global nesting_level_counter
        global local_bookmarks_count_stack

        logger.debug("handle_starttag: Encountered a start tag: " + tag)

        if tag == "meta": # no append/push
           logger.debug("handle_starttag: tag == meta")
        elif tag == "title":
           logger.debug("handle_starttag: tag == title")
           tag_stack.append(tag)
        elif tag == "dl": # begin new folder
           logger.debug("handle_starttag: tag == dl")
           nesting_level_counter += 1
           logger.debug("handle_starttag: updated nesting_level_counter: " + str(nesting_level_counter))
           tag_stack.append(tag)
           local_bookmarks_count_stack.append(0) # create and initialize the local bookmarks counter for the current folder
           offspring_bookmarks_count_stack.append(0) # create and initialize the offspring bookmarks counter for the current folder
           logger.debug("handle_starttag: offspring_bookmarks_count_stack: " + str(offspring_bookmarks_count_stack))
        elif tag == "dt":
           logger.debug("handle_starttag: tag == dt")
        elif tag == "p": # no append/push
           logger.debug("handle_starttag: tag == p")
        elif tag == "h1":
           logger.debug("handle_starttag: tag == h1")
           tag_stack.append(tag)
        elif tag == "h3":
           logger.debug("handle_starttag: tag == h3")
           tag_stack.append(tag)
        elif tag == "a": # begin bookmark/link
           logger.debug("handle_starttag: tag == a")
           local_bookmarks_count_stack[-1] += 1 # d[-1] is the top element of deque d
           tag_stack.append(tag)
        else: # parser encountered unexpected tag, so don't append/push
           logger.debug("handle_starttag: unexpected tag: " + tag)

# ------------------------------------------------------------------------------------------- METHOD OF CLASS BookmarksHTMLParser

    def handle_endtag(self, tag):
        global folder_name_stack
        global tag_stack
        global offspring_bookmarks_count_stack 
        global nesting_level_counter
        global local_bookmarks_count_stack
        global localandchild_bookmarks_counter
        global output_buffer

        logger.debug("handle_endtag: Encountered an end tag: " + tag)

        if tag == "title":
           logger.debug("handle_endtag: tag == title")
        elif tag == "h1":
           logger.debug("handle_endtag: tag == h1")
        elif tag == "dl": # end of folder
           logger.debug("handle_endtag: tag == dl")
           logger.debug("handle_endtag: updated nesting_level_counter before decrementing it: " + str(nesting_level_counter))
           logger.debug("handle_endtag: folder_name_stack before popping top element off of it: " + str(folder_name_stack))
           current_folder_name = BuildBookmarkFolderName(nesting_level_counter)
           logger.debug("handle_endtag: folder " + current_folder_name + " has " + str(local_bookmarks_count_stack[-1]) + " local bookmarks") # d[-1] is the top element of deque d

           # Note 1: len(offspring_bookmarks_count_stack) will be 1 less than len(folder_name_stack), because while lowest level folders have a name, they, by definition, have no offspring.
           # note 2: Bookmarks are encountered and counted from the lowest level folders toward their ancestor folders.
           # note 3: Each offspring folder needs to add its total (local + offspring) bookmark count to the offspring bookmark count of its parent.
           #         The running bookmark count for its parent will be on top of the offspring_bookmarks_count_stack. 

           logger.debug("handle_endtag: offspring_bookmarks_count_stack before popping it: " + str(offspring_bookmarks_count_stack))

           if len(offspring_bookmarks_count_stack) <= 0: # the offspring bookmarks count stack is empty
              print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
              logger.critical("handle_endtag: Critical error: tag == dl and len(offspring_bookmarks_count_stack) <= 0")
              print("Exiting CountBookmarks...")
              logger.critical("handle_endtag: Exiting CountBookmarks to avoid popping an empty offspring_bookmarks_count_stack...")
              raise SystemExit() # abort this program

           offspring_bookmarks_count = offspring_bookmarks_count_stack.pop()
           logger.debug("handle_endtag: offspring_bookmarks_count_stack after popping it: " + str(offspring_bookmarks_count_stack))
           logger.debug("handle_endtag: offspring_bookmarks_count: " + str(offspring_bookmarks_count))
           localandchild_bookmarks_counter = offspring_bookmarks_count + local_bookmarks_count_stack[-1] # TOS value + local_bookmarks_counter
           logger.debug("handle_endtag: folder " + current_folder_name + " has " + str(localandchild_bookmarks_counter) + " total bookmarks (local + offspring)")

           if len(folder_name_stack) <= 0: # the folder name stack is empty
              print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
              logger.critical("handle_endtag: Critical error: tag == dl and len(folder_name_stack) <= 0")
              print("Exiting CountBookmarks...")
              logger.critical("handle_endtag: Exiting CountBookmarks to avoid popping an empty folder_name_stack...")
              raise SystemExit() # abort this program

           folder_name_stack.pop()
           logger.debug("handle_endtag: folder_name_stack after popping top element off of it: " + str(folder_name_stack))
           nesting_level_counter -= 1
           logger.debug("handle_endtag: updated nesting_level_counter after decrementing it: " + str(nesting_level_counter))

           if nesting_level_counter > -1: # nesting level 0 is the top level of the folder name hierarchy (i.e. while parsing within a highest level DL tag, the nesting level should be 0)

              if len(offspring_bookmarks_count_stack) <= 0: # the offspring bookmarks count stack is empty
                 print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
                 logger.critical("handle_endtag: Critical error: nesting_level_counter > -1 and len(offspring_bookmarks_count_stack) <= 0")
                 print("Exiting CountBookmarks...")
                 logger.critical("handle_endtag: Exiting CountBookmarks to avoid popping an empty offspring_bookmarks_count_stack...")
                 raise SystemExit() # abort this program

              offspring_bookmarks_count_stack.append(offspring_bookmarks_count_stack.pop() + localandchild_bookmarks_counter) # propagate this folder's bookmarks total up to the level of its parent folder
              logger.debug("handle_endtag: offspring_bookmarks_count_stack after propagating this folder's bookmarks total up to the level of its parent folder: " + str(offspring_bookmarks_count_stack))

           logger.debug("handle_endtag: folder " + current_folder_name + " has " + str(local_bookmarks_count_stack[-1]) + " local bookmarks and " + str(localandchild_bookmarks_counter) + " total bookmarks (local + offspring)")
           output_buffer = output_buffer + current_folder_name + ";" + str(local_bookmarks_count_stack[-1]) + ";" + str(localandchild_bookmarks_counter) + "\n" # add next line to buffer string for output file

           if len(local_bookmarks_count_stack) <= 0: # the local bookmarks count stack is empty
              print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
              logger.critical("handle_endtag: Critical error: len(local_bookmarks_count_stack) <= 0")
              print("Exiting CountBookmarks...")
              logger.critical("handle_endtag: Exiting CountBookmarks to avoid popping an empty local_bookmarks_count_stack...")
              raise SystemExit() # abort this program

           local_bookmarks_count_stack.pop()
           localandchild_bookmarks_counter = 0 # reset counter
           print(".", end="") # progress indicator, newline suppressed
        elif tag == "h3":
           logger.debug("handle_endtag: tag == h3")
        elif tag == "a":
           logger.debug("handle_endtag: tag == a")
        else:
           logger.debug("handle_endtag: unexpected tag: " + tag)

        if len(tag_stack) <= 0: # the tag stack is empty
           print("Critical error. See file \"", log_file, "\" for more information.", sep="") # padding suppressed
           logger.critical("handle_endtag: Critical error: len(tag_stack) <= 0")
           print("Exiting CountBookmarks...")
           logger.critical("handle_endtag: Exiting CountBookmarks to avoid popping an empty tag_stack...")
           raise SystemExit() # abort this program

        tag_stack.pop()

# ------------------------------------------------------------------------------------------- METHOD OF CLASS BookmarksHTMLParser

    def handle_data(self, data):
        global tag_stack
        global folder_name_stack
        global nesting_level_counter

        logger.debug("handle_data: nesting_level_counter: " + str(nesting_level_counter))
        logger.debug("handle_data: Encountered some data: " + data)
        logger.debug("handle_data: tag_stack: " + str(tag_stack))

        if len(tag_stack) == 0: 
           logger.debug("handle_data: tag_stack is empty")

        if len(tag_stack) > 0 and (tag_stack[-1] == "h1" or tag_stack[-1] == "h3"): # d[-1] is the top element of deque d

           if data[0] != "\n":
              folder_name_stack.append("/" + data)
              logger.debug("handle_data: current foldername: " + BuildBookmarkFolderName(nesting_level_counter))
              logger.debug("handle_data: folder_name_stack: " + str(folder_name_stack))

# ------------------------------------------------------------------------------------------- END CLASS BookmarksHTMLParser

# ------------------------------------------------------------------------------------------- MAIN

# sys.argv[0]: CountBookmarks.py
# sys.argv[1]: -d or filename
# sys.argv[2]: <NULL> or filename

logger.setLevel(logging.INFO)
logger.info("main: The command line arguments to the Python interpreter are: " + str(sys.argv)) 
numPythonArgs = len(sys.argv)
numProgramArgs = numPythonArgs - 1 # number of arguments to CountBookmarks
logger.info("main: The number of command line arguments to CountBookmarks is: " + str(numProgramArgs))

if numProgramArgs == 0 or numProgramArgs > 2:
   print("Invalid command. The correct command syntax is: python CountBookmarks.py [-d] File")
   logger.critical("main: Invalid command. The correct command syntax is: python CountBookmarks.py [-d] File")
   print("Exiting CountBookmarks...")
   logger.critical("main: Exiting CountBookmarks...")
   raise SystemExit() # abort this program

if numProgramArgs == 1:
   bookmarks_file = sys.argv[1]

if numProgramArgs == 2:

   if sys.argv[1] == "-d":
      logger.setLevel(logging.DEBUG)
      logger.debug("main: sys.argv[1] == " + str(sys.argv[1]))
      bookmarks_file = sys.argv[2]
   else:
      print(sys.argv[1], " is an invalid command option.", sep="") # padding suppressed
      logger.critical("main: " + str(sys.argv[1]) + " is an invalid command option.")
      print("The correct command syntax is: python CountBookmarks.py [-d] File")
      logger.critical("main: The correct command syntax is: python CountBookmarks.py [-d] File")
      print("Exiting CountBookmarks...")
      logger.critical("main: Exiting CountBookmarks...")
      raise SystemExit() # abort this program

logger.debug("main: bookmarks_file name just before opening and reading it: " + str(bookmarks_file)) 

with open(bookmarks_file) as fin: # open the bookmarks file
   read_data = fin.read() # read the bookmarks file
fin.closed

print("Counting the bookmarks in file \"", bookmarks_file, "\"", sep="", end="") # padding and newline suppressed
logger.info("main: Counting the bookmarks in file \"" + str(bookmarks_file) + "\"")
parser = BookmarksHTMLParser()
parser.feed(read_data) # parse the bookmarks file and count its bookmarks

logger.debug("main: tag_stack after parsing file: " + str(tag_stack)) 
logger.debug("main: folder_name_stack after parsing file: " + str(folder_name_stack)) 
logger.debug("main: local_bookmarks_count_stack after parsing file: " + str(local_bookmarks_count_stack))
logger.debug("main: offspring_bookmarks_count_stack after parsing file: " + str(offspring_bookmarks_count_stack))
print("\nWriting the results to file \"", output_file, "\"...", sep="") # padding suppressed
logger.info("main: Writing the results to file \"" + output_file + "\"...")

with open(output_file, "w") as fout:
   fout.write(output_buffer) # write the results to output_file
fout.closed

print("The bookmarks in file \"", bookmarks_file, "\" were successfully counted.", sep="") # padding suppressed
logger.info("main: The bookmarks in file \"" + str(bookmarks_file) + "\" were successfully counted.")
print("The results may be found in file \"", output_file, "\", and a log may be found in file \"", log_file, "\", in the working directory.", sep="") # padding suppressed
logger.info("main: The results may be found in file \"" + output_file + "\", and a log may be found in file \"" + log_file + "\", in the working directory.")

