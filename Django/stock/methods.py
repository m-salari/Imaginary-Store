import multiprocessing
import threading
import time as time_lib
from redis import Redis
from django.conf import settings
import json
import random

redis_instance: Redis = settings.REDIS_INSTANCE


def verify_user():
    time_lib.sleep(random.randint(1, 100))
    # time_lib.sleep(x)
    return 0


lst_process = []


class process_info:
    def __init__(self, process, username):
        self.process: multiprocessing = process
        self.user = username
        self.time = 0


def find_user_in_redis(username):
    lst_users = redis_instance.lrange('users', 0, -1)  # get list users in redis
    for u in range(len(lst_users)):  # search user in redis

        user_info: dict = eval(lst_users[u].decode())
        if user_info.get('user') == username:  # find user
            return user_info, u


def handler_process():
    while True:

        for i in range(len(lst_process)):

            if lst_process[i].process.is_alive() and lst_process[i].time > 60:
                lst_process[i].process.kill()

                # change result_BuyStock in redis to stalling

                user_info, u = find_user_in_redis(lst_process[i].user)
                user_info['result_BuyStock'] = 'stalling'
                redis_instance.lset('users', u, json.dumps(user_info))

                del lst_process[i]

                break

            elif lst_process[i].process.is_alive():
                lst_process[i].time += 1
            else:
                # change result in redis to successful

                user_info, u = find_user_in_redis(lst_process[i].user)
                user_info['result_BuyStock'] = 'successful'
                redis_instance.lset('users', u, json.dumps(user_info))

                del lst_process[i]
                break

        time_lib.sleep(1)


thread_handler_process = threading.Thread(target=handler_process, daemon=True)
