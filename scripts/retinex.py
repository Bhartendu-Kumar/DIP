#function signatures
#SSR
#def retinex_SSR(img,sigma)

#MSR
#def retinex_MSR(img,sigmas=[15,80,250],weights=None)

#ASSR  or AMSR
# retinex_AMSR(img,sigmas=[12,80,250])

#weights should be a list of length equal to sigma and sum to 1

# MSR combines various SSR with different(or same) weights,
    #    commonly we select 3 scales(sigma) and equal weights, (15,80,250) is a good
    #    choice. If len(sigmas)=1, equal to SSR
    # args:
    #    sigmas: a list
    #    weights: None or a list, it represents the weight for each SSR, their sum should
    #       be 1, if None, the weights will be [1/t, 1/t, ..., 1/t], t=len(sigmas)
    # '''




# encoding:utf-8
'''
Retinex theory based on formula image = reflectance*luminance, what we need is to 
estimate the luminance function. This technology is suitable for high dynamic range 
image enhancement, underwater image enhancement, foggy image enhancement and 
low-light image enhancement.

In this code, we mainly recommend func retinex_gimp or retinex_MSRCR, retinex_MSRCP

Main function:
 -Path-based model
    retinex_FM, 
 -Center/Surround model
    retinex_SSR, retinex_MSR, retinex_MSRCR, retinex_gimp, retinex_MSRCP, 
    retinex_AMSR, 

References:
[1] D. J. Jobson, Z. Rahman and G. A. Woodell, "A multiscale retinex for bridging the 
    gap between color images and the human observation of scenes," in IEEE 
    Transactions on Image Processing, vol. 6, no. 7, pp. 965-976, July 1997.
[2] Frankle,Jonathan and McCann, John, “Method and Apparatus for Lightness Imaging”, 
    USPatent #4,384,336, May 17, 1983.
[3] Funt, Brian & Ciurea, Florian & McCann, John. (2004). Retinex in Matlab. Journal 
    of Electronic Imaging - J ELECTRON IMAGING. 13. 48-57. 10.1117/1.1636761.
[4] Ana Belén Petro, Catalina Sbert, and Jean-Michel Morel, Multiscale Retinex, Image 
    Processing On Line, (2014), pp. 71–88. https://doi.org/10.5201/ipol.2014.107

Provided by muggledy on 2020-3-18
'''

import numpy as np


#TOOLS

import time
import numpy as np
from functools import wraps
import cv2
import os.path

eps=np.finfo(np.double).eps

def measure_time(wrapped):
    @wraps(wrapped)
    def wrapper(*args,**kwds):
        t1=time.time()
        ret=wrapped(*args,**kwds)
        t2=time.time()
        print('@measure_time: {0} took {1} seconds'.format(wrapped.__name__,t2-t1))
        return ret
    return wrapper


def my_heq(img):
    '''process heq on 3-channel image just like single-channel, most of the time
       it's worse than func cv2_heq'''
    hist,_=np.histogram(img,256,[0,256])
    cdf=hist.cumsum()
    gaimi=cdf/cdf.max()
    return np.floor((gaimi*255)[img.ravel()]).astype('uint8').reshape(img.shape)


def cv2_heq(img,yuv=False):
    '''cv2's histogram equalization can only be implemented on single channel image,
       sometimes it doesn't work very well for 3-channel pic, you can contrast with
       func my_heq:
          >>> img=cv2.imread('./img/lena0.8.png')
          >>> contrast_plot(img,[cv2_heq(img),my_heq(img)],['cv2 heq','my heq'])
    '''
    if len(img.shape)==2:
        img=img[...,None]
    if yuv:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    ret=img.copy()
    for i in range(img.shape[-1]):
        ret[...,i]=cv2.equalizeHist(img[...,i])
        if yuv:
            break
    if yuv:
        return cv2.cvtColor(ret,cv2.COLOR_YCrCb2BGR)
    return ret.squeeze()

