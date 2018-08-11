import tkinter as tk
from pandastable import Table
import numpy as np
import os
import pandas as pd
import shlex

class MyTable(Table):
    """Customized Table for sorting ascending and descending"""
    def __init__(self, frame, data):
        super().__init__(parent=frame, dataframe=data, index=False, replace=False, \
              showtoolbar=False, showstatusbar=False, showindex=True, thefont=("Calibri", 12))
        self.ascending = 1

    def sortTable(self, columnIndex=None, ascending=1, index=False):
        """Set up sort order dict based on currently selected field"""
        super().sortTable(ascending=self.ascending)
        self.ascending = 1 - self.ascending

class Input:
    """Input box frame on the top"""
    def __init__(self, master, title, action=None):
        # Setup Labels
        label = tk.Label(master, text=title)
        label.config(font=("Calibri", 14))
        label.pack(side="left", anchor="n", padx=(5, 5));
        self.__data = tk.StringVar()
        self.__data_entry = tk.Entry(master, textvariable=self.__data)
        self.__data_entry.pack(side="left", expand="YES", fill="x", anchor="n", padx=(20, 20))
        self.__data_entry.config(font=("Calibri", 14))
        button_title = ' Select ' + title + ' ';
        button = tk.Button(master, text=button_title, width = int(config_dict['button_width']), command=action)
        button.config(font=("Calibri", 10))
        button.pack(side="right", anchor="n", padx=(10,10))

    def set_data(self, value):
        self.__data.set(value)

    def get_data(self):
        return self.__data.get()

