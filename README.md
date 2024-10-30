# Usage

## From github directory 

* Create a directory 
```mkdir pvault```
* Switch to directory
```cd pvault```
* Clone directory
```git clone https://github.com/RenniOG/png_bank```
* Create a python virtual environment
```python -m venv venv```
* Activate the virtual environment (required file may vary based on shell)
```source vemv/bin/activate```
* Install requirements
```pip install -r png_bank/requirements.txt```
* Run program
```python3 png_bank/png_bank/cli.py```

Furthermore, you can make this a command by adding the following command to your bashrc or equivalent file:
```alias command_name='source /path/to/directory/venv/bin/activate; python3 /path/to/directory/png_bank/png_bank/cli.py'```
for example:
```simpl```