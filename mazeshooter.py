import pygame
from pygame.locals import *
import numpy as np
import matplotlib as mpl
import time, random, math
import os, sys, subprocess, threading

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Defend the Town")


# ==================================================================================
# SPRITE CLASSES
# ==================================================================================
def get_resource(filename):   
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources", filename)

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


# ==================================================================================
# DIMENSIONS 
# ================================================================================== 
width, height = 1200, 700


# ==================================================================================
# FRAME CLOCK
# ==================================================================================
fps = 60
fps_clk = pygame.time.Clock()


# ==================================================================================
# COLOURS (based on their RGB values)
# ==================================================================================
red = (255, 0, 0)
dark_red = (139, 0, 0)

yellow = (255, 255, 0)

green = (0, 255, 0)

blue = (0, 0, 255)
turquoise = (64, 228, 208)

grey = (155, 155, 24)
black = (0, 0, 0)
white = (255, 255, 255)


# ==================================================================================
# FONTS
#   - Variable definitions are written in the format of the name of the font followed  
#       by the size of the font 
#   - All fonts in this section are system fonts on macOS 10.13, not yet verified 
#       for other versions of macOS and for other operating systems
# ==================================================================================
comic_font50 = pygame.font.SysFont("Comic Sans MS", 50)
comic_font100 = pygame.font.SysFont("Comic Sans MS", 100)
tnr30 = pygame.font.SysFont("Times New Roman", 30)
avant_grande100 = pygame.font.SysFont("Avant Grande", 100)
tnr150 = pygame.font.SysFont("Times New Roman", 150)


# ==================================================================================
# ICC PROFILE ADJUSTMENT (using ImageMagick) 
# ==================================================================================
'''
def adjust_ICC():
	res_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources"))
	subprocess.call("mogrify *.png", cwd = res_path)
	return None
'''


# ==================================================================================
# IMAGES AND SHAPES
# NOTE: See the Resources directory on the GitHub repo for the images
# ==================================================================================
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
background_img = pygame.image.load(get_resource("grass.jpg"))

