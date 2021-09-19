#!/usr/local/bin/python3

import socket
import struct as st
import re
import os
import time

HOST = '10.2.4.182'
PORT = 6969

def pack_message(message: str) -> bytes:
    format: str = '<?50s'
    action: bool
    if re.search('[0-9]', message) != None:
        action = False
    else:
        action = True
    p = st.pack(format, action, message.encode())
    return p

def unpack_message(data: bytes) -> tuple:
    format: str = '<???'
    field, found, dues = st.unpack(format, data)
    return field, found, dues

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    prompt: str = 'Please enter UT EID: '
    while True:
        try:
            os.system('cls||clear')
            message: str = input(prompt)
            if message == 'q': break
            s.sendall(pack_message(message))
            data = s.recv(1024)
            field, found, dues = unpack_message(data)
            if not dues:
                if not field:
                    if found:
                        print('Please pay full dues.')
                        prompt = 'Please enter your UT EID: '
                        time.sleep(3)
                    else:
                        prompt = 'Please enter \'FirstName\' \'LastName\': '
                else:
                    if found:
                        print('Please pay full dues.')
                        prompt = 'Please enter your UT EID: '
                        time.sleep(3)
                    else:
                        print('Not present in system.')
                        prompt = 'Please enter your UT EID: '
                        time.sleep(3)
            else:
                print('Welcome to this week\'s UFA meeting!')
                prompt = 'Please enter your UT EID: '
                time.sleep(3)
        except EOFError:
            break
