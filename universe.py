import pygame
import random
import pyperclip
import threading
import os
import time

from math import cos, sin

from settings import *
from astrobjs import Star

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1' #center window
clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

class Camera:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.speed = 1

	def move(self):
		pressed = False
		key = pygame.key.get_pressed()
		speed = self.speed
		if key[pygame.K_LSHIFT]:
			speed += 2
			if key[pygame.K_LCTRL]:
				speed += 100

		if key[pygame.K_w]:
				self.y -= speed
				pressed = True

		if key[pygame.K_s]:
				self.y += speed
				pressed = True

		if key[pygame.K_a]:
				self.x -= speed
				pressed = True

		if key[pygame.K_d]:
				self.x += speed
				pressed = True

		if key[pygame.K_o]:
				self.x = 0
				self.y = 0
				pressed = True

		if key[pygame.K_v]:
			#ako se pritisne V onda uzme od clipboarda podatke
			try:
				x, y = pyperclip.paste().split(":")
				x, y = int(x), int(y)
				self.teleport(x, y)
			except:
				return

		return pressed
			
	def teleport(self, x, y):
		self.x = x
		self.y = y

cam = Camera()

font = pygame.font.SysFont("Arial", 30)
font_star = pygame.font.SysFont("Arial", 12, bold=True)
font_info = pygame.font.SysFont("Arial", 25)

