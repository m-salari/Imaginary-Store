import json
from datetime import datetime
import time
from threading import Thread
from utils import stock_last_product, show_stocks_in_redis


def calculate_performance(stock_price):
    time.sleep(3)
    return 0


class stock_performance_calculation:
    def __init__(self, server):
        self.server = server
        self.stock2 = stock_last_product()
        self.stock3 = stock_last_product()
        self.stock1 = stock_last_product()
        self.lst_stock = [self.stock1, self.stock2, self.stock3]
        # create backup stocks nodes for comparison

    def run(self):
        while True:
            thread_stock1 = Thread(target=self.stock_performance_updator, args=('stock1', 1))
            thread_stock2 = Thread(target=self.stock_performance_updator, args=('stock2', 2))
            thread_stock3 = Thread(target=self.stock_performance_updator, args=('stock3', 3))

            thread_stock1.start()
            thread_stock2.start()
            thread_stock3.start()

            thread_stock1.join()
            thread_stock2.join()
            thread_stock3.join()

            show_stocks_in_redis(self.server)
            time.sleep(10)

    def stock_performance_updator(self, name_stock, stock_id: int):
        stock_id -= 1
        last_info = self.server.lrange(name_stock, -1, -1)[0].decode()  # get last info stock
        last_info = eval(last_info)  # convert str to dict

        # get time last stock
        last_time_from_redis = datetime.strptime(last_info['time'], '%H:%M:%S').time()

        s = time.time()

        # check time is changed. if time changed, check the price has also changed
        if last_time_from_redis > self.lst_stock[stock_id].time and last_info['price'] != self.lst_stock[
            stock_id].price:
            # change time and price last stock in nodes
            self.lst_stock[stock_id].time = last_time_from_redis
            self.lst_stock[stock_id].price = last_info['price']
            calculate_performance(self.lst_stock[stock_id].price)

        f = time.time()

        self.add_performance_value(name_stock, json.dumps({'performance': str(f - s)}))

    def add_performance_value(self, name_stock, value, index=0):
        # check field performance exist. if exist updated it. else add field performance in redis

        flag_exist_performance = eval(self.server.lrange(name_stock, 0, 0)[0].decode()).get('performance')
        if flag_exist_performance:
            self.server.lset(name_stock, index, value)
        else:
            self.server.lpush(name_stock, value)
