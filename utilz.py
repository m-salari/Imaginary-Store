from datetime import datetime


class stock_last_info:
    def __init__(self, time_stock='0:0:0', price_stock=0):
        self.time = datetime.strptime(time_stock, '%H:%M:%S').time()
        self.price = price_stock


def show_stocks_in_redis(server):
    print('\n************************************************************\n')
    s1 = server.lrange('stock1', 0, -1)
    s2 = server.lrange('stock2', 0, -1)
    s3 = server.lrange('stock3', 0, -1)

    print("stock1:", s1)
    print("stock2:", s2)
    print("stock3:", s3)
