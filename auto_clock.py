#!/usr/bin/python3

import sys
import clock_supp
import time

time_sleep = 3600
countdown_step = 5

auto_close_connection = True

night_mode = True
night_mode_start = {'hour': 0, 'min': 0}
night_mode_end = {'hour': 8, 'min': 0}



cl = clock_supp.Nixie_Clock()

def check_time(Nixie_Clock_Object):
    if not Nixie_Clock_Object.is_open():
        Nixie_Clock_Object.open()
        time.sleep(5)
    t = time.time()
    print('---------------------')
    print(time.asctime(time.localtime(t)) + ' check clock time...')
    Nixie_Clock_Object.save_time(t)
    if auto_close_connection:
        Nixie_Clock_Object.close()
    print('Finish')
    print('---------------------')
    time.sleep(5)

def turn_on_night_mode(Nixie_Clock_Object):
    if not Nixie_Clock_Object.is_open():
        Nixie_Clock_Object.open()
        time.sleep(5)
    t = time.time()
    print('---------------------')
    print(time.asctime(time.localtime(t)) + ' close clock light...')
    Nixie_Clock_Object.close_clock_light(t)
    if auto_close_connection:
        Nixie_Clock_Object.close()
    print('Finish')
    print('---------------------')
    time.sleep(5)

def in_night(timestamp=time.time()):
    struct_time = time.localtime(timestamp)
    
    tm_hour = struct_time.tm_hour
    tm_min = struct_time.tm_min

    if night_mode_start['hour'] == tm_hour:
        if night_mode_start['min'] <= tm_min < night_mode_end['min']:
            return True
    elif night_mode_start['hour'] < tm_hour < night_mode_end['hour']:
        return True
    elif night_mode_end['hour'] == tm_hour:
        if night_mode_end['min'] > tm_min:
            return True
    return False
        

if __name__ == "__main__":
    if cl.is_open():
        cl.close()
        time.sleep(10)
    
    if len(sys.argv) != 1:
        time_sleep = int(sys.argv[1])
    
    countdown = 0

    # Main loop 
    while True:
        while countdown > 0:
            if night_mode:
                t = time.time()
                if cl.is_night_mode():
                    if not in_night(t):
                        check_time(cl)
                        cl.night_mode = False
                        countdown = time_sleep
                    else:
                        time.sleep(countdown_step)
                else:
                    if in_night(t):
                        turn_on_night_mode(cl)
                        cl.night_mode = True
                        countdown = time_sleep
                    else:
                        countdown = countdown - countdown_step
                        time.sleep(countdown_step)
            else:
                countdown = countdown - countdown_step
                time.sleep(countdown_step)

        check_time(cl)
        countdown = time_sleep