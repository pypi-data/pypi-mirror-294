![USGS](USGS_ID_black.png)

Groundwater Nitrate Decision Support Tool (GW-NDST)
====================================================

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

Latest static release: ![Static Badge](https://img.shields.io/badge/DOI-10.5066%2FP13ETB4Q-blue)


Groundwater Nitrate Decision Support Tool (GW-NDST) for the State of Wisconsin

Description
-------------------
You are currently viewing the main development branch. For the latest release, please 
select the most recent tagged version (highest numberical value) in the upper-left drop 
down box above.

A Groundwater Nitrate Decision Support Tool (GW-NDST) for wells in Wisconsin was developed
to assist resource managers with assessing how legacy and possible future nitrate leaching
rates, combined with groundwater lag times and potential denitrification, influence nitrate
concentrations in wells (Juckem et al. 2024). The GW-NDST software is housed in this GIT
repository, and relies on several user actions for installation and setup of the software, as
described below. First, the software needs to be cloned or downloaded from this
repository. Then GIS data and parameter ensemble files need to be downloaded from USGS data
releases and unzipped into specific directories within the software file structure. Finally,
a specific python environment must be created for running the software. The software
relies upon several support models and calibration/uncertainty parameters to function. Cloning
(or downloading) this repository and downloading the contents of the two data releases provides
the information required to run the support models and tune the tool for application in
Wisconsin. Please follow the instructions below precisely.

Comments, bug-reports, and contributions to the code are welcome. Please reach out to the 
authors with any comments, bug reports, or to discuss possible contributions in advance of 
any merge request via GIT.  lschachter@usgs.gov, pfjuckem@usgs.gov, ncorson-dosch@usgs.gov, 
ctgreen@usgs.gov

How to use the tool
-------------------

1. Download this repository ("repo") or clone it using [git](https://git-scm.com/). 

	#### a.  Download
     To download, click the blue "Code" drop-down icon in the upper-right of the repo homepage (above), and click on the desired download format (zip for Windows). Un-zip the downloaded file in the directory (folder) you want to store the repo on your computer. Continue to step 2. 
	
	#### b.  Clone
    To clone, [download](https://git-scm.com/downloads) and install git, open a `git bash` window (if on Windows, or terminal on Linux or macOS) in the location you want to store the repo on your computer, and enter the following command:

         $ git clone https://code.usgs.gov/water/NDST/no3gwt.git
    
    After git has finished cloning the software to your computer, navigate the `git bash`
	prompt to the top-level `no3gwt/` directory (not the `no3gwt/no3gwt/` directory) by 
	typing the command:
	
		$ cd no3gwt 

    An advantage of cloning the repo using [git](https://git-scm.com/) 
    (instead of downloading it) is that future software updates can be easily 
    retrieved using the command:
    
        $ git pull

    Specific versions or releases of the software can be retrieved using
    [git checkout](https://git-scm.com/docs/git-checkout).
	
    You're now done with git and the `git bash` window (or terminal on Linux or macOS) for
    this session. The window or terminal can be closed by typing the command:
    	
    	$ exit 

2. Download external datasets from ScienceBase. The GW-NDST relies on several
   static, external data sets that are too large to be included with the repo 
   (acquired in step 1) and need to be downloaded separately. These data sets
   are: 

    #### a. [GIS data](https://doi.org/10.5066/P9Q1X606) 
    There are three zip files included in this archive (WI_County.zip, WT-ML.zip, and WI_Buff1km.zip). These three zip files should be downloaded and unzipped in the `data_in/gis/` directory of the repo. Users may need to create the `WI_County`, `WT-ML`, and `WI_buff1km` sub-directories if not created automatically during the un-zip process, and ensure the contents of the zipped files are stored in the sub-directories.

    #### b. [Parameter ensembles](https://doi.org/10.5066/P9QHPVU3) 
    There is one zip file included in this archive (ies_parameter_ensembles.zip). This file should be downloaded and the contents unzipped into the `pest/` directory of the repo. Users may need to create the 
    `ies_parameter_ensembles` sub-directory if it was not created automatically during the un-zip
    process, and ensure the contents of the zipped file are stored in this sub-directory.


3. Download and install the 64-bit [Anaconda python distribution](https://www.anaconda.com/download) 
or the smaller [Miniconda python distribution](https://docs.anaconda.com/miniconda/). 


4. Create a conda python environment using the `environment.yml` file included 
in the repo. To do this, open an `Anaconda Prompt` on Windows (terminal on Linux or 
macOS), and navigate to the repo (that is, the location of the `environment.yml` 
file) by typing the command:

        cd <path to repo>

    where the `<path to repo>` is your local path (no "<" or ">" symbols) to the `no3gwt` repo. 
    Then, to create the conda environment, type the command:

        conda env create -f environment.yml

   The default name of this environment is `NDST`. Building the `NDST` 
   environment will probably take several minutes.

5. Activate the conda environment. In the `Anaconda Prompt` (terminal on Linux or 
macOS) type the command:

         conda activate NDST

    to activate the python environment installed in step 4.

6. Once the NDST conda environment has been created and activated, install the GW-NDST software (no3gwt) from the [Python Package Index](https://pypi.org/) using pip with the command:

        pip install no3gwt

    Subsequent releases of no3gwt can then be installed with the command:

        pip install --upgrade no3gwt

7. Change the directory to the `no3gwt/ndst_gui` subdirectory. To do this, type 
in the `Anaconda Prompt` (terminal on Linux or macOS) the command:

        cd <path to repo>/ndst_gui

    replacing `<path to repo>` with your local path to the `no3gwt` repo.

8. To launch the Groundwater Nitrate Decision Support Tool's graphical user interface (GUI), 
type the command:

        jupyter notebook
    
     This will launch the [Jupyter Notebook](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html#notebook-app) 
	 App in a browser window. Keep the `Anaconda Prompt` open until step 14.

9. Click on the `GW-NDST_GUI.ipynb` link in the Jupyter app window to open and run the tool, or GUI,
	in the browser.

10. Open File Explorer (or other directory navigation tool) and navigate to the `no3gwt/data_in`
sub-directory. Open either of the example Excel input data files, and save the file with a new
name that is relevant to your well of interest. Replace information in this new Excel file with 
information for the well of interest. Only one well can be entered per analysis, however, 
multiple water chemistry sample results from a single well can be entered into the Excel file. Save
the Excel file and close it. If well construction information (casing and total depth) is not known,
users are encouraged to search the Wisconsin DNR's 
[Well Construction Reports finder](https://wi-dnr.maps.arcgis.com/apps/LocalPerspective/index.html?appid=0cc1b8d9c40749ba9b9e5c2c90848e23) 
or the Wisconsin DNR's [Groundwater Retreival Network](https://dnr.wisconsin.gov/topic/Groundwater/GRN.html) 
websites for assistance with identifying the well and obtaining associated data.

11. In the first cell of the GUI, change the name of the Excel file to match the Excel file 
you just created.  For example: 

	    input_file = '../data_in/your_new_file_name.xlsx'

12. Starting at the top of the GUI, execute the notebook cells in order, following instructions 
in the notebook. Notebook cells can be executed by typing `Shift + Enter` when the cursor is in
that cell.  Some cells will require more than a minute to complete.  An `*` appears near the 
upper left of a cell when it is running; when completed, the `*` changes to a sequential number, 
allowing the user to verify the order in which cells were executed. 

13. To restart the tool to analyze new well information (if well information is updated in the
Excel input file) or to analyze a new well, select `Kernel> Restart Kernel and Clear Output of 
All Cells` in the GUI, and then repeat steps 9-11, making updates as appropriate.

14. Prior to exiting the GUI, it is good practice to clear the results (note that `pdf` files 
of results for each scenario run of the GUI are automatically saved in the `output` directory). 
This can be done by selecting `Edit> Clear Outputs of All Cells`.  To save any changes to the GUI, 
such as the name of the Excel file containing well data that was read-in and used for your latest 
session, click on the `save` button, type `Ctrl + s` (Ctrl and S keys simultaneously), or select 
`File> Save Notebook`.  Then close the GUI by clicking `File> Close and Shut Down Notebook`. The 
`Home Page` window of the Jupyter app and any other browser windows can now be closed by clicking 
the `X` in the upper right of the window.  In the `Anaconda Prompt` where the command `jupyter
notebook` was entered in step 8, type `Ctrl + c` to halt the kernel that had been running the 
Jupyter app in the browser window.  Type `exit` (then `Enter`) to close the `Anaconda Prompt`.

* [Project Jupyter](https://jupyter.org/) development is ongoing, and some recent releases (part 
of the python environment installation in steps 4-6) occasionally present challenges for running
the GW-NDST_GUI in a Jupyter Notebook (step 8).  If this occurs, users may have better success by
using the new JupyterLab interface instead.  One way is to click a button labeled `JupyterLab` at
the upper right of the screen at step 9.  Alternatively, type "jupyter lab" (no quotes) at step 8.  
The interface will look slightly different, but steps 9 through 14 remain unchanged.

How to cite
-----------
###### Software/Code citation for the GW-NDST for Wisconsin:
Note: The version of the software on this branch is not officially published and is not for citation. Below 
is the citation for the latest *officially* published version of the software, including a link to
the corresponding (tagged) published version of the software:

Schachter, L.A., Juckem, P.F., Corson-Dosch, N.T., and Green, C.T., 2024, A Groundwater Nitrate 
Decision Support Tool (GW-NDST) for the State of Wisconsin, version 1.1.1: U.S. Geological Survey 
Software Release, 24 May 2024, [https://doi.org/10.5066/P13ETB4Q](https://doi.org/10.5066/P1IFJYEB)

###### Citation for GW-NDST publication:
Juckem, P.F., Corson-Dosch, N.T., Schachter, L.A., Green, C.T., Ferin, K., Booth, E.G., Kucharik, 
C.J., Austin, B., and Kauffman, L., 2024, Design and calibration of a Nitrate Decision Support Tool 
for groundwater wells in Wisconsin, USA. Environmental Modeling and Software, 
[https://doi.org/10.1016/j.envsoft.2024.105999](https://doi.org/10.1016/j.envsoft.2024.105999)

###### Supporting Data:
Juckem, P.F., Baker, A.C., Corson-Dosch, N.T., Smith, E.A., Schachter, L.A., Kauffman, L.J.,
Green, C.T., and Ha, W.S., 2024, Data to support a Groundwater Nitrate Decision Support Tool for 
Wisconsin: U.S. Geological Survey data release, https://doi.org/10.5066/P9TTAQ18.

Disclaimer
----------
[Link to disclaimer](https://code.usgs.gov/water/NDST/no3gwt/-/blob/main/DISCLAIMER.md?ref_type=heads)

License
-------
[Link to license](https://code.usgs.gov/water/NDST/no3gwt/-/blob/main/LICENSE.md?ref_type=heads)