# Welcome to GRATIS - A GRaph Tool for Information Systems Scientists!

## A tool made for graph creation, analysis and visualization.


1. In order to run this project you need:
 * Python3 or above

2. To install all needed packages and run the project:
 - Debian and Ubuntu based systems:  
  1.Clone or download zip and extract the project.  
  2.`cd Gratis/`  
  3.`sudo ./install-dependencies.sh`  
  4.`python3 App.py`
 - Windows systems:  
  1.Download and install python3 and above from [https://www.python.org/](https://www.python.org/) (python3.6 is the safe choice)  
  2.Download the appropriate python-igraph module for your windows system with the appropriate python version you installed. (e.g. if you have python3.6 and windows 64-bit you will download the file `python_igraph‑0.7.1.post6‑cp36‑cp36m‑win_amd64.whl` from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph).  
  3.Install the python-igraph module with `python -m pip install <module_name.whl>`  
  4.Clone or download zip and extract the project.  
  5.`cd Gratis\`  
  6.`python -m pip install -r requirements.txt`  
  7.`python App.py`

3. To install and run through pipenv:
   1. Download and install python3 or above.
   2. `python3.x -m pip install pipenv`
   3. `cd Gratis`
   4. `pipenv install`
   5. `pipenv shell`
   6. `python App.py`
