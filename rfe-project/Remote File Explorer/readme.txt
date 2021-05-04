To setup and install the required modules,
open the pycharm terminal and run the following
commands one by one:

*
python -m venv venv
venv\Scripts\activate
move requirements.txt venv
cd venv
pip install -r requirements.txt
*

if there is already a "venv" folder,
move the file "requirements.txt" into it and run:

*
cd venv
pip install -r requirements.txt
*

after running the commands and the installation was
successful, set up python 3.9 as the project's interpreter
and run the file "main_window.py"