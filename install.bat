

echo Download and install python

powershell -command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 ; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe', 'python-3.7.2-amd64.exe') }"

python-3.7.2-amd64.exe /quiet

echo Set environment variable permanently
setx PATH "%PATH%;%UserProfile%\AppData\Local\Programs\Python\Python37\Scripts\"
setx PATH "%PATH%;%UserProfile%\AppData\Local\Programs\Python\Python37\"



echo Install the Python package manager

python -m pip install -U pip



echo Create the virtual environment

pip install virtualenv

virtualenv env



echo Activate the virtual environment

call .\env\Scripts\activate.bat


echo Install dependencies

pip install ipykernel
ipython kernel install --user --name=env
pip3 install -r requirements.txt
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
jupyter nbextension enable collapsible_headings/main
python -m ipykernel install --user --name env
pip uninstall -y tornado
pip install tornado==5.1.1



echo Compile documentation
cd doc
make html


echo Done. Type 'run' to start your jupyter notebook

cd ..