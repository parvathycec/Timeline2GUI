# csvtable
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

How to install pandastable development version of Pandastable?

python -m pip install -e git://github.com/dmnfarrell/pandastable.git@pandastable#egg=pandastable

How to run the tool?

Checkout the csvtable repo. 
The files needed are Timeline.py, help.png, configuration.txt
All the above-mentioned files should be in one folder.

Command to run the tool in command line:

python Timeline.py

--------------------
Configuration.txt
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

