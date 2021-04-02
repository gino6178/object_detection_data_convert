# Object detection Data convert


This repository contains the conversion of common object detection formats, including the conversion of voc format and csv format
<br><br/>
You can use show_csv.py or show_voc.py to confirm that the annotations are correct
<br><br/>

csv format 


|  filename| width | height | class |  xmin  | ymin  |  xmax  |  ymax  |
|  ----    | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |
| 0_Parade_marchingband_1_5.jpg  | 1024 | 683 | face | 496 | 191 | 533 | 226 |

<br><br/>


## (1) 　voc to csv
    from data_convert import xml_to_csv

    annotation_path = 'xml/'
    image_path = 'image/'
    saved_csv_path = 'convert_csv/convert.csv'

    xml_to_csv(annotation_path, image_path, saved_csv_path, check_data=True)



## (2) 　csv to voc

    from data_convert import csv_to_xml

    csv_file = "csv/example.csv"
    image_path = 'image/'
    saved_xml_path = "convert_xml/"

    csv_to_xml(csv_file, image_path, saved_xml_path, check_data=True)



if check_data = True

(1) Check if the length and width are correct

(2) Check if the image data exists

(3) Check whether the bounding box is out of bounds
<br><br/>