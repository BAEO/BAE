# $Id: $
# Test your line(s) of the stripping
#  
# NOTE: Please make a copy of this file for your testing, and do NOT change this one!
#
'''
File used to rerun stripping 28 on 2012 MC  
Works with DaVinci v42r1
'''

LeptonType = "Muons" 

if LeptonType == "Muons" : 
    l = "mu"
    tuplename = "muon"
if LeptonType == "Electrons": 
    l = "e"
    tuplename = "electron"

print LeptonType 
print l 


from Gaudi.Configuration import *
from Configurables import DaVinci
from StrippingConf.Configuration import StrippingConf


from Configurables import EventNodeKiller, ProcStatusCheck 

# first kill the nodes 
event_node_killer = EventNodeKiller("StripKiller")
event_node_killer.Nodes = ["/Event/allStreams", "/Event/Strip","/Event/Leptonic" ]



# Specify the name of your configuration
confname='B2KLLXInclusive' #FOR USERS    

from StrippingSelections import buildersConf
confs = buildersConf()

#print confs

#clone lines for CommonParticles overhead-free timing





from Configurables import DecayTreeTuple, FitDecayTrees, TupleToolRecoStats, TupleToolTrigger, TupleToolSubMass
from Configurables import TupleToolTISTOS, CondDB, SelDSTWriter
from Configurables import TupleToolTrackInfo, TupleToolRICHPid, TupleToolGeometry, TupleToolPid
from Configurables import TupleToolANNPID
from DecayTreeTuple.Configuration import *

tupleB = DecayTreeTuple("bae-"+tuplename+"-data")


tupleB.Inputs = ["Phys/B2KLLXInclusive_InclKLLLine/Particles"]

#decay = ""
if LeptonType == "Muons" : 
    decay =  "[B+ -> ^(J/psi(1S) -> ^mu+ ^mu-) ^K+]CC"
    tupleB.addBranches ({
            "Kplus"  :  "[B+ -> ^K+ (J/psi(1S) -> mu+ mu-)]CC",
            "Jpsi"   :  "[B+ -> K+ ^(J/psi(1S) -> mu+ mu-)]CC",
            "lplus"  :  "[B+ -> K+ (J/psi(1S) -> ^mu+ mu-)]CC",
            "lminus" :  "[B+ -> K+ (J/psi(1S) -> mu+ ^mu-)]CC",
            "Bplus"  : "[B+ -> K+ J/psi(1S)]CC",
            })

if LeptonType == "Electrons":
    decay =  "[B+ -> ^(J/psi(1S) -> ^e+ ^e-) ^K+]CC"
    tupleB.addBranches ({
            "Kplus"  :  "[B+ -> ^K+ (J/psi(1S) -> e+ e-)]CC",
            "Jpsi"   :  "[B+ -> K+ ^(J/psi(1S) -> e+ e-)]CC",
            "lplus"  :  "[B+ -> K+ (J/psi(1S) -> ^e+ e-)]CC",
            "lminus" :  "[B+ -> K+ (J/psi(1S) -> e+ ^e-)]CC",
            "Bplus"  :  "[B+ -> K+ J/psi(1S)]CC",
            })
tupleB.Decay = decay



tupleB.ToolList =  [
      "TupleToolKinematic",
      "TupleToolEventInfo",
      "TupleToolRecoStats",
      "TupleToolTrackInfo",
      
] # Probably need to add many more Tools.




LoKi_All=tupleB.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_All")
LoKi_All.Variables = {
        'MINIPCHI2' : "MIPCHI2DV(PRIMARY)",
        'MINIP' : "MIPDV(PRIMARY)",
        'IPCHI2_OWNPV' : "BPVIPCHI2()",
        'IP_OWNPV' : "BPVIP()"
}



LoKi_lplus=tupleB.lplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_lplus")
LoKi_lplus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)", 
       
}

LoKi_Kplus=tupleB.Kplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_Kplus")
LoKi_Kplus.Variables = {
       'PIDmu' : "PIDmu",
       'PIDK' : "PIDK",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}
LoKi_lminus=tupleB.lminus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_lminus")
LoKi_lminus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}

