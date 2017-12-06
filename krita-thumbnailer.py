#!/usr/bin/env python3.5

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import argparse
from io import BytesIO
from PIL import Image
import os
from urllib.parse import urlparse, unquote
import zipfile

def main():
	# Extract arguments from the command line
	parser = argparse.ArgumentParser(description='Extract thumbnails from Krita files')
	parser.add_argument('-s', metavar='size', type=int, help='Maximum dimensions of thumbnail')
	parser.add_argument('input', help='Krita (.kra) file to process')
	parser.add_argument('output', help='Thumbnail file to save')
	args = parser.parse_args()

	# Input and output files can be filenames, or file:// url which may include quoted spaces
	# Convert these to absolute paths
	parse_input = urlparse(unquote(args.input))
	path_input = os.path.abspath(os.path.join(parse_input.netloc, parse_input.path))

	parse_output = urlparse(unquote(args.output))
	path_output = os.path.abspath(os.path.join(parse_output.netloc, parse_output.path))

	# Open the zip file and read the data
	with zipfile.ZipFile(path_input) as inputfile:
		data = inputfile.read('preview.png')
		if args.s is None:
			# Store image without resizing
			with open(path_output, 'wb') as outputfile:
				outputfile.write(data)
		else:
			# Scale image
			size = args.s, args.s
			with Image.open(BytesIO(data)) as image:
				image.thumbnail(size)
				image.save(path_output)

if __name__ == '__main__':
	main()
