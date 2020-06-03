import re

import numpy
from PIL import Image


def main():
	bit_size = 16
	shape = int(256 / bit_size)
	link = '/home/zen-net/Downloads/pine_apple.png'
	try:
		img = Image.open(link)
		img = img.convert(mode='RGB')
		img = img.resize((shape, shape), Image.ANTIALIAS)
		#
		pix = numpy.array(img.getdata())
		# print(pix[:10])
		# img = img.resize((1024, 1024), Image.ANTIALIAS)

		# img.show()

		s = pix
		x = '.eqv MONITOR_SCREEN 0x10010000\n\n.text\nli $k0, MONITOR_SCREEN\n\n# Shape 256x256, pixel 16x16\n\n'
		t = 0
		for color in s:
			r, g, b = color
			print(r, g, b)
			my_color = '0x' + str(hex(int(r)))[2:] + str(hex(int(g)))[2:] + str(hex(int(b)))[2:]
			#
			x += ('li $t0, ' + my_color + '\nsw $t0, ' + str(t) + '($k0)\n nop\n')
			t += 4
		print(x.count('\n'))

		with open(re.sub(r'\.\w+$', '.asm', link), 'w') as f:
			f.write(x)

	except IOError:
		pass


if __name__ == "__main__":
	main()
