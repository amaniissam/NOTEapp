from tkinter import *
from tkinter import messagebox
import csv
import os

#creat the working dir
try:
    os.makedirs('Note')
    os.makedirs('Note/names')
    os.makedirs('Note/notes')
except:
    pass

root = Tk()
root.title('Note')
root.geometry('222x222')
root.configure(bg='#ffef79')

#list of notes
list = []
file1 = open('Note/names/note_name.csv', 'a+')
file1.close()

with open('Note/names/note_name.csv') as file:
    reader = csv.reader(file)
    for note in reader:
        list.append(note[0])

def return_mynotes():
    menu_mynotes.forget()
    showmenu_note()

def return_creat():
    creat_page.forget()
    showmenu_note()

def showmenu_note():
    root.geometry('222x222')
    #show note menu
    menu_note.pack(padx=10, pady=10)    
    Creat.pack()
    space3.pack()    
    my_notes.pack()
    space4.pack()
    quitbutton.pack()

def delete_note():
    cur_index = list_note.curselection()
    if cur_index:
        msg_delete = messagebox.askyesno('Delete Note', 'You want to delete the Note?')
        if msg_delete == 1:
            cur = list_note.get(cur_index)
            main = open('Note/names/note_name.csv', 'r', newline='')
            tmp = open('Note/names/tmp.csv', 'w', newline='')
            reader = csv.reader(main)
            writer = csv.writer(tmp)
            for row in reader:
                if cur not in row:
                    writer.writerow(row)
            main.close()
            tmp.close()
            os.replace('Note/names/tmp.csv', 'Note/names/note_name.csv')

            list_note.delete(cur_index)
            os.remove(f'Note/notes/{cur}.txt')
            list.remove(cur)

def re_from_show_fun():
    cadr.forget()
    my_notes_menu()

def show_note():
    cur_index = list_note.curselection()
    if cur_index:
        root.geometry('550x400')
        curr = list_note.get(cur_index)
        the_show_note = f'Note/notes/{curr}.txt'
        the_show_note_file = open(the_show_note, 'r')
        reader = the_show_note_file.read()
        #show menu
        menu_mynotes.forget()
        global cadr
        cadr = LabelFrame(root, text=curr, padx=5, pady=5)
        contentt = Text(cadr,state=DISABLED, width=65, height=20)
        cadr.pack(padx=5,pady=5)
        contentt.config(state=NORMAL)
        contentt.insert(END, reader)        
        contentt.config(state=DISABLED)
        contentt.grid(row=0, column=0, columnspan=3)
        return_from_show = Button(cadr, text='Return', padx=30, bg='#ffef79', command=re_from_show_fun)
        return_from_show.grid(row=1,column=1, padx=5, pady=7)

def return_from_edit_with_yes():
    edit_page.forget()
    my_notes_menu()

def return_from_edit_butfun():
    assisstant_edit.configure(text='')
    edited_name = name_entry.get()
    edited_content = content_text.get('1.0', 'end-1c')

    fnote = open(f'Note/notes/{old_note_name}.txt', 'r')
    old_note_content = fnote.read()
    fnote.close()

    if old_note_name != edited_name or old_note_content != edited_content:
        save_msg = messagebox.askyesno('Save changes','You want to save changes?')
        if save_msg == 1:
            if edited_name != old_note_name and edited_name in list:
                assisstant_edit.configure(text='There is another Note with this name!')
            else:
                if old_note_name != edited_name and old_note_content != edited_content:
                    change_content_fun()
                    chang_name_fun()
                elif old_note_name != edited_name:
                    chang_name_fun()
                elif old_note_content != edited_content:
                    change_content_fun()
                return_from_edit_with_yes()
        else:
            return_from_edit_with_yes()
    else:
        return_from_edit_with_yes()
   
def chang_name_fun(): #the file handling function to change name
    edited_name2 = name_entry.get()
    os.rename(f'Note/notes/{old_note_name}.txt', f'Note/notes/{edited_name2}.txt')
    main2 = open('Note/names/note_name.csv', 'r', newline='')
    tmp2 = open('Note/names/tmp.csv', 'w', newline='')
    reader2 = csv.reader(main2)
    writer2 = csv.writer(tmp2)
    for row in reader2:
        if old_note_name not in row:
            writer2.writerow(row)
        else:
            writer2.writerow([edited_name2])
    main2.close()
    tmp2.close()
    os.replace('Note/names/tmp.csv', 'Note/names/note_name.csv')
    list.remove(old_note_name)
    list.append(edited_name2)

def change_content_fun(): #file handling (the process of change to edited content)
    edited_content2 = content_text.get('1.0', 'end-1c')
    with open(f'Note/notes/{old_note_name}.txt', 'w') as fcc:
        fcc.write(edited_content2)

def savee():
    #reset the assistant label
    assisstant_edit.configure(text='')
    global edited_name
    global edited_content
    edited_name = name_entry.get()
    edited_content = content_text.get('1.0', 'end-1c')

    fnote = open(f'Note/notes/{old_note_name}.txt', 'r')
    old_note_content = fnote.read()
    fnote.close()

    if edited_name != old_note_name and edited_name in list:
        assisstant_edit.configure(text='There is another Note with this name!')
    else:
        if old_note_name != edited_name or old_note_content != edited_content:
            save_msg = messagebox.askyesno('Save changes','You want to save changes?')
            if save_msg == 1:
                if old_note_name != edited_name and old_note_content != edited_content:
                    change_content_fun()                    
                    chang_name_fun()               
                elif old_note_name != edited_name:
                    chang_name_fun()
                elif old_note_content != edited_content:
                    change_content_fun() 
                return_from_edit_with_yes()

