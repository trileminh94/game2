import pygame

from coreItem import coreItem
from pygame.locals import *

class berry(coreItem):
	STEP_FLIP = 0.03
	move_length = 100
	velocity = 0.2
	direction = -1
	ITEM_TIME_TO_DIE = 4000
	ITEM_TIME_TO_LIVE = 1000

	def checkState(self):
		pass

	def move(self):
		pass