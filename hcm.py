# A simple CPU meter, for display on the Holiday IoTAS device.
# It uses the Holiday SecretAPI to push new values via UDP. It pushes these as often as it can.
# The fetch interval is defined in fetch_cpu_vals.
#
# You'll need psutil:
# 	easy_install psutil
# 
# Included is holidaysecretapi. You can get the latest version of this library from:
#	https://github.com/moorescloud/secretapi

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

	def my_render(self, cpus):
		""" Renders a list of CPU usage values to the Holiday """
		led_on = 0xFF
		led_off = 0x00

		globes = self.hol.NUM_GLOBES
		
		green = []
		blue = []
		red = []
		
		cpu_count = len(cpus)
		globes_per_fragment_base = globes // cpu_count
		remainder = globes % cpu_count
		stride = cpu_count // remainder
		fragment_counts = []

		for cpu in range(cpu_count):
			if (cpu % stride == 0):
				fragment_counts.append(globes_per_fragment_base + 1)
			else:
				fragment_counts.append(globes_per_fragment_base)
			
		for cpu in range(cpu_count):
			fragment_count = fragment_counts[cpu]
			greencount = (cpus[cpu] * fragment_count) / 100
			
			# Fill the arrays of colours
			for globe in range(fragment_count):
				if globe < greencount:
					if globe >= fragment_count - ((fragment_count * 25) / 100):
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
		for globeindex in range(globes):
			self.hol.setglobe(globeindex, red[globeindex], green[globeindex], blue[globeindex])
		self.hol.render()

	def fetch_cpu_vals(self):
		""" Get the CPU use values from psutil """
		return psutil.cpu_percent(interval=0.075, percpu=True)

# Main loop
if __name__ == '__main__':
	if len(sys.argv) > 1:
		holiday_address = sys.argv[1]		# Pass IP address of Holiday on command line
	else:
		sys.exit(1)                				# If not there, fail
	
	app = HCMapp()						# Instance thread & start it
	app.start()
	
	while True:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			app.terminate = True
			sys.exit(0)
