#!/usr/bin/python3.8

# The game of life

import pygame as pg
from pprint import pprint
import random
import sys

WIDTH = 800
HEIGHT = 800

SIZE = (WIDTH, HEIGHT)

RES = 10

reswid = int(HEIGHT / RES)
reshei = int(WIDTH / RES)

pg.init()

screen = pg.display.set_mode(SIZE)

running = False

stop_on_border = False
draw_grid = False


def create_2d_array(xlen, ylen):

	xlen = int(xlen)
	ylen = int(ylen)

	array = list()

	for x in range(xlen):
		array.append(list())
		for y in range(ylen):
			array[x].append(0)

	return array


def create_3d_array(xlen, ylen):

	xlen = int(xlen)
	ylen = int(ylen)

	array = list()

	for x in range(xlen):
		array.append(list())
		for y in range(ylen):
			array[x].append([0, (0, 0, 0)])

	return array


cells = create_3d_array(reswid, reshei)

a = 0


def update():
	global a
	global cells
	if running:
		a += 1
		print("Generation: ", a)

	p1, p2, p3 = pg.mouse.get_pressed()
	mousepos = pg.mouse.get_pos()

	xpos = int(mousepos[0] / RES)
	ypos = int(mousepos[1] / RES)

	if p1:
		cells[xpos][ypos][0] = 1
		cells[xpos][ypos][1] = (150, 150, 255)
	if p3:
		cells[xpos][ypos][0] = 0
		cells[xpos][ypos][1] = (0, 0, 0)


def draw():
	global cells
	if running:
		screen.fill(0)
	else:
		screen.fill((10, 10, 10))

	for x, col in enumerate(cells):
		for y, row in enumerate(col):
			if running:
				pg.draw.rect(screen, (cells[x][y][1]),
							 (x * RES, y * RES, RES, RES))
			else:
				if cells[x][y][0] == 0 and cells[x][y][1] == (0,0,0):
					pg.draw.rect(screen, (30,30,30),
								 (x*RES, y * RES, RES, RES))
				else:
					pg.draw.rect(screen, (cells[x][y][1]),
								 (x * RES, y * RES, RES, RES))

			if stop_on_border:
				if x == 0 or x == len(cells)-1 or y == 0 or y == len(cells[x])-1:
					pg.draw.rect(screen, (255,0,0), (x*RES, y*RES, RES, RES))
					cells[x][y][0] = 0

	if draw_grid:
		for x in range(reswid):
			for y in range(reshei):
				pg.draw.line(screen, (128,128,128), (x*RES, y*RES), (x*RES+reswid, y*RES))
				pg.draw.line(screen, (128,128,128), (x*RES, y*RES), (x*RES, y*RES+reshei))

	pg.display.update()


def ca():

	global cells

	next = create_3d_array(reswid, reshei)

	for x in range(0, len(cells)):
		for y in range(0, len(cells[x])):

			neighbours = 0
			for i in range(-1, 2):
				for j in range(-1, 2):
					try:
						neighbours += cells[x + i][y + j][0]
					except:

						if x + i >= len(cells):
							wx = 0
						elif x + i < 0:
							wx = len(cells) - 1
						else:
							wx = x + i

						if y + j >= len(cells[x]):
							wy = 0
						elif y + j < 0:
							wy = len(cells[x]) - 1
						else:
							wy = y + j

						if not stop_on_border:
							neighbours += cells[wx][wy][0]
						else:
							pass

			state = cells[x][y][0]
			neighbours -= state

			if state == 1:
				if neighbours < 2 or neighbours > 3:
					next[x][y][0] = 0
					next[x][y][1] = (20, 20, 20)
				elif neighbours >= 2 or neighbours <= 3:
					next[x][y][0] = state
					next[x][y][1] = (255, 255, 255)

			elif state == 0:
				if neighbours == 3:
					next[x][y][0] = 1
					next[x][y][1] = (0, 150, 0)
				else:
					next[x][y][1] = (0, 0, 0)
			else:
				next[x][y][0] = state
				next[x][y][1] = (255, 255, 255)

	cells = next


while True:
	update()
	draw()
	if running:
		ca()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				pg.quit()
				sys.exit()
			if event.key == pg.K_SPACE:
				running = not running
			if event.key == pg.K_c:
				cells = create_3d_array(reswid, reshei)

			if event.key == pg.K_r:
				cells = create_3d_array(reswid, reshei)
				for i in range(int(WIDTH/RES * 8)):
					randx = random.randint(0, reswid - 1)
					randy = random.randint(0, reshei - 1)

					cells[randx][randy][0] = 1
					cells[randx][randy][1] = (150, 150, 255)

			if event.key == pg.K_RETURN and not running:
				ca()
				a += 1
				print("Generation: ", a)

			if event.key == pg.K_s:
				stop_on_border = not stop_on_border

			if event.key == pg.K_g:
				draw_grid = not draw_grid

			if event.key == pg.K_F2:
				import png
				img = []
				for y in range(HEIGHT):
					row = ()
					for x in range(WIDTH):
						row = row + screen.get_at((x,y))[:-1]
					img.append(row)
				with open('map.png', 'wb') as f:
					w = png.Writer(WIDTH, HEIGHT, greyscale=False)
					w.write(f, img)
