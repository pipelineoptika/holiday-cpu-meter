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
import sys

# Change "localhost:8080" to the address of your target Holiday
hol = holiday.Holiday(remote=True,addr="localhost:8080")

globes = hol.NUM_GLOBES
# How many globes need to be illuminated to represent the cpu usage?
# We need to determine this based on the CPU count, which we'll fake for now
cpucount = 4
globesperfragment = globes/cpucount
cpus = []

#print "globesperfragment: %d" % globesperfragment

# Rendering for the Holiday
def my_render():
	global globes, globesperfragment, cpus, cpucount

	# Define some not-so-extreme values for "on"
	led_on = 0xFF
	led_off = 0x00
	
	green = []
	blue = []
	red = []
	
	for i in range(cpucount):
		#print "eval cpu %d" % i
		greencount = (cpus[i]*globesperfragment)/100
		
		#print "greencount: %d" % i
		
		# Fill the arrays of colours
		for j in range(globesperfragment):
			if j < greencount:
				if j >= globesperfragment - ((globesperfragment*25)/100):
					red.append(led_on)
					green.append(led_off)
				else:
					red.append(led_off)
					green.append(led_on)
				blue.append(led_off)
			else:
				green.append(led_off)
				blue.append(led_off)
				red.append(led_off)

	# Set the globe values and render
	for i in range(globesperfragment*cpucount):
		hol.setglobe(i, red[i], green[i], blue[i])
	hol.render()

# Get the CPU use values from psutil
def fetch_cpu_vals():
	global cpus
	
	generator = random.Random()
	
	cpus = []
		
	cpus.append(generator.randint(0, 100))
	cpus.append(generator.randint(0, 100))
	cpus.append(generator.randint(0, 100))
	cpus.append(generator.randint(0, 100))
	#cpus = psutil.cpu_percent(interval=0.2, percpu=True)

# Main loop
while True:
	fetch_cpu_vals()
	time.sleep(0.5)
	my_render()
	