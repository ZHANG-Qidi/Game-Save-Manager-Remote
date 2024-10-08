#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import os
import sys
import pathlib
import SaveLoadManagerFunc


def main():
    root = tkinter.Tk()
    root.title('SaveLoad Manager')
    root.configure(background='black')
    root.resizable(False, False)
    label_title = tkinter.Label(root, text='SaveLoad Manager', fg='light green', bg='black', font=(None, 15))
    label_title.pack(side=tkinter.TOP)

    def window_game_new_func():
        window_game_new = tkinter.Toplevel(root)
        window_game_new.title('NewGame')
        window_game_new.configure(background='black')
        window_game_new.resizable(False, False)
        grid_frame_entry = tkinter.Frame(window_game_new, bg='black')
        grid_frame_entry_label_width = 5
        grid_frame_entry_entry_width = 35
        grid_frame_entry_button_width = 10
        label_game = tkinter.Label(grid_frame_entry, text="Game", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_game.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        var_entry_game = tkinter.StringVar()
        var_entry_game.set('')
        entry_game = tkinter.Entry(grid_frame_entry, textvariable=var_entry_game, width=grid_frame_entry_entry_width, state="normal")
        entry_game.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        label_folder = tkinter.Label(grid_frame_entry, text="Folder", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_folder.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        var_entry_folder = tkinter.StringVar()
        var_entry_folder.set('')
        entry_folder = tkinter.Entry(grid_frame_entry, textvariable=var_entry_folder, width=grid_frame_entry_entry_width, state="readonly")
        entry_folder.grid(row=1, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        str_initialdir = '.'
        if sys.platform.startswith('win'):
            str_initialdir = os.getenv('APPDATA')
        elif sys.platform.startswith('linux'):
            if os.path.exists('{}/.local/share/Steam/steamapps/compatdata'.format(pathlib.Path.home())):
                str_initialdir = '{}/.local/share/Steam/steamapps/compatdata'.format(pathlib.Path.home())
            else:
                str_initialdir = pathlib.Path.home()

        def select_folder_func():
            if var_entry_file.get() != '':
                return
            folder = tkinter.filedialog.askdirectory(parent=window_game_new, initialdir=str_initialdir, title='Save Folder')
            if not folder:
                return
            if var_entry_game.get() == '':
                var_entry_game.set(pathlib.Path(folder).stem)
            # folder = folder.replace("/", "\\\\")
            var_entry_folder.set(folder)
        button_folder = tkinter.Button(grid_frame_entry, text="Save Folder", command=select_folder_func, width=grid_frame_entry_button_width)
        button_folder.grid(row=1, column=2, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        label_file = tkinter.Label(grid_frame_entry, text="File", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_file.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        var_entry_file = tkinter.StringVar()
        var_entry_file.set('')
        entry_file = tkinter.Entry(grid_frame_entry, textvariable=var_entry_file, width=grid_frame_entry_entry_width, state="readonly")
        entry_file.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)

        def select_file_func():
            if var_entry_folder.get() != '':
                return
            file = tkinter.filedialog.askopenfilename(parent=window_game_new, initialdir=str_initialdir, title='Save File')
            if not file:
                return
            if var_entry_game.get() == '':
                var_entry_game.set(pathlib.Path(file).stem)
            # file = file.replace("/", "\\\\")
            var_entry_file.set(file)
        button_file = tkinter.Button(grid_frame_entry, text="Save File", command=select_file_func, width=grid_frame_entry_button_width)
        button_file.grid(row=2, column=2, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_entry.pack(side=tkinter.TOP)
        grid_frame_ok_cancel = tkinter.Frame(window_game_new, bg='black')
        grid_frame_ok_cancel_button_width = 10

        def button_ok_func():
            if var_entry_game.get() == '':
                return
            SaveLoadManagerFunc.game_new(var_entry_game.get(), var_entry_folder.get(), var_entry_file.get())
            game_list_init()
            var_game.set(var_entry_game.get())
            profile_list_init()
            save_list_init_without_comment()
            window_game_new.destroy()
        button_ok = tkinter.Button(grid_frame_ok_cancel, text="OK", command=button_ok_func, width=grid_frame_ok_cancel_button_width)
        button_ok.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        button_cancel = tkinter.Button(grid_frame_ok_cancel, text="Cancel", command=lambda: window_game_new.destroy(), width=grid_frame_ok_cancel_button_width)
        button_cancel.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_ok_cancel.pack(side=tkinter.TOP)

    def window_game_delete_func():
        if '' == var_game.get():
            return
        window_game_delete = tkinter.Toplevel(root)
        window_game_delete.title('DeleteGame')
        window_game_delete.configure(background='black')
        window_game_delete.resizable(False, False)
        grid_frame_entry = tkinter.Frame(window_game_delete, bg='black')
        grid_frame_entry_label_width = 35
        grid_frame_entry_entry_width = 35
        label_game = tkinter.Label(grid_frame_entry, text="Delete the Game?", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_game.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        entry_game = tkinter.Entry(grid_frame_entry, textvariable=var_game, width=grid_frame_entry_entry_width, state="readonly")
        entry_game.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_entry.pack(side=tkinter.TOP)
        grid_frame_ok_cancel = tkinter.Frame(window_game_delete, bg='black')
        grid_frame_ok_cancel_button_width = 10

        def button_ok_func():
            SaveLoadManagerFunc.game_delete(var_game.get())
            game_list_init()
            profile_list_init()
            save_list_init_without_comment()
            window_game_delete.destroy()
        button_ok = tkinter.Button(grid_frame_ok_cancel, text="OK", command=button_ok_func, width=grid_frame_ok_cancel_button_width)
        button_ok.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        button_cancel = tkinter.Button(grid_frame_ok_cancel, text="Cancel", command=lambda: window_game_delete.destroy(), width=grid_frame_ok_cancel_button_width)
        button_cancel.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_ok_cancel.pack(side=tkinter.TOP)

    def window_profile_new_func():
        if var_game.get() == '':
            return
        window_profile_new = tkinter.Toplevel(root)
        window_profile_new.title('NewProfile')
        window_profile_new.configure(background='black')
        window_profile_new.resizable(False, False)
        grid_frame_entry = tkinter.Frame(window_profile_new, bg='black')
        grid_frame_entry_label_width = 5
        grid_frame_entry_entry_width = 35
        label_profile = tkinter.Label(grid_frame_entry, text="Profile", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_profile.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        var_entry_profile = tkinter.StringVar()
        var_entry_profile.set('')
        entry_profile = tkinter.Entry(grid_frame_entry, textvariable=var_entry_profile, width=grid_frame_entry_entry_width, state="normal")
        entry_profile.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_entry.pack(side=tkinter.TOP)
        grid_frame_ok_cancel = tkinter.Frame(window_profile_new, bg='black')
        grid_frame_ok_cancel_button_width = 10

        def button_ok_func():
            if var_entry_profile.get() == '':
                return
            SaveLoadManagerFunc.profile_new(var_game.get(), var_entry_profile.get())
            profile_list_init()
            var_profile.set(var_entry_profile.get())
            save_list_init_without_comment()
            window_profile_new.destroy()
        button_ok = tkinter.Button(grid_frame_ok_cancel, text="OK", command=button_ok_func, width=grid_frame_ok_cancel_button_width)
        button_ok.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        button_cancel = tkinter.Button(grid_frame_ok_cancel, text="Cancel", command=lambda: window_profile_new.destroy(), width=grid_frame_ok_cancel_button_width)
        button_cancel.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_ok_cancel.pack(side=tkinter.TOP)

    def window_profile_delete_func():
        if var_profile.get() == '':
            return
        window_profile_delete = tkinter.Toplevel(root)
        window_profile_delete.title('DeleteProfile')
        window_profile_delete.configure(background='black')
        window_profile_delete.resizable(False, False)
        grid_frame_entry = tkinter.Frame(window_profile_delete, bg='black')
        grid_frame_entry_label_width = 35
        grid_frame_entry_entry_width = 35
        label_profile = tkinter.Label(grid_frame_entry, text="Delete the Profile?", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_profile.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        entry_profile = tkinter.Entry(grid_frame_entry, textvariable=var_profile, width=grid_frame_entry_entry_width, state="readonly")
        entry_profile.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_entry.pack(side=tkinter.TOP)
        grid_frame_ok_cancel = tkinter.Frame(window_profile_delete, bg='black')
        grid_frame_ok_cancel_button_width = 10

        def button_ok_func():
            SaveLoadManagerFunc.profile_delete(var_game.get(), var_profile.get())
            profile_list_init()
            save_list_init_without_comment()
            window_profile_delete.destroy()
        button_ok = tkinter.Button(grid_frame_ok_cancel, text="OK", command=button_ok_func, width=grid_frame_ok_cancel_button_width)
        button_ok.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        button_cancel = tkinter.Button(grid_frame_ok_cancel, text="Cancel", command=lambda: window_profile_delete.destroy(), width=grid_frame_ok_cancel_button_width)
        button_cancel.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_ok_cancel.pack(side=tkinter.TOP)

    def window_delete_func():
        if var_save.get() == '':
            return
        window_delete = tkinter.Toplevel(root)
        window_delete.title('DeleteSave')
        window_delete.configure(background='black')
        window_delete.resizable(False, False)
        grid_frame_entry = tkinter.Frame(window_delete, bg='black')
        grid_frame_entry_label_width = 35
        grid_frame_entry_entry_width = 35
        label_save = tkinter.Label(grid_frame_entry, text="Delete the Save?", fg='light green', bg='black', width=grid_frame_entry_label_width)
        label_save.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        entry_save = tkinter.Entry(grid_frame_entry, textvariable=var_save, width=grid_frame_entry_entry_width, state="readonly")
        entry_save.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_entry.pack(side=tkinter.TOP)
        grid_frame_ok_cancel = tkinter.Frame(window_delete, bg='black')
        grid_frame_ok_cancel_button_width = 10

        def button_ok_func():
            SaveLoadManagerFunc.save_delete(var_game.get(), var_profile.get(), var_save.get(), var_folder.get(), var_file.get())
            save_list_init_with_comment()
            window_delete.destroy()
        button_ok = tkinter.Button(grid_frame_ok_cancel, text="OK", command=button_ok_func, width=grid_frame_ok_cancel_button_width)
        button_ok.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        button_cancel = tkinter.Button(grid_frame_ok_cancel, text="Cancel", command=lambda: window_delete.destroy(), width=grid_frame_ok_cancel_button_width)
        button_cancel.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
        grid_frame_ok_cancel.pack(side=tkinter.TOP)

    def save_func():
        if var_game.get() == '' or var_profile.get() == '':
            return
        SaveLoadManagerFunc.save_new(var_game.get(), var_profile.get(), var_folder.get(), var_file.get(), var_comment.get())
        save_list_init_with_comment()

    def read_func():
        game_list_init()
        profile_list_init()
        save_list_init_without_comment()
    pady_value = 10
    padx_value = 10
    grid_frame_button = tkinter.Frame(root, bg='black')
    grid_frame_button_width = 20
    button_game_new = tkinter.Button(grid_frame_button, text="New Game", command=window_game_new_func, width=grid_frame_button_width)
    button_game_new.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    button_game_delete = tkinter.Button(grid_frame_button, text="Delete Game", command=window_game_delete_func, width=grid_frame_button_width)
    button_game_delete.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    button_profile_new = tkinter.Button(grid_frame_button, text="New Profile", command=window_profile_new_func, width=grid_frame_button_width)
    button_profile_new.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    button_profile_delete = tkinter.Button(grid_frame_button, text="Delete Profile", command=window_profile_delete_func, width=grid_frame_button_width)
    button_profile_delete.grid(row=1, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    grid_frame_button.pack(side=tkinter.TOP)
    grid_frame_save_load_delete = tkinter.Frame(root, bg='black')
    grid_frame_save_load_delete_width = 12
    button_save_save = tkinter.Button(grid_frame_save_load_delete, text="Save", command=save_func, width=grid_frame_save_load_delete_width)
    button_save_save.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    button_save_delete = tkinter.Button(grid_frame_save_load_delete, text="Delete", command=window_delete_func,  width=grid_frame_save_load_delete_width)
    button_save_delete.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    button_save_load = tkinter.Button(grid_frame_save_load_delete, text="Load", command=lambda: SaveLoadManagerFunc.save_load(var_game.get(), var_profile.get(), var_save.get(), var_folder.get(), var_file.get()), width=grid_frame_save_load_delete_width)
    button_save_load.grid(row=2, column=2, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    grid_frame_save_load_delete.pack(side=tkinter.TOP)
    grid_framd_combobox = tkinter.Frame(root, bg='black')
    grid_framd_combobox_button_width = 8
    grid_framd_combobox_entry_width = 40
    label_game = tkinter.Label(grid_framd_combobox, text="Game", fg='light green', bg='black', width=grid_framd_combobox_button_width)
    label_game.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)

    def combobox_game_func(event):
        profile_list_init()
        save_list_init_without_comment()
    var_game = tkinter.StringVar()
    var_game.set('')
    combobox_game = tkinter.ttk.Combobox(grid_framd_combobox, textvariable=var_game, width=grid_framd_combobox_entry_width, state="readonly")
    combobox_game.bind("<<ComboboxSelected>>", combobox_game_func)
    combobox_game.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    label_folder = tkinter.Label(grid_framd_combobox, text="Folder", fg='light green', bg='black', width=grid_framd_combobox_button_width)
    label_folder.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    var_folder = tkinter.StringVar()
    var_folder.set('')
    entry_folder = tkinter.Entry(grid_framd_combobox, textvariable=var_folder, width=grid_framd_combobox_entry_width, state="readonly")
    entry_folder.grid(row=1, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    label_file = tkinter.Label(grid_framd_combobox, text="File", fg='light green', bg='black', width=grid_framd_combobox_button_width)
    label_file.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    var_file = tkinter.StringVar()
    var_file.set('')
    entry_file = tkinter.Entry(grid_framd_combobox, textvariable=var_file, width=grid_framd_combobox_entry_width, state="readonly")
    entry_file.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    label_profile = tkinter.Label(grid_framd_combobox, text="Profile", fg='light green', bg='black', width=grid_framd_combobox_button_width)
    label_profile.grid(row=3, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)

    def combobox_profile_func(event):
        save_list_init_without_comment()
    var_profile = tkinter.StringVar()
    var_profile.set("")
    combobox_profile = tkinter.ttk.Combobox(grid_framd_combobox, textvariable=var_profile, width=grid_framd_combobox_entry_width, state="readonly")
    combobox_profile.bind("<<ComboboxSelected>>", combobox_profile_func)
    combobox_profile.grid(row=3, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    label_comment = tkinter.Label(grid_framd_combobox, text="Comment", fg='light green', bg='black',  width=grid_framd_combobox_button_width)
    label_comment.grid(row=4, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    var_comment = tkinter.StringVar()
    var_comment.set('')
    entry_comment = tkinter.Entry(grid_framd_combobox, textvariable=var_comment, width=grid_framd_combobox_entry_width)
    entry_comment.grid(row=4, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    label_save = tkinter.Label(grid_framd_combobox, text="Save", fg='light green', bg='black', width=grid_framd_combobox_button_width)
    label_save.grid(row=5, column=0, pady=pady_value, padx=padx_value, sticky=tkinter.W)

    def combobox_save_func(event):
        combobox_save_init()
    var_save = tkinter.StringVar()
    var_save.set('')
    combobox_save = tkinter.ttk.Combobox(grid_framd_combobox, textvariable=var_save, width=grid_framd_combobox_entry_width, state="readonly")
    combobox_save.bind("<<ComboboxSelected>>", combobox_save_func)
    combobox_save.grid(row=5, column=1, pady=pady_value, padx=padx_value, sticky=tkinter.W)
    grid_framd_combobox.pack(side=tkinter.TOP)

    def game_list_init():
        game_list = SaveLoadManagerFunc.game_list_func()
        combobox_game['values'] = game_list
        combobox_game.current(0)
        print('game list:\n{}'.format('\n'.join(game_list)))

    def profile_list_init():
        (profile_list, folder, file) = SaveLoadManagerFunc.profile_list_func(var_game.get())
        var_folder.set(folder)
        var_file.set(file)
        combobox_profile['values'] = profile_list
        combobox_profile.current(0)
        print('profile list:\n{}'.format('\n'.join(profile_list)))

    def save_list_init_without_comment():
        save_list = SaveLoadManagerFunc.save_list_func(var_game.get(), var_profile.get())
        combobox_save['values'] = save_list
        combobox_save.current(0)
        combobox_save_init()
        print('save list:\n{}'.format('\n'.join(save_list)))

    def save_list_init_with_comment():
        save_list = SaveLoadManagerFunc.save_list_func(var_game.get(), var_profile.get())
        save_list_no_comment = [save for save in save_list if not '@' in save]
        save_list_with_comment = [save for save in save_list if '@' in save]
        if var_file.get() != '':
            save_list_with_same_comment = [save for save in save_list_with_comment if var_comment.get() == save[save.find('@')+1:save.rfind('.')]]
        if var_folder.get() != '':
            save_list_with_same_comment = [save for save in save_list_with_comment if var_comment.get() == save[save.find('@')+1:]]
        for save in save_list_no_comment[3:]:
            SaveLoadManagerFunc.save_delete(var_game.get(), var_profile.get(), save, var_folder.get(), var_file.get())
            save_list.remove(save)
        for save in save_list_with_same_comment[3:]:
            SaveLoadManagerFunc.save_delete(var_game.get(), var_profile.get(), save, var_folder.get(), var_file.get())
            save_list.remove(save)
        combobox_save['values'] = save_list
        if var_comment.get() != '' and save_list_with_same_comment != []:
            combobox_save.current(save_list.index(save_list_with_same_comment[0]))
        elif var_comment.get() == '' and save_list_no_comment != []:
            combobox_save.current(save_list.index(save_list_no_comment[0]))
        else:
            combobox_save.current(0)
            combobox_save_init()
        print('save list:\n{}'.format('\n'.join(save_list)))

    def combobox_save_init():
        if var_save.get().count('@') == 0:
            var_comment.set('')
            return
        if var_folder.get() != '':
            var_comment.set(var_save.get()[var_save.get().find('@')+1:])
        if var_file.get() != '':
            var_comment.set(var_save.get()[var_save.get().find('@')+1:var_save.get().rfind('.')])
    read_func()
    root.mainloop()


if __name__ == "__main__":
    main()
