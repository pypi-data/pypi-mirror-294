import os
import yaml
import json
from configparser import ConfigParser
import subprocess
from dotenv import set_key, load_dotenv

class ConfigParserModule:
    
    def __init__(self):
        print("======================================================")
        print("================ Config Parser Module ================")
        print("======================================================")
        print()
        self.config_dict = {}

    

    def flatten_dict(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def read_yaml(self, file_path):
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        self.config_dict = self.flatten_dict(config)
        return self.config_dict

    def read_cfg(self, file_path):
        """Reads a .cfg or .conf file and returns a flat dictionary."""
        parser = ConfigParser(interpolation=None)
        parser.read(file_path)
        config = {section: dict(parser.items(section)) for section in parser.sections()}
        self.config_dict = self.flatten_dict(config)
        return self.config_dict

    def write_env(self, file_path):
        """Writes configurations to a .env file."""
        print("Loading the configurations in .env file...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        load_dotenv(file_path)  # Load existing .env if it exists
        for key, value in self.config_dict.items():
            set_key(file_path, key, str(value))
        print("Done Successfully!")

        # with open(file_path, 'w') as f:
        #     for key, value in self.config_dict.items():
        #         f.write(f'{key}={value}\n')

    def write_json(self, file_path):
        """Writes configurations to a .json file."""
        print("Loading the configurations in .json file...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(self.config_dict, f, indent=4)
        print("Done Sucessfully!")

    def set_os_env(self):
        """Sets configurations in the OS environment."""
        for key, value in self.config_dict.items():
            os.environ[key] = str(value)

            # os.system(f'setx {key} "{value}"') -- for windows
            print("Setting the Configurations as Environment Variables in OS...")
            """For ubuntu - Setting environment variable in the current shell using export command"""
            command = f'export {key}="{value}"'
            subprocess.run(command, shell=True, executable='/bin/bash')
            print("Done Successfully!")

# Sample usage
if __name__ == "__main__":
    print()
    fileformat_option = int(input("Please Choose the file format you want to Parse. \n1. YAML\n2. CFG\n3. CONF\n"))
    filepath = input("Please Enter the full path of the file: ")
    print()
    load_option = int(input("How would you like to load your configuration?. \n1. Load in a .env file.\n2. Load in a .json file.\n3. Set all the configurations as environment variables.\n"))
    match fileformat_option:
        case 1:
            file_format = "yaml"
        case 2:
            file_format = "cfg"
        case 3:
            file_format = "conf"
        case default:
            raise Exception("Invalid File Format. Please enter [1,2,3] for \n1. YAML\n 2.CFG\n 3. CONF")
    match load_option:
        case 1:
            load_type = "env"
        case 2:
            load_type = "json"
        case 3:
            load_type = "env_variable"
        case default:
            raise Exception("Invalid Loading Option. Please enter [1,2,3] for \n1. Load in a .env file\n2. Load in a .json file\n3. Set all the configurations as environment variables.")

    print("Config File Format Chosen: ", file_format)
    print("Loading out as: ", load_type)
    print()
    config_parser = ConfigParserModule()
    if file_format == "yaml":
        configuration_dict = config_parser.read_yaml(file_path=filepath)
    elif file_format == "cfg" or file_format == "conf":
        configuration_dict = config_parser.read_cfg(file_path=filepath)
    else:
        raise Exception("Some issue with the file format entered. Please Try again")
    # print(configuration_dict)

    if load_type == "env":
        print("Loading the configurations in .env file...")
        config_parser.write_env(r"./loadedfiles/.env")
        print("Configurations loaded to .env file successfully!")
    elif load_type== "json":
        print("Loading the configurations in .json file...")
        config_parser.write_json(r"./loadedfiles/config-parsed.json")
        print("Configurations loaded to 'config-parsed.json' file successfully!")
    elif load_type == "env_variable":
        print("Setting the Configurations as Environment Variables in OS...")
        config_parser.set_os_env()
        print("Done Successfully!")

    
