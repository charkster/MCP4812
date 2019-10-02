#!/usr/bin/python

from MCP4812 import MCP4812
import time

def main():
	dac = MCP4812(spi_device=0, spi_channel=1, max_speed_hz = 1000000, debug=1)
	dac.set_voltage(channel=0, voltage=2.0)
	dac.set_voltage(channel=1, voltage=4.0)
	time.sleep(5)
	dac.disable(channel=0)
	dac.disable(channel=1)
	
if __name__ == '__main__':
    main()
