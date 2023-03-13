from main_test_reference import refactor_yaml
import yaml


# Test Case 1 - Base Case
def test_base_case():
    current_version = "cur_version.yaml"
    new_version = "new_version.yaml"
    refactor_yaml(current_version, new_version,replace = False, force = False)
    # Load the YAML data into dictionaries and sort them
    with open(current_version, "r", encoding="utf-8") as f:
        current_data = yaml.safe_load(f)
        current_data = {k: v for k, v in sorted(current_data.items())}
    with open(new_version, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)
        new_data = {k: v for k, v in sorted(new_data.items())}

    # Check to see if data not overwritten
    for key, value in current_data.items():
        #Check for sub-dictionaries
        if isinstance(value, dict):
            for key1,val1 in value.items():
                if key in new_data and key1 in new_data[key]:
                    #Check if value is the same
                    assert current_data[key][key1] == current_data[key][key1]
        #Check outside of sub-dictionary
        elif key in new_data and not isinstance(value,dict):
            assert current_data[key] == current_data[key]
    
    # Check to see if key added to current
    for key,value in new_data.items():
        if isinstance(value,dict):
            for key1,val1 in value.items():
                #If key not in current data sub-dictionary, add it
                if key not in current_data and key1 not in current_data[key]:
                    assert current_data[key][key1] == new_data[key][value]
        #If key not in higher level dictionary, add it
        elif key not in current_data:
            assert current_data[key] == new_data[key]

    #Check to see if key deleted in current
    for key,value in current_data.items():
        if isinstance(value,dict):
            for key1,val1 in value.items():
                #If key present in current but not new subdirectory, delete it
                if key not in new_data and key1 not in new_data[key]:
                    assert current_data[key][key1] not in current_data
        #Delete key in higher level subdirectory
        elif key not in new_data:
            assert current_data[key] not in current_data
    

#Test Case 2 - Check to see if values updated only
def test_replace_only():
    current_version = "cur_version.yaml"
    new_version = "new_version.yaml"
    refactor_yaml(current_version, new_version, replace=True)
    # Load the YAML data into dictionaries
    with open(current_version, "r", encoding="utf-8") as f:
        current_data = yaml.safe_load(f)
    with open(new_version, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)

    # Go into the subdirectory recursively
    def compare_dict(dict1, dict2):
        for key, val in dict1.items():
            #Check if subdirectrory exists
            if isinstance(val, dict):
                if key in dict2:
                    compare_dict(val, dict2[key])
            elif key in dict2:
                assert val == dict2[key]

    compare_dict(current_data, new_data)

#Test Case 3
def test_force_only():
    current_version = "cur_version.yaml"
    new_version = "new_version.yaml"
    refactor_yaml(current_version, new_version, force = True)
    # Load the YAML data into dictionaries and sort them
    with open(current_version, "r", encoding="utf-8") as f:
        current_data = yaml.safe_load(f)
        current_data = {k: v for k, v in sorted(current_data.items())}
    with open(new_version, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)
        new_data = {k: v for k, v in sorted(new_data.items())}

    # Compare the dictionaries to see if same
    assert current_data == new_data
        



