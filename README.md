# project1

alen-invasion.py : 為我們Project的主程式，裡面會創造出AI_game，及遊戲初始化，及整體遊戲運作。
ship.py: 定義飛船的功能，包括樣子和速度，和如何用左右鑑去控制它。
settings.py: 有遊戲裡的各種設定。可以改變這裡的數字來把遊戲個人化。
bullet.py: 劃出子彈的顏色和定義子彈的長寬高。
alien.py: 定義外星人的長相和他們如何移動(左右和往下)。
game_stats.py:：可以紀錄遊戲裡的等級。
button.py: 畫出遊戲剛開始的按鍵。
scoredboard.py：顯示出現在分數與歷史上最高分數。







alien invaion,py:

import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
from bullet import Bullet
class AlienInvasion:
	def __init__(self):
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("project1")
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		self.play_button = Button(self,"Play")

	def run_game(self):
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens() 
			self._update_screen()
	def _update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

			self._check_bullet_alien_collision()
	def _check_bullet_alien_collision(self):		
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points*len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score(  )
			self.sb.check_high_score()
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1
		self.sb.prep_level()
	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			if self.play_button.rect.collidepoint(mouse_pos):
				self.stats.reset_stats()
				self.stats.game_active = True
				self.sb.prep_score()
				self.sb.prep_level()
				self.sb.prep_ships()
				self.aliens.empty()
				self.bullets.empty()
				self._create_fleet()
				self.ship.center_ship()
				pygame.mouse.set_visible(False)
				
	def _check_keydown_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	def _create_fleet(self):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2*alien_height)
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)
	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
		self.aliens.add(alien)
	def _check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1
	def _ship_hit(self):
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.aliens.empty()
			self.bullets.empty
			self._create_fleet()
			self.ship.center_ship()
			sleep(0.5)
		else:
			self.stats.game_active = False


	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()
	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.sb.show_score()
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()
if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()


ship.py

import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		self.image = pygame.image.load('images/ship.jpg')
		self.rect = self.image.get_rect()

		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		self.moving_right = False
		self.moving_left = False
	def center_ship(self):
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
	def update(self):
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		self.rect.x = self.x
	def blitme(self):
		self.screen.blit(self.image, self.rect)


settings.py
class Settings():
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (255,255,255)
		self.ship_speed = 20
		self.ship_limit = 3
		self.bullet_speed = 5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 100
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
	def initialize_dynamic_settings(self):
		self.ship_speed = 5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0
		self.fleet_direction = 1
		self.alien_points = 50
	def increase_speed(self):
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)





bullet.py
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__(self,ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		self.rect = pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		self.y = float(self.rect.y)
	def update(self):
		self.y -= self.settings.bullet_speed
		self.rect.y = self.y
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color,self.rect)


alien.py
import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		self.image = pygame.image.load('images/alien.jpg')
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)
	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True
	def update(self):
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x
game_stats.py
class GameStats:
	def __init__(self,ai_game):
		self.settings = ai_game.settings
		self.reset_stats()
		self.game_active = False
		self.high_score = 0
		self.level = 1

	def reset_stats(self):
		self.ships_left =  self.settings.ship_limit
		self.score = 0


button.py
import pygame.font
class Button:
	def __init__(self, ai_game,msg):
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.width, self.height = 200, 50
		self.buttton_color = (0,255,0)
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None, 48)
		self.rect = pygame.Rect(0,0,self.width,self.height)
		self.rect.center = self.screen_rect.center
		self._prep_msg(msg)
	def _prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True,self.text_color,self.buttton_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
	def draw_button(self):
		self.screen.fill(self.buttton_color,self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

scoreboard
import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
	def __init__(self, ai_game):
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.ai_settings = ai_game.settings
		self.stats = ai_game.stats

		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	def prep_score(self):
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
	def prep_high_score(self):
		high_score = round(self.stats.high_score,-1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
	def show_score(self):
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()
	def prep_level(self):
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
	def prep_ships(self):
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)


