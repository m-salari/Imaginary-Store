import pandas as pd
from redis import Redis
import task1
import task2


class program:
    def __init__(self, port=6037, addr_csv='price_data.csv'):
        self.df = pd.read_csv(addr_csv)
        self.__my_server = Redis(host='localhost', port=port, db=0)
        self.__my_server.flushdb()

    def main(self):
        # task1
        task1.price_updater_service(self.df, self.__my_server)

        # task 2
        # tsk2 = task2.stock_performance_calculation(self.__my_server)
        # tsk2.run()

        pass


ttest = program()
ttest.main()
