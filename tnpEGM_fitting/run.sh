#!/bin/bash
echo $PWD
echo "Setting environment"

#workdir=$pwd;
#cmssw_path="$CMSSW_BASE/src";
#cd $cmssw_path; cmsenv; cd $workdir
#export PYTHONPATH=$workdir;
#make

# $1 config: etc/config/settings_pho_run2022FG.py
# $2 id
# $3 Run Number
# $4 MC or no

#python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --configuration $4 --checkBins $5 #--mcSig
#python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --configuration $4 --createBins $5 #--mcSig
#python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --configuration $4 --createHists $5 #--mcSig
#python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --configuration $4 --doFit $5 #--mcSig
#python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --configuration $4 --sumUp $5 #--mcSig

python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --checkBins $4
python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --createBins $4
python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --createHists $4
python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --doFit $4
python tnpEGM_fitter.py $1 --flag $2 --runNumber $3 --sumUp $4


#command
#./run.sh etc/config/settings_ele_PromptReco2023CD.py [cut] [run #] [-m]

#cut options
#passingCutBasedVeto122XV1 
#passingCutBasedLoose122XV1
#passingCutBasedMedium122XV1
#passingCutBasedTight122XV1
#passingPreselection
#passingPreselectionAndVetoID
#passingPreselectionAndLoose

#settings_ele_PromptReco2023CD.py
#45 - directory
#139 - bin definitions