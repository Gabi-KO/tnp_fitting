#############################################################
########## General settings
#############################################################
# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# Electron Preselection
Preselection = 'el_pt >= 5 && abs(el_eta) < 2.4 && el_sip < 8 && abs(el_dxy) < 0.05 && abs(el_dz) < 0.1 && el_relPfLepIso03 < (20 + 300/el_pt)'

# cut definitions for flags
passingPreselection                 = '({0})'.format(Preselection)
passingPreselectionAndVetoID        = '(passingCutBasedVeto122XV1 == 1 && {0})'.format(Preselection)
passingPreselectionAndLoose         = '(passingCutBasedLoose122XV1 == 1 && {0})'.format(Preselection)

# flag to be Tested
flags = {
    'passingPreselection'           : passingPreselection,
    'passingPreselectionAndVetoID'  : passingPreselectionAndVetoID,
    'passingPreselectionAndLoose'   : passingPreselectionAndLoose ,
    #'passingAllEvents'              : '(1 == 1)',
    'passingCutBasedVeto94XV2'      : '(passingCutBasedVeto94XV2 == 1)',
    'passingCutBasedLoose94XV2'     : '(passingCutBasedLoose94XV2 == 1)',
    'passingCutBasedMedium94XV2'    : '(passingCutBasedMedium94XV2 == 1)',
    'passingCutBasedTight94XV2'     : '(passingCutBasedTight94XV2 == 1)',
    'passingCutBasedVeto122XV1'     : '(passingCutBasedVeto122XV1   == 1)',
    'passingCutBasedLoose122XV1'    : '(passingCutBasedLoose122XV1  == 1)',
    'passingCutBasedMedium122XV1'   : '(passingCutBasedMedium122XV1 == 1)',
    'passingCutBasedTight122XV1'    : '(passingCutBasedTight122XV1  == 1)',
    'passingMVA94Xwp80isoV2'        : '(passingMVA94Xwp80isoV2 == 1 )',
    'passingMVA94Xwp80noisoV2'      : '(passingMVA94Xwp80noisoV2 == 1 )',
    'passingMVA94Xwp90isoV2'        : '(passingMVA94Xwp90isoV2 == 1 )',
    'passingMVA94Xwp90noisoV2'      : '(passingMVA94Xwp90noisoV2 == 1 )',
    'passingMVA122Xwp80isoV1'       : '(passingMVA122Xwp80isoV1 == 1)',
    'passingMVA122Xwp90isoV1'       : '(passingMVA122Xwp90isoV1 == 1)',
    'passingMVA122Xwp80noisoV1'     : '(passingMVA122Xwp80noisoV1 == 1)',
    'passingMVA122Xwp90noisoV1'     : '(passingMVA122Xwp90noisoV1 == 1)',
    'passingMVA122XwpLisoV1'        : '(passingMVA122XwpLisoV1 == 1)',
    'passingMVA122XwpLnoisoV1'      : '(passingMVA122XwpLnoisoV1 == 1)',
    'passingMVA122XwpHZZisoV1'      : '(passingMVA122XwpHZZisoV1 == 1)'
}

#baseOutDir = '/eos/user/b/bjoshi/www/EGM/TnP/PromptReco_official/tnpEleID_PromptReco2022FG/'
#baseOutDir = '/uscms/home/caleb/nobackup/KU_SUSY_Run3/CMS_EGamma/tnpAnalysis/tnpEleID_PromptReco2023CD'
#baseOutDir = '/uscms/home/gkennedy/nobackup/ScientificLinux7/CMSSW_11_2_0/src/egm_2/plots/fit_tests'
baseOutDir = '/uscms/home/gkennedy/nobackup/ScientificLinux7/CMSSW_11_2_0/src/egm_2/Loose_Cut/MC_Test/fit_' #OUTPUT DIRECTORY

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

# 2022

