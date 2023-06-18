import json

from django.conf import settings
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from redis import Redis

from .serializers import RegisterSerializer, LoginSerializer

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

redis_instance: Redis = settings.REDIS_INSTANCE
encrypt_algorithm = PBKDF2PasswordHasher()


def read_write_salt():
    salt = redis_instance.get('salt')
    if salt:
        return salt

    salt = encrypt_algorithm.salt()
    redis_instance.set('salt', salt)
    return salt.encode()


def check_username_exist(username):
    lst_user = redis_instance.lrange('users', 0, -1)
    for user in lst_user:
        if eval(user.decode())['user'] == username:
            # return True
            return eval(user.decode())


@api_view(['POST'])
def register_user(request: Request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('user')
        password = request.data.get('password')
        credit = request.data.get('credit')

        if not credit:
            credit = 0
        # check username not exist
        check_username = check_username_exist(username)
        if check_username:
            return Response(None, status.HTTP_302_FOUND)

        # add user in redis
        salt = read_write_salt().decode()
        password_hash = encrypt_algorithm.encode(password, salt)
        redis_instance.rpush('users', json.dumps({'user': username,
                                                  'password': password_hash,
                                                  'credit': credit}))
        # print('register done!')
        return Response(None, status.HTTP_201_CREATED)

    else:
        # print('password not same or not standard json')
        return Response(None, status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def login_user(request: Request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('user')
        password = request.data.get('password')

        user_in_redis = check_username_exist(username)
        if user_in_redis:

            check_password = encrypt_algorithm.verify(password, user_in_redis['password'])
            if check_password:

                # show panel
                response_login = profile(request)
                return Response(response_login, status.HTTP_200_OK)

    # print('user not found')
    return Response(None, status.HTTP_404_NOT_FOUND)


def profile(request: Request):
    username = request.data.get('user')
    user_info, u = find_user_in_redis(username)
    del user_info['password']
    return json.dumps(user_info)


def find_user_in_redis(username):
    lst_users = redis_instance.lrange('users', 0, -1)  # get list users in redis
    for u in range(len(lst_users)):  # search user in redis

        user_info: dict = eval(lst_users[u].decode())
        if user_info.get('user') == username:  # find user
            return user_info, u