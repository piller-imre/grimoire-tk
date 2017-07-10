"""
File importer graphical application
"""

import tkinter
from tkinter import ttk

from grimoire.database import Database
from grimoire.repository import Repository
from grimoire.scope import Scope
from grimoire.storage import Storage


database = Database('/tmp/importer/grimoire.log')
storage = Storage('/tmp/importer/storage/')
repository = Repository(database, storage)
scope = Scope(database)


def list_untracked_files():
    untracked_file_paths = repository.collect_untracked_file_paths()
    file_list.delete(0, tkinter.END)
    for file_path in untracked_file_paths:
        file_list.insert(tkinter.END, file_path)


def list_current_documents():
    document_view.delete(*document_view.get_children())
    documents = scope.get_selection_documents()
    for document in documents:
        document_view.insert('', tkinter.END, iid=document.id, text=document.name,
                             values=[document.path, document.type], tags=['selected'])
    documents = scope.get_concept_only_documents()
    for document in documents:
        document_view.insert('', tkinter.END, iid=document.id, text=document.name,
                             values=[document.path, document.type])
    document_view.tag_configure('selected', background='#FFFFBB')


def list_current_tags():
    tag_view.delete(0, tkinter.END)
    concept_tags = scope.get_concept_tags()
    for tag in concept_tags:
        tag_view.insert(tkinter.END, tag.name)
    selection_only_tags = scope.get_selection_only_tags()
    for tag in selection_only_tags:
        tag_view.insert(tkinter.END, tag.name)
    suggested_tags = scope.get_suggested_tags(tag_entry.get())
    for tag in suggested_tags:
        tag_view.insert(tkinter.END, tag)
    n_tags = len(concept_tags) + len(selection_only_tags) + len(suggested_tags)
    selection_offset = len(concept_tags)
    suggestion_offset = selection_offset + len(selection_only_tags)
    for index in range(selection_offset, suggestion_offset):
        tag_view.itemconfig(index, bg='#FFFFBB')
    for index in range(suggestion_offset, n_tags):
        tag_view.itemconfig(index, foreground='#88AA88')


def tag_entry_callback(key):
    list_current_tags()


def tag_view_select(event):
    print('tag view')


def document_view_select(event):
    print('document view')


def file_list_refresh(event):
    list_untracked_files()


def file_list_select(event):
    print('file list selection')


def import_selected_file():
    selection = file_list.curselection()
    file_path = file_list.get(selection[0])
    repository.track_file(file_path)
    list_untracked_files()
    list_current_documents()


def select_document(event):
    selected = document_view.selection()
    if len(selected) == 1:
        document_id = int(selected[0])
        scope.toggle_document_selection(document_id)
        list_current_documents()
        list_current_tags()


def select_tag(event):
    selection = tag_view.curselection()
    tag_name = tag_view.get(selection[0])
    tag = scope.create_tag(tag_name)
    scope.add_tag(tag.id)
    list_current_tags()
    list_current_documents()


def deselect_tag(event):
    selection = tag_view.curselection()
    tag_name = tag_view.get(selection[0])


root = tkinter.Tk()
root.title('Grimoire - Importer')

tag_entry = tkinter.Entry(root)
tag_entry.bind('<Key>', tag_entry_callback)
ordering_combobox = ttk.Combobox(root)
tag_view = tkinter.Listbox(root)
tag_view.bind('<<ListboxSelect>>', tag_view_select)
tag_view.bind('<Double-1>', select_tag)

document_view = ttk.Treeview(root, columns=('name', 'type'))
document_view.heading('name', text='name')
document_view.heading('type', text='type')
document_view.bind('<<TreeviewSelect>>', document_view_select)
document_view.bind('<Double-1>', select_document)

file_refresh_button = tkinter.Button(root, text='Import', command=import_selected_file)
file_list = tkinter.Listbox(root)
file_list.bind('<<ListboxSelect>>', file_list_select)
file_list.bind("<Button-3>", file_list_refresh)

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

list_untracked_files()
list_current_documents()
list_current_tags()

root.mainloop()
