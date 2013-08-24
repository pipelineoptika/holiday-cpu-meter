# A simple CPU meter for dual-core machines, for display on the Holiday IoTAS device.
# Support for more than two cores is left as an exercise for the reader. :)
#
# You'll need psutil:
# 	easy_install psutil
# 
# And holiday, which is available in:
#	https://github.com/moorescloud/tugofwar

import holiday
#import psutil
import time
import random

# Change "localhost:8080" to the address of your target Holiday
hol = holiday.Holiday(remote=True,addr="localhost:8080")

globes = hol.NUM_GLOBES
cpus = []

# Rendering for the Holiday
def my_render():
	global globes, cpus

	# Define some not-so-extreme values for "on"
	led_on = 0x90
	led_off = 0x00

	# How many globes need to be illuminated to represent the cpu usage?
	greencount = (cpus[0]*globes)/100
	bluecount = (cpus[1]*globes)/100

	green = []
	blue = []
	red = []

	# Fill the arrays of colours
	# From one end for CPU 1
	for i in range(globes):
		if i < greencount:
			green.append(led_on)
		else:
			green.append(led_off)

	# ...and from the other for CPU 2
	for i in reversed(range(globes)):
		if i < bluecount:
			blue.append(led_on)
		else:
			blue.append(led_off)

	# Any usage globes that overlap will be coloured red
	for i in range(globes):
		if green[i] == led_on and blue[i] == led_on:
			green[i] = led_off
			blue[i] = led_off
			red.append(led_on)
		else:
			red.append(led_off)

	# Set the globe values and render
	for i in range(globes):
		hol.setglobe(i, red[i], green[i], blue[i])
	hol.render()

# Get the CPU use values from psutil
def fetch_cpu_vals():
	global cpus
	
	generator = random.Random()
	
	cpus = []
		
	cpus.append(generator.randint(0, 100))
	cpus.append(generator.randint(0, 100))
	#cpus = psutil.cpu_percent(interval=0.2, percpu=True)

# Main loop
while True:
	fetch_cpu_vals()
	time.sleep(0.5)
	my_render()
	