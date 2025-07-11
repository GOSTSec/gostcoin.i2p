#!/usr/bin/python3

# requirements: matplotlib

import matplotlib;matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime, UTC
from decimal import Decimal
import math
import json
from urllib import request

every = 2
samples = 5000

RUR_CONFIG = {
    'plot_title': 'updated at {}'.format(datetime.now(UTC).strftime('%Y-%m-%d %H:%M %z')),
    'x_axis_name': 'graph for latest {} price records (each {} record)'.format(samples*every, every),
    'y_axis_name': 'RUR price',
    'png_thumb_filename': '../img/GSTRUR_graph_thumb.png',
    'png_filename': '../img/GSTRUR_graph.png',
    'history_url': 'http://obmen.i2p/api/dummy/gettradelog?e={}&c={}&bt=2'.format(every, samples),
}

BTC_CONFIG = {
    'plot_title': 'updated at {}'.format(datetime.now(UTC).strftime('%Y-%m-%d %H:%M')),
    'x_axis_name': 'graph for latest {} price records (each {} record)'.format(samples*every, every),
    'y_axis_name': 'BTC price',
    'png_thumb_filename': '../img/GSTBTC_graph_thumb.png',
    'png_filename': '../img/GSTBTC_graph.png',
    'history_url': 'http://obmen.i2p/api/dummy/gettradelog?e={}&c={}&bt=3'.format(every, samples),
}

THUMB_DPI               = 40        # thumbnail DPI
DPI                     = 300       # affects the size of output image

PROXY_URL = 'http://localhost:4444'
TIMEOUT = 60

def get_data_from_exchange(url):
    proxy_handler = request.ProxyHandler({
        'http': PROXY_URL
    })
    opener = request.build_opener(proxy_handler)
    try:
        response = opener.open(url, None, TIMEOUT)
        raw_result = response.read().decode()
        data = reversed(json.loads(raw_result)['data']['l'])
        return data
    except Exception as ex:
        print(ex)
        exit(1)

def adapt_data_for_plot(data):
    oneline = {'x': [], 'y': [], }
    secondline = {'x': [], 'y': [], }

    #for i, chunk in enumerate(data):
    for chunk in data:
        spl_chunk = chunk['d'].split('|')
        date = spl_chunk[0]
        price_buy = Decimal(spl_chunk[1])
        price_diff = Decimal(spl_chunk[2])
        price_sell = float(price_buy + price_diff)
        date = datetime.strptime(date, '%y%m%d%H%M')
        oneline['x'].append(date)
        oneline['y'].append(price_sell)
        secondline['x'].append(date)
        secondline['y'].append(price_buy)

    return oneline, secondline

def draw_plot(config, oneline, secondline):
    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(oneline['x'], oneline['y'], label='Sell', linewidth=0.75)
    ax.plot(secondline['x'], secondline['y'], label='Buy', linewidth=0.75)
    ax.legend()

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.xlabel(config['x_axis_name'], fontsize=8)
    plt.ylabel(config['y_axis_name'], fontsize=10)
    plt.title(config['plot_title'], fontsize=14)
    plt.grid(True)
    plt.savefig(config['png_filename'],
                bbox_inches='tight',
                dpi=DPI,
                orientation='landscape',
                transparent=True)
    plt.savefig(config['png_thumb_filename'],
                bbox_inches='tight',
                dpi=THUMB_DPI,
                orientation='landscape',
                transparent=True)

def generate_graphic(config):
    print ("Fetching data...")
    data = get_data_from_exchange(config['history_url'])
    print ("Adapting data for plot...")
    oneline, secondline = adapt_data_for_plot(data)
    print ("Generating plot...")
    draw_plot(config, oneline, secondline)


def generate_graphics():
    generate_graphic(RUR_CONFIG)
    generate_graphic(BTC_CONFIG)


if __name__ == "__main__":
    generate_graphics()
