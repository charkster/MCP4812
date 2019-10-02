#!/usr/bin/python

import spidev

# ============================================================================
# MCP4812 2 channel 10-Bit DAC
# ============================================================================

class MCP4812 :
	spi = None
	
	_MAX_DAC_VAL  = 1023
	_MAX_DAC_CODE = 0x3FF
	_DAC_REF      = 2.048

	# Constructor
	def __init__(self, spi_device=0, spi_channel=0, max_speed_hz = 100000, debug=0): # 100kHz
		self.spi = spidev.SpiDev(spi_device, spi_channel)
		self.spi.max_speed_hz = max_speed_hz
		self.debug = debug

	def set_voltage(self, channel=0, voltage=0.0, gain=2):
		# Only 2 channels 0 or 1 else return -1
		if ((channel > 1) or (channel < 0)):
			print "Invalid channel %d, must be 0 or 1" % channel
			return -1
		if (gain == 1 and voltage > self._DAC_REF) or (gain == 2 and voltage > (2 * self._DAC_REF)):
			print "Invalid voltage and gain setting"
			return -1
		if (gain == 2): bit_gain = 0
		else:           bit_gain = 1
		dac_val = int((voltage / (self._DAC_REF * gain) * self._MAX_DAC_VAL)) & self._MAX_DAC_CODE
		vout_enable = 1
		byte1 = ((channel<<7) + (bit_gain<<5) + (vout_enable<<4) + (dac_val>>6)) & 0xFF
		byte0 = (dac_val<<2) & 0xFF
		self.spi.xfer2([byte1,byte0])
		if (self.debug):
			print "Channel %d set to %0.2f Volts, dac value is 0x%x, byte 1 is 0x%x, byte 0 is 0x%x" % \
			(channel,voltage,dac_val,byte1,byte0)
		
	def disable(self, channel):
		# Only 2 channels 0 or 1 else return -1
		if ((channel > 1) or (channel < 0)):
			print "Invalid channel %d, must be 0 or 1" % channel
			return -1
		gain = 0
		dac_val = 0
		vout_enable = 0
		byte1 = ((channel<<7) + (gain<<5) + (vout_enable<<4) + (dac_val>>6)) & 0xFF
		byte0 = (dac_val<<2) & 0xFF
		self.spi.xfer2([byte1,byte0])
		if (self.debug):
			print "Channel %d is disabled" % channel
