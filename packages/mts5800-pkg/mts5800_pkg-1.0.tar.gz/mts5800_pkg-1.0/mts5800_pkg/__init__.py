# main.py 
# without any SCPI command 


from scpi_module import (
    execute_commands_for_port,
    command_sets,
    direct_testing_commands,
    timed_testing_commands,
    exit_application_commands
)

# IP configuration
device_ip = "10.91.11.51"

# Run the port 8002 testing options
def handle_port_8002_testing():
    while True:
        print("Select the testing option for port 8002:")
        print("1. Direct Testing")
        print("2. Timed Testing")
        user_choice = input("Enter the number of the option (or 'exit' to quit): ")

        if user_choice == "1":
            handle_direct_testing()

        elif user_choice == "2":
            handle_timed_testing()

        elif user_choice.lower() == "exit":
            print("Exiting program.")
            break

        else:
            print("Invalid selection. Please try again.")

def handle_direct_testing():
    print("Select the application for Direct Testing on port 8002:")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        specific_commands = direct_testing_commands("10G")
    elif app_choice == "2":
        specific_commands = direct_testing_commands("100G")
    elif app_choice.lower() == "exit":
        print("Exiting Direct Testing.")
        return
    else:
        print("Invalid application selection. Exiting Direct Testing.")
        return

    setup_commands = [":SENSE:TEST:ENABLE OFF"]
    commands = command_sets[8002] + specific_commands + setup_commands
    execute_commands_for_port(device_ip, 8002, commands)

def handle_timed_testing():
    print("Select the application for Timed Testing on port 8002:")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    app_choice = input("Enter the number of the application (or 'exit' to quit): ")

    if app_choice == "1":
        specific_commands = timed_testing_commands("10G")
    elif app_choice == "2":
        specific_commands = timed_testing_commands("100G")
    elif app_choice.lower() == "exit":
        print("Exiting Timed Testing.")
        return
    else:
        print("Invalid application selection. Exiting Timed Testing.")
        return

    commands = command_sets[8002] + specific_commands
    execute_commands_for_port(device_ip, 8002, commands)

# Execute commands for ports 8000 and 8001
execute_commands_for_port(device_ip, 8000, command_sets[8000])
execute_commands_for_port(device_ip, 8001, command_sets[8001])

# Run the port 8002 testing options
handle_port_8002_testing()

# Ask the user if they want to exit an application
def exit_application():
    print("Which application would you like to exit?")
    print("1. TermEth10GL2Traffic")
    print("2. TermEth100GL2Traffic")
    exit_choice = input("Enter the number of the application to exit (or 'exit' to quit): ")

    if exit_choice == "1" or exit_choice == "2":
        commands = exit_application_commands()
        execute_commands_for_port(device_ip, 8002, commands)
    elif exit_choice.lower() == "exit":
        print("Exiting program.")
    else:
        print("Invalid selection. Exiting program.")

exit_application()
