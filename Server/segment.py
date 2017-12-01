import numpy as np
import cv2


def get_equation(p1,p2):


	#Calculate slope
	slope = (p2[1] - p1[1]) / (p2[0] - p1[0])

	c = p1[1] - slope*p1[0]

	return c

def add_new_line(c):

	seen = False
	
	#Check if the line is close to an existing line..
	for val in range(c-5,c+6):
		if val in seen_lines:
			seen = True
	
	#If it is not close to any of the existing lines..
	if not seen:
		#print("***Line:",c)
		seen_lines.add(c)
		distances.append(first_line-c)

	return

def main():
	global distances, seen_lines, first_line
	#Load the image..
	image = cv2.imread('Binarized.jpg')
	
	#print(image)

	# inverted_image = ~image

	# #print(inverted_image)
	# cv2.imwrite("Inverted.jpg",inverted_image)

	# # Create images used to extract horizontal and 
	# # Vertical lines..
	# horizontal = inverted_image.copy()
	# #vertical = inverted_image.copy()


	# #print(type(horizontal))

	# #Sepcify horizontal axis..
	# cols = horizontal.shape[1]
	# #print(type(horizontal.size))
	# rows = horizontal.shape[0]

	# horizontal_size = cols // 100
	
	# #Create a structuring element..
	# horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size,1))

	# #Apply morphology operations
	# horizontal = cv2.erode(horizontal, horizontal_structure)
	# horizontal = cv2.dilate(horizontal, horizontal_structure)

	
	# cv2.imwrite("Horizontal.jpg",horizontal)

	gray = cv2.cvtColor(~image, cv2.COLOR_BGR2GRAY)

	# #Horizontal with additional processing..
	# kernel = np.ones((1,20),np.uint8)
	# d_im = cv2.dilate(horizontal, kernel, iterations = 1)
	# e_im = cv2.erode(d_im, kernel, iterations = 1)

	# cv2.imwrite("Horizontal-Processed.jpg",e_im)

	edged = cv2.Canny(gray, 75, 100)

	cv2.imwrite("Edged2.jpg",edged)

	lines = cv2.HoughLines(edged,0.08,np.pi/180,threshold = 100)

#	print(lines.shape)
#	print(type(lines))
#	print(lines)

	seen_lines = set()

	first_line = None

	distances = []

	for i in range(30):
		for rho,theta in lines[i]:
			#print(rho,theta)
			a = np.cos(theta)
			b = np.sin(theta)

			x0 = a*rho
			y0 = b*rho

			x1 = int(x0 + 3000*(-b))
			y1 = int(y0 + 3000*(a))
			x2 = int(x0 - 3000*(-b))
			y2 = int(y0 - 3000*(a))

			#Skip vertical lines..
			if (x2==x1):
				continue

			print(x1,y1,x2,y2)

			#Equation of lines...
			c = int(get_equation([x1,y1],[x2,y2]))


			if not first_line:
				first_line = c

			add_new_line(c)
			
			if len(distances)==0:
				cv2.line(image, (x1,y1),(x2,y2),(0,255,0),3)
				print("Detected First Line..")
			elif distances[-1] == 85.0:
				cv2.line(image, (x1,y1),(x2,y2),(0,0,255),3)

	distances.sort()
	for i in range(len(distances)):
		if distances[i]==0:
			inter_line_dist = distances[i+1]
		print(distances[i])

	print("*******inter_line_dist = ",inter_line_dist)
	#Print all lines
	cols = image.shape[1]
	print("cols = ",cols)
	c = first_line
	print("c = ",c)
	for _ in range(30):
		x1 = 0
		y1 = int(c)
		x2 = 3000
		y2 = int(c)
		cv2.line(image, (x1,y1),(x2,y2),(0,0,255),3)
		c+=inter_line_dist
		print(x1,y1,x2,y2)

	c = first_line
	for _ in range(30):
		x1 = 0
		y1 = int(c)
		x2 = 3000
		y2 = int(c)
		cv2.line(image, (x1,y1),(x2,y2),(0,0,255),3)
		c-=inter_line_dist
		print(x1,y1,x2,y2)

	cv2.imwrite('HoughLines4.jpg',image)



if __name__=='__main__':
	main()