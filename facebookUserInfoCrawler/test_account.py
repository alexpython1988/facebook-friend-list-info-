from selenium import webdriver
import config
import time

def test_accont(k1, k2):
	#create browser
	browser = webdriver.Chrome(executable_path = config.CHROME_DRIVER_PATH)
	browser.get(config.URL)
	browser.maximize_window()

	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(k1)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(k2)

	submit = browser.find_element_by_xpath("//input[@id='u_0_r']")
	time.sleep(1)
	submit.click()

	time.sleep(3)
	browser.quit()

def main():
	list1 = [config.ACCOUNT0,config.ACCOUNT1,config.ACCOUNT2,config.ACCOUNT3,config.ACCOUNT4,config.ACCOUNT5]
	list2 = [config.PASSWORD0,config.PASSWORD1,config.PASSWORD2,config.PASSWORD3,config.PASSWORD4,config.PASSWORD5]

	for i in range(2,6):
		test_accont(list1[i], list2[i])

if __name__ == '__main__':
	main()