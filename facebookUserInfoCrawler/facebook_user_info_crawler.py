from selenium import webdriver
import config
import time
from bs4 import BeautifulSoup as bs
import json

#data strcuture to store information obtained
friend_list = []
friend_friends_url = dict()

def crawler_config_and_login_account():
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
	browser.maximize_window()
	#login into account
	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(config.ACCOUNT)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(config.PASSWORD)

	browser.find_element_by_id("u_0_q").click()

	#broswer in the main page after login
	return browser

def scrapy_friend_list_based_on_account(browser):
	#go to friend lists
	browser.find_element_by_link_text("Friend Lists").click()
	browser.find_element_by_link_text("See All Friends").click()

	i = 0
	while(i < 15):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		i += 1

	html = browser.page_source
	soup = bs(html)
	
	# for a in soup.find_all('a', href = True):
	# 	s = str(a['href'])
	fl = []

	ul = soup.find_all("ul", "uiList _262m _4kg")
	ul_ext = soup.find_all("ul", "uiList _262m expandedList _4kg")
	#combine all ul together
	ul_list = ul + ul_ext
	#find all links for each friend in friend list in order to continue obtain information of their friends	
	for each_ul in ul_list:
		divs = each_ul.find_all("div", "fsl fwb fcb")
		for each_div in divs:
			a_list = each_div.find_all("a")
			for each_a in a_list:
				 href_info = each_a['href']
				 if(href_info.endswith("_tab")):
				 	fl.append(href_info)
				 	#extract user id from url, this user id is unique for each user
				 	#use this as key to distinguish if two people with same name is the same person
				 	id_url = href_info.split("/")[-1]
				 	fid = ""
				 	if(id_url.startswith("profile.php")):
				 		fid += id_url.split("?")[-1].split("&")[0].split("=")[-1]
				 	else:
				 		fid += id_url.split("?")[0]
				 	#add data to json file

def go_to_info_page_on_account(browser):
	browser.find_element_by_id("userNav").click()
	print(2)
	return browser

def scrapy_user_info(browser):
	print(1)

def main():
	browser_1 = crawler_config_and_login_account()
	scrapy_friend_list_based_on_account(browser_1)
	browser_1.back()
	browser_2 = go_to_info_page_on_account(browser_1)
	scrapy_user_info(browser_2)

	#obtain info of other users

	#create a new tab
	browser_2.execute_script("window.open('');")
	browser_2.get("url here")

if __name__ == '__main__':
	main()