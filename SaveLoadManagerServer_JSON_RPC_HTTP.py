#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import SaveLoadManagerFunc
import SaveLoadManagerServer_JSON_RPC_HTTP_String
import json


def game_list_func():
    game_list = SaveLoadManagerFunc.game_list_func()
    # game_list = '\n'.join(game_list)
    print('game_list:\n{}'.format('\n'.join(game_list)))
    result = {}
    result['game_list'] = game_list
    result_str = json.dumps(result)
    return result_str


def profile_list_func(game):
    (profile_list, folder, file) = SaveLoadManagerFunc.profile_list_func(game)
    profile_list.sort()
    # profile_list = '\n'.join(profile_list)
    print('folder:\n{}'.format(folder))
    print('file:\n{}'.format(file))
    print('profile_list:\n{}'.format('\n'.join(profile_list)))
    result = {}
    result['profile_list'] = profile_list
    result['folder'] = folder
    result['file'] = file
    result_str = json.dumps(result)
    return result_str


def save_list_func(game, profile):
    save_list = SaveLoadManagerFunc.save_list_func(game, profile)
    # save_list = '\n'.join(save_list)
    print('save_list:\n{}'.format('\n'.join(save_list)))
    result = {}
    result['save_list'] = save_list
    result_str = json.dumps(result)
    return result_str


def game_delete(game):
    return SaveLoadManagerFunc.game_delete(game)


def profile_new(game, profile):
    return SaveLoadManagerFunc.profile_new(game, profile)


def profile_delete(game, profile):
    return SaveLoadManagerFunc.profile_delete(game, profile)


def save_new(game, profile, folder, file, comment):
    return SaveLoadManagerFunc.save_new(game, profile, folder, file, comment)


def save_delete(game, profile, save, folder, file):
    return SaveLoadManagerFunc.save_delete(game, profile, save, folder, file)


def save_load(game, profile, save, folder, file):
    return SaveLoadManagerFunc.save_load(game, profile, save, folder, file)


@Request.application
def post_resource(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["game_list_func"] = game_list_func
    dispatcher['profile_list_func'] = profile_list_func
    dispatcher['save_list_func'] = save_list_func
    dispatcher['game_delete'] = game_delete
    dispatcher['profile_new'] = profile_new
    dispatcher['profile_delete'] = profile_delete
    dispatcher['save_new'] = save_new
    dispatcher['save_delete'] = save_delete
    dispatcher['save_load'] = save_load
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json', headers=[["Access-Control-Allow-Origin", "*"]])


@Request.application
def get_resource(request):
    # with open("./SaveLoadManagerServer_JSON_RPC_HTTP.html", mode="r", errors='ignore') as html_file:
    #     result = html_file.read()
    result = SaveLoadManagerServer_JSON_RPC_HTTP_String.html_string
    return Response(''.join(result), mimetype='text/html')


url_map = Map([
    Rule('/', endpoint=get_resource, methods=['get']),
    Rule('/jsonrpc', endpoint=post_resource, methods=['post']),
])


@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    endpoint, values = adapter.match()
    request.environ['values'] = values
    return endpoint


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application)