# these arrow images will appear whenever the respective movement keys (WASD/updownleftright) are pressed 
arrow_up = pygame.transform.scale(pygame.image.load(get_resource("arrowup.png")).convert_alpha(), (width//15, height//15))
arrow_left = pygame.transform.scale(pygame.image.load(get_resource("arrowleft.png")).convert_alpha(), (width//15, height//15))
arrow_down = pygame.transform.scale(pygame.image.load(get_resource("arrowdown.png")).convert_alpha(), (width//15, height//15))
arrow_right = pygame.transform.scale(pygame.image.load(get_resource("arrowright.png")).convert_alpha(), (width//15, height//15))

# mutes audio in all pages
audio_sign = pygame.transform.scale(pygame.image.load(get_resource("audiosign.jpg")), (width//15, height//10))
# resets the game back to round 1
redo_button = pygame.transform.scale(pygame.image.load(get_resource("redoarrow.png")), (width//15, height//10))
# switches the state of the game to "PAUSED", where timer and animations all stop 
pause_button = pygame.transform.scale(pygame.image.load(get_resource("pause.png")).convert_alpha(), (width//15, height//10))
# switches the state of the game to "PLAYING", reversing the "PAUSED" state
resume_button = pygame.transform.scale(pygame.image.load(get_resource("resume.png")).convert_alpha(), (width//15, height//10))
# starts the game from the main menu screen
start_button = pygame.transform.scale(pygame.image.load(get_resource("start.jpg")).convert_alpha(), (400, 50))
# returns the user to the main menu 
return_button = pygame.transform.scale(pygame.image.load(get_resource("returnarrow.jpg")).convert_alpha(), (width//15, height//10))


# ==================================================================================
# SPRITES & BLOCKS
# ==================================================================================
sprites_lst = pygame.sprite.Group()
shooter = Shooter(100, 100)
bullet = Bullet(20, 20, shooter.rect.x, shooter.rect.y)
enemy_end = pygame.Rect(0, 0, width/15, height)
enemy_one_master = EnemyOne(50, 50, 0, 0)

sprites_lst.add(shooter)


# ==================================================================================
# AUDIO 
# ==================================================================================
audio_muted = False
pygame.mixer.music.load(get_resource("mazegamemusic.wav"))
pygame.mixer.music.play(-1)


# ==================================================================================
# GAMEPLAY FUNCTIONS 
# ==================================================================================

# access_dev() allows you to "skip" rounds, through a multithreaded process, to test balance changes.
# The thread that calls this function can be found in the start_game() function 
def access_dev(n, thread_running):
	while thread_running:
		pw = input("")
		n[0] = -1
		if "pythongame-" in pw and len(pw) == 12 and pw[-1].isdigit():
			n[0] = int((pw.split("-"))[1])
			thread_running = False 
		else:
			print("Access Denied, error code %d" %n[0])

	return n[0]

def move_enemy(enemy_group):
	for enemy in enemy_group:                    
		enemy.rect.x -= random.randint(20, 50)
		enemy.rect.y += random.randint(-25, 25) if enemy.rect.y < height else random.randint(-25, 0)  
	enemy_group.update()
	return enemy_group

def play_audio(audio_muted):
	if audio_muted:
		pygame.mixer.music.unpause()
		audio_muted = False 
	else:
		pygame.mixer.music.pause()
		audio_muted = True
	return audio_muted

def shooting_angle():
	rel_cursor_psn = tuple(np.subtract(pygame.mouse.get_pos(), shooter.rect.center))
	angle_offset = 0 if rel_cursor_psn[0] >= 0 else 180
	return -(math.degrees(math.atan(rel_cursor_psn[1]/rel_cursor_psn[0]))) + angle_offset

def start(health_points, in_play, enemy_group, time_remaining, round_number, ammo_count, end_color = green):	
	screen.fill(0)
	for x in range(0, width, background_img.get_width() + 1):
		for y in range(0, height, background_img.get_height() + 1):
			screen.blit(background_img, (x, y))
	pygame.draw.rect(screen, blue, (0, 0, width/15, height), 0)
	pygame.draw.rect(screen, end_color, (width/15, 0, 20, height))
	end_color = blue

	for enemy in enemy_group:
		screen.blit(enemy_one_master.image, (enemy.rect.x, enemy.rect.y))

	if in_play:
		screen.blit(pause_button, (0, (8 * height)/10))
	else:
		screen.blit(resume_button, (0, (8 * height)/10))
		screen.blit(avant_grande100.render("PAUSED", True, black), (width/2 - 100, height/2))
	screen.blit(audio_sign, (0, (9 * height)/10))

	screen.blit(redo_button, ((13 * width)/15 - 1, (9 * height)/10))
	screen.blit(return_button, ((14 * width)/15, (9 * height)/10))

	round_title = tnr30.render("Round:", True, (0, 0, 0))
	screen.blit(round_title, (5, height/3 - 30))
	round_number = comic_font50.render(str(round_number), True, grey)
	screen.blit(round_number, (25, height/3 - 10))

	clk_time = tnr30.render("Time: ", True, (0, 0, 0))
	screen.blit(clk_time, (5, height/5))
	time_left = comic_font50.render(str(time_remaining), True, grey)
	screen.blit(time_left, (15, height/5 + 20)) 

	hp_title = tnr30.render("HP:", True, (0, 0, 0))
	screen.blit(hp_title, (5, height/7 - 20))
	hp = comic_font50.render(str(health_points), True, grey)
	screen.blit(hp, (15, height/7))

	ammo_title = tnr30.render("Ammo:", True, (0, 0, 0))
	screen.blit(ammo_title, (5, height/2 - 90))
	ammo_text = comic_font50.render(str(ammo_count), True, grey)
	screen.blit(ammo_text, (20, height/2 - 70))

	screen.blit(pygame.transform.rotate(shooter.image, shooting_angle()), (shooter.rect.x, shooter.rect.y))

	return None

def play_round(round_number, end_color):
	global audio_muted                        # audio_muted is kept as a global variable so that the setting is consistent across all game screens 
	game_in_progress = True            
	in_play = True				              # True if game is in "PLAYING" state; False if game is in "PAUSED" state
	ammo_count = 25                          
	time_remaining = 60              
	enemy_move_freq = 2250//round_number      # the amount of time required for another enemy to appear on the screen
	enemy_group = pygame.sprite.Group()
	health_points = 100 + round_number//3 * 50
	move_keys = {"up": False, "left": False, "down": False, "right": False, "space": False}
	ammo_keys = {"reload": False}

	# CUSTOM EVENTS 
	# 1: Round Timer
	round_tick = pygame.USEREVENT + 1 
	pygame.time.set_timer(round_tick, 1000)
	# 2: Addition of New Enemy 
	enemy_appear = pygame.USEREVENT + 2
	pygame.time.set_timer(enemy_appear, 2000)
	# 3: Movement of Enemy 
	enemy_move = pygame.USEREVENT + 3
	pygame.time.set_timer(enemy_move, enemy_move_freq)

	while game_in_progress:
		start(health_points, in_play, enemy_group, time_remaining, round_number, ammo_count, end_color)

		for event in pygame.event.get():
			mouse_psnX, mouse_psnY = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN and mouse_psnX <= width/15 and mouse_psnY > (8 * height)/10 and mouse_psnY < (9 * height)/10: 
				in_play = not in_play      # changes the state of the game from "PLAYING" to "PAUSED" when pause button is pressed, and vice versa when 
										   #    resume button is pressed (latter is the default)
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
						start(health_points, in_play, enemy_group, time_remaining, round_number, ammo_count, end_color)
						bullet_range = 10   # defines the number of iterations of the bullet animation
						while shooter.rect.right + bullet.width + dx <= screen_rect.right and bullet_range >= 0:
							angle = shooting_angle()
							bullet.rect.x = shooter.rect.right + dx
							bullet.rect.y = (shooter.rect.top  + shooter.rect.bottom)/2 + dx * math.tan(math.radians(-angle))
							screen.blit(pygame.transform.rotate(bullet.image, angle), (bullet.rect.x, bullet.rect.y))
							dx = dx + 30 if angle <= 180 and angle >= -180 else dx - 30
							bullet_range -= 1
							if pygame.sprite.spritecollide(bullet, enemy_group, True):
								bullet_range = -1
							enemy_group.update()
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
				elif mouse_psnX >= (13 * width)/15 and mouse_psnX < (14 * width)/15 and mouse_psnY >= (9 * height)/10: 
					shooter.rect.x, shooter.rect.y = 100, 100
					return False
				elif mouse_psnX > (14 * width)/15 and mouse_psnX <= width and mouse_psnY >= (9 * height)/10: 
					start_game(False)		
			elif event.type == round_tick and time_remaining > 0 and in_play: 
				time_remaining -= 1 
				start(health_points, in_play, enemy_group, time_remaining, round_number, ammo_count, end_color)
			elif event.type == enemy_appear and in_play:
				enemy_group.add(EnemyOne(50, 50, random.randint(500, width), random.randint(0, height)))
			elif event.type == enemy_move and in_play and enemy_group:
				enemy_group = move_enemy(enemy_group)

		enemy_group.update()

		if move_keys["up"]:
			shooter.rect.y -= 5
			screen.blit(arrow_up, (0, 0))
		elif move_keys["down"]:
			shooter.rect.y += 5
			screen.blit(arrow_down, (0, 0))
		if move_keys["left"] and not pygame.Rect.colliderect(enemy_end, shooter.rect):   # prevents the player sprite from moving beyond the town
			shooter.rect.x -= 5
			screen.blit(arrow_left, (0, 0))
		elif move_keys["right"]:
			shooter.rect.x += 5
			screen.blit(arrow_right, (0, 0))

		if ammo_keys["reload"]:
			reload_rect = pygame.draw.rect(screen, black, (width/2 - 200, height/2, 410, 60), 0)
			reload_msg = comic_font100.render("RELOADING", True, red)
			screen.blit(reload_msg, (width/2 - 200, height/2))
			time.sleep(1.5)
			ammo_count = 25
			ammo_keys["reload"] = False

		for enemy in enemy_group:
			if pygame.Rect.colliderect(pygame.Rect(width/15, 0, 20, height), enemy.rect):
				enemy.kill()
				health_points -= 10

		pygame.display.flip()	
		fps_clk.tick(fps)
		game_in_progress = (time_remaining != 0 and health_points > 0)  

	return health_points > 0  

def play_game(round_number):
	if round_number == 10:
		return "Complete"

	try:    
		if sys.platform.startswith("darwin"):
			os.system("osascript -e 'display notification \"{0}\" with title \"{1}\"'".format("Round %d has started" %round_number, "Defend the Town"))
		elif sys.platform.startswith("linux"):
			os.system("notify-send {0} {1}".format("Defend the Town", "Round %d has started" %round_number))
	except: raise OSError(1, "Notification cannot be displayed")
	else:   round_number = round_number + 1 if play_round(round_number, green) else 1

	return play_game(round_number)

def start_game(thread_running):
	begin = False
	n = [1]          # a list is used so that the value of n can be mutated when access_dev is called in the dev_key thread 

	if thread_running:
		dev_key = threading.Thread(target = access_dev, args = [n, thread_running], name = "Developer Key")
		dev_key.start()

	while not begin:
		screen.fill(turquoise)
		game_title = tnr150.render("Defend the Town", True, black)
		screen.blit(game_title, (width/2 - 400, 100))
		screen.blit(start_button, (width/2 - 200, height/2 - 25))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				begin = True

	play_game(n[0])

	return None

start_game(True)