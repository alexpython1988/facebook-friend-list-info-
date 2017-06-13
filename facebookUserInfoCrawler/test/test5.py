import time

def file1(i, j, file):
	l1 = []
	with open(file, "r") as f:
		for k, each in enumerate(f):
			if k >= i and k < j:
				l1.append(each)

def file2(i, j, file):
	l2 = []
	with open(file, "r") as f:
		lines = f.readlines()
		for k in range(i, j):
			l2.append(lines[k])

def write_file(file):
	with open(file, "a") as f:
		for i in range(100001, 1000000):
			s = "line{}".format(i)
			print(s, file = f, end = "\n")

#write_file("file.txt")

m1 = 0
m2 = 0

for z in range(100):
	t1 = time.process_time()
	file1(500000, 810001, "file.txt")
	t2 = time.process_time()
	m1 += (t2 - t1)


for v in range(100):
	t3 = time.process_time()
	file2(500000, 810001,"file.txt")
	t4 = time.process_time()
	m2 += (t4 - t3)

print("file1: {}".format(m1 / 100))
print("file2: {}".format(m2 / 100))