def get_gauss_kernel(sigma,dim=2):
    '''1D gaussian function: G(x)=1/(sqrt{2π}σ)exp{-(x-μ)²/2σ²}. Herein, μ:=0, after
       normalizing the 1D kernel, we can get 2D kernel version by
       matmul(1D_kernel',1D_kernel), having same sigma in both directions. Note that
       if you want to blur one image with a 2-D gaussian filter, you should separate
       it into two steps(i.e. separate the 2-D filter into two 1-D filter, one column
       filter, one row filter): 1) blur image with first column filter, 2) blur the
       result image of 1) with the second row filter. Analyse the time complexity: if
       m&n is the shape of image, p&q is the size of 2-D filter, bluring image with
       2-D filter takes O(mnpq), but two-step method takes O(pmn+qmn)'''
    ksize=int(np.floor(sigma*6)/2)*2+1 #kernel size("3-σ"法则) refer to
    #https://github.com/upcAutoLang/MSRCR-Restoration/blob/master/src/MSRCR.cpp
    k_1D=np.arange(ksize)-ksize//2
    k_1D=np.exp(-k_1D**2/(2*sigma**2))
    k_1D=k_1D/np.sum(k_1D)
    if dim==1:
        return k_1D
    elif dim==2:
        return k_1D[:,None].dot(k_1D.reshape(1,-1))

def gauss_blur_original(img,sigma):
    '''suitable for 1 or 3 channel image'''
    row_filter=get_gauss_kernel(sigma,1)
    t=cv2.filter2D(img,-1,row_filter[...,None])
    return cv2.filter2D(t,-1,row_filter.reshape(1,-1))

def gauss_blur_recursive(img,sigma):
    '''refer to “Recursive implementation of the Gaussian filter”
       (doi: 10.1016/0165-1684(95)00020-E). Paper considers it faster than
       FFT(Fast Fourier Transform) implementation of a Gaussian filter.
       Suitable for 1 or 3 channel image'''
    pass

def gauss_blur(img,sigma,method='original'):
    if method=='original':
        return gauss_blur_original(img,sigma)
    elif method=='recursive':
        return gauss_blur_recursive(img,sigma)

def simplest_color_balance(img_msrcr,s1,s2):
    '''see section 3.1 in “Simplest Color Balance”(doi: 10.5201/ipol.2011.llmps-scb).
    Only suitable for 1-channel image'''
    sort_img=np.sort(img_msrcr,None)
    N=img_msrcr.size
    Vmin=sort_img[int(N*s1)]
    Vmax=sort_img[int(N*(1-s2))-1]
    img_msrcr[img_msrcr<Vmin]=Vmin
    img_msrcr[img_msrcr>Vmax]=Vmax
    return (img_msrcr-Vmin)*255/(Vmax-Vmin)

def get_dir(flag=True):
    '''trace back this function's caller(flag=True) or this script's(flag=False) directory'''
    if flag:
        import traceback
        t=traceback.extract_stack()
        return os.path.dirname(os.path.realpath(t[0].filename))
    else:
        return os.path.dirname(os.path.realpath(__file__))


#tools

















#retinex methods



### Frankle-McCann Retinex[2,3]

def retinex_FM(img,iter=4):
    '''log(OP(x,y))=1/2{log(OP(x,y))+[log(OP(xs,ys))+log(R(x,y))-log(R(xs,ys))]*}, see
       matlab code in https://www.cs.sfu.ca/~colour/publications/IST-2000/'''
    if len(img.shape)==2:
        img=img[...,None]
    ret=np.zeros(img.shape,dtype='uint8')
    def update_OP(x,y):
        nonlocal OP
        IP=OP.copy()
        if x>0 and y==0:
            IP[:-x,:]=OP[x:,:]+R[:-x,:]-R[x:,:]
        if x==0 and y>0:
            IP[:,y:]=OP[:,:-y]+R[:,y:]-R[:,:-y]
        if x<0 and y==0:
            IP[-x:,:]=OP[:x,:]+R[-x:,:]-R[:x,:]
        if x==0 and y<0:
            IP[:,:y]=OP[:,-y:]+R[:,:y]-R[:,-y:]
        IP[IP>maximum]=maximum
        OP=(OP+IP)/2
    for i in range(img.shape[-1]):
        R=np.log(img[...,i].astype('double')+1)
        maximum=np.max(R)
        OP=maximum*np.ones(R.shape)
        S=2**(int(np.log2(np.min(R.shape))-1))
        while abs(S)>=1: #iterations is slow
            for k in range(iter):
                update_OP(S,0)
                update_OP(0,S)
            S=int(-S/2)
        OP=np.exp(OP)
        mmin=np.min(OP)
        mmax=np.max(OP)
        ret[...,i]=(OP-mmin)/(mmax-mmin)*255
    return ret.squeeze()

