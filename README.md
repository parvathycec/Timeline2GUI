# Timeline2GUI
This is a tool to import and view contents of a CSV file.
The features include filtering the data based on column values, searching for a text, saving the data to a CSV file and highlighting few rows.

-------------------------
Requirements:
-------------------------
Python 3.6

Pandastable (development version)

-----------------------
Installation
-----------------------

How to install?

Download the Timeline2GUI repo. 

Run the following command from command line.

python setup.py install

This command should automatically install all the dependencies.

If you face any issue with installation, run the following command in the command line.

python -m pip install -e git://github.com/dmnfarrell/pandastable.git@pandastable#egg=pandastable


Command to run the tool in command line:

python Timeline2GUI.py

--------------------
configuration.txt
------------------
The following is a description of what each value in Configuration.txt means.

window_x=1350# horizontal size of the main window (increase this for big screens)

window_y=700# vertical size of the main window (increase this for big screens)

button_width=25# default size of buttons (increase this for big screens)

entry_width=40# horizontal size of text fields (increase this for big screens)

search_window_x1=180# x1 of search window (increase this for big screens)

search_window_y1=180# y1 of search window (increase this for big screens)

search_window_x2=200# x2 of search window (increase this for big screens)

search_window_y2=160# y2 of search window (increase this for big screens)

max_cell_width=800# length of each cell in the table

--------------------
highlights.txt
------------------
Add all highlights you need here

You can give multiple highlight option, each seperated by a new line

In each highlight, there are 3 parts separated by =

first part can be the column name (ex:short here) or * to indicate all columns
second part is the text (to be searched for highlighting, ex: USB)

The search is case insensitive

Third option is the color hex code, give the hex code of the color you want to highlight the row

For Example:

*=USB=#add8e6

short=lnk=#FF0000
