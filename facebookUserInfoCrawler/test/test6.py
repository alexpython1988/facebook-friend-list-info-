num_lines = sum(1 for line in open("file.txt"))

for i in range(0, num_lines, 1000):
	print(i)