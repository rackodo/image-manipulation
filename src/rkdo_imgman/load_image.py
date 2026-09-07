from PIL import Image

# make callable class
class ImageRender:
	def __init__(self, path):
		self.im = Image.open( path ) # source image
		self.wsize, self.ysize = self.im.size

		self.offset = 0 # the offset according to image width
		self.chunks = 10 # how many columns should be sorted at any given time, before the image is returned

	# apply a pixel sort to the image up to a set column according to self.chunks, then return
	# this allows for iterative sorting that can be retrieved over time
	def updateImage(self):
		for _ in range(self.chunks):
			if self.offset >= self.wsize:
				return self.im

			# get a single column of pixels and turn them into rgba values
			inCol = self.im.crop((self.offset, 0, self.offset + 1, self.ysize))
			inPix = list(inCol.getdata())

			# sort according to an rgba value. r = p[0], g = p[1], b = p[2], a = p[3]
			inSort = sorted(inPix, key=lambda p: p[0])

			# create a temporary image for the sorted column, then place the sorted pixels
			outCol = Image.new(inCol.mode, (1, self.ysize))
			outCol.putdata(inSort)

			# paste the sorted portion over the original image
			self.im.paste(outCol, (self.offset, 0))
			self.offset += 1

		return self.im



