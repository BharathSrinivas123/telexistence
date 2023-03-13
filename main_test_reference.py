import yaml


def refactor_yaml(current_data_path,new_data_path,replace=False,force = False):

    #Helper function to iterate through nested dictionaries 
    def update_dict(original, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in original:
                update_dict(original[key], value)
            else:
                original[key] = value

    #Helper function to iterate through nested dictionaries and only replace values
    def replace_dict(original, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in original:
                update_dict(original[key], value)
            elif key in original:
                original[key] = value
                
    # Load the current version YAML file
    with open(current_data_path, 'r',encoding="utf8") as read:
        current_data= yaml.safe_load(read)

    # Load the new version YAML file
    with open(new_data_path, 'r',encoding="utf-8") as read:
        new_data = yaml.safe_load(read)

    # Force argument logic
    if force:
        #If key exist, replace value
        for key, value in new_data.copy().items():
            current_data[key] = value
        #Delete key if not in new_version
        for key in current_data.copy():
            if key not in new_data:
                del current_data[key]

    # Replace argument logic
    if replace:
        for key, value in new_data.copy().items():
            if key in current_data:
                if isinstance(value, dict) and isinstance(current_data[key], dict):
                    replace_dict(current_data[key], value)
                else:
                    current_data[key] = value 

    # No arguments provided
    if not replace and not force:
        for key, value in new_data.copy().items():
            if key in current_data:
                if isinstance(value, dict) and isinstance(current_data[key], dict):
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
    with open(current_data_path, 'w',encoding="utf-8") as write:
        yaml.dump(current_data, write)