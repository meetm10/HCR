import cv2
import shelve
import os
import numpy as np

with shelve.open('shelved_data/IAM_Data','c') as shelf:
	#image_labels = shelf['image_labels']
	#threshold_dict = shelf['image_thresholds']
	#chars = shelf['chars']
	image_paths = shelf['list_of_images']

#max_height = 310
heights = []
widths = []


for image_path in image_paths:

	#binary_path = binarized_prefix+image_path
	
	#new_path = padded_prefix + image_path

	#directory = os.path.dirname(new_path)
	
	#print(directory)
	
	#Does directory exist
	#if not os.path.exists(directory):
	#	os.makedirs(directory)

	#Does image_exits
# 	if os.path.exists(new_path):
# 		print("Image already exists....")
# 		continue

# 	elif image_path in ["Words/r06/r06-022/r06-022-03-05.png","Words/a01/a01-117/a01-117-05-02.png","Words/r02/r02-060/r02-060-08-05.png"
# ] :
# 		print("Found_culprit")
# 		continue

	# print(image_path)
	# print(binary_path)
	# print(new_path)	

	image = cv2.imread(image_path)
	#gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	image_height,image_width,_ = image.shape
	heights.append(image_height)
	widths.append(image_width)


	#padding = max_height - image_height

	# padding_top = int(padding/2)
	# padding_bottom = padding - padding_top

	# #Add Padding
	# pad_top_array = np.zeros((padding_top,image_width))
	# pad_top_array.fill(255)
	# pad_bottom_array = np.zeros((padding_bottom,image_width))
	# pad_bottom_array.fill(255)

	#print(gray_image,pad_top_array)
	# intermediate = np.insert(gray_image,0,pad_top_array,axis=0)
	# padded_image = np.append(intermediate,pad_bottom_array,axis=0)

	#cv2.imshow(new_image)
	#cv2.imwrite(new_path,padded_image)

print(len(widths))
print(len(heights))

with shelve.open('widths_and_heights','c',writeback=True) as shelf:
	shelf['widths'] = widths
	shelf['heights'] = heights