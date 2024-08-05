from libPython.tnpClassUtils import *
import etc.inputs.tnpSampleDef as tnpSamples
        

for sName in tnpSamples.Moriond17_80X.keys():
    sample = tnpSamples.Moriond17_80X[sName]
    if not sample is None:    sample.dump()
    