### Single-Scale Retinex[4]

def retinex_SSR(img,parameter_list):
    sigma = parameter_list[0]
    '''log(R(x,y))=log(S(x,y))-log(S(x,y)*G(x,y))=log(S(x,y))-log(L(x,y)), i.e. 
       r=s-l. S(x,y) and R(x,y) represent input image and retinex output image 
       respectively, L(x,y):=S(x,y)*G(x,y) represents the lightness function, 
       defined as the original image S operated with a gaussian filter G(named 
       as center/surround function)
    implement ssr on single channel:
       1) read original image and convert to double(type) as S
       2) calc coefficient of G with sigma, i.e. normalize the gaussian kernel
       3) calc r by r=s-l and then convert r to R(from log to real)
       4) stretch the values of R into the range 0~255
    issue:
       we don't convert values from log domain to real domain in step 3 above, 
       because it will bring terrible effect. In fact nobody does this, but the 
       reason still remains unknown
    note:
       gauss blur is the main operation of SSR, its time complexity is O(mnpq), 
       m&n is the shape of image, p&q is the size of filter, we can use recursive 
       gaussian filter(RGF), O(mn), to alternative it(see func fast_gauss_blur). 
       Or transform from time domain to frequency domain using Fourier Transform 
       to reduce complexity[4]
    '''
    if len(img.shape)==2:
        img=img[...,None]
    ret=np.zeros(img.shape,dtype='uint8')
    for i in range(img.shape[-1]):
        channel=img[...,i].astype('double')
        S_log=np.log(channel+1)
        gaussian=gauss_blur(channel,sigma)
        #gaussian=cv2.filter2D(channel,-1,get_gauss_kernel(sigma)) #conv may be slow if size too big
        # gaussian=cv2.GaussianBlur(channel,(0,0),sigma) #always slower
        L_log=np.log(gaussian+1)
        r=S_log-L_log
        R=r #R=np.exp(r)?
        mmin=np.min(R)
        mmax=np.max(R)
        stretch=(R-mmin)/(mmax-mmin)*255 #linear stretch
        ret[...,i]=stretch
    return ret.squeeze()

### Multi-Scale Retinex[4]

def retinex_MSR(img,parameter_list=[[15,80,250]]):
    sigmas = parameter_list[0]
    weights = None
    '''r=∑(log(S)-log(S*G))w, MSR combines various SSR with different(or same) weights, 
       commonly we select 3 scales(sigma) and equal weights, (15,80,250) is a good 
       choice. If len(sigmas)=1, equal to SSR
    args:
       sigmas: a list
       weights: None or a list, it represents the weight for each SSR, their sum should 
          be 1, if None, the weights will be [1/t, 1/t, ..., 1/t], t=len(sigmas)
    '''
    if weights==None:
        weights=np.ones(len(sigmas))/len(sigmas)
    elif not abs(sum(weights)-1)<0.00001:
        raise ValueError('sum of weights must be 1!')

    if len(img.shape) == 2:
        img = img[..., None]
    ret = np.zeros(img.shape, dtype='uint8')
    for i in range(img.shape[-1]):
        channel=img[...,i].astype('double')
        r=np.zeros_like(channel)
        for k,sigma in enumerate(sigmas):
            r+=(np.log(channel+1)-np.log(gauss_blur(channel,sigma,)+1))*weights[k]
        mmin=np.min(r)
        mmax=np.max(r)
        stretch=(r-mmin)/(mmax-mmin)*255
        ret[...,i]=stretch
    return ret.squeeze()

