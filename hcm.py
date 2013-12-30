# A simple CPU meter for dual-core machines, for display on the Holiday IoTAS device.
# Support for more than two cores is left as an exercise for the reader. :)
#
# You'll need psutil:
# 	easy_install psutil
# 
# And holiday, which is available in:
#	https://github.com/moorescloud/tugofwar

from holidaysecretapi import HolidaySecretAPI 
import psutil
import time
import random
import sys
import threading

class HCMapp(threading.Thread):

	def run(self):
		global holiday_address
		self.terminate = False
		self.hol = HolidaySecretAPI(addr=holiday_address)

		while True:
			if self.terminate:
				return
			cpus = self.fetch_cpu_vals()
			self.my_render(cpus)

	# Rendering for the Holiday
	def my_render(self, cpus):
		led_on = 0xFF
		led_off = 0x00

		globes = self.hol.NUM_GLOBES
		
		green = []
		blue = []
		red = []
		
		cpucount = len(cpus)
		globesperfragment = globes/cpucount
		
		for cpu in range(cpucount):
			greencount = (cpus[cpu] * globesperfragment) / 100
			
			# Fill the arrays of colours
			for globe in range(globesperfragment):
				if globe < greencount:
					if globe >= globesperfragment - ((globesperfragment * 25) / 100):
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
		for globeindex in range(globesperfragment*cpucount):
			self.hol.setglobe(globeindex, red[globeindex], green[globeindex], blue[globeindex])
		self.hol.render()

	# Get the CPU use values from psutil
	def fetch_cpu_vals(self):
		return psutil.cpu_percent(interval=0.075, percpu=True)

# Main loop
if __name__ == '__main__':
	if len(sys.argv) > 1:
		holiday_address = sys.argv[1]          # Pass IP address of Holiday on command line
	else:
		sys.exit(1)                 # If not there, fail
	
	app = HCMapp()               # Instance thread & start it
	app.start()
	
	while True:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			app.terminate = True
			sys.exit(0)
