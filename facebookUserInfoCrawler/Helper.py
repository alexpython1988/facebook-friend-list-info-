from bitarray import bitarray
import mmh3

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


class Bloom_Filter():
	def __init__(self, size, hash_count):
		self.bit_array = bitarray(size)
		self.bit_array.setall(0)
		self.size = size
		self.hash_count = hash_count
	
	def __len__(self):
		return self.size

	def capacity(self):
		count = 0
		for each in self.bit_array:
			if each == 1:
				count += 1
		return count

	def add(self, obj):
		for seed in range(self.hash_count):
			index = mmh3.hash(obj, seed) % self.size
			self.bit_array[index] = 1

	def contains(self, obj):
		for seed in range(self.hash_count):
			index = mmh3.hash(obj, seed) % self.size
			if(self.bit_array[index] != 1):
				return False
		return True

class Counter:
	count = 0

	def increase(self):
		self.count += 1

	def size(self):
		return self.count

def test():
	q = My_Queue()
	q.put(0)
	q.put(2)
	print(q.size())
	print(q.pop())
	print(q.pop())
	print(q.pop())
	print(q.size())
	print(q.is_empty())

	bf = Bloom_Filter(100, 5)
	tl = ["alex", "xlad", "sadfdsa", "dsafdsafdsaf","gdsagreewhjwetr","fawsbghawr", "not mee","dafgawerhgeraw", "dasfgfawe", "adgaweghewa", "dafwdahjajkiu87", "dafwdghwrhrweah", "dasfdswahjerky9ilou", "123256t4327", "dasft3y2y54u8i7o","dasf23t234ppjj"]
	for each in tl:
		bf.add(each)

	print(bf.capacity())

	tl1 = ["alex", "xlad", "sadfdsa", "dsafdsafdsaf","gdsagreewhjwetr", "i am a bad guy","fawsbghawr", "dafgawerhgeraw", "dasfgfawe", "not me","adgaweghewa", "dafwdahjajkiu87", "dafwdghwrhrweah", "dasfdswahjerky9ilou", "123256t4327", "dasft3y2y54u8i7o","dasf23t234ppjj", "1235"]
	for each in tl1:
		if bf.contains(each):
			print("contains " + each)
		else:
			print("not contains " + each)	

if __name__ == '__main__':
	test()