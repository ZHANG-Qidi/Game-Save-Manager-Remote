#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
import pathlib
import json
import SaveLoadManagerServer_JSON_RPC_HTTP_String
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound, MethodNotAllowed
from jsonrpc import JSONRPCResponseManager, dispatcher
import SaveLoadManagerCore


def game_list_func():
    game_list = SaveLoadManagerCore.game_list_func()
    print('game_list:\n{}'.format('\n'.join(game_list)))
    result = {}
    result['game_list'] = game_list
    result_str = json.dumps(result)
    return result_str


def profile_list_func(game):
    (profile_list, folder, file) = SaveLoadManagerCore.profile_list_func(game)
    profile_list.sort()
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
    save_list = SaveLoadManagerCore.save_list_func(game, profile)
    print('save_list:\n{}'.format('\n'.join(save_list)))
    result = {}
    result['save_list'] = save_list
    result_str = json.dumps(result)
    return result_str


def game_delete(game):
    return SaveLoadManagerCore.game_delete(game)


def profile_new(game, profile):
    return SaveLoadManagerCore.profile_new(game, profile)


def profile_delete(game, profile):
    return SaveLoadManagerCore.profile_delete(game, profile)


def save_new(game, profile, folder, file, comment):
    return SaveLoadManagerCore.save_new(game, profile, folder, file, comment)


def save_delete(game, profile, save, folder, file):
    return SaveLoadManagerCore.save_delete(game, profile, save, folder, file)


def save_load(game, profile, save, folder, file):
    return SaveLoadManagerCore.save_load(game, profile, save, folder, file)


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
    path = request.environ['values'].get('resource_path', '')
    if request.path == "/":
        result = SaveLoadManagerServer_JSON_RPC_HTTP_String.html_string
        return Response(''.join(result), mimetype='text/html')
    elif "SCREENSHOT" in path:
        image_type_list = ['jpg', 'png']
        for image_type in image_type_list:
            file_path = pathlib.Path(f"./{path}.{image_type}")
            if file_path.is_file():
                with open(file_path, 'rb') as image:
                    IMAGE_DATA = image.read()
                return Response(IMAGE_DATA, mimetype=f'image/{image_type}')
    return redirect('/')


url_map = Map([
    Rule('/', endpoint=get_resource, methods=['get']),
    Rule('/jsonrpc', endpoint=post_resource, methods=['post']),
    Rule('/<path:resource_path>', endpoint=get_resource, methods=['get']),
])


@Request.application
def application(request):
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        request.environ['values'] = values
        return endpoint
    except NotFound:
        return Response("Not Found", status=404)
    except MethodNotAllowed:
        return Response("Method Not Allowed", status=405)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=404)


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application)
