# SuCCESs Toolbox for post-processing and plotting model results

The [SuCCESs model](https://github.com/SuCCESsIAM) is a demand-driven, global scenario model that optimizes land use, material and energy flows, and assesses the climate impacts by these systems. It is implemented in GAMS. The model outputs (results) are provided in GAMS Data Exchange files (.gdx). These are instructions to make the toolbox work on your computer and analyse SuCCESs outputs in python. Follow the set up section closely to make the toolbox work as whole on your computer or simply browse the python files and cherry-pick the methods you find useful into your own code either directly or as the base of your own functions. Thank you for using! Also, we always welcome feedback!

Toolbox Authors: Tuukka Mattlar & Nadine-Cyra Freistetter (2024) 

Model Authors: Tommi Ekholm, Nadine-Cyra Freistetter, Aapo Rautiainen, Laura Thölix (2021-2024)

## General instructions

To get a smooth start, please follow the instructions listed in this file which is structured as:
- Toolbox structure
    - Describes how the toolbox is structured
- Requirements for using the toolbox
    - Describes what installations are required for starting with the toolbox
- Setup
    - Instructs the alternatives how to setup the toolbox development environment on your computer
- Running the code
    - Explains how to approach the toolbox code if you want to customize it to your own use
- Appendix
    - Includes e.g. some troubleshooting advice

. We encourage the use of python virtual environment (venv) and Visual Studio Code (vscode) for smooth use. In installation, the python pa `gdxpds` python library may require a few extra steps


## Toolbox structure
The SuCCESs Toolbox comes as a folder with python files (.py) and a jupyter notebook file (.ipynb). The folder is of the following structure:
* Root folder:
    * This `README.md` file with instructions
    * Example SuCCESs results `example.gdx` file
    * Requirements files `requirements.txt` and `success_python_env.yml` for setting up your python environment (instructions below)
    * `toolbox` folder containing the source code for plottinf functions. (Note that all functions exported from this module need to be imported in the `__init__.py` file)
    * `tutorial.ipynb` tutorial to the basic plotting functions included in the toolbox
    * Git files for managing the repository



## Requirements for using the Toolbox
1. To run SuCCESs, you need:
    * GAMS installed on your computer AND
    * A valid license for GAMS on your computer
2. Python installed on your computer (developed with version 3.12) and added to PATH (instructions e.g.: https://realpython.com/add-python-to-path/)
3. Jupyter notebook capability installed if you plan to explore the provided examples
4. Python packages, which include e.g. `gdxpds`, `ipykernel` and `seaborn`
5. Installing `gdxpds` may require the installation of [C++ Build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). [This](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst) example should help with the installation. If not, please search online for instructions with the error message(s) received in log when trying to  install the package. Note, our understanding is that the `gdxpds` can only be installed via the pip channel.


### Python versions
The toolbox is developed using Python versions 3.11 and 3.12. Under our understanding the toolbox should run smoothly at least for python versions 3.7-3.12. In all cases, please separately import necessary libraries (as instructed below), if the default method does not work. Once you have the environment up and running there should be no obvious issues with the version control so no worries if it takes a bit time to get create a running environment at first. For `gdxpds` related issues, please refer to the trouble shooting instructions below.


## Setup

We will go through the options of setting up the toolbox in:
* Visual Studio Code (VS Code) and creating a virtual environment (suggested)
* Anaconda Navigator using the environment manager (please make sure you have the required Anaconda license or that your institute/organization is eligible to use Anaconda)
* Manual set-up in the command prompt

The smoothest implementation for us seemed to be setting up the environment in VS Code.



### Alternative 1 - Creating the environment in VS Code
1. Clone the repository to your computer through <code>git clone https://github.com/SuCCESsIAM/SuCCESsIAM-toolbox.git </code>
2. Open the git repository folder in VS code and open the `.ipynb` file you wish to use
3. Press `Shift+Ctrl+p` and search for `Python: Create Environment`
4. Select `create a Venv`
5. Select the correct version of Python installation on your computer that you wish to use
6. Select the `requirements.txt` dependencies file and wait for the magic to happen
    * If you face problems with the package versions, you can also just create an environment without the `requirements.txt` and install the dependencies separately. This can be done by right-clicking the just created `.venv` folder in VS code and selecting `Open in Integrated Terminal`, where you can separately install the required dependencies with e.g. pip. For example `pip install numpy`.*
7. In the git root folder, you should now have a local `.venv` folder forming
    * *If the upper right corner of VS code does not state `.venv Python 3.[your version]`, press `Shift+Ctrl+p` and search for `Python: Select Interpreter`. Either search or directly set it to the recently created `.venv` in your current folder.*
    * *The `.venv` file is **automatically ignored** by git in `.gitignore`. Please keep it that way since the venv folders may face conflicts accross platforms.*




### Alternative 2 - Creating the environment in Anaconda3
The environment file (`success_python_env.yml`) includes all dependencies needed to run the scripts.

#### Install through Anaconda prompt:
Type:

* `cd C:\path\to\yml\file\`
* `conda env create -f success_python_env.yml`
* `python -m ipykernel install --user --name=success_env`


To remove the environment:
`conda remove --name success_env --all`

#### Install through Anaconda Navigator GUI:
1. Start the Anaconda Navigator GUI
2. Click "Environments" tab
3. Click "Import"
4. Navigate to the folder that contains the `success_python_env.yml` and select it
5. Give the environment a name
6. Click OK and wait for the magic to happen

From here, use the `.ipynb` files as usual, e.g. via jupyter lab or VS Code.



### Alternative 3 - Creating the environment in the command prompt
You probably know what you are doing if you do it this way, but in short:
1. Make sure you have pip installed
2. Create a venv where you like
3. Activate the environment from where you want to run the code
4. Install dependencies from `requirements.txt` or `success_python_env.yml`, or however you want, e.g. by running `pip install -r requirements.txt`
6. Run `jupyter notebook` in your active venv and locate to the localhost address provided, or just use VS code
7. Navigate to the code folder using the browser-based jupyter view and open the file you wish, or again, just use VS code





## Running the code
Now that hopefully the environment is up and running, you can start exploring the library and examples!

### Toolbox library
All toolbox methods are found in the `toolbox/` folder. The `__init__.py` file is the main file of the toolbox library which collects all necessary functions for the import of the module. 
All relevant mehtods of the toolbox can be imported at once by running `import toolbox` at the beginning of your script.

Note: The toolbox folder must be in the same location as your script. If your script is in a different location, refer to the Appendix below.



## Appendix


#### GDX-Pandas troubleshooting 
Assuming you have installed GAMS, python 3.7+, and the python environment correctly, there might be a few issues relating to the `gdxpds` package if for example the iPython Kernel crashes when you try to import gdxpds (a classic).
* First of all: Always import gdxpds _before_ pandas.
* Check if you installed the `gdxpds` package at all. It can only be installed via the pip channel: `pip install gdxpds`. Futher information on its [github page](https://github.com/NREL/gdx-pandas).
* Along with the `gdxpds` package comes the `gdxcc` library. You need to have correct C/C++ drivers installed and activated on your computer when installing it, otherwise you  get an error message. If so, please proceed by the error message, which likely suggests you to install certain C/C++ drivers.
* Check if GAMS path is added to the system environment variables in Windows:
    1. Find GAMS License path:
    Open GAMS --> Help --> GAMS Licensing --> Copy the License path
    2. Add License path to the Windows system variables:
    Open "Start" --> type "environment variables" --> click on "Edit the system environment variables"
    System Properties dialog field opens.
    Choose tab "Advanced" --> click on "Environment Variables..."
    Environment Variables dialog field opens.
    Click "New..." --> type:
    - Variable name: GAMSDIR  (example name)
    - Variable value: Paste the GAMS license path
    3. Test:
    Restart computer
    Try importing gdxpds to your script.
    If Kernel keeps crashing, try copying the GAMS license gamslice.txt file into the standard GAMS folder (e.g. C:\GAMS\39)
    and/or add the standard GAMS folder to the environment variables.





