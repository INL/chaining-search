# Chaining search installation

# in Linux

Create virtual environment
In the virtual environment, local copies of all Python dependencies will be installed. 
Install venv for python3, eg. on Ubuntu:
```
$ sudo apt install python3-venv
```

Create and activate virtual environment:
```
$ python3 -m venv cs_env
$ source cs_env/bin/activate
```

Install dependencies inside virtual environment
```
pip install -r requirements.txt
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
python3 -m ipykernel install --user --name
```

Run Jupyter notebook
```
jupyter notebook
```

-----------------------------------------------

# in Windows

Download the Python-installer from https://www.python.org/
Install!
When the installer asks, tell it to add Python to PATH

Upgrade the Python Package Installer (PIP)
```
python -m pip install -U pip
```

Create and activate virtual environment:
```
pip install virtualenv
cd <project location>
virtualenv env
.\env\Scripts\activate.bat
```

Install dependencies inside virtual environment
```
pip install ipykernel
ipython kernel install --user --name=cs_env
pip3 install -r requirements.txt
```

Run Jupyter notebook
```
jupyter notebook
```
