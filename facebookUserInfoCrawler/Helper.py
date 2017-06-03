class My_Queue:
	#fifo
	_repo = []

	def put(self, ele):
		self._repo.append(ele)

	def size(self):
		return len(self._repo)

	def pop(self, index = 0):
		if(len(self._repo) > 0):
			ele = self._repo.pop(index)
			return ele
		else:
			return None

	def is_empty(self):
		return len(self._repo) == 0 



		
# def test():
# 	q = My_Queue()
# 	q.put(0)
# 	q.put(2)
# 	print(q.size())
# 	print(q.pop())
# 	print(q.pop())
# 	print(q.pop())
# 	print(q.size())
# 	print(q.is_empty())

# if __name__ == '__main__':
# 	test()