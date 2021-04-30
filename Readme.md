# modtran dashboard

## Installation

1\) install conda-lock and mamba into your base environment

      conda activate base
      conda install -c conda-forge python=3.8 mamba conda-lock

\) build the lockfile from environment.yml

      conda-lock -f environment.yml -p linux-64

3\) create the modtran environment and activate it
 
      mamba create --name modtran --file conda-linux-64.lock

4\) activate the environment and run the app

      conda activate modtran
      python dash-modtran.py
      
## Description
Uses output data from MODTRAN to plot transmissivity and atmospheric profiles. 

User has options of choosing two different altitudes (20 and 70 km) and four different co2 concentrations (0, 10, 100 and 1000 ppm).

Dashboard also shows surface and top of atmosphere contributions in the transmissivity plot.

Workflow for setting up the dashboard is described as follows:

- Get data from David Archer's webpage
- Put the output file into a folder and name them appropriately i.e., mod_1000_co2_70_dir for 1000 pm co2 and altitude at 70km.
- Use a python script to create csv and pq files for each of these folders. These will serve as input for the dashboard
- Create a dash-plotly script containing main elements of the dashboard such as plots, checkboxes dropdowns and sections of text.


Current state of dashboard:

![modtran-dash](https://github.com/hari-ushankar/modtran-dash/blob/add_features/firefox_screenshot.JPG)
