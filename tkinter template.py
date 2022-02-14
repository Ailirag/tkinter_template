import os
import configparser
import sqlite3
import base64
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk


class IMAGE:
    str_edit = b'''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'''
    str_delete = b'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'
    str_add = b'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'
    str_refresh = b'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'


class stdPath:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    bin_dir = os.getcwd() + os.sep + 'bin'
    dataBase_path = bin_dir + os.sep + 'DataBase.db'
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.img_edit = tk.PhotoImage(data=IMAGE.str_edit)
        self.img_delete = tk.PhotoImage(data=IMAGE.str_delete)
        self.img_add = tk.PhotoImage(data=IMAGE.str_add)
        self.img_refresh = tk.PhotoImage(data=IMAGE.str_refresh)

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

        self.add_image = self.img_add
        btn_add = tk.Button(endbar, command=self.add_record,  bd=0,
                                    compound=tk.TOP, image=self.add_image)
        self.edit_image = self.img_edit
        btn_edit = tk.Button(endbar, command=self.update_record, bd=0,
                                    compound=tk.TOP, image=self.edit_image)
        self.delete_image = self.img_delete
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