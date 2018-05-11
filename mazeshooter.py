import pygame
import numpy as np
import matplotlib as mpl
import time, random, math
import os, subprocess, threading 
from pygame.locals import *


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Defend the Town")


def get_resource(filename):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources", filename)


# Sprite Classes
class Shooter(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(get_resource("person.png")).convert_alpha(), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = 100
		self.speed = 5

class Bullet(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height, X, Y):
		super().__init__()
		self.width = sprite_width
		self.height = sprite_height
		self.image = pygame.transform.scale(pygame.image.load(get_resource("bullet.png")).convert_alpha(), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()
		self.rect.x = X
		self.rect.y = Y
		self.speed = 10

class EnemyOne(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height, X, Y):
		super().__init__()
		self.width = sprite_width
		self.height = sprite_height
		self.image = pygame.transform.scale(pygame.image.load(get_resource("golfball.jpg")).convert_alpha(), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()
		self.rect.x = X
		self.rect.y = Y
		self.speed = 10

class AmmoBox(pygame.sprite.Sprite):
	def __init__(self, sprite_width, sprite_height):
		super().__init__()
		self.width = sprite_width
		self.height = sprite_height
		self.image = pygame.transform.scale(pygame.image.load(get_resource("golfball.jpg")).convert_alpha(), (sprite_width, sprite_height))
		self.rect = self.image.get_rect()

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

# Dimensions 
width, height = 1200, 700
fps = 30
audio_muted = False
move_keys = {"up": False, "left": False, "down": False, "right": False, "space": False}
rotate_keys = {"NE": False, "NW": False, "SW": False, "SE": False}
ammo_keys = {"reload": False}
key_up_flag = True


# Frame Clock
fps_clk = pygame.time.Clock()


# Colours
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_red = (139, 0, 0)
grey = (155, 155, 24)
black = (0, 0, 0)
white = (255, 255, 255)


# Fonts
# NOTES: Variable definitions are written in the format of the name of the font followed by the size of the font 
#        All fonts in this section are system fonts on macOS 10.13 -- not yet verified for other versions of macOS and for other operating systems
comic_font50 = pygame.font.SysFont("Comic Sans MS", 50)
comic_font100 = pygame.font.SysFont("Comic Sans MS", 100)
tnr30 = pygame.font.SysFont("Times New Roman", 30)
avant_grande100 = pygame.font.SysFont("Avant Grande", 100)


# ICC Profile Adjustments for Images (if necessary, using ImageMagick) 
'''
def adjust_ICC():
	res_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources"))
	subprocess.call("mogrify *.png", cwd = res_path)
	return None
'''


# Image Loads and Shape Definitions
# NOTE: See the Resources directory on the GitHub repo for the images
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
background_img = pygame.image.load(get_resource("grass.jpg"))
arrow_up = pygame.transform.scale(pygame.image.load(get_resource("arrowup.png")).convert_alpha(), (width//15, height//15))
arrow_left = pygame.transform.scale(pygame.image.load(get_resource("arrowleft.png")).convert_alpha(), (width//15, height//15))
arrow_down = pygame.transform.scale(pygame.image.load(get_resource("arrowdown.png")).convert_alpha(), (width//15, height//15))
arrow_right = pygame.transform.scale(pygame.image.load(get_resource("arrowright.png")).convert_alpha(), (width//15, height//15))
audio_sign = pygame.transform.scale(pygame.image.load(get_resource("audiosign.jpg")), (width//15, height//10))
cancel_round = pygame.transform.scale(pygame.image.load(get_resource("cancelround.png")), (width//15, height//10))
pause_button = pygame.transform.scale(pygame.image.load(get_resource("pause.png")).convert_alpha(), (width//15, height//10))
resume_button = pygame.transform.scale(pygame.image.load(get_resource("resume.png")).convert_alpha(), (width//15, height//10))
	

# Sprites and Blocks
sprites_lst = pygame.sprite.Group()
shooter = Shooter(100, 100)
bullet = Bullet(20, 20, shooter.rect.x, shooter.rect.y)
enemy_end = pygame.Rect(0, 0, width/15, height)
enemy_one_master = EnemyOne(50, 50, 0, 0)

sprites_lst.add(shooter)


# Audio Loads
pygame.mixer.music.load(get_resource("mazegamemusic.wav"))
pygame.mixer.music.play(-1)

def add_enemy(enemy_coords):
	enemy_X = random.randint(500, width)
	enemy_Y = random.randint(0, height)
	enemy_coords.append([enemy_X, enemy_Y])          # 2D list required due to mutation in the move_enemy function -- avoid tuples here 
	return None

def move_enemy(enemy_coords):
	for coords_set in enemy_coords:                    
		coords_set[0] -= random.randint(0, 25)
		if coords_set[1] < height:
			coords_set[1] += random.randint(-25, 25)  
		else:
			coords_set[1] += random.randint(0, 25)
	return None

def play_audio(audio_muted):
	if audio_muted:
		pygame.mixer.music.unpause()
		audio_muted = False 
	else:
		pygame.mixer.music.pause()
		audio_muted = True
	return audio_muted

def shooting_angle():
	rel_cursor_psn = tuple(np.subtract(pygame.mouse.get_pos(),shooter.rect.center))
	player_angle = -math.degrees(math.atan(rel_cursor_psn[1]/rel_cursor_psn[0]))
	return player_angle

def start(in_play, enemy_coords, time_remaining, round_number, ammo_count, end_color = green):	
	screen.fill(0)
	for x in range(0, width, background_img.get_width() + 1):
		for y in range(0, height, background_img.get_height() + 1):
			screen.blit(background_img, (x, y))
	pygame.draw.rect(screen, blue, (0, 0, width/15, height), 0)
	pygame.draw.rect(screen, end_color, (width/15, 0, 20, height))
	end_color = blue

	if in_play:
		screen.blit(pause_button, (0, (7 * height)/10))
	else:
		screen.blit(resume_button, (0, (7 * height)/10))
		screen.blit(avant_grande100.render("PAUSED", True, black), (width/2 - 100, height/2))
	screen.blit(cancel_round, (0, (8 * height)/10))
	screen.blit(audio_sign, (0, (9 * height)/10))

	clk_time = tnr30.render("Time: ", True, (0, 0, 0))
	screen.blit(clk_time, (5, height/5))
	
	time_left = comic_font50.render(str(time_remaining), True, grey)
	screen.blit(time_left, (20, height/5 + 20)) 

	round_title = tnr30.render("Round:", True, (0, 0, 0))
	screen.blit(round_title, (5, height/3))
	round_number = comic_font50.render(str(round_number), True, grey)
	screen.blit(round_number, (25, height/3 + 20))

	ammo_title = tnr30.render("Ammo:", True, (0, 0, 0))
	screen.blit(ammo_title, (5, height/2 - 25))
	ammo_text = comic_font50.render(str(ammo_count), True, grey)
	screen.blit(ammo_text, (20, height/2))

	screen.blit(pygame.transform.rotate(shooter.image, shooting_angle()), (shooter.rect.x, shooter.rect.y))

	for X, Y in enemy_coords:
		screen.blit(enemy_one_master.image, (X, Y))

	return None

def play_round(round_number, end_color):
	global audio_muted
	game_in_progress = True
	ammo_count = 25
	time_remaining = 120              
	enemy_freq = 1500//round_number   # the amount of time required for another enemy to appear on the screen
	enemy_coords = []                 # list of 2D coordinates of each enemy to be displayed on the screen
	enemy_group = pygame.sprite.Group()
	in_play = True				      # True if game is in "playing" state; False if game is in "resume" state

	# Custom Events (and the Timers)
	# EVENT 1: Round Timer
	round_tick = pygame.USEREVENT + 1 
	pygame.time.set_timer(round_tick, 1000)
	# EVENT 2: Addition of New Enemy 
	enemy_appear = pygame.USEREVENT + 2
	pygame.time.set_timer(enemy_appear, enemy_freq)

	while game_in_progress:
		start(in_play, enemy_coords, time_remaining, round_number, ammo_count, end_color)

		for event in pygame.event.get():
			mouse_psnX, mouse_psnY = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN and mouse_psnX <= width/15 and mouse_psnY > (7 * height)/10 and mouse_psnY < (8 * height)/10: 
				in_play = not in_play      # changes the state of the game from "playing" to "resumed" when pause button is pressed, and vice versa when 
										   # resume button is pressed (latter is the default)
			elif event.type == pygame.KEYDOWN and in_play: 
				if event.key == K_w or event.key == K_UP:
					move_keys["up"] = True
				elif event.key == K_a or event.key == K_LEFT:
					move_keys["left"] = True
				elif event.key == K_s or event.key == K_DOWN:
					move_keys["down"] = True
				elif event.key == K_d or event.key == K_RIGHT:
					move_keys["right"] = True
				elif event.key == K_SPACE:
					if ammo_count > 0:
						dx, dy = 0, 0 
						ammo_count -= 1
						start(in_play, enemy_coords, time_remaining, round_number, ammo_count, end_color)
						bullet_range = 12    # defines the number of iterations of the bullet animation, hence providing the gun with an approriate range
						enemy_group.empty()  # although not really necessary, it's a fail-safe measure to ensure that the group does not have duplicate sprites 
						while shooter.rect.right + bullet.width + dx <= screen_rect.right and bullet_range >= 0:
							bullet.rect.x = shooter.rect.right + dx
							bullet.rect.y = (shooter.rect.top  + shooter.rect.bottom)/2 + dx * math.tan(math.radians(-shooting_angle()))
							screen.blit(pygame.transform.rotate(bullet.image, shooting_angle()), (bullet.rect.x, bullet.rect.y))
							dx += 30
							bullet_range -= 1
							for enemyX, enemyY in enemy_coords:
								enemy_group.add(EnemyOne(50, 50, enemyX, enemyY))
							enemy_group.update()
							if pygame.sprite.spritecollide(bullet, enemy_group, True):
								bullet_range = -1
					else:
						reload_rect = pygame.draw.rect(screen, (0, 0, 0), (width/2 - 200, height/2, 350, 60), 0)
						reload_msg = comic_font100.render("NO AMMO", True, red)
						screen.blit(reload_msg, (width/2 - 200, height/2))
				elif event.key == K_r:
					ammo_keys["reload"] = True
				elif event.key == K_m:
					audio_muted = play_audio(audio_muted)
			elif event.type == pygame.KEYUP and in_play: 
				if event.key == K_w or event.key == K_UP:
					move_keys["up"] = False
				elif event.key == K_a or event.key == K_LEFT:
					move_keys["left"] = False
				elif event.key == K_s or event.key == K_DOWN:
					move_keys["down"] = False
				elif event.key == K_d or event.key == K_RIGHT:
					move_keys["right"] = False
				elif event.key == K_r:
					ammo_keys["reload"] = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if mouse_psnX <= width/15 and mouse_psnY >= (9 * height)/10: 
					audio_muted = play_audio(audio_muted)
				elif mouse_psnX <= width/15 and mouse_psnY > (8 * height)/10 and mouse_psnY < (9 * height)/10: 
					shooter.rect.x, shooter.rect.y = 100, 100
					return False					
			elif event.type == round_tick and time_remaining > 0 and in_play: 
				time_remaining -= 1 
				start(in_play, enemy_coords, time_remaining, round_number, ammo_count, end_color)
			elif event.type == enemy_appear and in_play:
				add_enemy(enemy_coords)
				move_enemy(enemy_coords)

		if move_keys["up"]:
			shooter.rect.y -= 3
			screen.blit(arrow_up, (0, 0))
		elif move_keys["down"]:
			shooter.rect.y += 3
			screen.blit(arrow_down, (0, 0))
		if move_keys["left"] and not pygame.Rect.colliderect(enemy_end, shooter.rect):   # prevents the player sprite from moving beyond the town
			shooter.rect.x -= 3
			screen.blit(arrow_left, (0, 0))
		elif move_keys["right"]:
			shooter.rect.x += 3
			screen.blit(arrow_right, (0, 0))

		if ammo_keys["reload"]:
			reload_rect = pygame.draw.rect(screen, (0, 0, 0), (width/2 - 200, height/2, 410, 60), 0)
			reload_msg = comic_font100.render("RELOADING", True, red)
			screen.blit(reload_msg, (width/2 - 200, height/2))
			time.sleep(1.5)
			ammo_count = 25
			ammo_keys["reload"] = False

		pygame.display.flip()	
		fps_clk.tick(fps)
		game_in_progress = (time_remaining != 0)  

	return True 


def play_game():
	n = 1
	while True:
		n = n + 1 if play_round(n, green) else 1


play_game()