from PIL import Image

# make callable class
class Sorter:
	def __init__(self, source, direction="vertical", chunks=10):
		self.source = source # source image
		self.wsize, self.ysize = self.source.size

		self.offset = 0 # the offset according to image width
		self.chunks = chunks # how many columns should be sorted at any given time, before the image is returned
		self.direction = direction.lower()

		if self.direction not in ("vertical", "horizontal"):
			raise ValueError("direction must be 'vertical' or 'horizontal'")

	# apply a pixel sort to the image up to a set column according to self.chunks, then return
	# this allows for iterative sorting that can be retrieved over time
	def updateImage(self):
		for _ in range(self.chunks):
			if self.direction == "vertical":
				if self.offset >= self.wsize:
					return self.source

				# get a single column of pixels and turn them into rgba values
				inCol = self.source.crop((self.offset, 0, self.offset + 1, self.ysize))
				inPix = list(inCol.getdata())

				# sort according to an rgba value. r = p[0], g = p[1], b = p[2], a = p[3]
				# here we're sorting by an average of the rgb values
				inSort = sorted(inPix, key=lambda p: (p[0] + p[1] + p[2]) / 3)

				# create a temporary image for the sorted column, then place the sorted pixels
				outCol = Image.new(inCol.mode, (1, self.ysize))
				outCol.putdata(inSort)

				# paste the sorted portion over the original image
				self.source.paste(outCol, (self.offset, 0))
			else:
				if self.offset >= self.ysize:
					return self.source
				
				# get a single column of pixels and turn them into rgba values
				inCol = self.source.crop((0, self.offset, self.wsize, self.offset + 1))
				inPix = list(inCol.getdata())
				
				# sort according to an rgba value. r = p[0], g = p[1], b = p[2], a = p[3]
				# here we're sorting by an average of the rgb values
				inSort = sorted(inPix, key=lambda p: (p[0]))
				
				# create a temporary image for the sorted column, then place the sorted pixels
				outCol = Image.new(inCol.mode, (self.wsize, 1))
				outCol.putdata(inSort)
				
				# paste the sorted portion over the original image
				self.source.paste(outCol, (0, self.offset))

			self.offset += 1

		return self.source



