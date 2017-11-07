# USAGE
# python scan.py --image images/page.jpg 

# import the necessary packages
from __future__ import print_function
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
import numpy as np
import argparse
import cv2

#Manual Contours
man_contours = []

#Handles the on_click event for setMouseCallBack
def on_click(event,x,y,flags,param):

	global image,man_contours

	if event == cv2.EVENT_LBUTTONDOWN:
		print("******You pressed -->({0},{1})".format(x,y))
		man_contours.append([x,y])

		#Found 4 contours..
		if len(man_contours)==4:
			print("*****Found 4 Contours :",man_contours)
			
			#Line drawing feature...
			# Drawing Polygon

			# To draw a polygon, first you need coordinates of vertices. Make those points into an array of shape ROWSx1x2 where ROWS are number of vertices and it should be of type int32. Here we draw a small polygon of with four vertices in yellow color.
			#pts = np.array(man_contours)
			#pts = pts.reshape((-1,1,2))
			#cv2.polylines(image,[pts],True,(0,255,255))
			#cv2.imshow("image", image)
			#     pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
			#     pts = pts.reshape((-1,1,2))
			#     cv2.polylines(img,[pts],True,(0,255,255))
			
	return


#Manually pick contours for Edge Detection
def pick_contours():

	global image,man_contours

	print("\n\n*********Manually Finding Contours, click on 4 corners to select a Region***********")

	#Create a window and setMouseCallback
	cv2.namedWindow("image",cv2.WINDOW_NORMAL)
	cv2.setMouseCallback("image",on_click)

	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF
		#print(type(key))
		#print(key,"Key")
		if key == ord('q'):
			break

	print("****Finished Finding Contours******")




def main():
	global image, screenCnt
	screenCnt = []
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required = True,
		help = "Path to the image to be scanned")
	args = vars(ap.parse_args())

	# load the image and compute the ratio of the old height
	# to the new height, clone it, and resize it
	image = cv2.imread(args["image"])
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)

	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)

	# show the original image and the edge detected image
	print("STEP 1: Edge Detection")
	cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
	cv2.imshow("Image", image)
	cv2.namedWindow("Edged",cv2.WINDOW_NORMAL)
	cv2.imshow("Edged", edged)
	cv2.imwrite("Edged.jpg",edged)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:15]

	# loop over the contours
	for c in cnts:
		# approximate the contour
		
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		#print(approx)
		#print(type(approx))
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break

	#If 4 contours not found..
	if len(screenCnt)!=4:
		print("******Automatic Edge Detection Failed*******")
		pick_contours()
		#man_contours = [[114, 42], [108, 479], [748, 475], [742, 42]]
		screenCnt = np.array(man_contours)
		#print(type(screenCnt),"From screenCnt")

	# show the contour (outline) of the piece of paper
	print("STEP 2: Find contours of paper")
	cv2.namedWindow("Outline",cv2.WINDOW_NORMAL)
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 7)
	cv2.imshow("Outline", image)
	cv2.imwrite("Outline.jpg",image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2)*ratio)
	#cv2.imshow("Perspective Image",warped)
	cv2.imwrite("Corrected Perspective.jpg",warped)
	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)


	warped_blur = cv2.medianBlur(warped,5)
	# thresholdValue = threshold_otsu(gray_blur, 256)
	# ret3,warped = cv2.threshold(gray_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	warped = cv2.adaptiveThreshold(warped_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
			cv2.THRESH_BINARY,3,2)

	#print(type(warped))
	#cv2.imwrite(warped,"MedianBlur1.bmp")
	# warped = gray_blur > thresholdValue
	# warped = warped.astype("uint8") * 255

	# show the original and scanned images
	
	print("STEP 3: Apply perspective transform")
	cv2.namedWindow("Original",cv2.WINDOW_NORMAL)
	cv2.imshow("Original", orig)
	cv2.imwrite("Original.jpg",orig)
	cv2.namedWindow("Scanned2",cv2.WINDOW_NORMAL)
	cv2.imshow("Scanned2", warped)
	cv2.imwrite("Final.jpg",warped)

	cv2.waitKey(0)

if __name__=='__main__':
	main()