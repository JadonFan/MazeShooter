import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import *
import os, random


edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))
faces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

width, height = 1200, 700

peach = (0.99, 0.85, 0.72)


def get_resource(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources", filename)


def cube_schematics(scale_factor = 1, offsetX = 0, offsetY = 0, offsetZ = 0):
	vertices = [[1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]]

	for vertex in vertices:
		vertex[0] = vertex[0] * scale_factor + offsetX
		vertex[1] = vertex[1] * scale_factor + offsetY
		vertex[2] = vertex[2] * scale_factor + offsetZ
		vertex = tuple(vertex)

	return tuple(vertices)


def render_texture(filename):
    glEnable(GL_TEXTURE_2D)
    texture = pygame.transform.scale(pygame.image.load(get_resource(filename)), (50, 50))
    texture_info = pygame.image.tostring(texture, "RGBA", 1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture.get_width(), texture.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_info)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return texture_id


def ball():
    roundquartic = gluNewQuadric()
    
    glEnable(GL_TEXTURE_2D)
    texture_id = render_texture("golf_ball_texture.png")
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    gluSphere(roundquartic, 0.75, 200, 200)
    render_texture("golf_ball_texture.png")
    glDisable(GL_TEXTURE_2D)
    
    gluDeleteQuadric(roundquartic)


def player(scale_factor = 1, offsetX = 0, offsetY = 0, offsetZ = 0):
    vertices = cube_schematics(scale_factor, offsetX, offsetY, offsetZ)
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # glBegin(GL_QUADS)
    # for face in faces:
    	# for vertex in face:
    		# glVertex3fv(vertices[vertex])
    		# glColor3fv(peach)
    # glEnd()


def laser():
 	curvequartic = gluNewQuadric()
 	gluCylinder(curvequartic, 0.02, 0.02, 3.0, 200, 200)
 	gluDeleteQuadric(curvequartic)


def win_challenge():
	pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
	gluPerspective(30, width/height, 0.1, 50.0)
	glTranslatef(0.0, 0.0, -8)

	ply_scale, ply_offsetX, ply_offsetY, ply_offsetZ = 0.1, 1, 0, 3  # player sprite dimensions 
	challenge_in_progress = True
	playerX, playerY, playerZ = 0.0, 0.0, 0.2
	enemy_appear_freq = 2000
	enemy_coords = []
	fire = False
	victory = False

	# 3D Enemy Generation 
	enemy_appear = pygame.USEREVENT 
	pygame.time.set_timer(enemy_appear, enemy_appear_freq)
	gen_enemy = False
	enemy_num = 0

	while challenge_in_progress:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					fire = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					playerX -= 0.1
				elif event.key == pygame.K_RIGHT:
					playerX += 0.1
				elif event.key == pygame.K_UP:
					playerY += 0.1
				elif event.key == pygame.K_DOWN:
					playerY -= 0.1
				elif event.key == pygame.K_SPACE:
					fire = True
			elif event.type == enemy_appear:		
				print(">> GENERATE ENEMY")	
				enemy_coords.append([random.uniform(-6.0, 6.0), random.uniform(-3.5, 3.5), -5.0])
				enemy_num += 1

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		# glTranslatef(0.0, 0.0, 0.01)

		# ---------------------------------------
		# ENEMY 
		# ---------------------------------------
		glPushMatrix()
		for enemy in enemy_coords:
			glTranslatef(enemy[0], enemy[1], enemy[2])
			ball()
		glPopMatrix()

		# ---------------------------------------
		# LASER 
		# ---------------------------------------
		if fire:
			glPushMatrix()
			glTranslatef(playerX + ply_offsetX, playerY + ply_offsetY, playerZ + ply_offsetZ)
			laser()
			glPopMatrix()

		# ---------------------------------------
		# PLAYER 
		# ---------------------------------------
		glPushMatrix()
		glTranslatef(playerX, playerY, playerZ)
		player(ply_scale, ply_offsetX, ply_offsetY, ply_offsetZ)
		glPopMatrix()

		victory = enemy_num == 10
		challenge_in_progress = enemy_num != 10

		pygame.display.flip()

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	return victory