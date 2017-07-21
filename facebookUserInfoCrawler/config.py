'''
change ACCDOUNT and PASSWORD to random before push the project to github
'''
CHROME_DRIVER_PATH = r"E:\driver\chromedriver.exe"
#CHROME_DRIVER_PATH = r"/usr/bin/chromedriver"

URL = "http://www.facebook.com"

START1 = 0
END1 = 300000

START2 = 300000
END2 = 600000

START3 = 600000
END3 = 1025749

ID = "alex"

THRESHOLD_FOR_MAX_NUMBER_OF_USER_TO_CRWAL = 10000000

EMAIL = False

INTO_DB = False

USE_VIETUAL_SCREEN = True

def get_account_pwd(index):
	acct = None
	pwd = None
	with open('accountandpwd.txt', "r") as f:
		for i, each in enumerate(f):
			if i == index * 2:
				acct = each[:-1]
			if i == index * 2 + 1:
				pwd = each[:-1]
	return acct, pwd
