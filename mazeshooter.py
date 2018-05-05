import pygame, time, numpy, os 
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze Shooter")

def get_resource(filename):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources", filename)

# dimensions and colours 
width = 1200
height = 700
blue = (0,0,255)
fps = 30
player_psn = [100, 100]
audio_muted = False

fps_clk = pygame.time.Clock() 
# image loads 
screen = pygame.display.set_mode((width, height))
shooter = pygame.transform.scale(pygame.image.load(get_resource("person.png")), (100, 100))
uw_logo = pygame.image.load(get_resource("uwlogo.png"))
arrow_up = pygame.transform.scale(pygame.image.load(get_resource("arrowup.png")), (width//15, height//15))
arrow_left = pygame.transform.scale(pygame.image.load(get_resource("arrowleft.png")), (width//15, height//15))
arrow_down = pygame.transform.scale(pygame.image.load(get_resource("arrowdown.png")), (width//15, height//15))
arrow_right = pygame.transform.scale(pygame.image.load(get_resource("arrowright.png")), (width//15, height//15))
audio_sign = pygame.transform.scale(pygame.image.load(get_resource("audiosign.jpg")), (width//15, height//10))

# audio loads
pygame.mixer.music.load(get_resource("mazegamemusic.wav"))
pygame.mixer.music.play(-1)

while True:
	screen.fill(0)
	for x in range(0, width, uw_logo.get_width() + 1):
		for y in range(0, height, uw_logo.get_height() + 1):
			screen.blit(uw_logo, (x, y))
	pygame.draw.rect(screen, blue, (0, 0, width/15, height), 0)
	screen.blit(audio_sign, (0, (9 * height)/10))

	move_keys = {"up": False, "left": False, "down": False, "right": False}

	screen.blit(shooter, player_psn)

	for event in pygame.event.get():
		mouse_psnX, mouse_psnY = pygame.mouse.get_pos()
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
		elif event.type == pygame.KEYDOWN: 
			if event.key == K_w or event.key == K_UP:
				move_keys["up"] = True
				screen.blit(arrow_up, (0, 0))
			elif event.key == K_a or event.key == K_LEFT:
				move_keys["left"] = True
				screen.blit(arrow_left, (0, 0))
			elif event.key == K_s or event.key == K_DOWN:
				move_keys["down"] = True
				screen.blit(arrow_down, (0, 0))
			elif event.key == K_d or event.key == K_RIGHT:
				move_keys["right"] = True
				screen.blit(arrow_right, (0, 0))
		elif event.type == pygame.KEYUP: 
			if event.key == K_w or event.key == K_UP:
				move_keys["up"] = False
			elif event.key == K_a or event.key == K_LEFT:
				move_keys["left"] = False
			elif event.key == K_s or event.key == K_DOWN:
				move_keys["down"] = False
			elif event.key == K_d or event.key == K_RIGHT:
				move_keys["right"] = False
		elif event.type == pygame.MOUSEBUTTONDOWN and mouse_psnX <= width/15 and mouse_psnY >= (9 * height)/10: 
			if audio_muted:
				pygame.mixer.music.unpause()
				audio_muted = False 
			else:
				pygame.mixer.music.pause()
				audio_muted = True

	if move_keys["up"]:
		player_psn[1] -= 5
	elif move_keys["down"]:
		player_psn[1] += 5
	if move_keys["left"]:
		player_psn[0] -= 5
	elif move_keys["right"]:
		player_psn[0] += 5
	pygame.display.update()
	fps_clk.tick(fps)