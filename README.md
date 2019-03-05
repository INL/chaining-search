# Chaining search installation

# Linux
Chaining search is a Jupyter notebook, which depends on Python 3 and pip (PyPi). Please install Python 3 and pip via your package management system.
Now, run our install script:
```
./install.sh
```
If permission is denied, issue the following command once:
```
sudo chmod +x install.sh
```
and then run the install script.

Every time you want to run the notebook, run the `run.sh` script:
```
./run.sh
```

A browser window will open. Now, click `Sandbox.ipynb`. The first time you use it, pick the kernel `env` from menu `Kernel > Change kernel > env`.

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
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
jupyter nbextension enable collapsible_headings/main
python -m ipykernel install --user --name env
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

