#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

number_of_positions_values = [3, 4, 5, 6, 7, 8, 10, 12, 13, 15, 17, 20, 22, 25, 30, 32]
number_of_rows = 2
termination_types = ["RA"]

hole_diameter = 1.00
pad_diameter = 1.7272
pin_pitch = 2.54
pin_diameter = 0.64

# ST_depth = 5.80
Rx_total_depth = 8.8
Rx_pin_to_plastic = (10.74+pin_pitch)-Rx_total_depth

hole_width = 4.5
hole_depth = 6.4
pin_length_in_hole = 6.0

pin_indicator_size = 1.5
pin_indicator_distance_to_top = 1.0

line_width = 0.15
crtyd_width = 0.05
crtyd_spacing = 0.5

# data from datasheet
B = {
	3: 15.12,
	4: 17.66,
	5: 20.20,
	6: 22.74,
	7: 25.28,
	8: 27.82,
	10: 32.90,
	12: 37.98,
	13: 40.52,
	15: 45.60,
	17: 50.68,
	20: 58.30,
	22: 63.38,
	25: 71.00,
	30: 83.70,
	32: 88.78
	}

def name(number_of_positions, termination_type):
	return "SBH11-xBPC-D%02u-%s-xx" % (number_of_positions, termination_type)

def description(number_of_positions, termination_type):
	return "Sullins SBH11 Series Shrouded (Box) Headers 2.54 mm Contact Centers, %s" % ("Straight" if termination_type == "ST" else "Right Angle" if termination_type == "RA" else "Surface Mount")

def tags(number_of_positions, termination_type):
	return "Sullins %02ux%02u %s %.2f mm pitch headers" % (
		number_of_rows,
		number_of_positions,
		"straight" if termination_type == "ST" else "angled" if termination_type == "RA" else "smd",
		pin_pitch)

def pad(position, x, y, diameter_pad, diameter_hole):
	return "  (pad %u thru_hole %s (at %.3f %.3f) (size %.3f %.3f) (drill %.3f) (layers *.Cu *.Mask F.SilkS))\n" % (position, "rect" if (position == 1) else "circle", x, y, diameter_pad, diameter_pad, diameter_hole)

