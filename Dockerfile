FROM continuumio/miniconda:latest

# Create a working directory
RUN mkdir wd
WORKDIR /wd/

# Copy everything
COPY . /wd/

# Create conda enviroment using the yml file
RUN conda env create -f modtran_env.yml

# Activate conda environment
ENV PATH /opt/conda/envs/modtran_env/bin
RUN /bin/bash -c "source activate modtran_env"
# Command to run dashboard script
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8000", "dash-modtran:server"]