# Chaining search installation

# Linux
 * Chaining search is a Jupyter notebook, which depends on Python 3 and pip (PyPi). Please first install Python 3 and pip via your package management system.
 * Now, run our install script in a terminal:
   ```
   ./install.sh
   ```
   If permission is denied, issue the following command once:
   ```
   sudo chmod +x install.sh
   ```
   and then run the install script.

 * Every time you want to run the notebook, run the `run.sh` script:
   ```
   ./run.sh
   ```
   A browser window will open. Now, click `Sandbox.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`.

-----------------------------------------------

# Windows

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
 * A browser window will open. Now, click `Sandbox.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`.
