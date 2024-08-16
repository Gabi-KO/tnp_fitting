# tnp_fitting
TnP fitting for egamma analysis

This is my fitting code I used for measuring electron efficiency using Tag & Probe.

The main fitting file is `MChistfit.py`, it fits the histograms given by a .C file.

These particular .C files were hand pulled from the files created running `tnpEGM_fitter.py` over the .root file `DY_1j_madgraph_PromptReco2022FG_tnpEleID.pu.puTree.root`. You can find both of these in the `tnpEGM_fitting` directory.


## Setup

In order for the these files to run on CMS el9 you need to run them in an sl7 container.

This the command to set up the sl7 container:

```
alias use_sl7='cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs --bind /uscmst1b_scratch -- /bin/bash -l' 
```

This will make it so the command `use_sl7` puts you in the container.

After which you need to run `cmsenv` set up the root environment.


## Creating .C Files

If you need to create the .C files you want to fit on, you can do so by running `tnpEGMfitter.py`. The instructions on how to do so are in the comments of `run.sh`. The .C files are functionally used as .txt files.


Here are two examples, one running on Data and one on Monte Carlo:

```
./run.sh etc/config/settings_ele_PromptReco2023CD.py passingPreselectionAndLoose 01

./run.sh etc/config/settings_ele_PromptReco2023CD.py passingPreselectionAndLoose 01mc -m
```
 
The code is by default set to output things in my directory, you'll want to change it to yours. This can be done by altering `baseOutDir` on line 46 in `settings_ele_PromptReco2023CD.py`.
 
The bins you want to use can be editing around line 199 in `settings_ele_PromptReco2023CD.py`.

Currently, this will output a fitting plot (alongside two extras that are useless). It'll be the one with "bin00" at the beginning.

It is supposed to give you a file called `datareadout.txt`, but that is currently not working. This file isn't actually necessary as you can calculate all the values it would give you using the numbers on the bin00 plot.

It will also output some .root files. The one you want to look at in the TBrowser is `data_Run2023C_passingPreselectionAndLoose.root`. Enter the root environment and then do the following.

```
TBrowser b("data_Run2023C_passingPreselectionAndLoose.root")

```

Inside there will be some root canvases. You will want to download bin00's Pass and Fail canvases as .C files. It might also be good to download them as .png files as well for reference.

These .C files are the ones the code is run over.


## Running the Fitter


The file `run2.sh` can be used to run `MChistfit.py`.

The .sh file itself contains the instructions on how to run it, you will want to put the name the .C file you're running on.

Here is an example of how to run the code:

```
./run2.sh 20-30_01mcF.C 01
```

This has the code read the given file and gives it a number for naming the outputs.

As the code stands, the directory created by this run would be `/Preselection_Loose/Final_Plots_v2/20-30_01mcF/fit_01`.

It will output the plot and text document called `results.txt` which contains fitting data.

If you want to edit the directory it puts the output in, that is located in line 167 of the `MChistfit.py` file.

For fine tuning the fit, you may need to edit the bounds on which you fit each function. You can do this on line 237.

Additionally, there are multiple fitting functions (single gaussian for signal and the background function for background work best I think). You can switch between them by editing the numbers around line 179. There is also a "manual override" that basically just helps the fit get the right amplitude for the signal.
