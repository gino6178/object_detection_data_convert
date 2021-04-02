import numpy as np
import pandas as pd
import cv2
import os

csv_file = "csv/example.csv"
image_path = 'image/'

total_csv_annotations = {}
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
    jpg_file = image_path + filename
    img = cv2.imread(jpg_file)
    height, _, _ = img.shape

    for bbox in labels:
        xmin = int(bbox[3])
        ymin = int(bbox[4])
        xmax = int(bbox[5])
        ymax = int(bbox[6])
        label = bbox[2]
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
        text_size = ((ymax - ymin) / height)*10
        text_offset = int((ymax - ymin)/10)
        cv2.putText(img, label, (xmin, ymin-text_offset), cv2.FONT_HERSHEY_SIMPLEX,
                    text_size, (255, 0, 0),  1, cv2.LINE_AA)
    cv2.imshow('show img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
