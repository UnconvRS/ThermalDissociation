"""
a python module for the image classes
"""
import pathlib
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import imutils
import copy

# import in-house modules
from modules.crystal import sIcrystal

# a class for the image object
class image:
    # specify the threshold for capturing the templates within the image
    matching_thr=0.5

    def __init__(self,img_path):
        self.sICrystals=[]
        self.img_path=img_path 
        self.img_filename= pathlib.Path(self.img_path).stem
        try:
            self.imgRGB=cv2.imread(self.img_path)
        except Exception as e:
            print(f"following exception occured while reading the image file: {e}")
        else:
            self.gray_img=cv2.cvtColor(self.imgRGB,cv2.COLOR_BGR2GRAY)
            self.img_w, self.img_h = self.gray_img.shape[::-1]
        


    def __OptimalScaleforTemplMatching(self,tmpl):
        # store width and height of template in w and h
        tW, tH = tmpl.gray_img.shape[::-1]

        self.optimalScale_tmplMatch=None
        # loop over the scales of the image
        for scale in np.linspace(0.2,2.0,20)[::-1]:
            # resize the image according to the scale, and keep track
		    # of the ratio of the resizing
            resized_img = imutils.resize(self.gray_img, width = int(self.gray_img.shape[1] * scale))

            r = self.gray_img.shape[1] / float(resized_img.shape[1])

            # if the resized image is smaller than the template, then break from the loop
            if resized_img.shape[0]<tH or resized_img.shape[1]<tW:
                break
                
            # detect edges in the resized, grayscale image and apply template-matching to find the template in the image
            edged = cv2.Canny(resized_img,50,200)
            result=cv2.matchTemplate(resized_img,tmpl.gray_img,cv2.TM_CCOEFF_NORMED)
            (_,maxVal,_,maxLoc)=cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then update
		    # the bookkeeping variable
            if self.optimalScale_tmplMatch is None or maxVal > self.optimalScale_tmplMatch[0]:
                self.optimalScale_tmplMatch = (maxVal, maxLoc, r)



    def TemplateMatching(self,tmpl):

        # fnid optimal image size ratio for template matching using the template image
        self.__OptimalScaleforTemplMatching(tmpl)

        # store width and height of template in w and h
        w, h = tmpl.gray_img.shape[::-1]
        # Perform match operations.
        # resize the image first using the optimal image size ratio
        resized_img = imutils.resize(self.gray_img, width = int(self.gray_img.shape[1] * (1/self.optimalScale_tmplMatch[2])))

        # resize the colored version for visualization purposes
        resized_img_color= imutils.resize(self.imgRGB, width = int(self.gray_img.shape[1] * (1/self.optimalScale_tmplMatch[2])))

        # find the matched templates
        res = cv2.matchTemplate(resized_img, tmpl.gray_img, cv2.TM_CCOEFF_NORMED)
        
        # store the coordinates of matched area in a numpy array
        loc = np.where(res >= self.matching_thr)

        # draw a rectangle around the matched region.
        ctrs={"x":[],"y":[]}
        mask = np.zeros(resized_img_color.shape[: 2], np.uint8) # altered the self.imgRBG to resized_img_color

        # determine the centroid of the matches found
        for pt in zip(*loc[::-1]):
            if mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))] != 255:
                mask[pt[1]: pt[1] + h, pt[0]: pt[0] + w] = 255
                cv2.rectangle( resized_img_color, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2) # draw rectangles around the matched crystals 
                # Get the centroid of the matched patterns
                sIcryst=sIcrystal()
                
                Xcentroid=pt[0]+w/2
                Ycentroid=pt[1] + h/2
                sIcryst.Xcentroid=Xcentroid
                sIcryst.Ycentroid=Ycentroid
                self.sICrystals.append(sIcryst)

                ctrs["x"].append(Xcentroid)
                ctrs["y"].append(Ycentroid)
                #cv2.circle( resized_img_color, (int(Xcentroid),int(Ycentroid)), radius=0, color=(255, 0, 0), thickness=4)

        
        self.numSiCrystals=len(self.sICrystals)

        # Show the final image with the matched area.

        #cv2.imshow('Detected', resized_img_color)
        # save the image and the matched templates
        #cv2.imwrite('template_matched_image'+self.img_filename+'.png',resized_img_color)
        #plt.imshow(resized_img)
        #plt.pause(0.000001)