def get_mouse_in_segment(galaxy=True):
	mos_pos = pygame.mouse.get_pos()
	mos_pos = (mos_pos[0]//SEGMENTS, mos_pos[1]//SEGMENTS) #poz. misa na ekranu
	mos_galaxy = (mos_pos[0] + cam.x, mos_pos[1] + cam.y) #poz. misa u svemiru

	if galaxy:
		return mos_galaxy
	else:
		return mos_pos

def clicked():
	click = pygame.mouse.get_pressed()

	if click[0]:
		return 1
	elif click[2]:
		return 2

def command():
	#Konzola thread
	print("To change coords paste this format \"x:y\" in the app",
		"or type it in the console.")
	print("Move with use WASD. Speed up with Shift and Ctrl.",
		"Reset to center with O.")
	while True:
		coords = input(">>> ")
		try:
			x, y = coords.split(":")
			x, y = int(x), int(y)
		except:
			continue

		cam.teleport(x, y)

threading.Thread(target=command, daemon=True).start()

width = HALF_WIDTH
height = HEIGHT
border = 1

selected = False
selectedStar = [0,0] #x,y

running = True
while running:
	clock.tick(60)
	win.fill(BLACK)

	cam.move()

	for x in range(SECTORS_X):
		for y in range(SECTORS_Y):
			#pygame.draw.rect(
			# win,
			# WHITE,
			# (x*SEGMENTS,y*SEGMENTS,SEGMENTS,SEGMENTS),
			# 1
			# )
			star = Star(x + cam.x, y + cam.y, False)
			if star.starExists:
				center = (x*SEGMENTS+SEGMENTS//2, y*SEGMENTS+SEGMENTS//2)
				pygame.draw.circle(win, star.color, center, star.radius)
				#renderuje zvijezde bez generisanja detalja (samo izgleda)

	if selected:
		x, y = selectedStar
	else:
		x, y = get_mouse_in_segment()
	star = Star(x, y)
	if star.starExists:
		x, y = x-cam.x, y-cam.y
		center = (x*SEGMENTS+SEGMENTS//2, y*SEGMENTS+SEGMENTS//2)
		if x > -SECTORS_X and x < SEGMENTS:
			if y > -SECTORS_Y and y < SEGMENTS:
				#ako je x,y u ekranu onda radi slijedece:
				pygame.draw.circle(win, WHITE, center, star.radius+5, 1)
				name_text = font_star.render(star.name, True, WHITE)
				name_w = name_text.get_width()
				name_h = name_text.get_height()
				win.blit(
					name_text,
					(center[0] - name_w//2,
					center[1] + star.radius+5)
				)
				try:
					pos_text = font_star.render(
						f"x:{x+cam.x} y: {y+cam.y}",
						True,
						WHITE
					)
					pos_w = pos_text.get_width()
					win.blit(
						pos_text,
						(center[0] - pos_w//2,
						center[1] +star.radius+20)
					)
				except:
					pass

		rel_x = 0
		rel_y = HEIGHT-height - border

		if x*SEGMENTS <= rel_x + width:
			#if y*SEGMENTS >= rel_y and y*SEGMENTS <= rel_y+height:
			#ako je x na lijevoj strani onda prikaze podatke na desnoj
			rel_x = WIDTH-width-border
			rel_y = 0 - border

		rel_x_center = rel_x+width//2
		rel_y_center = rel_y+height//2
		left_bottom = (rel_x, height)

		pygame.draw.rect(win, BLACK, (rel_x, rel_y, width, height))
		pygame.draw.rect(win, WHITE, (rel_x, rel_y, width, height), 2)

		pygame.draw.circle(
			win,
			star.color,
			(rel_x_center, rel_y_center),
			star.radius
		)
		mos_x, mos_y = pygame.mouse.get_pos()

		texts = []
		texts.append(font_info.render(
			f"Name: {star.name}",
			True,
			WHITE
		))
		texts.append(font_info.render(
			f"Type: {star.type.name}",
			True,
			WHITE
		))
		texts.append(font_info.render(
			f"Number of planets: {len(star.planets)}",
			True,
			WHITE
		))

		text_width = texts[2].get_width()
		text_height = texts[0].get_height()
		text_offset = -text_height
		for text in reversed(texts):
			win.blit(text, (rel_x+width-text_width, height+text_offset))
			text_offset -= text_height
			#Render textova

		orbit = star.radius*2 + 25
		for n, planet in enumerate(star.planets):
			n += 1
			
			if planet.reversedRotation:
				planet.t += -time.time()/n
			else:
				planet.t += time.time()/(n**2)

			planet_x = orbit * cos(planet.t) + rel_x_center
			planet_y = orbit * sin(planet.t) + rel_y_center

			pygame.draw.circle(
				win,
				WHITE,
				(rel_x_center, rel_y_center),
				orbit,
				1
			)

			if planet.ring:
				for ring in range(planet.rings):
					ring_radius = planet.radius + 10
					pygame.draw.circle(
						win, 
						GRAY, 
						(int(planet_x), int(planet_y)), 
						ring_radius, 
						4
					)

			if planet.moons:
				if planet.ring:
					moon_orbit = ring_radius + 10
				else:
					moon_orbit = planet.radius + 10
				for n, (t, reversedRotation) in enumerate(planet.moons):
					n += 1 #da ne bi bilo dijeljenja sa 0
					t += -time.time()/n if reversedRotation else time.time()/n
					moon_x = moon_orbit * cos(t) + planet_x
					moon_y = moon_orbit * sin(t) + planet_y
					moon_size = random.randint(3,5)
					pygame.draw.circle(
						win, 
						GRAY, 
						(int(planet_x), int(planet_y)), 
						moon_orbit, 
						1
					)
					pygame.draw.circle(
						win, 
						WHITE, 
						(int(moon_x), int(moon_y)), 
						moon_size
					)
					moon_orbit += 10

			if selected:
				if (mos_x - rel_x_center)**2 +\
					(mos_y - rel_y_center)**2 < (orbit+10)**2:
					if (mos_x - rel_x_center)**2 +\
						(mos_y - rel_y_center)**2 > (orbit-10)**2:
						pygame.draw.circle(
							win, 
							WHITE, 
							(int(planet_x), int(planet_y)), 
							planet.radius+3, 
							2
						)
						pygame.draw.circle(
							win, 
							WHITE, 
							(rel_x_center, rel_y_center), 
							orbit+1, 
							3
						)

						texts = []

						texts.append(font_info.render(
							f"Gasses: {round(planet.gasses)}%", 
							True, 
							WHITE
						))
						texts.append(font_info.render(
							f"Minerals: {round(planet.minerals)}%",
							True,
							WHITE
						))
						texts.append(font_info.render(
							f"Resources: {round(planet.resources)}%",
							True,
							WHITE
						))
						texts.append(font_info.render(
							f"Water: {round(planet.water)}%",
							True,
							WHITE
						))
						texts.append(font_info.render(
							f"Temperature: {planet.temperature}°C",
							True,
							WHITE
						))
						texts.append(font_info.render(
							f"Name: {planet.name}",
							True,
							WHITE
						))

						
						text_height = texts[0].get_height()
						text_offset = -text_height
						for text in texts:
							win.blit(text, (rel_x+3, height+text_offset))
							text_offset -= text_height


			pygame.draw.circle(
				win,
				planet.color,
				(int(planet_x),
				int(planet_y)),
				planet.radius)
			orbit += 45

		if clicked() == 1:
			if mos_x >= rel_x and mos_x <= rel_x+width:
				pass
			else:
				selected = False


	if clicked() == 1:
		x, y = get_mouse_in_segment()
		star = Star(x, y, False)
		if star.starExists:
			pyperclip.copy(f"{x - (SECTORS_X//2)}:{y - (SECTORS_Y//2)}")
			if not selected:
				selected = True
				selectedStar = [x,y]

	try:
			cords = font.render(
				f"X:{str(cam.x)}, Y: {str(cam.y)}",
				True,
				WHITE
			)
	except:
			cords = font.render(
				f"You are too far from the center. Don't get lost",
				True,
				WHITE
			)
	fps = font.render(f"FPS: {str(int(clock.get_fps()))}", True, WHITE)
	win.blit(fps, FPS_POS)
	win.blit(cords, CORD_POS)

	pygame.display.flip()
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
					running = False

pygame.quit()
quit()
