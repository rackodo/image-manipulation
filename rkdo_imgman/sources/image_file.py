from PIL import Image

def ImageFromFile(path):
	im = Image.open(path)
	im = im.convert("RGB")
	return im