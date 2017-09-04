#!/usr/bin/python3
# thanks to xcps
# requirements: sudo pip3 install matplotlib;sudo apt-get install python3-tk
# need python version of 3 
# TODO: check to (opportunity) more understanded code.

import plot_settings as settings

import math,json,matplotlib

import numpy as np

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker

from datetime import datetime, timedelta


import urllib as urls


def get_HTTP_proxy(http_proxy=settings.HTTP_PROXY_URL):
    return urls.request.build_opener(urls.request.ProxyHandler(	{'http': http_proxy} ) )

def response_proxies(url,opener=None):
	if opener is None:
		opener = get_HTTP_proxy()
	try:
		data = opener.open(url)
		return data.read().decode()
	except urls.HTTPError:
		print ("Maybe site is down")
		return False

def adapt_data_for_plot(data):
    #print(data)
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
    plt.ylabel(settings.Y_AXIS_NAME)
    plt.title(settings.PLOT_TITLE)
    plt.grid(True)
    plt.savefig(settings.IMAGE_EXIST_PATH, bbox_inches='tight', dpi=settings.DPI, transparent=True) 

def generate_graphic_from_nvspc():
    raw_result = response_proxies(settings.NVSPC_HISTORY_API) 
    if raw_result == False:
    	return None
    data = reversed(json.loads(raw_result)['data']['l'])
    raw_result=None
    oneline, secondline, dates = adapt_data_for_plot(data)
    draw_plot(oneline, secondline, dates)


if __name__ == "__main__":
    generate_graphic_from_nvspc()
