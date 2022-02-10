import os
import configparser
import sqlite3
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

class stdPath:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    bin_dir = os.getcwd() + os.sep + 'bin'
    dataBase_path = bin_dir + os.sep + 'DataBase.db'
    imagedir = os.getcwd() + '\\image\\'
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Editable
        self.title = 'Test window'
        self.all_columns = tuple('ID,Name,Regexp,Creator'.split(','))
        self.all_columns_width = (15, 300, 500, 250)
        self.all_columns_translate = 'ID,Name,Regexp,Creator'.split(',')
        self.all_columns_type_sqllite = 'INTEGER, TEXT, TEXT, TEXT'.split(',')
        self.height_window = 420
        self.length_child_entry = 50
        self.child_withxheight = '550x250'
        # End of edit

        self.all_width = sum(self.all_columns_width)
        self.max_width = max(self.all_columns_width)
        self.db = DB(self.all_columns, self.all_columns_type_sqllite)
        self.init_main()

    def button1_on_tree_action(self, field):
        # command = (path_to_exe,' -',idconnect)
        # subprocess.Popen(command, shell=True)
        pass

    def init_main(self):

        #toolbar START
        #toolbar END

        self.tree = ttk.Treeview(self, columns=self.all_columns, height=15, show='headings')

        for index in range(len(self.all_columns)):
            self.tree.column(self.all_columns[index], width=self.all_columns_width[index], anchor=tk.CENTER)
            self.tree.heading(self.all_columns[index], text=self.all_columns_translate[index])

        self.tree.bind('<Double-Button-1>', lambda event: self.button1_on_tree_action(self.tree.set(self.tree.selection()[0], '#2')))
        self.tree.pack()
        #endbar START

        endbar = tk.Frame(bd=2)
        endbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_image = tk.PhotoImage(file="image/plus.png")
        btn_add = tk.Button(endbar, command=self.add_record,  bd=0,
                                    compound=tk.TOP, image=self.add_image)
        self.edit_image = tk.PhotoImage(file="image/edit.png")
        btn_edit = tk.Button(endbar, command=self.update_record, bd=0,
                                    compound=tk.TOP, image=self.edit_image)
        self.delete_image = tk.PhotoImage(file="image/minus.png")
        btn_delete = tk.Button(endbar, command=self.delete_record, bd=0,
                             compound=tk.TOP, image=self.delete_image)
        btn_delete.pack(side=tk.RIGHT)
        btn_edit.pack(side=tk.RIGHT)
        btn_add.pack(side=tk.RIGHT)
        #endbar END

        sr_bar = tk.Frame(bg='#d7d8e0', bd=2)
        sr_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry_search = ttk.Entry(sr_bar)
        self.entry_search.bind('<Return>', lambda event : self.view_records(self.entry_search.get()))
        self.entry_search.pack(fill=tk.X)

        self.view_records()

    def update_record(self):
        Child('edit', self.tree.set(self.tree.selection()[0]))

    def update_record_sql(self, data_to_sql):
        selectid = self.tree.set(self.tree.selection()[0], '#1')
        set_string = []
        mas_arg = []
        for column in self.all_columns:
            if column != 'ID':
                mas_arg.append(data_to_sql[column])
                set_string.append(f'{column}=?')

        mas_arg.append(selectid)
        mas_arg = tuple(mas_arg)

        self.db.c.execute(f'''UPDATE data SET {','.join(set_string)} WHERE ID=?''', mas_arg)
        self.db.conn.commit()

    def delete_record(self):
        yesno = mb.askyesno('Внимание!','Вы действительно хотите удалить выделенные записи?')
        if yesno:
            for selection_item in self.tree.selection():
                self.db.c.execute('DELETE FROM data WHERE id={}'.format(self.tree.set(selection_item, '#1')))
            self.db.conn.commit()
            self.view_records()

    def add_record(self):
        Child('add')

    def open_dialog(self):
        filename = fd.askopenfilename()
        if filename > '':
            self.path_to_file_to_pars = filename

    def insert_data(self, data_to_sql):
        mas_arg = []
        mas_quest = []
        mas_column = []
        for column in self.all_columns:
            if column != 'ID':
                mas_arg.append(data_to_sql[column])
                mas_quest.append('?')
                mas_column.append(column)

        self.db.c.execute(f"INSERT INTO data({','.join(mas_column)}) VALUES ({','.join(mas_quest)})",
                       tuple(mas_arg))
        self.db.conn.commit()

    def view_records(self, search=''):
        mas_argv = []
        mas_string = []
        for column in self.all_columns:
            if column != 'ID':
                mas_argv.append('%'+search+'%')
                mas_string.append(f'{column} like ? ')

        if search == '':
            self.db.c.execute('''SELECT * FROM data ''')
        else:
            self.db.c.execute(f'''SELECT * FROM data WHERE {' OR '.join(mas_string)}''',
                         tuple(mas_argv))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class DB:
    def __init__(self, columns, columns_type):
        self.conn = sqlite3.connect(stdPath.dataBase_path)
        self.c = self.conn.cursor()

        all_fields = []
        for index in range(len(columns)):
            if columns[index] != 'ID':
                all_fields.append(f'{columns[index]} {columns_type[index]}')


        connect_table = f'''\
                       CREATE TABLE IF NOT EXISTS data (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       {','.join(all_fields)}
                       );'''

        self.c.execute(connect_table)
        self.conn.commit()

