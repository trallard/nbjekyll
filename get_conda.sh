# This will get the appropriate conda environment make sure
# to put this in the install step of the CI

sudo apt-get update
# We do this conditionally because it saves us some downloading if the
# version is the same.
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh;

chmod +x miniconda.sh
./miniconda.sh -b -f -p $MINICONDA
export PATH=/home/travis/miniconda/bin:$PATH
conda config --set always_yes yes
conda update --yes conda

# Useful for debugging any issues with conda
conda info -a
