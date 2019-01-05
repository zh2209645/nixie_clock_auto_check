#!/usr/bin/python3

import sys
import clock_supp
import time

time_sleep = 3600
auto_close_connection = True
cl = clock_supp.Nixie_Clock()

def check_time(Nixie_Clock_Object):
    if not Nixie_Clock_Object.is_open():
        Nixie_Clock_Object.open()
    t = time.time()
    print('---------------------')
    print(time.asctime(time.localtime(t)) + ' check clock time...')
    Nixie_Clock_Object.save_time(t)
    if auto_close_connection:
        Nixie_Clock_Object.close()
    print('Finish')
    print('---------------------')


if __name__ == "__main__":
    if cl.is_open():
        cl.close()
    
    if len(sys.argv) != 1:
        time_sleep = int(sys.argv[1])
    
    while True:
        check_time(cl)
        time.sleep(time_sleep)