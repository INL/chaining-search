# CLARIAH Chaining search
*CLARIAH chaining search* is a Python library and Jupyter web interface to easily combine exploration of linguistic resources published in the CLARIN/CLARIAH infrastructure, such as corpora, lexica and treebanks. *CLARIAH chaining search* is developed by the [Dutch Language Institute (INT)](https://ivdnt.org).

## Background
Linguistic resources, such as lexica and corpora, are usually published as web applications, where users issue a search term, and a number of results are shown in the browser. However, connecting multiple web applications in a single process for research and analysis, is a difficult task.

As a solution, *CLARIAH chaining search* supplies a platform in which search and analysis operations can be freely combined in a single interface. One can build customizable workflows with any number of steps, in which heterogeneous resources (specifically from the CLARIN ecosystem) can be sequentially searched and quantitatively analysed. Any step in such a workflow is to be built programmatically, by means of the Python programming language. Working examples of both simple and complex workflows are provided as a reference for the user.


## Run online on Azure

The notebook can be run online on [Azure](https://notebooks.azure.com/ivdnt/projects/chaining-search).
Create an account, clone the notebook, and you can run it in the cloud!

## Installation on own computer

### Linux/Mac
 * Chaining search is a Jupyter notebook, which depends on Python 3, pip (PyPi) and venv. Please first install Python 3 and pip via your package management system. E.g. for Ubuntu:
 ```
 sudo apt install python3-pip python3-venv
 ```
 * Now, run our install script in a terminal, as a normal user (without `sudo`):
   ```
   ./install.sh
   ```
   If permission is denied, issue the following command once:
   ```
   sudo chmod +x install.sh
   ```
   and then run the install script.

 * Every time you want to run the notebook, run the `run.sh` script as a normal user (without `sudo`):
   ```
   ./run.sh
   ```
   A browser window will open. Now, click `Sandbox.ipynb` or `Examples.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`.


### Windows

Chaining search can be easily installed using our install script. This will install all prerequisites for Chaining search.
 * Open a command prompt (Windows key + R, then issue "cmd").
 * Change to the Chaining search directory (the directory where this README is located):
 ```
 cd CHAINING\SEARCH\DIRECTORY
 ```
 * If you don't have Python yet, install it now:
 ```
 python_install.bat
 ```
 * Close the command prompt after this (required!)

Now we're ready to install our notebook:
 * Open a command prompt (again: Windows key + R, then type "cmd").
 * Change to the Chaining search directory (the directory where this README is located): 
 * Invoke the install script:
 ```
 install.bat
 ```

Every time you would like to run chaining search, invoke our run script:
 * Open a command prompt (Windows key + R, then issue `cmd`).
 * Change to the Chaining search directory (the directory where this README is located):
 ```
 cd CHAINING\SEARCH\DIRECTORY
 ```
 * Invoke the run script:
 ```
 run.bat
 ```
 * A browser window will open. Now, click `Sandbox.ipynb` or `Examples.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`.

## Using Chaining Search
* `Examples.ipynb` gives a number of case studies of accessing and chaining together lexica, corpora and treebanks. Use `Sandbox.ipynb` to start chaining yourself. The `contrib` folder contains a number of more specific case studies.
 * For a tutorial, refer to our [Quickstart](Quickstart.pdf).
 * Reference of our library *chaininglib*, described in the documentation ([online](https://chaining-search.readthedocs.io/en/latest/) or [local (not for Azure cloud instance)](doc/_build/html/index.html)).

## Trouble?
If you encounter any bugs or errors, please let us know via our [GitHub issue tracker](https://github.com/INL/chaining-search/issues) or send an e-mail to servicedesk@ivdnt.org.