LoKi_B=tupleB.Bplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_B")
LoKi_B.Variables = {
       'DTF_CHI2' : "DTF_CHI2NDOF(True)",
       'TAU' : "BPVLTIME()",
       'DIRA_OWNPV' : "BPVDIRA",
       'FD_CHI2' : "BPVVDCHI2",
       'ENDVERTEX_CHI2' : "VFASPF(VCHI2/VDOF)",
       'PVX' : "BPV(VX)",
       'PVY' : "BPV(VY)",
       'PVZ' : "BPV(VZ)",
       'VX' : "VFASPF(VX)",
       'VY' : "VFASPF(VY)",
       'VZ' : "VFASPF(VZ)",
       'X_travelled' : "VFASPF(VX)-BPV(VX)",
       'Y_travelled' : "VFASPF(VY)-BPV(VY)",
       'Z_travelled' : "VFASPF(VZ)-BPV(VZ)",
       'P_Parallel' : "BPVDIRA*P",
       'P_Perp' : "sin(acos(BPVDIRA))*P",
       'Corrected_Mass' : "BPVCORRM"
}


TriggerListL0 = [
    "L0MuonDecision",
    "L0DiMuonDecision"
  ]

TriggerListHlt =[   
    "Hlt1TrackMuonDecision",
    "Hlt1TrackMVADecision",
    "Hlt2TopoMu2BodyDecision",
    "Hlt2TopoMuMu2BodyDecision",
    "Hlt2DiMuonDetachedDecision",
]



#tupleB.Bplus.ToolList += [ "TupleToolTISTOS" ]
#tupleB.Bplus.addTool( TupleToolTISTOS, name = "TupleToolTISTOS" )
#tupleB.Bplus.TupleToolTISTOS.Verbose = True
#tupleB.Bplus.TupleToolTISTOS.TriggerList = TriggerListL0
#tupleB.Bplus.TupleToolTISTOS.TriggerList += TriggerListHlt

#tupleB.Bplus.TupleToolTISTOS.Verbose = True
#tupleB.Bplus.TupleToolTISTOS.VerboseL0= True
#tupleB.Bplus.TupleToolTISTOS.VerboseHlt1= True
#tupleB.Bplus.TupleToolTISTOS.VerboseHlt2= True




tupleB.Jpsi.ToolList += [ "TupleToolTISTOS" ]
tupleB.Jpsi.addTool( TupleToolTISTOS, name = "TupleToolTISTOS" )
tupleB.Jpsi.TupleToolTISTOS.Verbose = True
tupleB.Jpsi.TupleToolTISTOS.TriggerList =TriggerListL0
tupleB.Jpsi.TupleToolTISTOS.TriggerList += TriggerListHlt

tupleB.Jpsi.TupleToolTISTOS.Verbose = True
tupleB.Jpsi.TupleToolTISTOS.VerboseL0= True
tupleB.Jpsi.TupleToolTISTOS.VerboseHlt1= True
tupleB.Jpsi.TupleToolTISTOS.VerboseHlt2= True



#tupleB.addTool(TupleToolANNPID, name = "TupleToolANNPID")
#tupleB.TupleToolANNPID.ANNPIDTunes = ['MC12TuneV2', 'MC12TuneV3', "MC12TuneV4"]


#tupleB.Bplus.addTupleTool( 'TupleToolSubMass' )
#tupleB.Bplus.ToolList += [ "TupleToolSubMass" ]

#tupleB.Bplus.TupleToolSubMass.Substitution += ["K+ => pi+"]
#tupleB.Bplus.TupleToolSubMass.Substitution += ["K+ => p+"]


# rerun the Calo reconstruction 
#importOptions("$APPCONFIGOPTS/DaVinci/DV-RedoCaloPID-Stripping21.py")

#Configure DaVinci


DaVinci().HistogramFile = 'xdummy.root'
DaVinci().EvtMax = -1
DaVinci().PrintFreq = 2000
DaVinci().appendToMainSequence([tupleB])

DaVinci().RootInTES = "/Event/Leptonic"
DaVinci().DataType  = "2016"
DaVinci().InputType = "MDST"
DaVinci().Simulation = False
DaVinci().Lumi = True

DaVinci().TupleFile = "bae-"+str(tuplename)+"-data.root"

MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"
# database


#DaVinci().DDDBtag   = "dddb-20150522-2"
#DaVinci().CondDBtag = "sim-20150522-vc-md100"

#input file
#importOptions("$HOME/BAEO/BAE/davinci_scripts/B2Kmm.py")