def MultiScaleRetinex(img,sigmas=[15,80,250],weights=None,flag=True):
    '''equal to func retinex_MSR, just remove the outer for-loop. Practice has proven 
       that when MSR used in MSRCR or Gimp, we should add stretch step, otherwise the 
       result color may be dim. But it's up to you, if you select to neglect stretch, 
       set flag as False, have fun'''
    if weights==None:
        weights=np.ones(len(sigmas))/len(sigmas)
    elif not abs(sum(weights)-1)<0.00001:
        raise ValueError('sum of weights must be 1!')
    r=np.zeros(img.shape,dtype='double')
    img=img.astype('double')
    for i,sigma in enumerate(sigmas):
        r+=(np.log(img+1)-np.log(gauss_blur(img,sigma)+1))*weights[i]
    if flag:
        mmin=np.min(r,axis=(0,1),keepdims=True)
        mmax=np.max(r,axis=(0,1),keepdims=True)
        r=(r-mmin)/(mmax-mmin)*255 #maybe indispensable when used in MSRCR or Gimp, make pic vibrant
        r=r.astype('uint8')
    return r

'''old version
def retinex_MSRCR(img,sigmas=[12,80,250],s1=0.01,s2=0.01):
    alpha=125
    ret=np.zeros(img.shape,dtype='uint8')
    csum_log=np.log(np.sum(img,axis=2).astype('double')+1)
    msr=retinex_MSR(img,sigmas)
    for i in range(img.shape[-1]):
        channel=img[...,i].astype('double')
        r=(np.log(alpha*channel+1)-csum_log)*msr[...,i]
        stretch=simplest_color_balance(r,0.01,0.01)
        ret[...,i]=stretch
    return ret

def retinex_gimp(img,sigmas=[12,80,250],dynamic=2):
    alpha=128
    gain=1
    offset=0
    ret=np.zeros(img.shape,dtype='uint8')
    csum_log=np.log(np.sum(img,axis=2)+1)
    msr=retinex_MSR(img,sigmas)
    for i in range(img.shape[-1]):
        channel=img[...,i].astype('double')
        r=gain*(np.log(alpha*channel+1)-csum_log)*msr[...,i]+offset
        mean=np.mean(r)
        var=np.sqrt(np.sum((r-mean)**2)/r.size)
        mmin=mean-dynamic*var
        mmax=mean+dynamic*var
        stretch=(r-mmin)/(mmax-mmin)*255
        stretch[stretch>255]=255
        stretch[stretch<0]=0
        ret[...,i]=stretch
    return ret
'''

### Multi-Scale Retinex with Color Restoration, see[4] Algorithm 1 in section 4

def retinex_MSRCR(img,sigmas=[12,80,250],s1=0.01,s2=0.01):
    '''r=βlog(αI')MSR, I'=I/∑I, I is one channel of image, ∑I is the sum of all channels, 
       C:=βlog(αI') is named as color recovery factor. Last we improve previously used 
       linear stretch: MSRCR:=r, r=G[MSRCR-b], then doing linear stretch. In practice, it 
       doesn't work well, so we take another measure: Simplest Color Balance'''
    alpha=125
    img=img.astype('double')+1 #
    csum_log=np.log(np.sum(img,axis=2))
    msr=MultiScaleRetinex(img-1,sigmas) #-1
    r=(np.log(alpha*img)-csum_log[...,None])*msr
    #beta=46;G=192;b=-30;r=G*(beta*r-b) #deprecated
    #mmin,mmax=np.min(r),np.max(r)
    #stretch=(r-mmin)/(mmax-mmin)*255 #linear stretch is unsatisfactory
    for i in range(r.shape[-1]):
        r[...,i]=simplest_color_balance(r[...,i],0.01,0.01)
    return r.astype('uint8')


