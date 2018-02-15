#TODO
#Clean up code
#Change to pack and not place completely
#Configuration file
#error handling
#Processing
#set date
#date format
import tkinter as tk
from pandastable import Table
import numpy as np
import os
import pandas as pd

class LabelTag:

    def __init__(self, master, title, x_coor, y_coor, width, font_size=18, border=0, relief='flat'):
        label = tk.Label(master, text=title, borderwidth=border, relief=relief)
        label.config(font=("Calibri", font_size))
        label.place(x=x_coor, y=y_coor, width=width, height=25)

class CustomButton:

    def __init__(self, master, title, x_coor, y_coor, width, action=None):
        button = tk.Button(master, text=title, command=action)
        button.config(font=("Calibri", 10))
        button.place(x=x_coor, y=y_coor, width=width, height=25)

class CustomButton1:

    def __init__(self, master, title, width=100, action=None):
        button = tk.Button(master, text=title, command=action)
        button.config(font=("Calibri", 10))
        button.pack(fill=tk.BOTH, padx=10, pady=10);#place(x=x_coor, y=y_coor, width=width, height=25)

class Input:

    def __init__(self, master, title, x_coor, y_coor, width=900, has_button=False, action=None):
        # Setup Labels
        label = tk.Label(master, text=title)
        label.config(font=("Calibri", 12))
        label.place(x=x_coor, y=y_coor, height=25)

        self.__data = tk.StringVar()
        self.__data_entry = tk.Entry(master, textvariable=self.__data)
        self.__data_entry.place(x=150, y=y_coor, width=width, height=25)

        if has_button:
            self.__data_entry.config()
            button_title = 'Select ' + title
            print(action)
            button = tk.Button(master, text=button_title, command=action)
            button.config(font=("Calibri", 10))
            button.place(x=1050, y=y_coor, width=180, height=25)

    def set_data(self, value):
        self.__data.set(value)

    def get_data(self):
        return self.__data.get()

    def change_state(self, state):
        self.__data_entry.config(state=state)



