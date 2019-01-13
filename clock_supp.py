#!/usr/bin/python3

import serial
import time

class Nixie_Clock:

    __debug_mode = False

    night_mode = False

    baud_rate = 115200
    port = '/dev/ttyACM0'
    light_color = ['FF8C00', 'FF8C00', 'FF8C00', 'FF8C00', 'FF8C00', 'FF8C00']

    close_light = ['000000', '000000', '000000', '000000', '000000', '000000']
    
    ser = None
    timeout = 0.5

    def __init__(self):
        self.read_config()
        if self.__debug_mode:
            print('Port={}, baudrate={} open finished.'.format(self.port, self.baud_rate))
        else:
            self.ser = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=self.timeout)
    
    def change_baud_rate(self, baud_rate=int()):
        self.baud_rate = baud_rate
        self.save_config()

    def change_port(self, port=str()):
        self.port = port
        self.save_config()

    def change_color(self, light_index, color_str):
        self.light_color[light_index] = color_str
        self.save_config()
    
    def save_time(self, timestamp=time.time()):
        time_data = self.__time_convert(timestamp)
        write_data = self.__encode_data(self.light_color, time_data)
        
        self.write_to_clock(write_data.encode())

    def close_clock_light(self, timestamp=time.time()):
        time_data = self.__time_convert(timestamp)
        write_data = self.__encode_data(self.close_light, time_data)
        print('close clock light')
        self.write_to_clock(write_data.encode())

    def __time_convert(self, timestamp):
        struct_time = time.localtime(timestamp)
        time_list = ['0', '0', '0', '0', '0', '0']
        
        tm_hour = str(struct_time.tm_hour)
        if len(tm_hour) == 1:
            time_list[0] = '0'
        else:
            time_list[0] = tm_hour[0]
        time_list[1] = tm_hour[-1]
        
        tm_min = str(struct_time.tm_min)
        if len(tm_min) == 1:
            time_list[2] = '0'
        else:
            time_list[2] = tm_min[0]
        time_list[3] = tm_min[-1]

        tm_sec = str(struct_time.tm_sec)
        if len(tm_sec) == 1:
            time_list[4] = '0'
        else:
            time_list[4] = tm_sec[0]
        time_list[5] = tm_sec[-1]
        
        return time_list

    def connection(self):
        if self.__debug_mode:
            print("Connected")
        else:
            if self.ser.isOpen():
                print("Connected")
            else:
                print('Disconnected')

    def close(self):
        if self.__debug_mode:
            print("Connection closed")
        else:
            if self.ser.isOpen():
                self.ser.close()
                print("Connection closed")
            else:
                print("Connection already closed")
        
    def open(self):
        if self.__debug_mode:
            print("Connection opened")
        else:
            if self.ser.isOpen():
                print("Already connected")
            else:
                self.ser.open()
                print("Connection opened")
    
    def is_open(self):
        if self.__debug_mode:
            return True
        else:
            return self.ser.isOpen()

    def is_night_mode(self):
        return self.night_mode

    def __encode_data(self, color_setting, time_data):
        write_data = '*'

        for i in range(6):
            write_data = write_data + time_data[i] + color_setting[i]
        
        return write_data

    def write_to_clock(self, bytes_data):
        if self.__debug_mode:
            print('write data {}'.format(bytes_data.decode()))
        else:
            self.ser.write(bytes_data)
            for line in self.ser.readlines():
                print(line.decode())

    def recv_data(self):
        for line in self.ser.readlines():
            print(line.decode())

    def save_config(self):
        with open('n_clock.config', 'w') as file_to_write:
            file_to_write.write(str(self.baud_rate))
            file_to_write.write('\n')
            file_to_write.write(self.port)
            file_to_write.write('\n')
            l_color = ' '.join(self.light_color)
            file_to_write.write(l_color)

    def read_config(self):
        try:
            setting = list()
            with open('n_clock.config', 'r') as file_to_read:
                for line in file_to_read.readlines():
                    line = line.strip()
                    setting.append(line)
            self.load_setting_from_list(setting)
            
        except FileNotFoundError as err:
            print(err)
            print('Nixie clock Profile does not exist')
            print('Using default setting...')
            self.save_config()

    def load_setting_from_list(self, setting=list()):
        if len(setting) != 0:
            print('-------- load setting --------')
            self.baud_rate = setting[0]
            print('Set baud rate {}'.format(self.baud_rate))
            self.port = setting[1]
            print('Set port {}'.format(self.port))
            l_color = setting[2].split(' ')
            self.light_color = l_color
            print('Set light color {}'.format(self.light_color))