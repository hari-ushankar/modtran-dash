# modtran dashboard

## Installation

1) install conda-lock and mamba into your base environment

     conda activate base
     conda install -c conda-forge python=3.8 mamba conda-lock

2) build the lockfile from environment.yml

    conda-lock -f environment.yml -p linux-64

3) create the modtran environment and activate it
 
    mamba create --name modtran --file conda-linux-64.lock

4) activate the environment and run the app

    conda activate modtran
    python dash-modtran.py
