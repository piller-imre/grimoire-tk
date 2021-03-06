"""
Two pane commander application
"""

import tkinter
from tkinter import ttk


def left_tag_view_select(event):
    print('left tag view')


def left_document_view_select(event):
    print('left document view')


def right_tag_view_select(event):
    print('right tag view')


def right_document_view_select(event):
    print('right document view')


root = tkinter.Tk()
root.title('Grimoire - Commander')

left_tag_entry = tkinter.Entry(root)
left_ordering_combobox = ttk.Combobox(root)
left_tag_view = tkinter.Listbox(root)
left_tag_view.bind('<<ListboxSelect>>', left_tag_view_select)

left_document_view = ttk.Treeview(root, columns=('name', 'type'))
left_document_view.heading('name', text='name')
left_document_view.heading('type', text='type')
left_document_view.bind('<<TreeviewSelect>>', left_document_view_select)

right_tag_entry = tkinter.Entry(root)
right_ordering_combobox = ttk.Combobox(root)
right_tag_view = tkinter.Listbox(root)
right_tag_view.bind('<<ListboxSelect>>', right_tag_view_select)

right_document_view = ttk.Treeview(root, columns=('name', 'type'))
right_document_view.heading('name', text='name')
right_document_view.heading('type', text='type')
right_document_view.bind('<<TreeviewSelect>>', right_document_view_select)

full = (tkinter.N, tkinter.S, tkinter.E, tkinter.W)

left_tag_entry.grid(row=0, column=0, sticky=full)
left_ordering_combobox.grid(row=0, column=1, sticky=full)
left_tag_view.grid(row=1, column=0, sticky=full)
left_document_view.grid(row=1, column=1, sticky=full)

right_tag_entry.grid(row=0, column=2, sticky=full)
right_ordering_combobox.grid(row=0, column=3, sticky=full)
right_tag_view.grid(row=1, column=2, sticky=full)
right_document_view.grid(row=1, column=3, sticky=full)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=4)

# TODO: Remove the following sample documents!
left_document_view.insert('', 0, iid=1, text='first', values=['my name', 'my type'])
right_document_view.insert('', 0, iid=2, text='second', values=['other name', 'other type'])

root.mainloop()
