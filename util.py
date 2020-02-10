# -*- coding: utf-8 -*-
__date__ = '2020/2/10 22:37'


import time

weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

monthname = [None,
             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# 返回日期字符串
def date_time_string(timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    year, month, day, hh, mm, ss, wd, y, z = time.localtime(timestamp)
    s = "%s, %02d %3s %4d %02d:%02d:%02d" % (
        weekdayname[wd],
        day, monthname[month], year,
        hh, mm, ss)
    return s
