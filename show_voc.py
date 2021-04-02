import xml.etree.ElementTree as ET
import glob
import cv2

annotation_path = 'xml/'
image_path = 'image/'

for xml_file in glob.glob(annotation_path + '/*.xml'):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    bbox_set = []

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
        bbox_set.append([xmin, ymin, xmax, ymax, label])

    jpg_file = image_path + filename
    img = cv2.imread(jpg_file)
    height, _, _ = img.shape
    for bbox in bbox_set:
        xmin = int(bbox[0])
        ymin = int(bbox[1])
        xmax = int(bbox[2])
        ymax = int(bbox[3])
        label = str(bbox[4])
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        text_size = ((ymax - ymin) / height)*10
        text_offset = int((ymax - ymin)/10)
        cv2.putText(img, label, (xmin, ymin-text_offset), cv2.FONT_HERSHEY_SIMPLEX,
                    text_size, (255, 0, 0),  1, cv2.LINE_AA)
    cv2.imshow('show img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
