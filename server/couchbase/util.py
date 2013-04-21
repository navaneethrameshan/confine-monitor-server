import time
import datetime
import calendar

RD_PORT = '8080'

SERVER_IP = '127.0.0.1'
SERVER_PORT = '8000'

DB_IP = '147.83.35.241'
DB_PORT= '8091'

CONTROLLER_IP = 'controller.confine-project.eu'
CONTROLLER_PORT= '8080'

TIMEPERIOD = 20

LAST_SEEN_SEQ_NUMBER = 0

def convert_secs_to_time_elapsed(secs):
    if(secs):
        return((datetime.timedelta(seconds = secs)))


def get_most_recent_sequence_number(page):
    #TODO: Remove the use of max=0 and instead use first key as max, then compare. After this change make changes in collect().
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

def convert_epoch_to_date_time_dict_attributes_lstrip(epoch):
    date_time= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch))
    (date, local_time) = date_time.split()
    (year, month, date) = date.split('-')
    (hour, minute, second) = local_time.split(':')
    return ({'year':year.lstrip('0'),'month': month.lstrip('0'), 'date': date.lstrip('0'), 'hour': hour.lstrip('0'), 'minute':minute.lstrip('0'), 'second': second.lstrip('0')}) #Do not remove lstrip. Needed for stats view to work.

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


def split_arguments_return_dict(arguments):
    '''
    Accepts an argument of the form [start_time=2013-03-14&end_time=2013-03-16&limit=123] or any combination of elements
    in the list.

    Returns a dict of the form {'start_time_epoch':epoch, 'end_time_epoch':epoch, 'limit':123, 'start_time_year' =year,
    'start_time_month' = month, 'start_time_day' = day, 'end_time_day,month,year'=...}, whichever exists.

    The default values are {'start_time_year,month,day':"", 'end_time':"{}", 'limit':1000, start_time_epoch= "",
    end_time_epoch= "{}"}
    '''

    ret_dict = {'start_time_epoch':"", 'end_time_epoch':"{}", 'start_time_year': None,'start_time_month': None,
                'start_time_day': None,'end_time_year': None,'end_time_month': None,
                'end_time_day': None,'limit':100}

    arguments_list = arguments.split('&')
    for value in arguments_list:
        temp = value.split('=')
        if(len(temp)==2):
            type = compare_and_return_argument(temp[0])
            if type:
                if type!='limit':
                    epoch= convert_time_to_epoch(temp[1])
                    ret_dict[type+'_epoch']=str(epoch)
                    ret_dict[type+'_year'] = return_year_month_day_from_time(temp[1]).tm_year
                    ret_dict[type+'_month'] = return_year_month_day_from_time(temp[1]).tm_mon
                    ret_dict[type+'_day'] = return_year_month_day_from_time(temp[1]).tm_mday
                else:
                    ret_dict[type]=int(temp[1])
        else:
            continue

    return ret_dict


def compare_and_return_argument(type):
    if(type == 'start_time'):
        return 'start_time'
    elif(type == 'end_time'):
        return 'end_time'
    elif(type == 'limit'):
        return 'limit'
    else:
        return None

def return_year_month_day_from_time(date_time, pattern ='%Y-%m-%d'):
    return(time.strptime(date_time, pattern))

def convert_time_to_epoch(date_time,pattern = '%Y-%m-%d'):
    #date_time = '2007-02-05'

    epoch = int(calendar.timegm(time.strptime(date_time, pattern)))
    return epoch

convert_time_to_epoch('2013, 4, 20, 12, 0','%Y, %m, %d, %H, %M')
