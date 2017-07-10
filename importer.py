"""
File importer graphical application
"""

import tkinter
from tkinter import ttk


def tag_entry_callback(key):
    print('key event on tag entry')


def tag_view_select(event):
    print('tag view')


def document_view_select(event):
    print('document view')


def file_refresh():
    print('file list refresh')


def file_select(event):
    print('file list selection')


root = tkinter.Tk()
root.title('Grimoire - Importer')

tag_entry = tkinter.Entry(root)
tag_entry.bind('<Key>', tag_entry_callback)
ordering_combobox = ttk.Combobox(root)
tag_view = tkinter.Listbox(root)
tag_view.bind('<<ListboxSelect>>', tag_view_select)

document_view = ttk.Treeview(root, columns=('name', 'type'))
document_view.heading('name', text='name')
document_view.heading('type', text='type')
document_view.bind('<<TreeviewSelect>>', document_view_select)

file_refresh_button = tkinter.Button(root, text='Refresh', command=file_refresh)
file_list = tkinter.Listbox(root)
file_list.bind('<<ListboxSelect>>', file_select)

full = (tkinter.N, tkinter.S, tkinter.E, tkinter.W)

tag_entry.grid(row=0, column=0, sticky=full)
ordering_combobox.grid(row=0, column=1, sticky=full)
tag_view.grid(row=1, column=0, sticky=full)
document_view.grid(row=1, column=1, sticky=full)

file_refresh_button.grid(row=0, column=2, sticky=full)
file_list.grid(row=1, column=2, sticky=full)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=3)

root.mainloop()
