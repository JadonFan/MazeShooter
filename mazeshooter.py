import pygame
import numpy as np
import time, random, math
import os, subprocess, threading 
from pygame.locals import *


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze Shooter")


def get_resource(filename):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources", filename)

class Shooter(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(get_resource("person.png")), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = 100
		self.speed = 5

class Bullet(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height):
		super().__init__()
		self.width = sprite_width
		self.image = pygame.transform.scale(pygame.image.load(get_resource("bullet.jpg")), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()
		self.speed = 10

'''
class Maze():
	def __init__(self, maze_width, maze_height):
		maze_vertical = [(x, y, x+1, y) for x in range(maze_width-1) for y in range(maze_height)]
		maze_horizontal = [(x, y, x, y+1) for x in range(maze_width) for y in range(maze_height-1)]
		self.layout = maze_vertical + maze_horizontal
		self.kruskal_sets = [set([(x,y)]) for x in range(maze_width) for y in range(maze_height)]

	def generate_map(self):
		maze_copy = list(maze_layout)
		random.shuffle(maze_copy)

		for step in self.layout:
			set1, set2 = None

			for indiv_set in kruskal_sets:
				if (self.layout[0], self.layout[1]) in indiv_set:
					set1 = indiv_set
				if (self.layout[2], self.layout[3]) in indiv_set:
					set2 = indiv_set

			if set1 is not set2:
				self.kruskal_sets.remove(set1)
				self.kruskal_sets.remove(set2)
				self.kruskal_sets.append(set1.union(set_b))
				self.layout.remove(step)

	def __repr__(self):
		return self.layout.generate_map()

	def draw(self):

		return 
'''

# Dimensions and Colours 
width, height = 1200, 700
blue = (0, 0, 255)
yellow = (255, 255, 0)
fps = 30
audio_muted = False
move_keys = {"up": False, "left": False, "down": False, "right": False, "space": False}
rotate_keys = {"NE": False, "NW": False, "SW": False, "SE": False}
key_up_flag = True

fps_clk = pygame.time.Clock()


# Fonts
timer_font = pygame.font.SysFont("Comic Sans MS", 50)


# Image ICC Profile Adjustments (if necessary, using ImageMagick) 
'''
def adjust_ICC():
	res_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources"))
	subprocess.call("mogrify *.png", cwd = res_path)
	return None
'''


# Image Loads 
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
uw_logo = pygame.image.load(get_resource("uwlogo.png"))
arrow_up = pygame.transform.scale(pygame.image.load(get_resource("arrowup.png")), (width//15, height//15))
arrow_left = pygame.transform.scale(pygame.image.load(get_resource("arrowleft.png")), (width//15, height//15))
arrow_down = pygame.transform.scale(pygame.image.load(get_resource("arrowdown.png")), (width//15, height//15))
arrow_right = pygame.transform.scale(pygame.image.load(get_resource("arrowright.png")), (width//15, height//15))
audio_sign = pygame.transform.scale(pygame.image.load(get_resource("audiosign.jpg")), (width//15, height//10))
	

# Spites and Blocks
spites_lst = pygame.sprite.Group()
shooter = Shooter(100, 100)
spites_lst.add(shooter)
bullet = Bullet(20, 20)
enemy_end = pygame.Rect(0, 0, width/15, height)


# Audio Loads
pygame.mixer.music.load(get_resource("mazegamemusic.wav"))
pygame.mixer.music.play(-1)


def start(redraw_player = True, end_color = blue):	
	screen.fill(0)
	for x in range(0, width, uw_logo.get_width() + 1):
		for y in range(0, height, uw_logo.get_height() + 1):
			screen.blit(uw_logo, (x, y))
	pygame.draw.rect(screen, end_color, (0, 0, width/15, height), 0)
	end_color = blue
	screen.blit(audio_sign, (0, (9 * height)/10))

	if redraw_player:
		spites_lst.update()
		spites_lst.draw(screen)

	return None


def play_round(end_color):
	cursor_moved = False

	while True:
		global audio_muted
		start(end_color)

		for event in pygame.event.get():
			mouse_psnX, mouse_psnY = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.KEYDOWN: 
				if event.key == K_w or event.key == K_UP:
					move_keys["up"] = True
				elif event.key == K_a or event.key == K_LEFT:
					move_keys["left"] = True
				elif event.key == K_s or event.key == K_DOWN:
					move_keys["down"] = True
				elif event.key == K_d or event.key == K_RIGHT:
					move_keys["right"] = True
				elif event.key == K_SPACE:
					move_keys["space"] = True
					dx, dy = 0, 0 
					while shooter.rect.right + bullet.width + dx <= screen_rect.right:
						screen.blit(bullet.image, (shooter.rect.right + dx, (shooter.rect.top  + shooter.rect.bottom)/2 + dy))
						dx += 5
			elif event.type == pygame.KEYUP: 
				if event.key == K_w or event.key == K_UP:
					move_keys["up"] = False
				elif event.key == K_a or event.key == K_LEFT:
					move_keys["left"] = False
				elif event.key == K_s or event.key == K_DOWN:
					move_keys["down"] = False
				elif event.key == K_d or event.key == K_RIGHT:
					move_keys["right"] = False
				elif event.key == K_SPACE:
					move_keys["space"] = False
			elif event.type == pygame.MOUSEBUTTONDOWN and mouse_psnX <= width/15 and mouse_psnY >= (9 * height)/10: 
				if audio_muted:
					pygame.mixer.music.unpause()
					audio_muted = False 
				else:
					pygame.mixer.music.pause()
					audio_muted = True
			
		cursor_moved = True
		rel_cursor_psn = tuple(np.subtract(pygame.mouse.get_pos(),shooter.rect.center))
		player_angle = -math.degrees(math.atan(rel_cursor_psn[1]/rel_cursor_psn[0]))
		start(False, end_color)
		screen.blit(pygame.transform.rotate(shooter.image, player_angle), (shooter.rect.x, shooter.rect.y))


		if move_keys["up"]:
			shooter.rect.y -= 3
			screen.blit(arrow_up, (0, 0))
		elif move_keys["down"]:
			shooter.rect.y += 3
			screen.blit(arrow_down, (0, 0))
		if move_keys["left"] and not pygame.Rect.colliderect(enemy_end, shooter.rect):
			shooter.rect.x -= 3
			screen.blit(arrow_left, (0, 0))
		elif move_keys["right"]:
			shooter.rect.x += 3
			screen.blit(arrow_right, (0, 0))


		if pygame.Rect.colliderect(enemy_end, shooter.rect):
			end_color = yellow
		else:
			end_color = blue

		pygame.display.flip()	
		fps_clk.tick(fps)

	return True 


def play_game():
	play_round(blue)


play_game()