from selenium import webdriver
import config
import time
from multiprocessing import Process

def task1(browser):
	# chrome_options = webdriver.ChromeOptions()
	# prefs = {"profile.default_content_setting_values.notifications" : 2, "credentials_enable_service": False, "profile.password_manager_enabled": False}
	# chrome_options.add_experimental_option("prefs",prefs)
	#chrome_options.add_argument("--enable-save-password-bubble=false")
	# chrome_options.add_user_profile_preference("credentials_enable_service", False);
	# chrome_options.add_user_profile_preference("profile.password_manager_enabled", False);

	#create browser
	# browser = webdriver.Chrome(executable_path = config.CHROME_DRIVER_PATH, chrome_options = chrome_options)
	# browser.get(config.URL)
	# browser.maximize_window()
	#login into account
	browser.execute_script("window.open('');")
	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(config.ACCOUNT0)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(config.PASSWORD0)

	submit = browser.find_element_by_xpath("//input[@id='u_0_r']")
	time.sleep(10)
	submit.click()

def task2(browser):
	
	#chrome_options.add_argument("--enable-save-password-bubble=false")
	# chrome_options.add_user_profile_preference("credentials_enable_service", False);
	# chrome_options.add_user_profile_preference("profile.password_manager_enabled", False);

	#create browser
	# browser = webdriver.Chrome(executable_path = config.CHROME_DRIVER_PATH, chrome_options = chrome_options)
	# browser.get(config.URL)
	# browser.maximize_window()
	#login into account
	browser.execute_script("window.open('');")
	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(config.ACCOUNT4)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(config.PASSWORD4)

	submit = browser.find_element_by_xpath("//input[@id='u_0_r']")
	time.sleep(10)
	submit.click()

def main():
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2, "credentials_enable_service": False, "profile.password_manager_enabled": False}
	chrome_options.add_experimental_option("prefs",prefs)
	browser = webdriver.Chrome(executable_path = config.CHROME_DRIVER_PATH, chrome_options = chrome_options)
	browser.get(config.URL)
	browser.maximize_window()
	#cause driver problem
	p1 = Process(target=task1, args=(browser, ))
	p2 = Process(target=task2, args=(browser, ))

	p1.start()
	p2.start()

if __name__ == '__main__':
	main()