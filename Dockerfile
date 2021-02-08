FROM python:3.9.1

# Create a working directory
RUN mkdir wd
WORKDIR /wd/

RUN apt-get update && apt-get --yes install \
  build-essential \
  lsb-release \
  wget \
  software-properties-common
#RUN bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

RUN wget https://apt.llvm.org/llvm.sh && \
  chmod +x llvm.sh && \
  ./llvm.sh 10
ENV LLVM_CONFIG /usr/bin/llvm-config-10
#  python3-pip
# Install requirements
RUN pip install numpy

# Copy everything
# TODO: only copy requirements.txt
COPY . /wd/

RUN pip install -r requirements.txt

## TODO: AND now copy the rest

# Command to run dashboard script
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8000", "dash-modtran:server"]
