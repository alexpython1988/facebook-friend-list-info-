from multiprocessing import Process

def task():
	with open("list.txt", "a") as f:
		for i in range(1000000):
			print("test" + str(i), file = f, end = "\n")

def main():
	p1 = Process(target=task)
	p2 = Process(target=task)

	p1.start()
	p2.start()

if __name__ == '__main__':
	main()
