import logging
import random

FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(filename='get_user_info.log',level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("task")


def m1(l):
	for i in range(50):
		l.append(random.randint(0,10))
	for each in l:
		try:
			print(10/ each)
			msg = "each is " + str(each)
			logger.info(msg)
		except:
			logger.error("0 have been found!")

l = []
m1(l)