#edit note function
def edit_note():
    selected_index = list_note.curselection()
    if selected_index:
        selected_note = list_note.get(selected_index)

        global old_note_name

        old_note_name = selected_note
        menu_mynotes.forget()
        root.geometry('545x490')
        global edit_page
        edit_page = LabelFrame(root, text='Edit', padx=10, pady=10)
        name_frame = Frame(edit_page, padx=5, pady=5)        
        global assisstant_edit 
        assisstant_edit = Label(name_frame, text='')
        global name_entry
        name_entry = Entry(name_frame)
        name_entry.insert(0, selected_note)
        content_frame = Frame(edit_page, padx=5, pady=5)
        global content_text
        content_text = Text(content_frame, width=60, height=20)
        ed_note = open(f'Note/notes/{selected_note}.txt', 'r')
        
        content_text.insert(END, ed_note.read())
        ed_note.close()
        
        save_edit_button = Button(edit_page, text='save', padx=50, bg='#ffef79', command=savee)
        return_from_edit_button = Button(edit_page, text='Return', padx=50, bg='#ffef79', command=return_from_edit_butfun)

        edit_page.pack(padx=10, pady=10)
        name_frame.grid(row=0, column=0,columnspan=2)
        assisstant_edit.pack(padx=2, pady=2)
        name_entry.pack(padx=5, pady=5)
        content_frame.grid(row=1, column=0,columnspan=2)
        content_text.pack(padx=5, pady=5)
        save_edit_button.grid(row=2, column=0, columnspan=1)
        return_from_edit_button.grid(row=2, column=1, columnspan=1)

def my_notes_menu():
    root.geometry('222x222')
    #mynotesmenu
    menu_note.forget()
    global menu_mynotes
    menu_mynotes = LabelFrame(root, text='My Notes', bg='#ffef79')
    edit = Button(menu_mynotes, text='Edit', command=edit_note)
    show = Button(menu_mynotes, text='Show', command=show_note)
    delete = Button(menu_mynotes, text='Delete', command=delete_note)
    return_note_menu = Button(menu_mynotes, text='Return', command=return_mynotes)
    global list_note
    list_note = Listbox(menu_mynotes)
    for i in list:
        list_note.insert(END, i)
    menu_mynotes.pack()
    edit.grid(column=0, row=0, padx=10, pady=10)
    show.grid(column=0, row=1, padx=10, pady=10)
    delete.grid(column=0, row=2, padx=10, pady=10)
    return_note_menu.grid(column=0, row=3, padx=10, pady=10)
    list_note.grid(rowspan=4,column=1,row=0)

#note funtion
def creatf():
    menu_note.forget()
    root.geometry('500x575')

    #creat page function
    def snf(name, content):
        if name == '':
            assistant_lbl.configure(text='You didnt enter a NAME to your Note.')
        elif name in list:
            assistant_lbl.configure(text='There is another NOTE with this NAME.')
        elif name not in list:
            save_msg = messagebox.askyesno("save", "You want Save this Note ?")
            if save_msg == 1:
                with open(f'Note/notes/{name}.txt', 'w') as note_file:
                    note_file.write(content)
                #add name of the note
                add = open(f'Note/names/note_name.csv', 'a', newline='')
                writer = csv.writer(add)
                writer.writerow([name])
                add.close()
                list.append(name)
                return_creat()
        else:
            assistant_lbl.configure(text='')

    #creat page widget
    global creat_page
    creat_page = LabelFrame(root, text='New Note', bg='#ffef79', padx=10, pady=10)
    assistant_lbl = Label(creat_page, text='', bg='#ffef79')
    space5 = Label(creat_page, text='', bg='#ffef79')
    name_lbl = Label(creat_page, text='Enter name to your NOTE:', bg='#ffef79')
    name_entry = Entry(creat_page)
    space6 = Label(creat_page, text='', bg='#ffef79')
    text_lbl = Label(creat_page, text='Enter content to your NOTE:', bg='#ffef79')
    text = Text(creat_page, width=65, height=20)
    save_note = Button(creat_page, text='Save',padx=34, command=lambda: snf(name_entry.get(), text.get(1.0, END)))
    return_button = Button(creat_page, text='Return', padx=30,command=return_creat)
    
    #show creat page
    creat_page.pack(padx=10, pady=10)
    assistant_lbl.pack()
    space5.pack()
    name_lbl.pack()
    name_entry.pack()
    space6.pack()
    text_lbl.pack()
    text.pack()
    save_note.pack(pady=10)
    return_button.pack()
  
menu_note = LabelFrame(root, text='Note', bg='#ffef79', padx=10, pady=10)
Creat = Button(menu_note, text='New Note',padx=20, command=creatf)
space3 = Label(menu_note, text='', bg='#ffef79')
my_notes = Button(menu_note, text='  My Notes  ',padx=15, command=my_notes_menu)
space4 = Label(menu_note, text='', bg='#ffef79')
quitbutton = Button(menu_note, text='   Exit  ', padx=29, command=quit)

#show note menu
menu_note.pack(padx=10, pady=10)    
Creat.pack()
space3.pack()    
my_notes.pack()
space4.pack()
quitbutton.pack()

root.mainloop()