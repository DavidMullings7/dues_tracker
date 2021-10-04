import socket
import struct as st
import re
import os
import time

PORT = 33878

"""
function: pack_message:
    purpose: packs client message for delivery to server according to protocol (see dues_tracker/protocol_definition.txt)
    parameters:
        message: str:
            the query to be delivered to the server
    return values:
        p: bytes:
            the raw bytes to be delivered to the server
"""
def pack_message(message: str) -> bytes:
    format: str = '<?50s'
    
    # if query is name, set action to 1
    # else, set action to 0
    action: bool
    if re.search('[0-9]', message) != None:
        action = False
    else:
        action = True
    p: bytes = st.pack(format, action, message.encode())
    return p

"""
function: unpack_message:
    purpose: unpacks server message according to protocol (see dues_tracker/protocol_definition.txt)
    parameters:
        data: bytes:
            the raw bytes received from dues_tracker server
    return values:
        field, found, dues: tuple:
            field: bool: 
                indicates the field of the previously queried information (EID or Name)
            found: bool:
                indicates whether the previously queried information was found in dataframe
            dues: bool:
                indicates whether dues has been paid for queried EID / Name
"""
def unpack_message(data: bytes) -> tuple:
    format: str = '<???'
    field, found, dues = st.unpack(format, data)
    return field, found, dues

"""
function: display_text
purpose: display text in header
parameters:
    delimiter: chr:
        character to delimit text
    text:
        message to be displayed
return values:
none
"""
def display_text(delimiter: chr, text: str):
    columns, lines = os.get_terminal_size()
    print(delimiter * columns)
    print()
    print(str(' ' * (columns // 2 - len(text) // 2)) + text + str(' ' * (columns // 2)))
    print(delimiter * columns)

"""
function: main
parameters: 
    none
return values:
    none
"""
def main():

    # clear terminal for clean look
    os.system('cls||clear')

    display_text('#', 'UFA Sign-In Sheet')

    # prompt user to enter desired IP address
    HOST = input('Server IP Address: ')

    # use context manager to maintain socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # connect to server listening port
        s.connect((HOST, PORT))
        prompt: str = 'Please enter UT EID: '
        while True:
            
            # continue reading user input until 'q' or EOF error
            try:
                os.system('cls||clear')
                display_text('#', 'UFA Sign-In Sheet')
                message: str = input(prompt)
                if message == 'q': break
                s.sendall(pack_message(message))
                data = s.recv(1024)

                # unpack server message and process future behavior
                field, found, dues = unpack_message(data)
                if not dues: # dues not paid
                    if not field: # field is EID
                        if found: # EID found
                            print('\n' * 2)
                            display_text('!', 'Please pay full dues.')
                            prompt = 'Please enter your UT EID: '
                            time.sleep(3)
                        else: # EID not found
                            prompt = 'Please enter \'FirstName\' \'LastName\': '
                    else: # field is Name
                        if found: # Name found
                            print('\n' * 2)
                            display_text('!', 'Please pay full dues.')
                            prompt = 'Please enter your UT EID: '
                            time.sleep(3)
                        else: # Name not found
                            print('\n' * 2)
                            display_text('!', 'Not present in system.')
                            prompt = 'Please enter your UT EID: '
                            time.sleep(3)
                else: # dues paid
                    print('\n' * 2)
                    display_text('!', 'Welcome to this week\'s UFA meeting!')
                    prompt = 'Please enter your UT EID: '
                    time.sleep(3)
            except EOFError:
                break

if __name__ == "__main__":
    main()
