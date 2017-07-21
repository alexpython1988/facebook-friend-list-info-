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

	time.sleep(1)

def main():
	for i in range(7):
		acct, pwd = config.get_account_pwd(i)
		test_accont(acct, pwd)

if __name__ == '__main__':
	main()