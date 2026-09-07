import pygame

from rkdo_imgman.load_image import ImageRender

class Viewer:
	def __init__(self, w: int, h: int, path: str):
		self.w = w
		self.h = h

		# pygame boilerplate
		pygame.init()
		self.screen = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption("Shit fuck")
		self.clock = pygame.time.Clock()

		# call our image render class. it's called this until i think of a better name
		self.render = ImageRender(path)

	# start the thingy
	def start(self):
		self.paintPillowImage() # get the initial painted, edited image
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.screen.fill((0, 0, 0))
			self.paintPillowImage()
			self.clock.tick(60)

		pygame.quit()

	def getPillowImage(self):
		# get the updated, partially sorted image from the renderer
		return self.render.updateImage()

	def processPillowImage(self, pil_img):
		pil_img = pil_img.convert("RGB")
		pil_img.thumbnail((self.w, self.h))
		# turn the Pillow image into a Pygame Surface
		imgBytes = pil_img.tobytes()
		imgSize = pil_img.size
		imgMode = pil_img.mode

		# fit the image into the window.

		pygSurface = pygame.image.frombytes(imgBytes, imgSize, "RGB")

		if imgMode == 'RGBA':
			return pygSurface.convert_alpha()
		return pygSurface.convert()

	def paintPillowImage(self):
		pil_img = self.getPillowImage() # get the image from pillow
		surface = self.processPillowImage(pil_img) # get the surface from the processed pillow

		self.screen.blit(surface, (0, 0))
		pygame.display.flip()