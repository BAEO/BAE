import ROOT as r
from module import module
from math import *

class addRestFrameVars(module):

  def __init__(self):
    self.name = 'add_rest_frame_vars'
    self.requiredBranches = ['Bplus_*_travelled','Bplus_P*','Bplus_M','Kplus_P*']

  def run(self,t):
    mB = 5284.0
    pz = (mB/t.Bplus_M)*t.Bplus_PZ
    Bvect = r.TVector3(t.Bplus_X_travelled,t.Bplus_Y_travelled,t.Bplus_Z_travelled).Unit()
    p = pz/Bvect.Z()
    px = p*Bvect.X()
    py = p*Bvect.Y()
    E = sqrt(p*p+mB*mB)
    BLvect = r.TLorentzVector(px,py,pz,E)
    visLvect = r.TLorentzVector(t.Bplus_PX,t.Bplus_PY,t.Bplus_PZ,t.Bplus_PE)
    missingvect = BLvect - visLvect
    missingmass = missingvect.M2()/1e6
    kaonvect = r.TLorentzVector(t.Kplus_PX,t.Kplus_PY,t.Kplus_PZ,t.Kplus_PE)
    Xsvect = kaonvect+missingvect
    mXs = Xsvect.M()
    mXs_branch = t.Branch('mXs','d','mXs/d')
    mXs_branch.Fill()i

    return True
  


