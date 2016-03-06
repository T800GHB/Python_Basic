# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 23:25:17 2016

@author: T800GHB
This file will demostrate how use some function contain in datatime model.
"""
from datetime import datetime
from datetime import timedelta
from datetime import timezone

def run_demo():
    """
    Acquire current time
    """
    now = datetime.now()
    print('Current time is :', now)
    
    #Create a datetime object
    dt = datetime(2016,3,3,23,33,40)
    print('datetime object :', dt)
    
    #Convert from datetime object to timestamp. Timestamp is global unique.
    ts = dt.timestamp()
    print('Timestamp of 2016-03-03-23:33:40 is: ', ts)
    
    #Convert from timestamp to datetime object
    dt_r = datetime.fromtimestamp(ts)
    print('Datetime convert from timestamp is: ', dt_r)
    
    #Adjust to UTC time
    dt_utc = datetime.utcfromtimestamp(ts)
    print('UTC time is: ', dt_utc)
    
    #Create datetime from string
    dt_s = datetime.strptime('2016-3-3 23:45:23', '%Y-%m-%d %H:%M:%S')
    print('Time convert from string is: ', dt_s)
    
    #Create string from datetime
    s_dt = now.strftime('%a, %b %d %H:%M')
    print('Time convert to string is: ', s_dt)
    
    #Time offset operation. Use current time as basis.
    t_p = now + timedelta(hours = 10)
    print('Time after 10 hours is: ',t_p)
    t_m = now - timedelta(days = 1)
    print('Time before a day is: ', t_m)
    t_d = now + timedelta(days = 2, hours = 5)
    print('Time after 2 days and 5 hours: ', t_d)
    
    #Convert local time to UTC time. 
    tz_utc_8 = timezone(timedelta(hours = 8))
    dt_8 = now.replace(tzinfo = tz_utc_8)
    print('UTC time: ', dt_8)
    
    """
    Timezone convertion. 
    Set one kind of time as basis, then use astimezone complete convertion.
    """
    utc_dt = datetime.utcnow().replace(tzinfo = timezone.utc)
    print('UTC timezone: ', utc_dt)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours = 8)))
    print('Beijing time: ', bj_dt)
    tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours = 9)))
    print('Tokyo time: ', tokyo_dt)
    tokyo_dt = bj_dt.astimezone(timezone(timedelta(hours = 9)))
    print('Tokyo time: ', tokyo_dt)