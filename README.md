# Chaining search installation

# Linux
This guide assumes you have a Python 3 interpreter on your system. If not, install it from your distribution's package management system. In this guide, we install all required Python packages in a virtual environment, so packages do not interfere with the systemwide installation.

First, install `venv` for python3. On Ubuntu, this is done by opening a terminal and typing:
```
$ sudo apt install python3-venv
```

Now, we create a virtual environment in the folder `env`, and activate it:
```
$ python3 -m venv cenv
```
We activate the environement by typing:
```
$ source env/bin/activate
```
`(env)` will appear in front of your terminal

Now, type the following commands in the terminal, one after the other, to install
the required Python packages:
```
pip install -r requirements.txt
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
python3 -m ipykernel install --user --name env
```

Every time you want to run the notebook, make sure the environment is activated (`source env/bin/activate`) and then issue:
```
jupyter notebook
```

A browser window will open. Now, click `chaining_search.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`

If you would like to move out of the virtual environment, after using the notebook, issue the following command:
```
deactivate
```

-----------------------------------------------

# in Windows

## Step 1

First download the code of this project. To do so, click on the 'Clone or download' button on top of the github project page. Click on 'Download ZIP' and save the file to the location of your choice.

Open the Windows explorer, browse to the file location, and unzip the file. 

Then browse the unzipped folder till you find the `Chaining search.ipynb` file. Copy its exact location (full path): you will need it later on.

## Step  2

Download the Python-installer from https://www.python.org/  

Install!

When the installer asks, tell it to add Python to PATH

## Step  3

Now, open a Command prompt window. To do so, press keys Windows+R and then type 'cmd' (and press enter).

In the Command prompt window, upgrade the Python Package Installer (PIP) by typing:
```
python -m pip install -U pip
```

Still in the Command prompt window, create the virtual environment:
```
pip install virtualenv
```
Switch to the folder where you unzipped the project code (you copied that location at the beginning):

```
cd <project location>
```

Now you're ready to activate the virtual environment. Type:
```
virtualenv env
.\env\Scripts\activate.bat
```

As a final step in the Command prompt, install the dependencies:
```
pip install ipykernel
ipython kernel install --user --name=env
pip3 install -r requirements.txt
``` 

## Step  4

Run the Jupyter notebook!
```
jupyter notebook
```

Done!


## Next sessions

You're done with installing. So, in the next sessions, restarting the notebook will be easy!

Open a Command prompt window (press keys Windows+R and then type 'cmd', remember?).
Then go to the project folder (fill in the right path here):

```
cd <project location>
```

Activate the virtual environment:
```
.\env\Scripts\activate.bat
```

Run the Jupyter notebook!
```
jupyter notebook
```

