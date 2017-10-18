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

	submit = browser.find_element_by_xpath("//input[@value='Log In']")
	time.sleep(1)
	submit.click()
     
    ################### add to crawler #########################  
	time.sleep(3)

	for i in range(5):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.5)
	browser.execute_script("window.scrollTo(0, 0);")

	#process notification pop up
	try:
		browser.find_element_by_xpath("//a[@action='cancel']").click()
	except:
		pass

	#process phone pop up
	try: 
		browser.find_element_by_xpath("//input[@value='Not now']").click()
	except:
		pass

	time.sleep(1)

	bar = browser.find_element_by_xpath("//div[@id='userNavigationLabel']")
	bar.click()
	time.sleep(1)
	logout = browser.find_element_by_xpath("//*[contains(text(), 'Log Out')]")
	logout.click()
	############################################################

	browser.quit()

def main():
	for i in range(4):
		acct, pwd = config.get_account_pwd(i)
		test_accont(acct, pwd)

if __name__ == '__main__':
	main()