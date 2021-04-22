# Welcome to GRATIS - A GRaph Tool for Information Systems Scientists!

## A tool made for graph creation, analysis and visualization.

### CLI (Command Line Interface)

Gratis also supports a command line interface that can be used in order to generate graphs.

* Help  
  - `python app.py -h` <br><br>
    
* Gratis version
  - `python app.py -v` <br><br>

Available graph models:

| Graph model | Number  |
|:---:|:---:|
| Homogeneous        | 1  |
| Erdős Rényi        | 2  |
| Custom Erdős Rényi | 3  |
| Random Fixed       | 4  |
| Scale Free         | 5  |
| Custom Scale Free  | 6  |

<br>
Graph creation examples:  

* Creating a **Homogeneous** graph with 10 nodes:  
  - `python app.py -g -m 1 -nov 10` <br><br>
    
* Creating an **Erdős Rényi** graph with 10 nodes, 0.5 probability of connection and the number 7 as the seed:  
  - `python app.py -g -m 2 -nov 10 -p 0.5 -s 7`  <br><br>

* Creating a **Custom Erdős Rényi** graph with 10 nodes, 0.5 probability of connection, 12 edges, and the number 7 as the seed:  
  - `python app.py -g -m 3 -nov 10 -p 0.5 -noe 12 -s 7`  <br><br>   

* Creating a **Random Fixed** graph with 10 nodes, 3 graph degree, and the number 7 as the seed:  
  - `python app.py -g -m 4 -nov 10 -gd 3 -s 7`  <br><br>
    
* Creating a **Scale Free** graph using the Preferential Attachment mechanism with 10 nodes, and the number 7 as the seed:  
  - `python app.py -g -m 5 -nov 10 -s 7`  <br><br>
    
* Creating a **Full Scale Free** graph using the Preferential Attachment and the Incremental growth mechanisms
  with 10 nodes, 3 initial nodes, and the number 7 as the seed:  
  - `python app.py -g -m 5 -nov 10 -noin 3 -s 7`  <br><br>

* Creating a **Custom Scale Free** graph using the Preferential Attachment mechanism with 10 nodes, 12 edges, and the number 7 as the seed:  
  - `python app.py -g -m 6 -nov 10 -noe 12 -s 7`  <br><br>

* Creating a **Custom Full Scale Free** graph using the Preferential Attachment and the Incremental growth mechanisms
  with 10 nodes, 3 initial nodes, 2 initial connections per node, and the number 7 as the seed:  
  - `python app.py -g -m 6 -nov 10 -noin 3 -icpn 2 -s 7`

The default graph representation is as an Adjacency Matrix. This can be changed by using the `-gr` flag
which stands for `graph representation` e.g.:
`python app.py -g -m 3 -nov 10 -p 0.5 -noe 12 -s 7 -gr 2`

Available graph representations:

| Graph representation | Number  |
|:---:|:---:|
| Adjacency Matrix | 1  |
| Adjacency List   | 2  |

Note: The `python app.py` should be replaced by the corresponding gratis executable/binary file e.g.:
`./gratis -g -m 3 -nov 10 -p 0.5 -noe 12 -s 7`

### Development setup
1. In order to run this project you need:
   * Python3 or above
    
2. To install all needed packages and run the project:  
  2.1. Debian and Ubuntu based systems:  
   1. Clone or download zip and extract the project.
   2. `cd Gratis/`
   3. `sudo ./install-dependencies.sh`
   4. `python3 App.py`
   
   2.2. Windows systems:
    1. Download and install python3 and above from [https://www.python.org/](https://www.python.org/) (python3.6 is the safe choice)  
    2. Download the appropriate python-igraph module for your windows system with the appropriate python version you installed. (e.g. if you have python3.6 and windows 64-bit you will download the file `python_igraph‑0.7.1.post6‑cp36‑cp36m‑win_amd64.whl` from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph).  
    3. Install the python-igraph module with `python -m pip install <module_name.whl>`  
    4. Clone or download zip and extract the project.  
    5. `cd Gratis\`  
    6. `python -m pip install -r requirements.txt`  
    7. `python App.py`  

3. To install and run through pipenv:
   1. Download and install python3 or above.
   2. `python3.x -m pip install pipenv` (Note: .x is a wildcard)
   3. `cd Gratis`
   4. `pipenv install`
   5. `pipenv shell`
   6. `python App.py`

* Note: For a stable version of the tool work with the master branch.
