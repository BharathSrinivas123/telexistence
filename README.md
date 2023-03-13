# Software QA Test Engineer Assignment 
## <b>Libraries and test files used</b>
The following libraries were used in order to develop and compile the main and test code.
- yaml
- argparse
- logging
- pytest
<br> <br>With regards to the code development,the `cur_version.yaml` and `new_version.yaml` were created and used for testing purposes. Note that the `motor_config.yaml` file was used for testing after the development process was completed to ensure the code works as expected.
## <b>Files and Design</b>
### <u>main.py</u>
This file contains the main code for processing the two YAML files. The code has 3 cases, namely the base, replace and force case. <br><br>
Base Case <br>
This code block follows the following parameters provided down below
- If a field within the new is not present in `cur_version`, it should be
  added to `cur_version` with its value set to the value from `new_version`.
- If a field of `new_version` is present in `cur_version`, it should keep the
  value from `cur_version`.
- If a field of `cur_version` is not present in `new_version`, it should be
  removed from `cur_version`. <br>

Replace Option<br>
This block compares the values of the `cur_version` file with the `new_version` and replaces the values of the key if it exists. <br>

Force Option<br>
Force the update of `cur_version` by replacing the values of the currently existing fields with the values from `new_version` and adding or removing the fields, similar to the base case

### <u>main_test_reference.py</u>
This file is exactly the same as the main.py source code, except that it does not include arg parameters. This replication is done such that it is easier to point the `test_main.py` file to this one for testing purposes, avoiding integration of args to the `test_main.py` file and thus making it overly complicated.

### <u>test_main.py</u>
This file is the testing file that checks the validity of the `main.py` code, ensuring that it is running as expected.
The three test cases provided are as follows.
- test_base_Case - This test case checks that the following parameters are met:
  - If a field of `new_version` is not present in `cur_version`, it should be
  added to `cur_version` with its value set to the value from `new_version`.
  - If a field of `new_version` is present in `cur_version`, it should keep the
  value from `cur_version`.
  - If a field of `cur_version` is not present in `new_version`, it should be
  removed from `cur_version`.
- test_replace_only - This test case checks to see if the fields in `cur_version` are updated and matched to the values of `new_version` and no other changes are done
- test_force_only - This test case checks to see if values in `cur_version` are added/deleted or changed, based on the `new_version` file as well as updating the values of the keys in `cur_version`.

## <b>Execution of main.py file</b>
The program is designed such that it run via the terminal. There are two optional arguments --replace and --force. If neither are provided, the base case will run. The following commands shown below is the syntax that should be used.

```
python main.py <current file> <new file> --replace --force --log <Parameter>
```
For the logging parameter, the following options can be used
- DEBUG
- INFO
- WARNING
- ERROR

Lets say for example you want to run the force paramter, with INFO for the logs
```
python main.py curr_version.yaml new_version.yaml --force log-- INFO
```
where the `cur_version.yaml` and `new_version.yaml` files are the files that were used for testing and is stored in the current directory. Change these file names accordingly to the files you have stored and want to execute <br>

## <b>Execution of test_main.py file</b>
In order to execute the test file, simply follow the following command in the terminal
```
pytest test_main.py
```
This will execute every test within the file. If you want to change the specific files to be tested, change the following values within this file to the name of your new files.
- current_version = <Current_File.yaml>
- new_version = <New_File.yaml>

To specify running a specific test case, run the following command in the terminal
```
pytest test_main.py::<name_of_test>
```
Here is the result of a successfull test run 
![image](https://user-images.githubusercontent.com/35479198/224661465-bc06f5c2-96c1-4553-8c55-cc27a4709144.png)

Note - Testing has been done with motor-config.yaml and all 3 test have passed
