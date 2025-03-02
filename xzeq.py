#!/usr/bin/env python3

import subprocess
import os

# Function to load commands for a given program from commands.txt
def load_commands(program_name):
    commands = []
    current_commands = []
    current_category = None
    
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
        
        # Skip empty lines
        if not line:
            continue
        
        # Start of a new program section
        if line.startswith(f"{program_name}:"):
            program_found = True
            continue
        
        # End of program section
        if program_found and line.startswith("#"):
            if current_commands:  # If there are commands in the previous category, save them
                commands.append((current_category, current_commands))
            current_category = line.strip('#').strip()  # Set the current category
            current_commands = []
            continue
        
        # End of program section
        if program_found and line == "":
            break
        
        # If we're in the section for the correct program, add commands
        if program_found:
            # Split the line to get the command number and command text
            try:
                command_number, command_text = line.split(":", 1)
                current_commands.append((command_number.strip(), command_text.strip()))
            except ValueError:
                continue  # Skip lines that don't follow the "number: command" format
    
    # If the program was found, append any remaining commands
    if program_found and current_commands:
        commands.append((current_category, current_commands))
    
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
    
    # Step 3: Present the available commands to the user, grouped by category
    print(f"\nAvailable commands for {program_name}:")
    for category, command_list in commands:
        print(f"\n{category}:")  # Print the category heading
        for number, command in command_list:
            print(f"  {number}. {command}")
    
    # Step 4: Ask the user to select a command
    try:
        choice = int(input(f"\nEnter the number of the command you want to run: "))
        # Find the selected command by number
        selected_command = None
        for category, command_list in commands:
            for num, command in command_list:
                if int(num) == choice:
                    selected_command = command
                    break
            if selected_command:
                break

        if not selected_command:
            print("Invalid choice, please select a valid number.")
            return
    except ValueError:
        print("Invalid input, please enter a valid number.")
        return
    
    # Step 5: Prompt for any user input if needed (replace placeholders)
    final_command = prompt_for_input(selected_command)
    
    # Step 6: Execute the command
    execute_command(final_command)

if __name__ == "__main__":
    main()
