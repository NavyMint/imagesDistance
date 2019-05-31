import numpy as np
from PIL import Image
from PIL import ImageChops
from PIL import ImageChops
from PIL import ImageFilter
import sys
import os
import glob

dir = sys.argv[1]
print(dir)
if (os.path.isdir(dir)):
    print ("Directory path exists ", dir)
else:
	print ("Cannot find directory")


# realization of duplicates search without numpy

def listOfImg(path):
	image_list = []
	for filename in glob.glob(path): #assuming all jpg 
		im=Image.open(filename)
		image_list.append(im)
	return image_list

def duplicatesFunc1(dir):
	image_list = listOfImg(dir+'/*.jpg')
	print(len(image_list))
	
	for particularImg in image_list:
		if (len(image_list)>1):
			for indx in range(1, len(image_list)):
				if(particularImg.filename != image_list[indx].filename):
					resultBound =  ImageChops.difference(particularImg, image_list[indx]).getbbox()
					if resultBound is None :
							print ('Duplicates ', particularImg.filename, ' and ', image_list[indx].filename)				
		#image_list.remove(particularImg)
			

def dist(x,y):
	#print ("Array 1: ", x)
	#print ("Array 2: ", y)
	return (np.sum((x-y)**2))**0.5
	#return np.sqrt(np.sum([(a - b) ** 2 for a, b in zip(x, y)]))
	
def findDistance(img1,img2):
	imgArr1 = np.array(img1.getdata())
	imgArr2 = np.array(img2.getdata())
	if(imgArr1.shape==imgArr2.shape):
		return abs(np.floor(dist(imgArr1, imgArr2)))
	else:
		#print("Shape don`t match")
		return -1
	
	

def duplicatesFunc2(dir):
	image_list = listOfImg(dir +'/*.jpg')
	
	for particularImg in image_list:
		if len(image_list)>1:
			for indx in range(1, len(image_list)):
				if(particularImg.filename != image_list[indx].filename):
				
					actualDistance = findDistance(particularImg,image_list[indx])	
					#print(actualDistance)
						
					if actualDistance==0:
						print ('Duplicates ', particularImg.filename, image_list[indx].filename)	
							
					else:
					#commented due to Nan distance result in case of completely different images
					
						#newSize = (np.minimum(particularImg.size[0], image_list[indx].size[0]), np.minimum(particularImg.size[1], image_list[indx].size[1]))
						#resizedImg1 = particularImg.resize(newSize, resample=Image.ANTIALIAS)
						#resizedImg2 = image_list[indx].resize(newSize, resample=Image.ANTIALIAS)
						
						resizedImg1 = particularImg.resize((50,50), resample=Image.ANTIALIAS)
						resizedImg2 = image_list[indx].resize((50,50), resample=Image.ANTIALIAS)
							
						actualDistance = findDistance(resizedImg1, resizedImg2)
							
						#print('Actual distance between images after resize ', actualDistance)
						
						if (actualDistance==0 or actualDistance < 500):
							print('Probable modification ', particularImg.filename, image_list[indx].filename )
			image_list.remove(particularImg)
			
			
def findBlurred(dir):
	image_list = listOfImg(dir+'/*.jpg')
	for particularImg in image_list:
		if len(image_list)>1:
			for indx in range(1, len(image_list)):
				if(particularImg.filename != image_list[indx].filename):
				
					actualDistance = findDistance(particularImg,image_list[indx])	
					#print(actualDistance)
						
					if actualDistance==0:
						print ('Duplicates ', particularImg.filename, image_list[indx].filename)	
							
					else:
						image1 = particularImg.resize((300,300), resample=Image.ANTIALIAS).convert(mode='L')
						image2 = image_list[indx].resize((300,300), resample=Image.ANTIALIAS).convert(mode='L')
						distResList = []
						for i in range(30):					
							imageBlurred = image1.filter(ImageFilter.GaussianBlur(i))
							img1Arr = np.array(imageBlurred.getdata())
							img2Arr = np.array(image2.getdata())
								
							if(img1Arr.shape==img2Arr.shape):
								distRes = dist(img1Arr, img2Arr);
								if (len(distResList)<=1):
									distResList.append(distRes)
								else :
									distResList[1]=distRes
									print(distResList)
									
								if distRes < 2000:
									print("Modification, probably blurred ", particularImg.filename, image_list[indx].filename)
									break
								elif len(distResList)>1:
									if(distResList[-1]<distResList[0]):
										#print("Continue, new distance less then previously")
										continue
								else:
									#print("Break, new distance more then previously, switch blurring of images")
										
									distResList = []
									imageBlurred = image2.filter(ImageFilter.GaussianBlur(i))
									img1Arr = np.array(image1.getdata())
									img2Arr = np.array(imageBlurred.getdata())
									if(img1Arr.shape==img2Arr.shape):
										distRes = dist(img1Arr, img2Arr);
										if (len(distResList)<=1):
											distResList.append(distRes)
										else :
											distResList[1]=distRes
											print(distResList)
													
										if distRes < 2000:
											#print("Modification, probably blurred ", particularImg.filename, image_list[indx].filename)
											break
										else: 
											#print("Images different")
											break
										
										
										
			
print("Results for first realization of function. It will print only duplicates")		
duplicatesFunc1(dir)
print("Result for blurred distance function . It should print blurred modifications and duplicates")
findBlurred(dir)
print("Result for second realization of function. It should print duplicates and size modifications")
duplicatesFunc2(dir)


