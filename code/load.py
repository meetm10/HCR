import numpy as np
import os
import xml.etree.ElementTree as ET
import pdb

'''
The class is used to load data
'''

class loadData:
    def __init__(self):
        pass

    
    def load(self, file_location, file_xml_location):
        '''
        The method is used to load data as line images(i.e image is an entire line)
        '''

        list_xml= os.listdir(file_xml_location)
        list_dir = os.listdir(file_location)
        list_data=[]
        total_text = ""
        dict_data = {}
        thresh_dict = {}
        for i in range(len(list_dir)):
            file_location_subdir =  file_location + list_dir[i]
            list_sub_dir = os.listdir(file_location_subdir)
            for j in range (len(list_sub_dir)):
                list_files_subdir = os.listdir(file_location_subdir + "/" + list_sub_dir[j])
                xml_file = file_xml_location + list_sub_dir[j] + '.xml'
                tree = ET.parse(xml_file)
                root = tree.getroot()
                count= 0
                for tag in root.iter('line'):
                    thresh_line = tag.attrib['threshold']
                    line_data = ""
                    for sub_tag in tag.iter('word'):
                        line_data += sub_tag.attrib['text'] + " "
                    if count >= 10:
                        img_file = list_sub_dir[j] + '-' + str(count)+'.png'
                    else:
                        img_file = list_sub_dir[j] + '-'+'0'+str(count)+'.png'
                    img_path = file_location_subdir + "/" + list_sub_dir[j] + "/" + img_file
                    list_data.append(img_path)
                    dict_data[img_path] = line_data
                    thresh_dict[img_path] = thresh_line
                    total_text +=line_data
                    count = count + 1
              
        chars = set(total_text)
        return dict_data,thresh_dict,chars,list_data
    


    
    def loadData_word(self, file_location, file_xml_location):

        '''
        The method is used to load data as word images rather than lines (i.e each image is a word)
        '''
        list_xml= os.listdir(file_xml_location)
        list_dir = os.listdir(file_location)
        list_data=[]
        total_text = ""
        dict_data = {}
        thresh_dict = {}
        for i in range(len(list_dir)):
            file_location_subdir =  file_location + list_dir[i]
            list_sub_dir = os.listdir(file_location_subdir)
            for j in range (len(list_sub_dir)):
                list_files_subdir = os.listdir(file_location_subdir + "/" + list_sub_dir[j])
                xml_file = file_xml_location + list_sub_dir[j] + '.xml'
                tree = ET.parse(xml_file)
                root = tree.getroot()
                count= 0
                count_line=0
                for tag in root.iter('line'):
                    thresh_line = tag.attrib['threshold']
                    line_data = ""
                    count_word=0
                    for sub_tag in tag.iter('word'):
                        
                        #Hackish solution to corrupt data
                        if sub_tag.attrib['id'] == "a01-117-05-02":
                            print("Found culprit")
                            continue
                                                        
                        word = sub_tag.attrib['text'] 
                        if count_line>=10:
                            str_count_line = '-' + str(count_line) 
                        else:
                            str_count_line = '-0' + str(count_line)
 
                        if count_word >= 10:
                            img_file = list_sub_dir[j] + str_count_line + '-' + str(count_word)+'.png'
                        else:
                            img_file = list_sub_dir[j] + str_count_line + '-'+'0'+str(count_word)+'.png'

                        img_path = file_location_subdir + "/" + list_sub_dir[j] + "/" + img_file
                        list_data.append(img_path)
                        dict_data[img_path] = word
                        thresh_dict[img_path] = thresh_line 
                        count_word +=1
                        total_text+= word
                    count_line+=1
                    count = count + 1
       
        chars = set(total_text)          
        return dict_data,thresh_dict,chars,list_data
