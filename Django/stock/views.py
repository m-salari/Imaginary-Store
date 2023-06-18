import json

from django.conf import settings
from .serializers import UserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import multiprocessing
from .methods import process_info, verify_user, lst_process, thread_handler_process
from redis import Redis

# connect to redis
redis_instance: Redis = settings.REDIS_INSTANCE

if not thread_handler_process.is_alive():
    thread_handler_process.start()


@api_view(['POST'])
def buy_stock(request: Request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        request_username = request.data.get('user')

        lst_users = redis_instance.lrange('users', 0, -1)  # get list users in redis

        for i in range(len(lst_users)):  # search user in redis
            user = lst_users[i]
            user_info: dict = eval(user.decode())

            if user_info.get('user') == request_username:  # if user exist
                stock_name = request.data.get('stockname')

                if stock_name not in ['stock1', 'stock2', 'stock3']:  # check stock
                    return Response(None, status.HTTP_406_NOT_ACCEPTABLE)

                quantity = request.data.get('quantity')

                # get last price stock
                last_info_stock: dict = eval(redis_instance.lrange(stock_name, -1, -1)[0].decode())

                # check credit
                if last_info_stock['price'] * quantity <= int(user_info.get('credit')):
                    # print('success')

                    p = multiprocessing.Process(target=verify_user)
                    p.start()
                    lst_process.append(process_info(p, request_username))

                    user_info['result_BuyStock'] = 'processing'
                    redis_instance.lset('users', i, json.dumps(user_info))
                    return Response(None, status.HTTP_200_OK)

                else:
                    # print('not success')
                    return Response(None, status.HTTP_406_NOT_ACCEPTABLE)

        # print('user not found')
        return Response(None, status.HTTP_404_NOT_FOUND)
    else:
        # print("not valid")
        return Response(None, status.HTTP_401_UNAUTHORIZED)
