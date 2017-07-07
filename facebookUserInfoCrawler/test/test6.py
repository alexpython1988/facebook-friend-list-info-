# import mmap

# def get_output_size():
# 	lines = 0
# 	with open("file.txt", "r+") as f:
# 		buf = mmap.mmap(f.fileno(), 0)
# 		readline = buf.readline
# 		while readline():
# 			lines += 1
# 	return "No. of total urls: {}".format(lines)

# print(get_output_size())
import json

for i in range(10,20):
	data = dict()
	data[i] = "alex"
	data[i+1] = [1,23]
	with open("test.json", "a") as f:
			data = json.dumps(data)
			print(data, file = f, end='\n')

with open('test.json') as f:
	for each in f:
		data = json.loads(each)
		print(data)
