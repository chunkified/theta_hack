import exifread

path_name = './'
# Open image file for reading (binary mode)
f = open(path_name, 'rb')

# Return Exif tags
tags = exifread.process_file(f)