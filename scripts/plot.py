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

RUR_CONFIG = {
    'plot_title': '',
    'y_axis_name': 'RUR price',
    'png_thumb_filename': '../img/GSTRUR_graph_thumb.png',
    'png_filename': '../img/GSTRUR_graph.png',
    'history_url': 'http://nvspc.i2p/api/dummy/gettradelog?e=5&c=500&bt=2',
}

BTC_CONFIG = {
    'plot_title': '',
    'y_axis_name': 'BTC price',
    'png_thumb_filename': '../img/GSTBTC_graph_thumb.png',
    'png_filename': '../img/GSTBTC_graph.png',
    'history_url': 'http://nvspc.i2p/api/dummy/gettradelog?e=5&c=500&bt=3',
}

THUMB_DPI               = 40        # thumbnail DPI
DPI                     = 120       # affects the size of output image

PROXY_URL = 'http://localhost:4444'

def get_data_from_nvspc(url):
    proxy_handler = urllib.request.ProxyHandler({
        'http': PROXY_URL
    })
    opener = urllib.request.build_opener(proxy_handler)
    response = opener.open(url)
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

def draw_plot(config, oneline, secondline, dates):
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
    plt.ylabel(config['y_axis_name'])
    plt.title(config['plot_title'])
    plt.grid(True)
    plt.savefig(config['png_filename'],
                bbox_inches='tight',
                dpi=DPI,
                transparent=True)
    plt.savefig(config['png_thumb_filename'],
                bbox_inches='tight',
                dpi=THUMB_DPI,
                transparent=True)

def generate_graphic(config):
    data = get_data_from_nvspc(config['history_url'])
    oneline, secondline, dates = adapt_data_for_plot(data)
    draw_plot(config, oneline, secondline, dates)


def generate_graphics():
    generate_graphic(RUR_CONFIG)
    generate_graphic(BTC_CONFIG)


if __name__ == "__main__":
    generate_graphics()
