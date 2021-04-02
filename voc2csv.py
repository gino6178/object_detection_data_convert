from data_convert import xml_to_csv

annotation_path = 'xml/'
image_path = 'image/'
saved_csv_path = 'convert_csv/convert.csv'

xml_to_csv(annotation_path, image_path, saved_csv_path, check_data=True)
