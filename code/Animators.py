import time
ANIMATION_SPEED = .1

class Animators:
	@staticmethod
	def enter_down(screen, string):
		size = screen.getmaxyx()
		for i in range (size[0]/2):
			screen.clear()
			screen.addstr(i+1, size[1]/2 - len(string)/2, string)
			screen.refresh()
			time.sleep(ANIMATION_SPEED)

	@staticmethod
	def exit_up(screen, string):
		size = screen.getmaxyx()
		for i in range (size[0]/2 + 1):
			screen.clear()
			screen.addstr(size[0]/2 - i, size[1]/2 - len(string)/2, string)
			screen.refresh()
			time.sleep(ANIMATION_SPEED)

