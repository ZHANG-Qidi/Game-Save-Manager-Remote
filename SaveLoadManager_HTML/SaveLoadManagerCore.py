#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import shutil
import pathlib
import datetime
from configparser import ConfigParser


def game_list_func():
    if not os.path.exists('./SaveLoad'):
        os.makedirs('./SaveLoad')
    game_list = [game for game in os.listdir('./SaveLoad')]
    if len(game_list) == 0:
        game_list = ['']
    game_list.sort()
    return game_list


def profile_list_func(game):
    profile_list = ['']
    folder = ''
    file = ''
    if game == '':
        return (profile_list, folder, file)
    config = ConfigParser()
    config.read("./SaveLoad/{}/Path.ini".format(game), encoding='utf-8')
    folder = config.get('path', 'folder')
    file = config.get('path', 'file')
    profile_list = [profile for profile in os.listdir('./SaveLoad/{}'.format(game))]
    profile_list.remove('Path.ini')
    if 0 == len(profile_list):
        profile_list = ['']
    profile_list.sort()
    return (profile_list, folder, file)


def save_list_func(game, profile):
    save_list = ['']
    if '' != game and '' != profile:
        save_list = [save for save in os.listdir('./SaveLoad/{}/{}'.format(game, profile))]
        if 0 == len(save_list):
            save_list = ['']
    save_list.sort(reverse=True)
    return save_list


def game_new(game, folder, file):
    folder_target = './SaveLoad/{}'.format(game)
    if os.path.exists(folder_target):
        return
    print('Game New: {}'.format(game))
    os.makedirs(folder_target)
    config = ConfigParser()
    config.add_section('path')
    config.set('path', 'folder', folder)
    config.set('path', 'file', file)
    with open("./SaveLoad/{}/Path.ini".format(game), mode="w", encoding="utf-8", errors='ignore') as path_file:
        config.write(path_file)
    return


def game_delete(game):
    if game == '':
        return 'NG'
    shutil.rmtree('./SaveLoad/{}'.format(game))
    print('Game Delete: {}'.format(game))
    return 'OK'


def profile_new(game, profile):
    if game == '' or profile == '':
        return 'NG'
    folder_target = './SaveLoad/{}/{}'.format(game, profile)
    if os.path.exists(folder_target):
        return 'NG'
    print('Profile New: {}'.format(profile))
    os.makedirs(folder_target)
    return 'OK'


def profile_delete(game, profile):
    if game == '' or profile == '':
        return 'NG'
    shutil.rmtree('./SaveLoad/{}/{}'.format(game, profile))
    print('Profile Delete: {}'.format(profile))
    return 'OK'


def find_all_file_func(base):
    for path, dir_list, file_list in os.walk(base):
        for file_name in file_list:
            fullname = os.path.join(path, file_name)
            yield fullname


def save_new(game, profile, folder, file, comment):
    if game == '' or profile == '':
        return 'NG'
    modified_time_last = 0
    if folder != '':
        folder_source = folder
        if not os.path.exists(folder_source):
            return 'NG'
        for file_obj in find_all_file_func(folder_source):
            modified_time = pathlib.Path(file_obj).stat().st_mtime
            if modified_time > modified_time_last:
                modified_time_last = modified_time
        str_modified_time_last = datetime.datetime.fromtimestamp(modified_time_last).strftime("%Y-%m-%d %H-%M-%S")
        if comment == '':
            folder_target = './SaveLoad/{}/{}/{}'.format(game, profile, str_modified_time_last)
        else:
            folder_target = './SaveLoad/{}/{}/{}@{}'.format(game, profile, str_modified_time_last, comment)
        if not os.path.exists(folder_target):
            print('Save New: {}'.format(os.path.basename(folder_target)))
            shutil.copytree(folder_source, folder_target)
    if file != '':
        file_source = file
        if not os.path.exists(file_source):
            return 'NG'
        modified_time_last = pathlib.Path(file_source).stat().st_mtime
        str_modified_time_last = datetime.datetime.fromtimestamp(modified_time_last).strftime("%Y-%m-%d %H-%M-%S")
        if comment == '':
            file_target = './SaveLoad/{}/{}/{}{}'.format(game, profile, str_modified_time_last, pathlib.Path(file_source).suffix)
        else:
            file_target = './SaveLoad/{}/{}/{}@{}{}'.format(game, profile, str_modified_time_last, comment, pathlib.Path(file_source).suffix)
        if not os.path.exists(file_target):
            print('Save New: {}'.format(os.path.basename(file_target)))
            shutil.copy2(file_source, file_target)
    return 'OK'


def save_delete(game, profile, save, folder, file):
    if game == '' or profile == '' or save == '':
        return 'NG'
    if '' != folder:
        shutil.rmtree('./SaveLoad/{}/{}/{}'.format(game, profile, save))
    if '' != file:
        pathlib.Path('./SaveLoad/{}/{}/{}'.format(game, profile, save)).unlink()
    file_path = pathlib.Path('./SaveLoad/{}/{}/{}.SCREENSHOT.png'.format(game, profile, save))
    if file_path.is_file():
        pathlib.Path(file_path).unlink()
    print('Save Delete: {}'.format(save))
    return 'OK'


def save_load(game, profile, save, folder, file):
    if game == '' or profile == '' or save == '':
        return 'NG'
    if '' != folder:
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            shutil.rmtree(folder)
        shutil.copytree('./SaveLoad/{}/{}/{}'.format(game, profile, save), folder, dirs_exist_ok=True)
    if '' != file:
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        shutil.copy2('./SaveLoad/{}/{}/{}'.format(game, profile, save), file)
    print('Save Load: {}'.format(save))
    return 'OK'
