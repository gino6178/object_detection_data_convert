from data_convert import csv_to_xml

csv_file = "csv/example.csv"
image_path = 'image/'
saved_xml_path = "convert_xml/"

csv_to_xml(csv_file, image_path, saved_xml_path, check_data=True)