for termination_type in termination_types:
	for number_of_positions in number_of_positions_values:
		filename = "%s.kicad_mod" % (name(number_of_positions, termination_type))

		x_start = (-(B[number_of_positions]-((number_of_positions-1)*pin_pitch))/2.0)
		x_end = x_start + B[number_of_positions]
		x_mid = (x_start+x_end)/2.0

		# if (termination_type == "ST"):
		# 	y_lines = [ST_depth/2.0,-ST_depth/2.0]
		# 	x_lines = [x_start, x_end]
		# elif (termination_type == "RA"):
		y_lines = [-(Rx_pin_to_plastic+Rx_total_depth), -(Rx_pin_to_plastic)]
		x_lines = [x_start, x_end]

		output = open(filename, 'w')

		output.write("(module %s (layer F.Cu) (tedit %X)\n" % (name(number_of_positions, termination_type), int(time.time())))

		# description
		output.write("  (descr \"%s\")\n" % (description(number_of_positions, termination_type)))

		# tags
		output.write("  (tags \"%s\")\n" % (tags(number_of_positions, termination_type)))

		# reference
		output.write("  (fp_text reference REF** (at %.3f %.3f 270) (layer F.SilkS)\n" % (-pin_pitch, -pin_pitch/2.0))
		output.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
		output.write("  )\n")

		#value
		output.write("  (fp_text value %s (at %.3f %.3f 270) (layer F.Fab)\n" % (name(number_of_positions, termination_type), number_of_positions*pin_pitch, -pin_pitch/2.0))
		output.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
		output.write("  )\n")


 		# pins
		for pos in xrange(1, number_of_positions+1):
			for row in xrange(1, number_of_rows+1):
				output.write(pad(2*(pos-1)+row, (pos-1)*pin_pitch, -(row-1)*pin_pitch, pad_diameter, hole_diameter))

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

		# hole
		if (termination_type == "RA"):
			for x in [x_mid-hole_width/2.0, x_mid+hole_width/2.0]:
				output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.SilkS) (width %.3f))\n" % (
					x,
					y_lines[0]+hole_depth,
					x,
					y_lines[0],
					line_width
					))

			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.SilkS) (width %.3f))\n" % (
				x_mid-hole_width/2.0,
				y_lines[0]+hole_depth,
				x_mid+hole_width/2.0,
				y_lines[0]+hole_depth,
				line_width
				))

		# pin indicator
		if (termination_type == "RA"):
			pin_indicator_offset = 1.0 if number_of_positions <= 3 else 0.0
			output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
				-pin_indicator_offset,
				y_lines[0]+pin_indicator_distance_to_top+pin_indicator_size,
				-pin_indicator_offset-pin_indicator_size/2.0,
				y_lines[0]+pin_indicator_distance_to_top,
				-pin_indicator_offset+pin_indicator_size/2.0,
				y_lines[0]+pin_indicator_distance_to_top,
				line_width
				))

		if (termination_type == "RA"):
			# pin drawings
			for pos in xrange(1, number_of_positions+1):
				x = (pos-1)*pin_pitch
				output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
					x+pin_diameter/2.0,
					-Rx_pin_to_plastic,
					x-pin_diameter/2.0,
					-Rx_pin_to_plastic,
					x-pin_diameter/2.0,
					-(pin_pitch+pad_diameter/2.0),
					x+pin_diameter/2.0,
					-(pin_pitch+pad_diameter/2.0),
					line_width
					))

			# for pos in xrange(int(number_of_positions/2.0), int(number_of_positions/2.0)+2):
			# 	x = (pos-1)*pin_pitch
			# 	output.write("  (fp_poly (pts (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f) (xy %.3f %.3f)) (layer F.SilkS) (width %.3f))\n" % (
			# 		x+pin_diameter/2.0,
			# 		y_lines[0]+hole_depth-pin_length_in_hole,
			# 		x-pin_diameter/2.0,
			# 		y_lines[0]+hole_depth-pin_length_in_hole,
			# 		x-pin_diameter/2.0,
			# 		y_lines[0]+hole_depth,
			# 		x+pin_diameter/2.0,
			# 		y_lines[0]+hole_depth,
			# 		line_width
			# 		))

		# courtyard
		# if (termination_type == "ST"):
		# 	crtyd_y_lines = [ST_depth/2.0+crtyd_spacing,-(ST_depth/2.0+crtyd_spacing)]
		# 	crtyd_x_lines = [x_start-pin_direction*crtyd_spacing, x_end+pin_direction*crtyd_spacing]
		# elif (termination_type == "RA") or (termination_type == "RB"):
		crtyd_y_lines = [-(Rx_pin_to_plastic+Rx_total_depth+crtyd_spacing),-(Rx_pin_to_plastic-crtyd_spacing), (pad_diameter/2.0+crtyd_spacing)]
		crtyd_x_lines = [x_start-crtyd_spacing, -pad_diameter/2.0-crtyd_spacing, (number_of_positions-1)*pin_pitch+pad_diameter/2.0+crtyd_spacing, x_end+crtyd_spacing]

		# round values to crtyd_width
		for lines in [crtyd_x_lines, crtyd_y_lines]:
			for i in xrange(0, len(lines)):
				lines[i] = round((lines[i])/0.05)*0.05

		# top
		output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
			crtyd_x_lines[0],
			crtyd_y_lines[0],
			crtyd_x_lines[-1],
			crtyd_y_lines[0],
			crtyd_width
	 		))

		# middle
		output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
			crtyd_x_lines[0],
			crtyd_y_lines[1],
			crtyd_x_lines[1],
			crtyd_y_lines[1],
			crtyd_width
			))

		output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
			crtyd_x_lines[-1],
			crtyd_y_lines[1],
			crtyd_x_lines[-2],
			crtyd_y_lines[1],
			crtyd_width
			))


		# bottom
		output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
			crtyd_x_lines[1],
			crtyd_y_lines[-1],
			crtyd_x_lines[-2],
			crtyd_y_lines[-1],
			crtyd_width
	 		))

		for x in [crtyd_x_lines[0], crtyd_x_lines[-1]]:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
				x,
				crtyd_y_lines[0],
				x,
				crtyd_y_lines[1],
				crtyd_width
				))

		for x in [crtyd_x_lines[1], crtyd_x_lines[-2]]:
			output.write("  (fp_line (start %.3f %.3f) (end %.3f %.3f) (layer F.CrtYd) (width %.3f))\n" % (
				x,
				crtyd_y_lines[1],
				x,
				crtyd_y_lines[-1],
				crtyd_width
				))

		output.write(")\n")
		output.close()
