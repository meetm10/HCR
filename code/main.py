from load import loadData
import cv2
import joblib

images = 'Lines/'
xml = 'XML_Data/'
shelve_loc = 'shelved_data/'

data = loadData()



# for image_path in to_remove:
# 	list_data.remove(image_path)
# 	dict_data.pop(image_path)
# 	thresh_dict.pop(image_path)

#Dictionary:

#pad_prefix = "Padded_"

print(len(list_data))

image_arrays = { image_path : cv2.imread(pad_prefix+image_path,cv2.IMREAD_GRAYSCALE) for image_path in list_data }

#print("Done saving Image_labels,chars and list_of_images")

joblib.dump(image_arrays,"shelved_data/image_arrays",compress=True)

#print(image_arrays)

#print(list_data)
# print(thresh_dict)