def retinex_gimp(img,sigmas=[12,80,250], weights=None,dynamic=2):
    '''refer to the implementation in GIMP, it improves the stretch operation based 
       on MSRCR, introduces mean and standard deviation, and a dynamic parameter to 
       eliminate chromatic aberration, experiments show that it works well. see 
       source code in https://github.com/piksels-and-lines-orchestra/gimp/blob/master \
       /plug-ins/common/contrast-retinex.c'''
    alpha=128
    gain=1
    offset=0
    img=img.astype('double')+1 #
    csum_log=np.log(np.sum(img,axis=2))
    msr=MultiScaleRetinex(img-1,sigmas , weights) #-1
    r=gain*(np.log(alpha*img)-csum_log[...,None])*msr+offset
    mean=np.mean(r,axis=(0,1),keepdims=True)
    var=np.sqrt(np.sum((r-mean)**2,axis=(0,1),keepdims=True)/r[...,0].size)
    mmin=mean-dynamic*var
    mmax=mean+dynamic*var
    stretch=(r-mmin)/(mmax-mmin)*255
    stretch[stretch>255]=255
    stretch[stretch<0]=0
    return stretch.astype('uint8')

### Multi-Scale Retinex with Chromaticity Preservation, see[4] Algorithm 2 in section 4

def retinex_MSRCP(img,sigmas=[12,80,250],s1=0.01,s2=0.01):
    '''compare to others, simple and very fast'''
    Int=np.sum(img,axis=2)/3
    Diffs=[]
    for sigma in sigmas:
        Diffs.append(np.log(Int+1)-np.log(gauss_blur(Int,sigma)+1))
    MSR=sum(Diffs)/3
    Int1=simplest_color_balance(MSR,s1,s2)
    B=np.max(img,axis=2)
    A=np.min(np.stack((255/(B+eps),Int1/(Int+eps)),axis=2),axis=-1)
    return (A[...,None]*img).astype('uint8')


def retinex_AMSR(img,sigmas=[12,80,250],weights =None):
    '''see Proposed Method ii in "An automated multi Scale Retinex with Color 
       Restoration for image enhancement"(doi: 10.1109/NCC.2012.6176791)'''
    img=img.astype('double')+1 #
    msr=MultiScaleRetinex(img-1,sigmas,weights,flag=False) #
    y=0.05
    for i in range(msr.shape[-1]):
        v,c=np.unique((msr[...,i]*100).astype('int'),return_counts=True)
        sort_v_index=np.argsort(v)
        sort_v,sort_c=v[sort_v_index],c[sort_v_index] #plot hist
        zero_ind=np.where(sort_v==0)[0][0]
        zero_c=sort_c[zero_ind]
        #
        _=np.where(sort_c[:zero_ind]<=zero_c*y)[0]
        if len(_)==0:
            low_ind=0
        else:
            low_ind=_[-1]
        _=np.where(sort_c[zero_ind+1:]<=zero_c*y)[0]
        if len(_)==0:
            up_ind=len(sort_c)-1
        else:
            up_ind=_[0]+zero_ind+1
        #
        low_v,up_v=sort_v[[low_ind,up_ind]]/100 #low clip value and up clip value
        msr[...,i]=np.maximum(np.minimum(msr[:,:,i],up_v),low_v)
        mmin=np.min(msr[...,i])
        mmax=np.max(msr[...,i])
        msr[...,i]=(msr[...,i]-mmin)/(mmax-mmin)*255
    msr=msr.astype('uint8')
    return msr
    '''step of color restoration, maybe all right
    r=(np.log(125*img)-np.log(np.sum(img,axis=2))[...,None])*msr
    mmin,mmax=np.min(r),np.max(r)
    return ((r-mmin)/(mmax-mmin)*255).astype('uint8')
    '''



