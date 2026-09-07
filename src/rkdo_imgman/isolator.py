from PIL import Image

# make callable class
class Isolator:
	def __init__(self, path, direction="vertical", channel="r", chunks=10):
		self.im = Image.open( path ) # source image
		self.wsize, self.ysize = self.im.size

		self.offset = 0 # the offset according to image width
		self.chunks = chunks # how many columns should be sorted at any given time, before the image is returned
		self.direction = direction.lower()
		if self.direction not in ("vertical", "horizontal"):
			raise ValueError("direction must be 'vertical' or 'horizontal'")

		self.channel = channel.lower()
		if self.channel not in ("r", "g", "b"):
			raise ValueError("channel must be 'r', 'g' or 'b'")

	# apply a pixel sort to the image up to a set column according to self.chunks, then return
	# this allows for iterative sorting that can be retrieved over time
	def updateImage(self):
		for _ in range(self.chunks):
			if self.direction == "vertical":
				if self.offset >= self.wsize:
					return self.im

				# get a single column of pixels and turn them into rgba values
				inCol = self.im.crop((self.offset, 0, self.offset + 1, self.ysize))
				inPix = list(inCol.getdata())

				# isolate a colour channel according to self.channel
				inIsolate = list()

				for i in range(len(inPix)):
					match self.channel:
						case "r": inIsolate.append((inPix[i][0], 0, 0))
						case "g": inIsolate.append((0, inPix[i][1], 0))
						case "b": inIsolate.append((0, 0, inPix[i][1]))

				# create a temporary image for the sorted column, then place the sorted pixels
				outCol = Image.new(inCol.mode, (1, self.ysize))
				outCol.putdata(inIsolate)

				# paste the sorted portion over the original image
				self.im.paste(outCol, (self.offset, 0))
			else:
				if self.offset >= self.ysize:
					return self.im
				
				# get a single column of pixels and turn them into rgba values
				inCol = self.im.crop((0, self.offset, self.wsize, self.offset + 1))
				inPix = list(inCol.getdata())
				
				# isolate a colour channel according to self.channel
				inIsolate = list()
				
				for i in range(len(inPix)):
					match self.channel:
						case "r": inIsolate.append((inPix[i][0], 0, 0))
						case "g": inIsolate.append((0, inPix[i][1], 0))
						case "b": inIsolate.append((0, 0, inPix[i][2]))
				
				# create a temporary image for the sorted column, then place the sorted pixels
				outCol = Image.new(inCol.mode, (self.wsize, 1))
				outCol.putdata(inIsolate)
				
				# paste the sorted portion over the original image
				self.im.paste(outCol, (0, self.offset))

			self.offset += 1

		return self.im



