#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
from concurrent import futures
import logging
import grpc
import SaveLoadManager_pb2
import SaveLoadManager_pb2_grpc
import SaveLoadManagerFunc


class SaveLoadManager(SaveLoadManager_pb2_grpc.SaveLoadManagerServicer):
    def game_list_func(self, request, context):
        game_list = SaveLoadManagerFunc.game_list_func()
        game_list = '\n'.join(game_list)
        print('game_list:\n{}'.format(game_list))
        return SaveLoadManager_pb2.response_game_list(game_list=game_list)

    def profile_list_func(self, request, context):
        (profile_list, folder, file) = SaveLoadManagerFunc.profile_list_func(request.game)
        profile_list.sort()
        profile_list = '\n'.join(profile_list)
        print('folder: {}'.format(folder))
        print('file: {}'.format(file))
        print('profile_list:\n{}'.format(profile_list))
        return SaveLoadManager_pb2.response_profile_list(profile_list=profile_list, folder=folder, file=file)

    def save_list_func(self, request, context):
        save_list = SaveLoadManagerFunc.save_list_func(request.game, request.profile)
        save_list = '\n'.join(save_list)
        print('save_list:\n{}'.format(save_list))
        return SaveLoadManager_pb2.response_save_list(save_list=save_list)

    def game_delete(self, request, context):
        return SaveLoadManager_pb2.response_game_delete(message=SaveLoadManagerFunc.game_delete(request.game))

    def profile_new(self, request, context):
        return SaveLoadManager_pb2.response_profile_new(message=SaveLoadManagerFunc.profile_new(request.game, request.profile))

    def profile_delete(self, request, context):
        return SaveLoadManager_pb2.response_profile_delete(message=SaveLoadManagerFunc.profile_delete(request.game, request.profile))

    def save_new(self, request, context):
        return SaveLoadManager_pb2.response_save_new(message=SaveLoadManagerFunc.save_new(request.game, request.profile, request.folder, request.file, request.comment))

    def save_delete(self, request, context):
        return SaveLoadManager_pb2.response_save_delete(message=SaveLoadManagerFunc.save_delete(request.game, request.profile, request.save, request.folder, request.file))

    def save_load(self, request, context):
        return SaveLoadManager_pb2.response_save_load(message=SaveLoadManagerFunc.save_load(request.game, request.profile, request.save, request.folder, request.file))


def serve():
    port = "8000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SaveLoadManager_pb2_grpc.add_SaveLoadManagerServicer_to_server(SaveLoadManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
