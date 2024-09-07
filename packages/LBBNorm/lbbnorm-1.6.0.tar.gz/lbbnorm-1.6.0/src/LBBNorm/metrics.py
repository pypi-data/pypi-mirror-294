


from typing_extensions import Self
import statistics
from torchmetrics import MultiScaleStructuralSimilarityIndexMeasure
import torch
import lpips
import numpy
from image_similarity_measures.quality_metrics import fsim,ssim,psnr

class NMI:
  """
  Args:
    numpy array of images in N*W*H*C
  Example:
    myNMI=NMI(np.asarray([image1,image2])) # each image has W*H*C shape
    print(myNMI.NMIValue)
    print(myNMI.Mean)
    print(myNMI.Sd) 
    """
  def __init__(self,ImageList):
    self.ImageList=ImageList
    self.NMIValue=self.ComputeNMI()
    self.Mean=self.MeanNMI()
    self.Sd=self.SdNMI()

  def SingleNMI(Img):
    ImgPixelWiseMean=numpy.mean(Img, axis=2)
    ImgNMI=np.median(ImgPixelWiseMean)/np.max(ImgPixelWiseMean)
    return(ImgNMI)

  def ComputeNMI(self):
    return(list(map(NMI.SingleNMI,self.ImageList)))

  def MeanNMI(self):
    return(statistics.mean(self.NMIValue))

  def SdNMI(self):
    return(statistics.stdev(self.NMIValue))


class MSSSIM:
  """
  Args:
     2 numpy array of images in (B,W,H,C) or torch array with (B,C,W,H) shape
  Example:
      MSSSIM(images1,images2).measure
    """
  def __init__(self,ImageList1,ImageList2):
    if(type(ImageList1)==numpy.ndarray):
      self.ImageList1=ReorderChannels(ImageList1).ConvertedImages
      self.ImageList2=ReorderChannels(ImageList2).ConvertedImages
    if(type(ImageList1)==torch.Tensor):
      self.ImageList1=ImageList1
      self.ImageList2=ImageList2
    self.measure=self.ComputeMSSSIM()

  def ComputeMSSSIM(self):
    ms_ssim= MultiScaleStructuralSimilarityIndexMeasure()
    ms_ssim=ms_ssim(self.ImageList1,self.ImageList2)
    return(ms_ssim)


class ReorderChannels:
  def __init__(self,ImageList,OnlyNumpyToTorch=False):
    self.ImageList=ImageList
    self.ReorderedImages=self.Reorder()
    if(OnlyNumpyToTorch==True):
      self.ReorderedImages=ImageList
    self.ConvertedImages=self.NumpyToTorch()

  def Reorder(self):
    return(self.ImageList.transpose(0,3,1,2))
  def NumpyToTorch(self):
    return(torch.Tensor(self.ReorderedImages))


class LPIPSimilarity:
  """
  images should be RGB, IMPORTANT: normalized to [-1,1]
  set net as alex or vgg
  image should be normalized to [-1,1]
  Example:
    LPIPS=LPIPSimilarity()
    LPIPS.Computesimilarity(images1,images2)
    """
  def __init__(self,net="alex"):
    self.net=net
    self.loss_fn=lpips.LPIPS(net=self.net)

  def Computesimilarity(self,ImageList1,ImageList2):
    if(type(ImageList1)==numpy.ndarray):
      ImageList1=ReorderChannels(ImageList1,OnlyNumpyToTorch=True).ConvertedImages
      ImageList2=ReorderChannels(ImageList2,OnlyNumpyToTorch=True).ConvertedImages
    if(type(ImageList1)==torch.Tensor):
      ImageList1=ImageList1
      ImageList2=ImageList2
      similarity=1-self.loss_fn(ImageList1, ImageList2)
    return(similarity)

class FSIM:
  """
  Args:
      two numpy array with shape (N,W,H,C)
  Example:
      FSIM(images1,images2).measure
  """
  def __init__(self,ImageList1,ImageList2):
    self.ImageList1=ImageList1
    self.ImageList2=ImageList2
    self.measure=self.ComputeSimilarity()
  def ComputeSimilarity(self):
    return(list(map(fsim,self.ImageList1, self.ImageList2)))

class SSIM:
  """
  Args:
      two numpy array with shape (N,W,H,C)
  Example:
      FSIM(images1,images2).measure
  """
  def __init__(self,ImageList1,ImageList2):
    self.ImageList1=ImageList1
    self.ImageList2=ImageList2
    self.measure=self.ComputeSimilarity()
  def ComputeSimilarity(self):
    return(list(map(ssim,self.ImageList1, self.ImageList2)))

class PSNR:
  """
  Args:
      two numpy array with shape (N,W,H,C)
  Example:
      FSIM(images1,images2).measure
  """
  def __init__(self,ImageList1,ImageList2):
    self.ImageList1=ImageList1
    self.ImageList2=ImageList2
    self.measure=self.ComputeSimilarity()
  def ComputeSimilarity(self):
    return(list(map(psnr,self.ImageList1, self.ImageList2)))

class RMSE:
  """
  Args:
      two numpy array with shape (N,W,H,C)
  Example:
      FSIM(images1,images2).measure
  """
  def __init__(self,ImageList1,ImageList2):
    self.ImageList1=ImageList1
    self.ImageList2=ImageList2
    self.measure=self.ComputeSimilarity()
  def ComputeSimilarity(self):
    return(list(map(rmse,self.ImageList1, self.ImageList2)))