# samplesDef = {
#         'data'  : tnpSamples.Run3_124X_PromptReco2022F['data_Run2022F'].clone(),
#         'mcNom' : tnpSamples.Run3_124X_PromptReco2022F['DY_1j_madgraph_postEE'].clone(),
#         'tagSel': tnpSamples.Run3_124X_PromptReco2022F['DY_1j_madgraph_postEE'].clone(),
#         'mcAlt': None,
# }
# 
# ## can add data samples easily
# 
# samplesDef['data'].add_sample(tnpSamples.Run3_124X_PromptReco2022G['data_Run2022G'].clone()) 

# 2023

def data_sel(choice):

    tnpSamples.parameters(choice)
    global samplesDef

    
    #Data
    if choice == 'd':
        samplesDef = {
            'data'   : tnpSamples.Run3_2023['data_Run2023C'].clone(),
            'mcNom'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'tagSel'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'mcAlt': None,
        }
    '''
    #Monte Carlo as Data
    if choice == 'd':
        samplesDef = {
            'data'   : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'mcNom'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'tagSel'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'mcAlt': None,
        }
    '''
    #Monte Carlo
    if choice == 'm':
        samplesDef = {
            'data'   : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'mcNom'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'tagSel'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
            'mcAlt': None,
        }



    samplesDef['data' ].set_tnpTree(tnpTreeDir)
    if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
    if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
    if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

    if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
    if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
    if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
    if not samplesDef['tagSel'] is None:
        samplesDef['tagSel'].rename('mcAltSel_DY_madgraph_postEE')
        samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut

    puFile = 'DY_1j_madgraph_PromptReco2022FG_tnpEleID.pu.puTree.root'
    weightName = 'weights_2022_runFG.totWeight'

    if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
    if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
    if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
    if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree(puFile)
    if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree(puFile)
    if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree(puFile)

#samplesDef = {
        #'data'  : tnpSamples.Run3_PromptReco2023C['data_Run2023C'].clone(),
        #'mcNom' : tnpSamples.Run3_PromptReco2023C['DY_4j_madgraph_2023preBPIX'].clone(),
        #'tagSel': tnpSamples.Run3_PromptReco2023C['DY_4j_madgraph_2023preBPIX'].clone(),
        
        #'data'   : tnpSamples.Run3_2023['data_Run2023C'].clone(), #DATA
        #'data'   : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(), #MC
        #'mcNom'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
        #'tagSel'  : tnpSamples.Run3_2023['DY_4j_madgraph_2023preBPIX'].clone(),
        #'mcAlt': None,
#}

## can add data samples easily

#samplesDef['data'].add_sample(tnpSamples.Run3_PromptReco2023D['data_Run2023D'].clone()) 


## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
'''
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph_postEE')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut
'''
## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking periods
#puFile = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-04-25/2022/pu/DY_1j_madgraph_PromptReco2022FG_tnpEleID.pu.puTree.root'
#weightName = 'weights_2022_runFG.totWeight'

# FIXME:
# - We need to update the puFile and weightName for 2023.
# - For now, we will use the puFile and weightName from 2022.
# - The file can be accessed from lxplus using the "/eos/cms/store/group/phys_egamma/..." above.
# - To access the file from cmslpc, we are using the global CERN redirector root://cms-xrd-global.cern.ch/
#   and starting with "root://cms-xrd-global.cern.ch//store/group/phys_egamma/...".
#puFile = 'root://cms-xrd-global.cern.ch//store/group/phys_egamma/tnpTuples/bjoshi/2023-04-25/2022/pu/DY_1j_madgraph_PromptReco2022FG_tnpEleID.pu.puTree.root'
'''
puFile = 'DY_1j_madgraph_PromptReco2022FG_tnpEleID.pu.puTree.root'
weightName = 'weights_2022_runFG.totWeight'

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree(puFile)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree(puFile)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree(puFile)
'''
#############################################################
########## bining definition  [can be nD bining]
#############################################################
#biningDef = [
#   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
#   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,200,500] },
#]

biningDef = [
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [1.5,2.4]},
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [5,10] },
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#additionalCuts = { 
#    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    1 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    2 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    3 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    4 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    5 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    6 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    7 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    8 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    9 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'
#}

#### or remove any additional cut (default)
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
]
        