class Main(tk.Frame):

    def __init__(self, master=None):
        """Constructor"""
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        """Main window initial with just file dialog option"""
        frame_title = 'Timeline Highlight'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1350)
        self.input_label_frame = tk.LabelFrame(self.master, text="Input Data")
        self.input_label_frame.config(font=("Calibri", 14))
        self.input_label_frame.propagate(0)
        self.input_label_frame.place(x=20, y=30, width=1240, height=125)
        self.__data_file_input = Input(self.input_label_frame, 'CSV File', 5, 10, has_button=True, action=self.select_file)

    def select_file(self):
        """Selects a file, get data, convert to dataframe and load it to table"""
        self.__file_name = tk.filedialog.askopenfilename(initialdir=os.getcwd(), \
                                                         filetypes=(('CSV files', 'csv'),), title="Select Input CSV File.")
        self.__data_file_input.set_data(self.__file_name)
        self.csv_data = None
        #dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y')
        self.csv_data = pd.read_csv(self.__file_name, low_memory = False)#, parse_dates=['date'], date_parser=dateparse, keep_date_col=True)
        #self.csv_data['date'] = pd.to_datetime(self.csv_data['date'], format='%m/%d/%Y', errors='coerce').dt.date;#.strftime
        self.load_btns()

    def reset(self):
        self.table_frame.destroy();
        self.master.update();
        self.csv_data = pd.read_csv(self.__file_name, low_memory = False)
        #self.csv_data['date'] = pd.to_datetime(self.csv_data['date'], format='%m/%d/%Y', errors='coerce').dt.date
        self.load_btns()

    def load_btns(self):
        """load buttons like filter, search and query builder"""
        filter_label = tk.Label(self.input_label_frame, text='Filter Columns')
        filter_label.config(font=("Calibri", 12))
        filter_label.place(x=10, y=50, height=20)
        self.filter_value = tk.StringVar()
        self.filter_value = tk.Entry(self.input_label_frame, textvariable=self.filter_value)
        self.filter_value.place(x=150, y=50, width=300, height=25)
        self.load_table(self.csv_data);
        filter = CustomButton(self.input_label_frame, 'Filter', 450, 50, 180, lambda :self.filter(self.filter_value.get()))
        query_builder = CustomButton(self.input_label_frame, 'Query Builder', 650, 50, 180, self.filter_query_window)
        search = CustomButton(self.input_label_frame, 'Search', 850, 50, 180, self.search_window)
        reset = CustomButton(self.input_label_frame, 'Reset', 1050, 50, 180, self.reset)


    def load_table(self, data=None):
        if data is None or len(data) == 0:
            tk.messagebox.showerror(message="No data to show!");
            return;
        self.table_frame = tk.Frame(self.master)
        self.table_frame.place(x=20, y=160, width=1250, height=500)
        self.table = Table(self.table_frame, dataframe=data, index=False, replace=False, \
                                showtoolbar=False, showstatusbar=False, showindex=True, theFont=("Calibri", 12))
        self.table.model.df = self.table.model.df.reset_index(drop=True)
        self.table.maxcellwidth = 600
        self.table.show()

        source_webhist_highlight = self.table.model.df.index[self.table.model.df['source'].astype(str).str.contains('WEBHIST')].tolist()
        source_lnk_highlight = self.table.model.df.index[self.table.model.df['source'] == 'LNK'].tolist()
        short_lnk_highlight = self.table.model.df.index[self.table.model.df['short'].astype(str).str.endswith('.lnk', na=False)].tolist()
        win_prefetch_highlight = self.table.model.df.index[self.table.model.df['sourcetype'] == 'WinPrefetch'].tolist()
        sys_highlight = self.table.model.df.index[self.table.model.df['short'].astype(str).str.endswith('.sys', na=False)].tolist()
        self.table.setRowColors(source_webhist_highlight, '#FFC001', 'all')  # using row numbers
        self.table.setRowColors(source_lnk_highlight, '#92D051', 'all')
        self.table.setRowColors(short_lnk_highlight, '#92D051',  'all')
        self.table.setRowColors(win_prefetch_highlight, '#FF0000', 'all')
        self.table.setRowColors(sys_highlight, '#0070C0', 'all')


    def search_window(self):
        self.search_win = tk.Toplevel(self.master)
        self.search_win.wm_title("Search Text")
        self.search_win.geometry("%dx%d%+d%+d" % (150, 180, 180, 150))
        self.search_frame = tk.LabelFrame(self.search_win, text="Search Text")
        self.search_frame.config(font=("Calibri", 14))
        self.search_frame.propagate(0)
        self.search_value = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_value)
        self.search_entry.config(width=80)
        self.search_entry.pack()
        btn = CustomButton1(self.search_frame, title="Search", action=lambda :self.search(self.search_value.get()))
        btn = CustomButton1(self.search_frame, title="Close", action=lambda: self.search_win.destroy())
        self.search_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.search_entry.focus_set();

    def filter_query_window(self):
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
            self.query_value.config(width=20)
            self.query_value.pack(side=tk.RIGHT)
            equal_label = tk.Label(self.child_frame, text=' = ')
            equal_label.config(font=("Calibri", 12))
            equal_label.pack();
            self.child_frame.pack(side="top", fill="both", padx=5, pady=5)
            self.filter_cols.append(self.query_filter)
            self.filter_values.append(self.query_value)
        btn = CustomButton1(self.frame, title="Buid Query", action=self.create_query)
        self.frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)

    def create_query(self):
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
                        date_range1 = pd.to_datetime(date_range1, format='%m/%d/%Y', errors='raise').date
                        date_range2 = pd.to_datetime(date_range2, format='%m/%d/%Y', errors='raise').date
                        query += field_name + ' >= ' + '@date_range1' + ' and ' + field_name + ' <= @date_range2';
                    else:
                        date_range1 = pd.to_datetime(field_value, format='%m/%d/%Y', errors='raise').date
                        query += field_name + '==' + '@date_range1'
                else:
                    query += field_name + '==' + '"' + field_value + '"'
        self.filter_value.insert(0, query)
        self.child_win.destroy()
        self.filter(query, date_range1, date_range2)
        return;

    def search(self, srch_value):
        self.table_frame.destroy();
        self.master.update();
        self.search_win.destroy();
        mask = np.column_stack([self.csv_data[col].astype(str).str.contains(srch_value, na=False) for col in self.csv_data])
        self.csv_data_1 = self.csv_data.loc[mask.any(axis=1)]
        self.load_table(data=self.csv_data_1);

    def filter(self, query, date_range1=None, date_range2=None):
        if query == '':
            tk.messagebox.showerror(message="Empty query!");
            return;
        self.table_frame.destroy();
        #self.master.update();
        self.csv_data['date'] = pd.to_datetime(self.csv_data['date'], format='%m/%d/%Y',
                                               errors='coerce');  # .strftime
        date_range = []
        counter = -1;
        arr_query = [];
        if 'date' in query:
            arr_query = query.split();
            indx = -1;
            for part in arr_query:
                indx += 1;
                if part == 'date':
                    if len(arr_query) > (indx+2):
                        date_range.append(pd.to_datetime(arr_query[indx+2],format='%m/%d/%Y', errors='raise'));
                        counter += 1;
                        print(date_range[counter])
                        arr_query [indx+2] = '@date_range['+str(counter)+']'
        query = ' '.join(arr_query);
        try:
            print('Query is : ', query);
            self.csv_data_1 = self.csv_data.query(query)
            self.csv_data['date'] = self.csv_data['date'].dt.strftime(date_format='%m/%d/%Y')
            self.csv_data_1['date'] = self.csv_data_1['date'].dt.strftime(date_format='%m/%d/%Y')

        except Exception as e:
            print('Exception ', e)
            tk.messagebox.showerror(message="Check your query!");
        else:
            self.load_table(data=self.csv_data_1);



if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0,0)
    root.geometry("%dx%d+0+0" % (1300, 700))
    title = 'Timeline Highlight'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()

