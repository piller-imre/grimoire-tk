"""
File importer graphical application
"""

import os
import subprocess
import tkinter
from tkinter import ttk
from tkinter import StringVar

from grimoire.database import Database
from grimoire.repository import Repository
from grimoire.scope import Scope
from grimoire.storage import Storage


database = Database('/tmp/importer/grimoire.log')
storage = Storage('/tmp/importer/storage/')
repository = Repository(database, storage)
scope = Scope(database)


def open_path(file_path):
    absolute_path = os.path.join(storage.path, file_path)
    if not os.path.isfile(absolute_path):
        raise ValueError('Invalid file path! {}'.format(absolute_path))
    extension = os.path.splitext(file_path)[1]
    if len(extension) > 1:
        t = extension[1:].lower()
        if t == 'pdf':
            _ = subprocess.Popen(['evince', absolute_path])
        elif t in ['png', 'jpg', 'jpeg', 'bmp']:
            _ = subprocess.Popen(['viewnior', absolute_path])
        elif t in ['py', 'h', 'c', 'cpp', 'txt', 'html', 'js', 'css']:
            _ = subprocess.Popen(['gedit', absolute_path])
        elif t in ['doc', 'docx', 'ppt', 'pptx']:
            _ = subprocess.Popen(['libreoffice', absolute_path])
        elif t in ['dia']:
            _ = subprocess.Popen(['dia', absolute_path])


def list_untracked_files():
    untracked_file_paths = repository.collect_untracked_file_paths()
    file_view.delete(*file_view.get_children())
    for file_path in untracked_file_paths:
        file_view.insert('', tkinter.END, iid=file_path, text=file_path)


def open_file(event):
    file_path = file_view.identify_row(event.y)
    print('Open {}'.format(file_path))
    open_path(file_path)


def import_file(event):
    file_path = file_view.identify_row(event.y)
    repository.track_file(file_path)
    list_untracked_files()
    list_current_documents()


def refresh_file_list(event):
    list_untracked_files()


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
    tag_view.delete(*tag_view.get_children())
    if scope.has_document_selection():
        selection_only_tags = scope.get_selection_only_tags()
        for tag in selection_only_tags:
            args = {
                'iid': tag.id,
                'text': tag.name,
                'tags': ['document']
            }
            tag_view.insert('', tkinter.END, **args)
    concept_tags = scope.get_concept_tags()
    for tag in concept_tags:
        args = {
            'iid': tag.id,
            'text': tag.name,
            'tags': ['query']
        }
        tag_view.insert('', tkinter.END, **args)
    suggested_tags = scope.get_suggested_tags(tag_entry.get())
    for tag in suggested_tags:
        args = {
            'text': tag,
            'tags': ['suggestion']
        }
        tag_view.insert('', tkinter.END, **args)
    tag_view.tag_configure('document', background='#FFFFBB')
    tag_view.tag_configure('query', background='#BBBBFF')
    tag_view.tag_configure('suggestion', background='#EEEEEE')


def tag_entry_callback(*args):
    list_current_tags()


def open_document(event):
    iid = document_view.identify_row(event.y)
    document_id = int(iid)
    print('Open document {}'.format(document_id))
    document = database.get_document(document_id)
    open_path(document.path)


def select_single_document(event):
    iid = document_view.identify_row(event.y)
    document_id = int(iid)
    scope.deselect_all_documents()
    scope.toggle_document_selection(document_id)
    list_current_documents()
    list_current_tags()


def select_document(event):
    iid = document_view.identify_row(event.y)
    document_id = int(iid)
    scope.toggle_document_selection(document_id)
    list_current_documents()
    list_current_tags()


def add_tag_to_query(tag_id):
    scope.add_tag(tag_id)
    list_current_tags()
    list_current_documents()


def remove_tag_from_query(tag_id):
    scope.remove_tag(tag_id)
    list_current_tags()
    list_current_documents()


def add_tag_to_documents(tag_id):
    scope.add_tag(tag_id)
    list_current_tags()
    list_current_documents()


def remove_tag_from_documents(tag_id):
    scope.remove_tag(tag_id)
    list_current_tags()
    list_current_documents()


def left_click_on_tag(event):
    iid = tag_view.identify_row(event.y)
    if iid != '':
        try:
            tag_id = int(iid)
        except ValueError:
            tag_id = None
        tags = tag_view.item(iid, 'tags')
        item_type = tags[0]
        if scope.has_document_selection() is False:
            if item_type == 'query':
                remove_tag_from_query(tag_id)
            elif item_type == 'suggestion':
                tag_name = tag_view.item(iid, 'text')
                try:
                    tag_id = scope.find_tag_id(tag_name)
                except ValueError:
                    tag = scope.create_tag(tag_name)
                    tag_id = tag.id
                add_tag_to_query(tag_id)
                tag_entry.delete(0, tkinter.END)
        else:
            if item_type == 'document':
                add_tag_to_query(tag_id)
            elif item_type == 'query':
                remove_tag_from_query(tag_id)


def right_click_on_tag(event):
    iid = tag_view.identify_row(event.y)
    if iid != '':
        try:
            tag_id = int(iid)
        except ValueError:
            tag_id = None
        tags = tag_view.item(iid, 'tags')
        item_type = tags[0]
        if scope.has_document_selection():
            if item_type == 'document':
                remove_tag_from_documents(tag_id)
            elif item_type == 'suggestion':
                tag_name = tag_view.item(iid, 'text')
                try:
                    tag_id = scope.find_tag_id(tag_name)
                except ValueError:
                    tag = scope.create_tag(tag_name)
                    tag_id = tag.id
                add_tag_to_query(tag_id)
                tag_entry.delete(0, tkinter.END)


root = tkinter.Tk()
root.title('Grimoire - Importer')

tag_entry_value = StringVar()
tag_entry = tkinter.Entry(root, textvariable=tag_entry_value)
tag_entry_value.trace('w', tag_entry_callback)
ordering_combobox = ttk.Combobox(root)

tag_view = ttk.Treeview(root, selectmode='none')
tag_view.bind('<Button-1>', left_click_on_tag)
tag_view.bind('<Button-3>', right_click_on_tag)

document_view = ttk.Treeview(root, columns=('name', 'type'), selectmode='none')
document_view.heading('name', text='name')
document_view.heading('type', text='type')
document_view.bind('<Button-1>', select_single_document)
document_view.bind('<Shift-Button-1>', select_document)
document_view.bind('<Button-3>', open_document)

file_view = ttk.Treeview(root, selectmode='none')
file_view.bind('<Button-1>', refresh_file_list)
file_view.bind('<Button-2>', import_file)
file_view.bind('<Button-3>', open_file)

full = (tkinter.N, tkinter.S, tkinter.E, tkinter.W)

tag_entry.grid(row=0, column=0, sticky=full)
ordering_combobox.grid(row=0, column=1, sticky=full)
tag_view.grid(row=1, column=0, sticky=full)
document_view.grid(row=1, column=1, sticky=full)

file_view.grid(row=2, column=0, columnspan=2, sticky=full)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

list_untracked_files()
list_current_documents()
list_current_tags()

root.mainloop()
