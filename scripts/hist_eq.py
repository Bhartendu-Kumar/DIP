



import  cv2 as cv



#hist equalization
def hist_eq(img , parameter_list):


    if len(img.shape) == 3:
        img[:,:,0] = cv.equalizeHist(img[:,:,0])
        img[:,:,1] = cv.equalizeHist(img[:,:,1])
        img[:,:,2] = cv.equalizeHist(img[:,:,2])
        return img


    img = cv.equalizeHist(img)
    return img




#clahe





