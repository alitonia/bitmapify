import re

import numpy
from PIL import Image


def main():
	bit_size_x = 4
	bit_size_y = 4
	shape_x = 256
	shape_y = 256

	size_x = int(shape_x / bit_size_x)
	size_y = int(shape_y / bit_size_y)

	link = '/abc/xyz.png'

	try:
		img = Image.open(link)
		img = img.convert(mode='RGB')
		img.show()
		img = img.resize((size_x, size_y), Image.ANTIALIAS)
		#
		pix = numpy.array(img.getdata())
		# print(pix[:10])
		# img = img.resize((1024, 1024), Image.ANTIALIAS)

		s = pix
		x = '.eqv MONITOR_SCREEN 0x10010000\n\n.text\nli $k0, MONITOR_SCREEN\n\n'
		x += (
				'# shape ' + str(shape_x) + 'x' + str(shape_y)
				+ ', pixel ' + str(bit_size_x) + 'x' + str(bit_size_y) + '\n'
				+ '# from ' + str(re.search(r'/[\w.-]+$', link).group(0))[1:] + '\n\n'
		)
		t = 0
		for color in s:
			r, g, b = color
			my_color = '0x' + str(hex(int(r)))[2:] + str(hex(int(g)))[2:] + str(hex(int(b)))[2:]
			x += ('li $t0, ' + my_color + '\nsw $t0, ' + str(t) + '($k0)\nnop\nnop\nnop\n')
			t += 4
		print(x.count('\n'))

		with open(re.sub(r'\.\w+$', '.asm', link), 'w') as f:
			f.write(x)

	except IOError:
		pass


if __name__ == "__main__":
	main()