class Main(tk.Frame):
    """Main class"""
    def __init__(self, master=None):
        """Constructor"""
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        """Main window initial with just file dialog option"""
        label = tk.Label(self.master, text='Timeline2GUI')
        label.config(font=("Calibri", 16))
        label.pack(side=tk.TOP, anchor="n")
        self.table_frame = None;
        self.inner_fields_frame_2 = None;
        self.inner_fields_frame_1 = None;
        self.input_label_frame = None;
        self.csv_data = None;
        self.show_data = None;
        self.current_data = None;
        self.input_label_frame = tk.LabelFrame(self.master, text="Input Data")
        self.input_label_frame.config(font=("Calibri", 14))
        self.input_label_frame.pack(side=tk.TOP, anchor="n", fill="x", \
                                    padx=(20, 20), pady=(5, 5), ipadx=20, ipady=10);
        self.inner_fields_frame_1 = tk.Frame(self.input_label_frame);
        self.inner_fields_frame_1.pack(side=tk.TOP, fill="x")
        self.__data_file_input = Input(self.inner_fields_frame_1, 'CSV File', action=self.select_file);



    def show_loading(self):
        self.loading_label = tk.Label(self.master, text='Loading... Please Wait..')
        self.loading_label.config(font=("Calibri", 16))
        self.loading_label.pack(side=tk.TOP, anchor="n")

    def hide_loading(self):
        self.loading_label.destroy();

    def select_file(self):
        """Selects a file, get data, convert to dataframe and load it to table"""
        self.clearBtns();
        self.__file_name = tk.filedialog.askopenfilename(initialdir=os.getcwd(), \
                                                filetypes=(('CSV files', 'csv'),), title="Select Input CSV File.")
        if self.__file_name is not None and self.__file_name is not '':
            self.__data_file_input.set_data(self.__file_name)
            self.load_btns();
        else:
            tk.messagebox.showerror(message="Please select a valid file.");
            return;

    def load_data(self):
        if self.table_frame is not None:
            print('destroyed');
            self.table_frame.destroy();
        self.show_loading();
        self.master.update();
        self.csv_data = None;
        self.current_data = None;
        try:
            self.csv_data = pd.read_csv(self.__file_name, low_memory=False)
            self.csv_data['date'] = pd.to_datetime((self.csv_data['date'] + " " + \
                                                    self.csv_data['time']),infer_datetime_format=True, errors='coerce');
        except Exception as e:
            self.hide_loading();
            print('Exception ', e)
            tk.messagebox.showerror(message="No column named date, please check your CSV file.");
        else:
            self.hide_loading();
            self.csv_data = self.csv_data.drop(['time'], axis=1)
            self.current_data = self.csv_data;
            self.filter(self.filter_value_1.get())


    def save_csv(self):
        if self.current_data is None or len(self.current_data) == 0:
            tk.messagebox.showerror(message="Load data before saving!");
            return;
        filename = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), \
                    initialfile='Timeline.csv', filetypes=(('CSV files', 'csv'),), \
                                            title="Select Input CSV File.", defaultextension='*.csv')
        try:
            self.current_data.to_csv(filename, index=False, encoding='utf-8');
        except Exception as e:
            tk.messagebox.showerror(message="Sorry, Could not save!");
            print(e);
        else:
            tk.messagebox.showinfo("Success", "CSV file saved to "+filename);

    def reset(self):
        """Reset the data to the initial data loaded from the CSV"""
        self.clearBtns();
        self.show_loading();
        self.master.update();
        #if self.csv_data is not None:
        #    self.current_data = self.csv_data;
        self.current_data = None;
        self.hide_loading();
        if self.inner_fields_frame_2 is not None:
            self.load_btns()

    def clearBtns(self):
        if self.table_frame is not None:
            print('destroyed');
            self.table_frame.destroy();
        if self.inner_fields_frame_2 is not None:
            self.inner_fields_frame_2.destroy();
        if self.show_data is not None:
            self.show_data.destroy();

    def load_btns(self):
        """load buttons like filter, search and query builder"""
        self.inner_fields_frame_2 = tk.Frame(self.input_label_frame);
        self.inner_fields_frame_2.pack(side=tk.BOTTOM, fill="x")
        filter_label = tk.Label(self.inner_fields_frame_2, text='Filter Columns')
        filter_label.config(font=("Calibri", 12))
        filter_label.pack(side="left");
        self.filter_value_1 = tk.StringVar()
        self.filter_value = tk.Entry(self.inner_fields_frame_2, textvariable=self.filter_value_1)
        self.filter_value.config(font=("Calibri", 14), width=int(config_dict['entry_width']))
        self.filter_value.pack(side="left");
        help = tk.Button(self.inner_fields_frame_2, width=20, height=20, command=self.help_window)
        img = tk.PhotoImage(file="help.png", width=20, height=20)
        help.config(image=img)
        help.image = img;
        help.pack(side='left')

        self.show_data = tk.Button(self.inner_fields_frame_2, text="Load data", \
                                   width=int(config_dict['button_width']),
                                   command=self.load_data)
        self.show_data.pack(side='left', padx=10)
        #self.load_table();
        #filter = tk.Button(self.inner_fields_frame_2, text="Filter", \
        #                   width=int(config_dict['button_width']), command=(lambda :self.filter(self.filter_value.get())))
        #filter.pack(side='left')
        search = tk.Button(self.inner_fields_frame_2, text="Search", width = int(config_dict['button_width']), \
                           command=self.search_window)
        search.pack(side='left', padx=10)
        reset = tk.Button(self.inner_fields_frame_2, text="Clear", width = int(config_dict['button_width']), \
                          command=self.reset)
        reset.pack(side='left', padx=10)
        save = tk.Button(self.inner_fields_frame_2, text="Save as CSV", width=int(config_dict['button_width']), \
                          command=self.save_csv)
        save.pack(side='left', padx=10)

    def load_table(self):
        """Loads the table - excel sheet like"""
        if self.current_data is None or len(self.current_data) == 0:
            tk.messagebox.showerror(message="No data to show!");
            return;
        self.table_frame = tk.Frame(self.master)
        self.table_frame.config();
        self.table_frame.pack(anchor="c", fill=tk.BOTH, expand="YES")
        self.table = MyTable(self.table_frame, self.current_data);
        self.table.model.df = self.table.model.df.reset_index(drop=True)
        self.table.maxcellwidth = int(config_dict['max_cell_width'])
        self.table.show()
        self.highlight()


    def highlight(self):
        """Highlights rows based on a text"""
        try:
            highlights_file = open("highlights.txt", 'r')
        except:
            print("No highlights found!");
            return; 
        for row in highlights_file:
            highlight = row.rstrip('\n').rstrip('\r')
            if highlight:#To avoid empty rows
                highlight_options = highlight.split('=')
                if len(highlight_options) == 3:
                    column = highlight_options[0].strip()
                    if column != '*' and column not in self.csv_data.columns.values:
                        print(column, ' -mentioned in highlights.txt - does not exist')
                        continue
                    search_text = highlight_options[1].strip()
                    highlight_color = highlight_options[2].strip()
                    if column == '*':
                        for col in self.table.model.df.columns:
                            highlight = self.table.model.df.index[\
                                self.table.model.df[col].astype(str).str.contains(search_text, na=False, case=False)].tolist()
                            self.table.setRowColors(highlight, highlight_color, 'all')
                    else:
                        highlight = self.table.model.df.index[\
                            self.table.model.df[column].astype(str).str.contains(search_text, na=False, case=False)].tolist()
                    self.table.setRowColors(highlight, highlight_color, 'all')
                else:
                    print('Please check your settings for highlight option.')
                    print('This is an example of the format: highlights=*=USB=#FF0000,*=LNK=#EE0000')


    def help_window(self):
        """Displays a search window box"""
        lines = ['You may enter the query to filter the data based on column names.',\
                 'The comparison operators you may use include ==, <, > and !=.',
                 'The values should be in single quotes.',
                 'Paranthesis, and, or opertors work.',
                 'For date comparisons, you can either give date alone or date time.',
                 'If only date is given, the query considers the default time to be 00:00:00',
                 'Preferred date format is YYYY-MM-DD HH:MM:SS, though the program will try to infer other valid date formats.',
                 '', 'A few of the examples are:',
                 "date > '2017-01-01' and date < '2018-01-01'",
                 "date == '2015-03-16 10:53:00'",
                 "type=='ctime' or type == 'atime'"]
        #self.master.option_add('*Dialog.msg.font', 'Calibri 14')
        tk.messagebox.showinfo('Help on Filter', "\n".join(lines), )

    def search_window(self):
        """Displays a search window box"""
        self.search_win = tk.Toplevel(self.master)
        self.search_win.wm_title("Search Text")
        self.search_win.geometry("%dx%d%+d%+d" % (int(config_dict['search_window_x1']), \
                                                int(config_dict['search_window_y1']), \
                                                int(config_dict['search_window_x2']), \
                                                    int(config_dict['search_window_y2'])))
        self.search_frame = tk.LabelFrame(self.search_win, text="Search Text")
        self.search_frame.config(font=("Calibri", 14))
        self.search_frame.propagate(0)
        self.search_value = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_value)
        self.search_entry.config(width=80)
        self.search_entry.pack()
        search_btn = tk.Button(self.search_frame, text="Search",command=lambda :self.search(self.search_value.get()))
        search_btn.config(font=("Calibri", 10))
        search_btn.pack(fill="x")
        close_btn = tk.Button(self.search_frame, text="Close", width="40", command=lambda: self.search_win.destroy())
        close_btn.config(font=("Calibri", 10))
        close_btn.pack(fill="x")
        self.search_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.search_entry.focus_set();

    def search(self, srch_value):
        """Performs case insensitive search on data loaded from CSV"""
        if self.current_data is None or len(self.current_data) == 0:
            tk.messagebox.showerror(message="No data to search! Please load data first.");
            return;
        if srch_value is None or srch_value is '':
            tk.messagebox.showerror(message="Enter a search value!");
            return;
        if self.table_frame:
            self.table_frame.destroy();
        self.show_loading();
        self.master.update();
        self.search_win.destroy();
        mask = np.column_stack(\
            [self.current_data[col].astype(str).str.lower().astype(str).str.contains(srch_value.lower(), na=False, regex=True) for col in self.current_data])
        self.current_data = self.current_data.loc[mask.any(axis=1)]
        self.hide_loading();
        self.load_table();

    def filter(self, query):
        """Filter data based on the query"""
        #if query == '':
        #    tk.messagebox.showerror(message="Empty query!");
        #    return;
        if self.table_frame:
            self.table_frame.destroy()
        self.show_loading();
        self.master.update();
        print('Query : ', query);
        try:
            if query != '':
                self.current_data = self.csv_data.query(query)
        except Exception as e:
            self.hide_loading();
            print('Exception ', e)
            tk.messagebox.showerror(message="Check your query!");
        else:
            self.hide_loading();
            self.load_table();



if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0,0)
    try:
        config_file = open("configuration.txt", 'r')
    except:
        tk.messagebox.showerror(message="Configuration Error: \
        The configuration.txt file should be in the same folder as python file.");
    else:
        config_dict = {}
        for row in config_file:
            row = row.rstrip('\n').rstrip('\r')
            if row:#To avoid empty rows
                key_values = row.split('=', 1)
                #print('key_values ', key_values)
                key_values[1] = key_values[1].rstrip('\n').rstrip('\r')
                config_dict[key_values[0]] = key_values[1]
        root.geometry("%dx%d+0+0" % (int(config_dict['window_x']),int(config_dict['window_y'])))
        title = 'Timeline Highlight'
        root.title(title)
        app = Main(root)
        app.focus_displayof()
        app.mainloop()

