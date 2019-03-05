#This guide assumes you have a Python 3 interpreter and pip (pypi) on your system. If not, install from your distribution's package management system.

# We install all required Python packages in a virtual environment, so packages do not interfere with the systemwide installation.
# Install virtualenv locally, for this user
pip install --user virtualenv
# Create virtual environment
virtualenv -p python3 env
# Activate virtual environment
source env/bin/activate
# All required packages are instlled via pip in the virtual environment
pip install -r requirements.txt
# Re-install old tornado version, to fix bug
pip uninstall -y tornado
pip install tornado==5.1.1.
# Jupyter Notebook extensions are set up
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
# Collapsible headings extension is enabled
jupyter nbextension enable collapsible_headings/main
# Kernel is configured to work with the virtual environment
python3 -m ipykernel install --user --name env