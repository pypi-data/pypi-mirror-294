import numpy as np
from numba import jit
from scipy.stats import rankdata
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

# Calculate mass ratio matrix
@jit(nopython=True)
def _Massratio(Indexdm,Sortdm,n):
  n= Indexdm.shape[1]
  MassRatio=np.ones((Indexdm.shape[0],Indexdm.shape[1]))
  for r in range(n):
      rm = Sortdm[r,n-1]
      ii = n-1
      for i in range(n-1,-1,-1) :
# when pairwise distance is same, the mass is also same
        if Sortdm[r,i] !=rm:
          rm = Sortdm[r,i]
          ii =i
# Calculate mass ratio
        MassRatio[int(Indexdm[r,i]),r]=MassRatio[int(Indexdm[r,i]),r]*(ii+1)
        MassRatio[r,int(Indexdm[r,i])]=MassRatio[r,int(Indexdm[r,i])]/(ii+1)
  return MassRatio

class MOF:
  '''
  Mass ratio variance-based outlier factor (MOF)
  the outlier score of each data point is called MOF.
  It measures the global deviation of density given sample with respect to other data points.
  it is global in the outlier score depend on how isolated
  data point is with respect to all data points in the data set.
  the variance of mass ratio can identify data points that have a substantially
  lower density compared to other data points.
  These are considered outliers.
  '''
  # Parameters-free
  # ----------
  def __init__(self):
    self.name='MOF'
    self.Sortdm = []
    self.Data = []

  def fit(self,Data,y=None):

    
    '''Fit detector. y is ignored in unsupervised methods.'''
    '''
    Parameters
    ----------
    Data : numpy array of shape (n_samples, n_features)
        The input samples.
    y : Ignored #     Not used
    '''
    '''
    Returns
    -------
    self : object
    '''
#     Fitted estimator.
    n = len(Data)
    self.Data =Data
# Calculate distance matrix
    Dm=cdist(Data,Data)

# Calculate sorted distance matrix
    self.Sortdm = np.sort(Dm)

# Calculate indices of sorted distance matrix
    self.Indexdm = np.argsort(Dm)

# Calculate mass ratio variance (MOF)
    MassRatio=_Massratio(self.Indexdm,self.Sortdm,n)
    self.dif = MassRatio

#  Calculate mass ratio variance (MOF)
    np.fill_diagonal(MassRatio,np.nan)
    self.MassRatio = MassRatio
    score=np.nanvar(MassRatio,axis=1)
    self.decision_scores_=score

def WRS(D,m,V=[],seed=42):
# fix seed
  np.random.seed(seed)
# random value between 0 and 1
  u = np.random.uniform(0,1,int(len(D)))
# calculate key score
  K = u**(1/V)

  return D[np.argsort(K)[:m]]

class SMOF:
  '''
  Streaming Mass ratio variance-based outlier factor (SMOF)
  the outlier score of each data point is called SMOF.
  It measures the global deviation of density of data points in current window with respect to data points in the refernce window. this algoihtm process in non-overlapping window. the mutipy between variance of mass ratio of each data point and average of them in present window can identify data points that have a substantially lower density compared to other data points. These are considered outliers.
  '''
  '''
  Parameters-free
  ----------
  win (int) window size of sum of reference and current window
  seed (int) random seed
  Train (array) data points for intilized model
  '''

  def __init__(self,win=256,seed=42,Train=[]):

    self.win = win
    self.seed = seed
    self.window_current = Train
    self.count = 0
    self.SMOFs =[]


  def init(self):

# calculate average of MOF score in both window
    MOFrc=MOF()
    MOFrc.fit(MinMaxScaler().fit_transform(self.window_current))
    uw = np.mean(MOFrc.decision_scores_)

# calculate average of MOF score in reference window
    MOFr=MOF()
    MOFr.fit(MinMaxScaler().fit_transform(self.window_current[:int(self.win*2/4)]))
    ur = np.mean(MOFr.decision_scores_)

# calculate average of MOF score in current window
    MOFc=MOF()
    MOFc.fit(MinMaxScaler().fit_transform(self.window_current[int(self.win*2/4):]))
    uc = np.mean(MOFc.decision_scores_)

# calculate SMOF score
    SMOFs = MOFrc.decision_scores_
    SMOFs[:int(self.win*2/4)] = SMOFs[:int(self.win*2/4)]*ur
    SMOFs[int(self.win*2/4):] = SMOFs[int(self.win*2/4):]*uc
    self.SMOFs =  list(SMOFs)

# sampling data point by WRS samplig and keep to reference window
    V = MOFrc.decision_scores_
    V[:int(self.win*2/4)] = V[:int(self.win*2/4)]  + uw
    self.window_current= WRS(D=self.window_current,V = V,m =int(self.win/2), seed=self.seed)


  def fit(self,X_current):
# Move current data point to current window and assign SMOF scores
# Parameters
# ----------
# X_current: current data point from streaming data


# move a new data points to current window
    self.count = self.count+1
    self.SMOFs.append(0)
    self.window_current=np.r_[self.window_current,np.array([X_current])]


# data points in current reach full
    if len(self.window_current) >= self.win :

# calculate average of MOF score in both window
      MOFrc=MOF()
      MOFrc.fit(MinMaxScaler().fit_transform(self.window_current))
      uw = np.mean(MOFrc.decision_scores_)
# calculate average of MOF score in reference window
      MOFr=MOF()
      MOFr.fit(MinMaxScaler().fit_transform(self.window_current[:int(self.win*2/4)]))
      ur = np.mean(MOFr.decision_scores_)
      self.SMOFs[-int(self.win*2/4):] = (MOFrc.decision_scores_[int(self.win*2/4):])*ur

# sampling data point by WRS samplig and keep to reference window
      V = MOFrc.decision_scores_
      V[:int(self.win*2/4)] = V[:int(self.win*2/4)]  + uw
      self.window_current= WRS(D=self.window_current,V = V,m =int(self.win/2), seed=self.seed)

# assign SMOF score to remain data points in current window
  def END(self):

    if len(self.window_current) != int(self.win/2):
      MOFrc=MOF()
      MOFrc.fit(MinMaxScaler().fit_transform(self.window_current))
      MOFr=MOF()
      MOFr.fit(MinMaxScaler().fit_transform(self.window_current[:int(self.win*2/4)]))
      ur = np.mean(MOFr.decision_scores_)
      CC = len(self.window_current[int(self.win*2/4):])
      self.SMOFs[-CC:] = MOFrc.decision_scores_[int(self.win*2/4):]*ur

    self.SMOFs = np.array(self.SMOFs)

