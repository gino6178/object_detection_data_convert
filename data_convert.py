import glob
import xml.etree.ElementTree as ET
import pandas as pd
import cv2
import os
import codecs
import numpy as np


def xml_to_csv(annotation_path, image_path, saved_csv_path, check_data=True):
    xml_list = []
    miss_file_list = []
    for xml_file in glob.glob(annotation_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            filename = root.find('filename').text
            width = int(root.find('size')[0].text),
            height = int(root.find('size')[1].text),
            bbox = member.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            label = member.find('name').text

            if check_data:
                jpg_file = image_path + filename
                if os.path.isfile(jpg_file):
                    img = cv2.imread(jpg_file)
                    img_height, img_width, img_channels = img.shape
                    # check width and height
                    if height != img_height:
                        height = img_height
                    if width != img_width:
                        width = img_width
                    # check bounding box
                    if xmin < 0 or xmin > xmax or xmin > width:
                        print(filename + ' data xmin is wrong')
                    if xmax < 0 or xmax < xmin or xmax > width:
                        print(filename + ' data xmax is wrong')
                    if ymin < 0 or ymin > ymax or ymin > height:
                        print(filename + ' data ymin is wrong')
                    if ymax < 0 or ymax < ymin or ymax > height:
                        print(filename + ' data ymax is wrong')
                elif jpg_file not in miss_file_list:
                    miss_file_list.append(jpg_file)
                    print('There is no ' + filename + ' data')

            value = (
                filename, width, height, label, xmin, ymin, xmax, ymax
            )
            xml_list.append(value)
    column_name = [
        'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'
    ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv(saved_csv_path, index=None)
    print('Successfully converted xml to csv')


def csv_to_xml(csv_file, image_path, saved_xml_path, check_data=True):

    total_csv_annotations = {}
    miss_file_list = []

    annotations = pd.read_csv(csv_file, header=None).values
    for annotation in annotations:
        key = annotation[0].split(os.sep)[-1]
        value = np.array([annotation[1:]])
        if key in total_csv_annotations.keys():
            total_csv_annotations[key] = np.concatenate(
                (total_csv_annotations[key], value), axis=0)
        else:
            total_csv_annotations[key] = value

    for filename, labels in total_csv_annotations.items():

        width = labels[0][0]
        height = labels[0][1]

        if check_data:
            jpg_file = image_path + filename
            if os.path.isfile(jpg_file):
                img = cv2.imread(jpg_file)
                img_height, img_width, img_channels = img.shape
                # check width and height
                if height != img_height:
                    height = img_height
                if width != img_width:
                    width = img_width
            elif jpg_file not in miss_file_list:
                miss_file_list.append(jpg_file)
                print('There is no ' + filename + ' data')

        # def the xml name
        if filename.endswith('.jpg'):
            xml_filename = filename.replace(".jpg", ".xml")
        elif filename.endswith('.png'):
            xml_filename = filename.replace(".png", ".xml")
        else:
            print('have to check ' + filename + ' end with')

        # write xml
        with codecs.open(saved_xml_path + xml_filename, "w", "utf-8") as xml:
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + ' ' + '</folder>\n')
            xml.write('\t<filename>' + filename + '</filename>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database> </database>\n')
            xml.write('\t\t<annotation> </annotation>\n')
            xml.write('\t\t<image>NULL</image>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t</source>\n')
            xml.write('\t<owner>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t\t<name>NULL</name>\n')
            xml.write('\t</owner>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>' + str(img_width) + '</width>\n')
            xml.write('\t\t<height>' + str(img_height) + '</height>\n')
            xml.write('\t\t<depth>' + str(img_channels) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            if isinstance(labels, float):
                xml.write('</annotation>')
                continue
            for label_detail in labels:
                xmin = int(label_detail[3])
                ymin = int(label_detail[4])
                xmax = int(label_detail[5])
                ymax = int(label_detail[6])
                label = label_detail[2]

                if check_data:
                    # check bounding box
                    if xmin < 0 or xmin > xmax or xmin > width:
                        print(filename + ' data xmin is wrong')
                    if xmax < 0 or xmax < xmin or xmax > width:
                        print(filename + ' data xmax is wrong')
                    if ymin < 0 or ymin > ymax or ymin > height:
                        print(filename + ' data ymin is wrong')
                    if ymax < 0 or ymax < ymin or ymax > height:
                        print(filename + ' data ymax is wrong')

                xml.write('\t<object>\n')
                xml.write('\t\t<name>'+label+'</name>\n')
                xml.write('\t\t<pose>Unspecified</pose>\n')
                xml.write('\t\t<truncated>1</truncated>\n')
                xml.write('\t\t<difficult>0</difficult>\n')
                xml.write('\t\t<bndbox>\n')
                xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                xml.write('\t\t</bndbox>\n')
                xml.write('\t</object>\n')
                # print(filename, xmin, ymin, xmax, ymax, label)
            xml.write('</annotation>')
