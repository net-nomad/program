#!/usr/bin/env python3

import subprocess
import os

# Function to load commands for a given program from commands.txt
def load_commands(program_name):
    commands = []
    
    # Check if the commands.txt file exists
    commands_file = 'commands.txt'
    if not os.path.exists(commands_file):
        print(f"Commands file '{commands_file}' not found.")
        return None
    
    # Read the commands from the file
    with open(commands_file, 'r') as file:
        lines = file.readlines()
    
    program_found = False
    for line in lines:
        line = line.strip()
        
        # Start of a new program section
        if line.startswith(f"{program_name}:"):
            program_found = True
            continue
        
        # End of program section
        if program_found and line.startswith("#"):
            break
        
        # If we're in the section for the correct program, add commands
        if program_found and line:
            command_number, command_text = line.split(":", 1)
            commands.append((command_number.strip(), command_text.strip()))
    
    if not commands:
        print(f"No commands found for {program_name}.")
        return None
    
    return commands

# Function to prompt user for input for placeholders like {user_input}
def prompt_for_input(command):
    import re
    # Find all placeholders like {user_input}, {file_path}, etc.
    placeholders = re.findall(r'\{([^}]+)\}', command)
    
    for placeholder in placeholders:
        user_value = input(f"Enter {placeholder}: ").strip()
        command = command.replace(f"{{{placeholder}}}", user_value)
    
    return command

# Function to execute the selected command
def execute_command(command):
    try:
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError as e:
        print(f"Command not found: {e}")

# Main program logic
def main():
    # Step 1: Ask the user for the program name
    program_name = input("Enter the name of the program you want to run: ").strip()
    
    # Step 2: Load the commands for the selected program
    commands = load_commands(program_name)
    if not commands:
        return  # No commands found, exit
    
    # Step 3: Present the available commands to the user
    print("\nAvailable commands:")
    for idx, (number, command) in enumerate(commands, 1):
        print(f"{idx}. {command}")
    
    # Step 4: Ask the user to select a command
    try:
        choice = int(input(f"\nEnter the number of the command you want to run: "))
        if choice < 1 or choice > len(commands):
            print("Invalid choice, please select a valid number.")
            return
    except ValueError:
        print("Invalid input, please enter a valid number.")
        return
    
    selected_command = commands[choice - 1][1]  # Get the actual command
    
    # Step 5: Prompt for any user input if needed (replace placeholders)
    final_command = prompt_for_input(selected_command)
    
    # Step 6: Execute the command
    execute_command(final_command)

if __name__ == "__main__":
    main()
