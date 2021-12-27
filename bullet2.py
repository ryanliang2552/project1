import pygame
from pygame.sprite import Sprite

class Bullet2(Sprite):
	def __init__(self,ai_game, direction):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		self.dir = direction

		self.rect = pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		self.y = float(self.rect.y)
		self.x = float(self.rect.x)
	def update(self):
		self.y -= self.settings.bullet_speed
		self.rect.y = self.y
		if (self.dir == True):
			self.x -= self.settings.bullet_speed
			self.rect.x = self.x
		else:
			self.x += self.settings.bullet_speed
			self.rect.x = self.x
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color,self.rect)	