#!/usr/bin/env python3
import subprocess

# Function to read commands from the 'commands.txt' file
def load_commands(file_path):
    commands = {}
    current_app = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                current_app = line[:-1]
                commands[current_app] = []
            elif line and current_app:
                commands[current_app].append(line)
    return commands

# Function to execute the user command
def execute_command(command):
    try:
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError as e:
        print(f"Command not found: {e}")

# Function to prompt the user for inputs
def get_user_input(placeholder):
    return input(f"Enter the value for {placeholder}: ")

# Main logic
def main():
    # Load the commands from 'commands.txt'
    commands = load_commands('commands.txt')

    print("Enter the application name (e.g., notepad, nmap):")
    app_name = input().strip().lower()

    if app_name not in commands:
        print(f"Application '{app_name}' not found.")
        return

    print(f"\nAvailable commands for {app_name}:")
    # Display commands with descriptions
    for idx, command in enumerate(commands[app_name], 1):
        print(f"{idx}. {command}")

    # Ask user for a command number to run
    try:
        command_number = int(input("\nChoose a command number to execute: "))
        if command_number < 1 or command_number > len(commands[app_name]):
            print("Invalid command number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Get the chosen command template
    chosen_command = commands[app_name][command_number - 1]
    
    # Find all placeholders (e.g., {ip_address}, {port_range}, etc.)
    placeholders = [part for part in chosen_command.split() if part.startswith("{") and part.endswith("}")]

    # Collect input for each placeholder
    for placeholder in placeholders:
        user_input = get_user_input(placeholder)
        chosen_command = chosen_command.replace(placeholder, user_input)

    # Execute the command
    execute_command(chosen_command)

if __name__ == "__main__":
    main()
