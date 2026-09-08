import argparse

from rkdo_imgman.view_image import Viewer

parser = argparse.ArgumentParser()

parser.add_argument("image", help="Image file", type=str)

args = parser.parse_args()

if not args.image:
	print("No image provided")
else:
	view = Viewer(500, 500, args.image)
	view.start()