# scpi_module.py

import socket
import time

# Function to send SCPI commands and receive responses
def send_scpi_command(command, sock):
    try:
        sock.sendall((command + '\n').encode())
        response = sock.recv(4096).decode().strip()
        return response
    except socket.timeout:
        return "Error: timed out"

# Connect to the MTS-5800 device
def connect_to_device(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((ip, port))
    return sock

# Function to execute commands for a given port
def execute_commands_for_port(ip, port, commands):
    if not commands:
        print(f"No commands configured for port {port}")
        return
    
    # Establish connection to the port
    sock = connect_to_device(ip, port)
    print(f"Connected to port {port}")
    
    # Send each command and print the response
    for command in commands:
        response = send_scpi_command(command, sock)
        if response != "Error: timed out":
            print(f"Response: {response}\n")
        
        # Pause after launching the application to allow it to settle down
        if ":SYST:APPL:LAUNch" in command:
            print("Application launched. Waiting 30 seconds for it to settle down...")
            time.sleep(30)
    
    # Close the connection to the port
    sock.close()
    print(f"Connection to port {port} closed\n")

# Common commands that should always execute on port 8002
common_commands = [
    "*REM VISIBLE FULL",
    "*IDN?",
    ":SESS:CRE",
    ":SESS:STAR",
]

# SCPI command sets for different ports
command_sets = {
    8000: [
        "*REM",
        "*IDN?",
        "MOD:FUNC:LIST? BOTH,BASE",
        "MOD:FUNC:PORT? BOTH,BASE,\"BERT\"",
    ],
    8001: [
        "*REM",
        "*IDN?",
        ":SYST:FUNC:PORT? BOTH,BASE,\"BERT\"",
    ],
    8002: common_commands  # This will be dynamically updated for specific tests
}

# Functions for specific testing configurations
def turn_on_laser_and_traffic():
    return [
        ":OUTPUT:OPTIC ON",  # Turn on laser
        ":SOURCE:MAC:ETH:PAYLOAD BERT",  # Set Payload
        ":SOURCE:MAC:ETH:PAYLOAD?",  # Confirm Payload
        ":SOURCE:MAC:TRAFFIC ON",  # Start Traffic
        ":ABOR",
        ":INIT",
    ]

def direct_testing_commands(application):
    if application == "10G":
        return [
            ":SYST:APPL:LAUNch TermEth10GL2Traffic 2",
            ":SYST:APPL:SEL TermEth10GL2Traffic_102",
        ] + turn_on_laser_and_traffic()
    elif application == "100G":
        return [
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
        ] + turn_on_laser_and_traffic()
    else:
        return []

def timed_testing_commands(application):
    if application == "10G":
        return [
            ":SYST:APPL:LAUNch TermEth10GL2Traffic 2",
            ":SYST:APPL:SEL TermEth10GL2Traffic_102",
        ] + turn_on_laser_and_traffic() + [
            ":SENSE:TEST:ENABLE ON",
            ":SENSE:TEST:DURATION 100MIN",
        ]
    elif application == "100G":
        return [
            ":SYST:APPL:LAUNch TermEth100GL2Traffic 1",
            ":SYST:APPL:SEL TermEth100GL2Traffic_101",
        ] + turn_on_laser_and_traffic() + [
            ":SENSE:TEST:ENABLE ON",
            ":SENSE:TEST:DURATION 100MIN",
        ]
    else:
        return []

# Function to exit an application
def exit_application_commands():
    return [":EXIT"]
