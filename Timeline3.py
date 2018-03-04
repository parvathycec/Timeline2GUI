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
        label = tk.Label(self.master, text='Timeline Highlight')
        label.config(font=("Calibri", 16))
        label.pack(side=tk.TOP, anchor="n")
        self.input_label_frame = tk.LabelFrame(self.master, text="Input Data")
        self.input_label_frame.config(font=("Calibri", 14))
        self.input_label_frame.pack(side=tk.TOP, anchor="n", fill="x", \
                                    padx=(20, 20), pady=(5, 5), ipadx=20, ipady=10);
        self.inner_fields_frame_1 = tk.Frame(self.input_label_frame);
        self.inner_fields_frame_1.pack(side=tk.TOP, fill="x")
        self.__data_file_input = Input(self.inner_fields_frame_1, 'CSV File', action=self.select_file);

    def select_file(self):
        """Selects a file, get data, convert to dataframe and load it to table"""
        self.__file_name = tk.filedialog.askopenfilename(initialdir=os.getcwd(), \
                                                filetypes=(('CSV files', 'csv'),), title="Select Input CSV File.")
        self.__data_file_input.set_data(self.__file_name)
        self.csv_data = None
        self.csv_data = pd.read_csv(self.__file_name, low_memory = False)
        try:
            self.csv_data['date'] = pd.to_datetime((self.csv_data['date'] + " " + \
                                                    self.csv_data['time']),infer_datetime_format=True, errors='coerce');
        except Exception as e:
            print('Exception ', e)
            tk.messagebox.showerror(message="No column named date, please check your CSV file.");
        else:
            self.csv_data = self.csv_data.drop(['time'], axis=1)
            self.load_btns()

    def reset(self):
        """Reset the data to the initial data loaded from the CSV"""
        self.table_frame.destroy();
        self.inner_fields_frame_2.destroy();
        self.master.update();
        self.csv_data = pd.read_csv(self.__file_name, low_memory = False)
        self.csv_data['date'] = pd.to_datetime((self.csv_data['date'] + " " + self.csv_data['time']),
                                               infer_datetime_format=True, errors='coerce');
        self.csv_data = self.csv_data.drop(['time'], axis=1)
        self.load_btns()

    def load_btns(self):
        """load buttons like filter, search and query builder"""
        self.inner_fields_frame_2 = tk.Frame(self.input_label_frame);
        self.inner_fields_frame_2.pack(side=tk.BOTTOM, fill="x")
        filter_label = tk.Label(self.inner_fields_frame_2, text='Filter Columns')
        filter_label.config(font=("Calibri", 12))
        filter_label.pack(side="left");
        self.filter_value = tk.StringVar()
        self.filter_value = tk.Entry(self.inner_fields_frame_2, textvariable=self.filter_value)
        self.filter_value.config(font=("Calibri", 14), width=int(config_dict['entry_width']))
        self.filter_value.pack(side="left");
        self.load_table(self.csv_data);
        filter = tk.Button(self.inner_fields_frame_2, text="Filter", \
                           width=int(config_dict['button_width']), command=(lambda :self.filter(self.filter_value.get())))
        filter.pack(side='left')
        #query_builder = CustomButton(self.input_label_frame, 'Query Builder', 650, 50, 180, self.filter_query_window)
        search = tk.Button(self.inner_fields_frame_2, text="Search", width = int(config_dict['button_width']), \
                           command=self.search_window)
        search.pack(side='left')
        reset = tk.Button(self.inner_fields_frame_2, text="Reset", width = int(config_dict['button_width']), \
                          command=self.reset)
        reset.pack(side='left')

    def load_table(self, data=None):
        """Loads the table - excel sheet like"""
        if data is None or len(data) == 0:
            tk.messagebox.showerror(message="No data to show!");
            return;
        self.table_frame = tk.Frame(self.master)
        self.table_frame.config();
        self.table_frame.pack(anchor="c", fill=tk.BOTH, expand="YES")
        self.table = MyTable(self.table_frame, data);
        self.table.model.df = self.table.model.df.reset_index(drop=True)
        self.table.maxcellwidth = int(config_dict['max_cell_width'])
        self.table.show()

        source_webhist_highlight = \
            self.table.model.df.index[self.table.model.df['source'].astype(str).str.contains('WEBHIST')].tolist()
        source_lnk_highlight = self.table.model.df.index[self.table.model.df['source'] == 'LNK'].tolist()
        short_lnk_highlight = \
            self.table.model.df.index[self.table.model.df['short'].astype(str).str.endswith('.lnk', na=False)].tolist()
        win_prefetch_highlight = \
            self.table.model.df.index[self.table.model.df['sourcetype'].str.lower() == 'winprefetch'].tolist()
        sys_highlight = \
            self.table.model.df.index[self.table.model.df['short'].astype(str).str.endswith('.sys', na=False)].tolist()
        self.table.setRowColors(source_webhist_highlight, '#FFC001', 'all')  # using row numbers
        self.table.setRowColors(source_lnk_highlight, '#92D051', 'all')
        self.table.setRowColors(short_lnk_highlight, '#92D051',  'all')
        self.table.setRowColors(win_prefetch_highlight, '#FF0000', 'all')
        self.table.setRowColors(sys_highlight, '#0070C0', 'all')


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

    def filter_query_window(self):
        """TODO: Query Builder"""
        self.child_win = tk.Toplevel(self.master)
        self.child_win.wm_title("Build Filter Query")
        self.child_win.geometry("%dx%d%+d%+d" % (600, 400, 250, 125))
        self.headers = list(self.csv_data.columns.values)

        self.frame = tk.LabelFrame(self.child_win, text="Filter Query Builder")
        self.frame.config(font=("Calibri", 14))
        self.frame.propagate(0)
        self.filter_cols = []
        self.filter_values = []
        for num in range(5):
            self.child_frame = tk.Frame(self.frame);
            self.query_filter = tk.StringVar(self.frame)
            self.header_options = tk.OptionMenu(self.child_frame, self.query_filter, *self.headers)
            self.header_options.config(width=15)
            self.header_options.pack(side=tk.LEFT)
            self.query_value = tk.StringVar()
            self.query_value = tk.Entry(self.child_frame, textvariable=self.query_value)
            self.query_value.config(width=80)
            self.query_value.pack(side=tk.RIGHT)
            equal_label = tk.Label(self.child_frame, text=' = ')
            equal_label.config(font=("Calibri", 12))
            equal_label.pack();
            self.child_frame.pack(side="top", fill="both", padx=5, pady=5)
            self.filter_cols.append(self.query_filter)
            self.filter_values.append(self.query_value)
        #btn = CustomButton1(self.frame, title="Buid Query", action=self.create_query)
        self.frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)

    def create_query(self):
        """TODO: Query Builder"""
        query = '';
        date_range1 = None
        date_range2 = None
        for i in range(5):
            if not self.filter_cols[i].get() is '':
                if i > 0:
                    query += ' and '
                field_name = self.filter_cols[i].get();
                field_value = self.filter_values[i].get();
                if field_name == 'date':
                    if '-' in field_value:
                        date_ranges = field_value.split('-')
                        date_range1 = date_ranges[0]
                        date_range2 = date_ranges[1]
                        date_range1 = pd.to_datetime(date_range1, infer_datetime_format=True, errors='raise').date
                        date_range2 = pd.to_datetime(date_range2, infer_datetime_format=True, errors='raise').date
                        query += field_name + ' >= ' + '@date_range1' + ' and ' + field_name + ' <= @date_range2';
                    else:
                        date_range1 = pd.to_datetime(field_value, infer_datetime_format=True, errors='raise').date
                        query += field_name + '==' + '@date_range1'
                else:
                    query += field_name + '==' + '"' + field_value + '"'
        self.filter_value.insert(0, query)
        self.child_win.destroy()
        self.filter(query, date_range1, date_range2)
        return;

    def search(self, srch_value):
        """Performs case insensitive search on data loaded from CSV"""
        self.table_frame.destroy();
        self.master.update();
        self.search_win.destroy();
        mask = np.column_stack(\
            [self.csv_data[col].astype(str).str.lower().astype(str).str.contains(srch_value.lower(), na=False) for col in self.csv_data])
        self.csv_data_1 = self.csv_data.loc[mask.any(axis=1)]
        self.load_table(data=self.csv_data_1);

    def filter(self, query):
        """Filter data based on the query"""
        if query == '':
            tk.messagebox.showerror(message="Empty query!");
            return;
        self.table_frame.destroy()
        print('Query : ', query);
        try:
            if 'date' in query:
                query_arr = shlex.split(query, posix=False)
                indx = -1;
                date_found = False;
                for part in query_arr:
                    indx += 1
                    if (part == 'date') and (query_arr[indx+1] == '==' or query_arr[indx+1] == '!='):
                        if(len(query_arr[indx+2].split()) == 1):
                            query_arr[indx] = "date.dt.strftime('%Y-%m-%d')"
                            date_found = True

                if date_found:
                    query = ' '.join(query_arr)
            print(query)
            self.csv_data_1 = self.csv_data.query(query)
        except Exception as e:
            print('Exception ', e)
            tk.messagebox.showerror(message="Check your query!");
        else:
            self.load_table(data=self.csv_data_1);



if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0,0)
    try:
        config_file = open("configuration.txt", 'r')
    except:
        tk.messagebox.showerror(message="Please put the configuration.txt file in the same folder as python file.");
    else:
        config_dict = {}
        for row in config_file:
            key_values = row.split('=')
            config_dict[key_values[0]] = key_values[1]
        root.geometry("%dx%d+0+0" % (int(config_dict['window_x']),int(config_dict['window_y'])))
        title = 'Timeline Highlight'
        root.title(title)
        app = Main(root)
        app.focus_displayof()
        app.mainloop()


