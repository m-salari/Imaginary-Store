from datetime import datetime
import json


def price_updater_service(df, server):
    # add each row to my_server as keys: x['Stock'] and value: {x['Time'], x['Price']}
    df.apply(lambda x: server.rpush(x['Stock'],
                                    json.dumps({'time': str(
                                        datetime.strptime(str(x['Time']), '%H%M%S').time()),
                                        'price': x['Price']})), axis=1)  # set value
    print('finish price updator service')