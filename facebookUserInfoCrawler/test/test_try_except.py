a = [1,2,3,4,5,0,6,7,8,9]

while len(a) > 0:
	n = a.pop()
	try: 
		print(100//n)
	except Exception as e:
		print(e)
		continue
