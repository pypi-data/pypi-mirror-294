# nrt_analyzer

Tools for analysing NRT data from cochlear and generate pipelines in python. 

Examples can be found in [nrt_analyzer](https://open-source-brain.gitlab.io/nrt_analyzer/) website. 

## Installation
This software requires Python >= 3.9

Standard installation of stable release can be obtained from the official repository 
```commandline
pip install nrt_analyzer
```
### Windows enviroment
The easiest and painless installation is via [Anaconda](https://www.anaconda.com/products/distribution).
Once you have installed Anaconda, create a new python environment and launch the terminal in this environment.
In the terminal run: 
```commandline
pip install nrt_analyzer
```
nrt_analyzer will be installed in that new environment. 


## Development version
The development version can be obtained from our official Gitlab repository 

```commandline
git clone https://gitlab.com/jundurraga/nrt_analyzer.git
```

This will clone into the folder 'nrt_analyzer'.

To be able to look in the (generated) sql-databases, we recommend using DB Browser (https://sqlitebrowser.org/)

### For Windows

Precompiled PyFFTW is easier to install via conda.
If you are using window, this is the easiest way to have PyFFT running.

```commandline
conda install -c conda-forge pyfftw
```

## Examples
Please have a look at the 'examples' folder
