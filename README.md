# tnp_fitting
TnP fitting for egamma analysis

This is my fitting code I used for measuring electron efficiency using
Tag & Probe.

The file `run2.sh` can be used to run `MChistfit.py`.

The .sh file itself contains the instructions on how to run it, you
will want to put the name the .C file you're running on.

These particular .C files were hand pulled from the files created
using `tnpEGM_fitter.py` and `run.sh`, which are located in the `tnpEGM_fitter` folder.

I may need to edit the files for that a bit to get them to work right again.

In order for the these files to run on CMS el9 you need to run them in
an sl7 container.

This the command to set up the sl7 container:

```
alias use_sl7='cmssw-el7 -p --bind `readlink $HOME` --bind `readlink
-f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs --bind
/uscmst1b_scratch -- /bin/bash -l' 
```

After which you need to run `cmsenv` set up the root environment.

Here is an example of how to run the code:

```
./run2.sh 20-30_01mcF.C 01
```

This has the code read the given file and gives it a number for naming
the outputs.

If you want to edit the directory it puts the output in, that is
located in line 167 of the `MChistfit.py` file.

In order to run `tnpEGMfitter.py`, you can follow the instructions in
the comments of `run.sh`. 

Here are two examples, one running on Data and one on Monte Carlo:



```
./run.sh etc/config/settings_ele_PromptReco2023CD.py
passingPreselectionAndLoose 01

./run.sh etc/config/settings_ele_PromptReco2023CD.py
passingPreselectionAndLoose 01mc -m
```
 
 The bins you want to use can be editing around line 199 in
 `settings_ele_PromptReco2023CD.py`. Additionally the output directory
 can be edited on line 46.

