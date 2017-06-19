import mmap

def get_output_size():
	lines = 0
	with open("file.txt", "r+") as f:
		buf = mmap.mmap(f.fileno(), 0)
		readline = buf.readline
		while readline():
			lines += 1
	return "No. of total urls: {}".format(lines)

print(get_output_size())