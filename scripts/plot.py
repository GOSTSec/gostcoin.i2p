#!/usr/bin/python3

# requirements: sudo pip3 install matplotlib

import matplotlib;matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
import math
import json
import urllib

PLOT_TITLE = 'BTC_GST graph'
Y_AXIS_NAME = 'BTC price'
PNG_FILENAME = '../img/GSTBTC_graph.png'
DPI = 60 # affects the size of output image

HISTORY_URL = 'http://nvspc.i2p/api/dummy/gettradelog?e=5&c=500&bt=3'
PROXY_URL = 'http://localhost:4444'

def get_data_from_nvspc():
    proxy_handler = urllib.request.ProxyHandler({
        'http': PROXY_URL
    })
    opener = urllib.request.build_opener(proxy_handler)
    response = opener.open(HISTORY_URL)
    raw_result = response.read().decode()
    data = reversed(json.loads(raw_result)['data']['l'])
    return data

def adapt_data_for_plot(data):
    oneline = {'x': [], 'y': [], }
    secondline = {'x': [], 'y': [], }
    dates = []

    for i, chunk in enumerate(data):
        spl_chunk = chunk['d'].split('|')
        date = spl_chunk[0]
        price_buy = spl_chunk[1]
        price_diff = spl_chunk[2]
        price_sell = float(price_buy) + float(price_diff)
        date = datetime.strptime(date, '%y%m%d%H%M')
        oneline['x'].append(i)
        oneline['y'].append(price_sell)
        secondline['x'].append(i)
        secondline['y'].append(price_buy)
        dates.append(date)

    return oneline, secondline, dates

def draw_plot(oneline, secondline, dates):
    fig, ax = plt.subplots()
    ax.plot(oneline['x'], oneline['y'])
    ax.plot(secondline['x'], secondline['y'])
    N = len(dates)
    ind = np.arange(N)
    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, N - 1)
        if thisind > N - 1: thisind = N - 1
        return dates[thisind].strftime('%Y-%m-%d')

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    plt.ylabel(Y_AXIS_NAME)
    plt.title(PLOT_TITLE)
    plt.grid(True)
    plt.savefig(PNG_FILENAME, bbox_inches='tight', dpi=DPI)

def generate_graphic():
    data = get_data_from_nvspc()
    oneline, secondline, dates = adapt_data_for_plot(data)
    draw_plot(oneline, secondline, dates)


if __name__ == "__main__":
    generate_graphic()
