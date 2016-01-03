#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

number_of_positions_min = 2
number_of_positions_max = 20
termination_types = ["ST", "RA", "RB"]

hole_diameter = 1.00
pad_diameter = 1.7272
pin_pitch = 2.54
pin_diameter = 0.64

ST_depth = 5.80

Rx_pin_to_plastic = 1.9
Rx_base_depth = 3.2
Rx_total_depth = 11.4
Rx_pin_length = 12.0

line_width = 0.15
crtyd_width = 0.05
crtyd_spacing = 0.5

clip_width = 1.0 # measured

# data from datasheet
B = {
	2: 5.12,
	3: 7.66,
	4: 10.20,
	5: 12.74,
	6: 15.30,
	7: 17.94,
	8: 20.48,
	9: 23.02,
	10: 25.58,
	11: 28.12,
	12: 30.68,
	13: 33.10,
	14: 35.80,
	15: 38.34,
	16: 40.94,
	17: 43.30,
	18: 45.90,
	19: 48.56,
	20: 50.80
	}

def name(number_of_positions, termination_type):
	return "SWR25X-NRTC-%02u-%s-BA" % (number_of_positions, termination_type)

def description(number_of_positions, termination_type):
	return "Sullins SWR25X Series Single Row Wafer 2.54 mm Contact Centers, %s" % ("Straight" if termination_type == "ST" else "Right Angle")

def tags(number_of_positions, termination_type):
	return "Sullins %02ux%02u %s %.2f mm pitch headers" % (
		1,
		number_of_positions,
		"straight" if termination_type == "ST" else "angled",
		pin_pitch)

def pad(position, x, y, diameter_pad, diameter_hole):
	return "  (pad %u thru_hole %s (at %.3f %.3f) (size %.3f %.3f) (drill %.3f) (layers *.Cu *.Mask F.SilkS))\n" % (position, "rect" if (position == 1) else "circle", x, y, diameter_pad, diameter_pad, diameter_hole)

for termination_type in termination_types:
	for number_of_positions in xrange(number_of_positions_min, number_of_positions_max+1):
		filename = "%s.kicad_mod" % (name(number_of_positions, termination_type))

		if (termination_type == "ST") or (termination_type == "RA"):
			pin_direction = 1.0
		elif (termination_type == "RB"):
			pin_direction = -1.0

		x_start = pin_direction*(-(B[number_of_positions]-((number_of_positions-1)*pin_pitch))/2.0)
		x_end = x_start + pin_direction*B[number_of_positions]

		if (termination_type == "ST"):
			y_lines = [ST_depth/2.0,-ST_depth/2.0]
			x_lines = [x_start, x_end]
		elif (termination_type == "RA") or (termination_type == "RB"):
			y_lines = [-(Rx_pin_to_plastic+Rx_total_depth), -(Rx_pin_to_plastic+Rx_base_depth), -(Rx_pin_to_plastic)]
			x_lines = [x_start, x_end]


		output = open(filename, 'w')

		output.write("(module %s (layer F.Cu) (tedit %X)\n" % (name(number_of_positions, termination_type), time.time()))

		# description
		output.write("  (descr \"%s\")\n" % (description(number_of_positions, termination_type)))

		# tags
		output.write("  (tags \"%s\")\n" % (tags(number_of_positions, termination_type)))

		# reference
		output.write("  (fp_text reference REF** (at %.3f %.3f 270) (layer F.SilkS)\n" % (-pin_direction*pin_pitch, (y_lines[0]+y_lines[1])/2.0))
		output.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
		output.write("  )\n")

		#value
		output.write("  (fp_text value %s (at %.3f %.3f 270) (layer F.Fab)\n" % (name(number_of_positions, termination_type), pin_direction*number_of_positions*pin_pitch, (y_lines[0]+y_lines[1])/2.0))
		output.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
		output.write("  )\n")


 		# pins
		for pos in xrange(1, number_of_positions+1):
			output.write(pad(pos, pin_direction*(pos-1)*pin_pitch, 0, pad_diameter, hole_diameter))

		# drawing
		for y in y_lines:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.SilkS) (width %.3f))\n" % (
				x_lines[0],
				y,
				x_lines[-1],
				y,
				line_width
				))

		for x in x_lines:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.SilkS) (width %.3f))\n" % (
				x,
				y_lines[0],
				x,
				y_lines[-1],
				line_width
				))

		# clip
		if (termination_type == "ST"):
			output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
				pin_direction*(number_of_positions-1)*pin_pitch,
				-y_lines[-1],
				0.0,
				-y_lines[-1],
				0.0,
				-(y_lines[-1]+clip_width),
				pin_direction*(number_of_positions-1)*pin_pitch,
				-(y_lines[-1]+clip_width),
				line_width
				))

		if (termination_type == "RA") or (termination_type == "RB"):
			# pin drawings
			for pos in xrange(1, number_of_positions+1):
				x = pin_direction*(pos-1)*pin_pitch
				output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
					x+pin_diameter/2.0,
					-Rx_pin_to_plastic,
					x-pin_diameter/2.0,
					-Rx_pin_to_plastic,
					x-pin_diameter/2.0,
					-pad_diameter/2.0,
					x+pin_diameter/2.0,
					-pad_diameter/2.0,
					line_width
					))

				if (termination_type == "RB"):
					output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
						x+pin_diameter/2.0,
						-(Rx_pin_to_plastic+Rx_base_depth),
						x-pin_diameter/2.0,
						-(Rx_pin_to_plastic+Rx_base_depth),
						x-pin_diameter/2.0,
						-Rx_pin_length,
						x+pin_diameter/2.0,
						-Rx_pin_length,
						line_width
						))

		# courtyard
		if (termination_type == "ST"):
			crtyd_y_lines = [ST_depth/2.0+crtyd_spacing,-(ST_depth/2.0+crtyd_spacing)]
			crtyd_x_lines = [x_start-pin_direction*crtyd_spacing, x_end+pin_direction*crtyd_spacing]
		elif (termination_type == "RA") or (termination_type == "RB"):
			crtyd_y_lines = [-(Rx_pin_to_plastic+Rx_total_depth+crtyd_spacing), (pad_diameter/2.0+crtyd_spacing)]
			crtyd_x_lines = [x_start-pin_direction*crtyd_spacing, x_end+pin_direction*crtyd_spacing]

		# round values to crtyd_width
		for lines in [crtyd_x_lines, crtyd_y_lines]:
			for i in xrange(0, len(lines)):
				lines[i] = round((lines[i])/0.05)*0.05

		for y in crtyd_y_lines:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
				crtyd_x_lines[0],
				y,
				crtyd_x_lines[-1],
				y,
				crtyd_width
				))

		for x in crtyd_x_lines:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
				x,
				crtyd_y_lines[0],
				x,
				crtyd_y_lines[-1],
				crtyd_width
				))

		output.write(")\n")
		output.close()
