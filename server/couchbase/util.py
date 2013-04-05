import time
import datetime

RD_PORT = '8080'

SERVER_IP = '147.83.35.241'
SERVER_PORT = '8000'

DB_IP = '147.83.35.241'
DB_PORT= '8091'

CONTROLLER_IP = 'controller.confine-project.eu'
CONTROLLER_PORT= '8080'

TIMEPERIOD = 20

LAST_SEEN_SEQ_NUMBER = 0

def convert_secs_to_time(secs):
    return((datetime.timedelta(seconds = secs)))


def get_most_recent_sequence_number(page):
    max=0
    for key in page.keys():
        if int(key) > max:
            max = int(key)

    return max

def get_timestamp():
    timestamp = time.time()
    return  timestamp

def find_recent_timestamp(max_so_far, absolute_value):
    if absolute_value > max_so_far:
        return absolute_value
    else:
        return max_so_far

def convert_epoch_to_date_time_dict(epoch):
    date_time= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch))
    return ({'time': date_time})

def convert_epoch_to_date_time_dict_attributes(epoch):
    date_time= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch))
    (date, local_time) = date_time.split()
    (year, month, date) = date.split('-')
    (hour, minute, second) = local_time.split(':')
    return ({'year':year,'month': month, 'date': date, 'hour': hour, 'minute':minute, 'second': second})

def convert_epoch_to_date_time_javascript(epoch):
    date_time= convert_epoch_to_date_time_dict_attributes(epoch)
    date_time['month'] = int (date_time['month']) -1
    return date_time


def convert_bytes_to_human_readable(bytes=[]):
    '''
    Accepts a list
    Returns updated values
    '''

    length = len(bytes)
    for index in range(length):
        value = bytes2human(bytes[index])
        bytes[index]= value
    return bytes


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

