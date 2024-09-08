from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from http.server import HTTPServer, SimpleHTTPRequestHandler
import SaveLoadManagerFunc
import json
import threading


def game_list_func():
    game_list = SaveLoadManagerFunc.game_list_func()
    # game_list = '\n'.join(game_list)
    print('game_list:\n{}'.format(game_list))
    result = {}
    result['game_list'] = game_list
    result_str = json.dumps(result)
    return result_str


def profile_list_func(game):
    (profile_list, folder, file) = SaveLoadManagerFunc.profile_list_func(game)
    profile_list.sort()
    # profile_list = '\n'.join(profile_list)
    print('folder: {}'.format(folder))
    print('file: {}'.format(file))
    print('profile_list:\n{}'.format(profile_list))
    result = {}
    result['profile_list'] = profile_list
    result['folder'] = folder
    result['file'] = file
    result_str = json.dumps(result)
    return result_str


def save_list_func(game, profile):
    save_list = SaveLoadManagerFunc.save_list_func(game, profile)
    # save_list = '\n'.join(save_list)
    print('save_list:\n{}'.format(save_list))
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
def application(request):
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


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    thread_server_http = threading.Thread(target=run)
    thread_server_json_rpc = threading.Thread(target=run_simple, args=('0.0.0.0', 4000, application))
    thread_server_http.start()
    thread_server_json_rpc.start()
    thread_server_http.join()
    thread_server_json_rpc.join()
