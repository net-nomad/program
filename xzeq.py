import subprocess

def read_commands_from_file(file_path):
    applications = {}
    current_app = None
    current_category = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.endswith(':'):
                # New application or category
                key = line[:-1].strip()
                if key not in applications:
                    # This is a new application
                    current_app = key
                    applications[current_app] = {"description": "", "categories": {}}
                elif current_app:
                    # This is a category for the current application
                    current_category = key
                    applications[current_app]["categories"][current_category] = {}
            elif line.startswith('description:'):
                # Description for the current application
                description = line.split(":", 1)[1].strip()
                if current_app:
                    applications[current_app]["description"] = description
            else:
                # Command line
                if current_app and current_category:
                    command_number, command = line.split(":", 1)
                    command_number = int(command_number.strip())
                    command = command.strip().strip('"')
                    applications[current_app]["categories"][current_category][command_number] = {
                        "command": command,
                        "requires_input": any(placeholder in command for placeholder in ["{path_to_file}", "{ip_address}", "{user_input}"])  # Check for user input placeholders
                    }

    return applications

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def list_commands(app_name, applications):
    if app_name not in applications:
        print(f"Application '{app_name}' not found.")
        return
    
    app = applications[app_name]
    print(f"{app_name.capitalize()} - {app['description']}\n")
    
    # Display commands categorized by functionality
    for category, commands in app["categories"].items():
        print(f"{category}:")
        for num, cmd_info in commands.items():
            command = cmd_info['command']
            print(f"  {num}. {command}")  # Print the command as is
        print()  # Space between categories

def get_user_input(command_info):
    command = command_info['command']
    # Identify placeholders in the command to ask the user for input
    placeholders = ["{path_to_file}", "{ip_address}", "{user_input}"]
    
    for placeholder in placeholders:
        if placeholder in command:
            user_input = input(f"Enter the value for {placeholder} (e.g., file path, IP address): ")
            # Replace the placeholder in the command with the user input
            command = command.replace(placeholder, user_input)

    return command

def main():
    applications = read_commands_from_file("commands.txt")
    
    app_name = input("Enter the application name (e.g., notepad, server): ").lower()
    
    list_commands(app_name, applications)
    
    try:
        command_number = int(input(f"Choose a command number for {app_name}: "))
        found_command = False
        
        # Find the command in the selected application and execute it
        for category, commands in applications[app_name]["categories"].items():
            if command_number in commands:
                found_command = True
                command_info = commands[command_number]
                command = get_user_input(command_info)
                print(f"Executing command: {command}")
                execute_command(command)
                break
        
        if not found_command:
            print("Invalid command number.")
    
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
