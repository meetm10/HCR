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
			
	return


#Manually pick contours for Edge Detection
def pick_contours():
	global image,man_contours

	print("\n\n*********Manually Finding Contours, click on 4 corners to select a Region***********")

	#Create a window and setMouseCallback
	cv2.namedWindow("Original_Image",cv2.WINDOW_NORMAL)
	cv2.setMouseCallback("Original_Image",on_click)

	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("Original_Image", image)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break

	print("****Finished Finding Contours******")

	return

def main():
	global image, screenCnt
	
	#ScreenCountours..
	screenCnt = []
	
	# construct the argument parser and parse the arguments
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-i", "--image", required = True,
	#	help = "Path to the image to be scanned")
	#args = vars(ap.parse_args())

	# load the image and compute the ratio of the old height
	# to the new height, clone it, and resize it
<<<<<<< HEAD
	name = raw_input("Enter file name: ")
	image = cv2.imread("Images/"+name)
	#image = cv2.imread(args["image"])
=======

	image = cv2.imread(args["image"])
	if image is None:
		print("******Failed to load Image*******")
		exit(0)

>>>>>>> e526806a5fe3f5e71cab00f21f18d1f269b371bb
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)
	outline = image.copy()

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

	
	#Flag for automatic edge detection..
	auto = False

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			auto = True
			break

	#If 4 contours not found..
	if auto:
		# show the contour (outline) of the piece of paper
		print("STEP 2: Find contours of paper")
		cv2.namedWindow("Outline",cv2.WINDOW_NORMAL)
		cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 4)
		cv2.imshow("Outline", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		print("Is the Output Satisfactory? \nDo you want to pick Contours Manully? Y/N : ", end="")
		response = input()
		if response.upper()=="Y":
			#Reset the image
			image = outline
			pick_contours()
			screenCnt = np.array(man_contours)
			cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
			cv2.namedWindow("Outline",cv2.WINDOW_NORMAL)
			cv2.imshow("Outline", image)
			cv2.imwrite("Outline.jpg",image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	else:
		print("******Automatic Edge Detection Failed*******")
		pick_contours()
		screenCnt = np.array(man_contours)
		cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
		cv2.namedWindow("Outline",cv2.WINDOW_NORMAL)
		cv2.imshow("Outline", image)
		cv2.imwrite("Outline.jpg",image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	
	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2)*ratio)

	cv2.imwrite("Corrected Perspective.jpg",warped)

	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	# cv2.imshow("GrayScale",gray_warped)
	# cv2.waitKey(0)

	gray_warped_blur = cv2.medianBlur(gray_warped,5)
	# cv2.imshow("Blurred",gray_warped_blur)
	# cv2.waitKey(0)

	# thresholdValue = threshold_otsu(gray_blur, 256)
	# ret3,warped = cv2.threshold(gray_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	binarized = cv2.adaptiveThreshold(gray_warped_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
										cv2.THRESH_BINARY,3,2)

	# show the original and scanned images
	print("STEP 3: Apply perspective transform")
	cv2.imwrite("Original.jpg",orig)
	cv2.namedWindow("Scanned",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Scanned",width=500,height = 500)
	cv2.imshow("Scanned", binarized)
	cv2.imwrite("Binarized.jpg",binarized)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__=='__main__':
	main()