class Child(tk.Toplevel):
    def __init__(self, variable, editdict = {}):
        super().__init__(root)
        self.view = app
        self.init_child(variable, editdict)

    def init_child(self, variable,editdict):

        if variable == 'add':
            dict_set = {'title':'Добавить', 'name_ok':'Добавить', 'command':self.add_record}
        elif variable == 'edit':
            dict_set = {'title':'Изменить', 'name_ok':'Изменить', 'command':self.edit_record}

        start_position_y = 50

        for column in self.view.all_columns:
            if column != 'ID':
                label = tk.Label(self, text=f'{column}:')
                label.place(x=50, y=start_position_y)
                start_position_y+=30

        start_position_y = 50
        self.entry_dict = dict()
        for index in range(1, len(self.view.all_columns)):
            self.entry_dict['entry' + str(index)] = ttk.Entry(self, width=self.view.length_child_entry)
            self.entry_dict['entry' + str(index)].place(x=200, y=start_position_y)
            start_position_y += 30

        self.title(dict_set['title'])
        self.geometry(f'{self.view.child_withxheight}+400+300')
        # self.resizable(False, False)

        if not editdict == {}:
            for index in range(1, len(self.view.all_columns)):
                self.entry_dict['entry' + str(index)].insert(0, editdict[self.view.all_columns[index]])

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=200)

        btn_ok = ttk.Button(self, text=dict_set['name_ok'], command=dict_set['command'])
        btn_ok.place(x=220, y=200)
        btn_ok.bind('<Button-1>')

        self.grab_set()
        self.focus_set()

    def get_all_data(self):
        result_dict = {}
        for index in range(1, len(self.view.all_columns)):
            result_dict[self.view.all_columns[index]] = self.entry_dict['entry' + str(index)].get()
        return result_dict

    def data_is_full(self,data_to_sql):
        fill = True
        for data in data_to_sql:
            if data == '':
                fill = False
                break
        return fill

    def edit_record(self):
        data_to_sql = self.get_all_data()
        if self.data_is_full(data_to_sql):
            self.view.update_record_sql(data_to_sql)
            self.view.view_records()
            self.destroy()
        else:
            mb.showinfo('Внимание', "Заполните все поля")

        print('edit_record')

    def add_record(self):
        data_to_sql = self.get_all_data()
        if self.data_is_full(data_to_sql):
            self.view.insert_data(data_to_sql)
            self.view.view_records()
            print('add_record')
            self.destroy()
        else:
            mb.showinfo('Внимание', "Заполните все поля")


if __name__ == "__main__":
    root = tk.Tk()
    # root.iconbitmap('image/icon.ico')
    app = Main(root)
    app.pack()
    root.title(app.title)
    root.geometry(f"{app.all_width}x{app.height_window}+300+200")
    root.resizable(False, False)
    root.mainloop()