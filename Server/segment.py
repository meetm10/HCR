import numpy as np
import cv2


def main():
	#Load the image..
	image = cv2.imread('Original.jpg')
	
	#print(image)

	inverted_image = ~image

	#print(inverted_image)
	cv2.imwrite("Inverted.jpg",inverted_image)

	# Create images used to extract horizontal and 
	# Vertical lines..
	horizontal = inverted_image.copy()
	#vertical = inverted_image.copy()


	#print(type(horizontal))

	#Sepcify horizontal axis..
	cols = horizontal.shape[1]
	#print(type(horizontal.size))
	rows = horizontal.shape[0]

	horizontal_size = cols // 100
	
	#Create a structuring element..
	horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size,1))

	#Apply morphology operations
	horizontal = cv2.erode(horizontal, horizontal_structure)
	horizontal = cv2.dilate(horizontal, horizontal_structure)

	
	cv2.imwrite("Horizontal.jpg",horizontal)

	#Horizontal with additional processing..
	kernel = np.ones((1,20),np.uint8)
	d_im = cv2.dilate(horizontal, kernel, iterations = 1)
	e_im = cv2.erode(d_im, kernel, iterations = 1)

	cv2.imwrite("Horizontal-Processed.jpg",e_im)

if __name__=='__main__':
	main()