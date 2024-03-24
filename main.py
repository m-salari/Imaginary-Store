import pandas as pd
from redis import Redis
import price_updater
import stock_performance_calculation


class program:
    def __init__(self, port=6037, addr_csv='price_data.csv'):
        self.df = pd.read_csv(addr_csv)
        self.__my_server = Redis(host='localhost', port=port, db=0)
        self.__my_server.flushdb()

    def run_price_updater(self):
        # task1
        price_updater.price_updater_service(self.df, self.__my_server)

    def run_performance_calculation(self):
        # task 2
        tsk2 = stock_performance_calculation.stock_performance_calculation(self.__my_server)
        tsk2.run()


if __name__ == '__main__':
    number_task = 0
    while True:
        try:
            number_task = int(input('''
            price_updater_service -- > 1
            stock_performance_calculation --> 2
            '''))

            if not (number_task == 1 or number_task == 2):
                raise ValueError('Please enter a valid number!!!')
            break
        except ValueError as e:
            print(e)

    app = program()
    if number_task == 1:
        app.run_price_updater()
    else:
        app.run_performance_calculation()




