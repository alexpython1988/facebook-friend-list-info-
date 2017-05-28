from selenium import webdriver
import config
import time

def crawler_setup():
	# deactivate notifications from chrome
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2, "credentials_enable_service": False, "profile.password_manager_enabled": False}
	chrome_options.add_experimental_option("prefs",prefs)
	#chrome_options.add_argument("--enable-save-password-bubble=false")
	# chrome_options.add_user_profile_preference("credentials_enable_service", False);
	# chrome_options.add_user_profile_preference("profile.password_manager_enabled", False);

	#create browser
	browser = webdriver.Chrome(executable_path = config.CHROME_DRIVER_PATH, chrome_options = chrome_options)
	browser.get(config.URL)

	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(config.ACCOUNT)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(config.PASSWORD)

	#login
	browser.find_element_by_id("u_0_q").click()

	#go to friend lists
	browser.find_element_by_link_text("Friend Lists").click()
	browser.find_element_by_link_text("See All Friends").click()

	i = 0
	while(i < 30):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		i += 1

	return browser

def scrapy_friend_list(browser):
	pass

crawler_setup()