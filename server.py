#!/usr/local/bin/python3

import socket
import threading
import struct as st
import pandas as pd

HOST = ''
PORT = 6969
df = pd.read_csv("/Users/davidmullings/Desktop/College/junior_first_semester/ufa/updated_dues.csv")
df.drop(columns = df.columns[0], inplace=True)
df["Name"] = df["Name"].astype('string')
df["EID"] = df["EID"].astype('string')
e: threading.Event = threading.Event()

def quit_on_stdin(event: threading.Event):
    user_input: str = '\n'
    while not event.is_set():

        try:
            user_input = input()
            if user_input == 'q':
                event.set()

                break
        except EOFError:
            event.set()
            break

def unpack_message(data: bytes) -> tuple:
    format: str = '<?50s'
    action, message = st.unpack(format, data)
    return action, message.decode('utf-8')

def pack_message(field: bool, found: bool, dues: bool) -> bytes:
    format: str = '<???'
    p = st.pack(format, field, found, dues)
    return p

def dataframe_perform_actions(action: chr, message: str, last_eid: str) -> tuple:
    if action == 0:
        eid_entry = df.loc[df["EID"] == message]
        if len(eid_entry) > 0:
            return 0, 1, eid_entry.iloc[0]["Dues Paid"] >= 30
        else:
            return 0, 0, 0
    elif action == 1:
        name_entry = df.loc[df["Name"] == message]
        if len(name_entry) > 0:
            print(last_eid)
            df.loc[df["Name"] == message + '', ['EID']] = str(last_eid)
        else:
            return 1, 0, 0
        return 1, 1, name_entry.iloc[0]["Dues Paid"] >= 30



def interact(conn: socket.socket, addr: socket.AddressInfo):
    with conn:
        print('Connected by', addr)
        last_eid: str = ''
        while not e.is_set():
            data: bytes = conn.recv(64)
            if not data: break

            # unpack message and perform actions
            action, message = unpack_message(data)
            message = message.rstrip('\x00')
            print(action, message)
            if (action == 0):
                last_eid = message

            # search / write to Pandas dataframe
            print(message)
            field, found, dues = dataframe_perform_actions(action, message, last_eid)
            print(field, found, dues)
            conn.sendall(pack_message(field, found, dues))
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    t1 = threading.Thread(target=quit_on_stdin, args=(e,))
    t1.start()
    s.listen(6)
    while not e.is_set():
        conn, addr = s.accept()
        temp = threading.Thread(target=interact, args=(conn, addr))
        temp.start()

df.to_csv('/Users/davidmullings/Desktop/College/junior_first_semester/ufa/updated_dues.csv')


        