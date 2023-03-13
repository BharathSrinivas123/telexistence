import argparse
import yaml
import logging

# Required paramters within terminal - File names 
parser = argparse.ArgumentParser()
parser.add_argument('current_data_path', help='Name of Current File')
parser.add_argument('new_data_path', help='Name of New File')

#Optional parameters within terminal
parser.add_argument('--replace', action='store_true', help='replace only existing fields only')
parser.add_argument('--force', action='store_true', help='Add/remove values and update')
parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set the logging level')
args = parser.parse_args()

#set up logging
if args.log:
    log_level = args.log
else:
    log_level = 'WARNING'
logging.basicConfig(level=log_level)

def refactor_yaml(current_data_path,new_data_path,replace=False,force = False):

    #Helper function to iterate through sub dictionaries 
    def update_dict(original, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in original:
                update_dict(original[key], value)
            else:
                original[key] = value

    #Helper function to iterate through sub dictionaries and only replace specific values
    def replace_dict(original, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in original:
                update_dict(original[key], value)
            elif key in original:
                original[key] = value

    # Load the current version YAML file
    with open(args.current_data_path, 'r',encoding="utf8") as read:
        current_data= yaml.safe_load(read)

    # Load the new version YAML file
    with open(args.new_data_path, 'r',encoding="utf-8") as read:
        new_data = yaml.safe_load(read)

    # Force argument logic
    if args.force:
        logging.info("Using force option to add/remove values and update")
        #If key exist, replace value
        for key, value in new_data.copy().items():
            current_data[key] = value
        #Delete key if not in new_version
        for key in current_data.copy():
            if key not in new_data:
                del current_data[key]

    # Replace argument logic
    if args.replace:
        logging.info("Using replace option to replace existing fields")
        for key, value in new_data.copy().items():
            if key in current_data:
                #Check if subdictionary
                if isinstance(value, dict) and isinstance(current_data[key], dict):
                    #Helper function recursion - replace specific value
                    replace_dict(current_data[key], value)
                else:
                    current_data[key] = value 

    # No arguments provided
    if not args.replace and not args.force:
        logging.info("Using base case option to update existing fields and add/delete new fields")
        for key, value in new_data.copy().items():
            if key in current_data:
                #Check if subdictionary
                if isinstance(value, dict) and isinstance(current_data[key], dict):
                    #Helper function recursion - replace all values
                    update_dict(current_data[key], value)
                else:
                    # keep value from current_data
                    pass
            #If key does not exist in current, add it
            elif key not in current_data:
                current_data[key] = value

        #Delete key if not in new_version
        for key in current_data.copy():
            if key not in new_data:
                del current_data[key]
            elif isinstance(current_data[key], dict) and isinstance(new_data[key], dict):
                update_dict(current_data[key], new_data[key])



    # Write the updated current version YAML file
    with open(args.current_data_path, 'w',encoding="utf-8") as write:
        yaml.dump(current_data, write)


refactor_yaml(args.current_data_path,args.new_data_path,args.replace,args.force)



