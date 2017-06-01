from selenium import webdriver
import config
import time
from bs4 import BeautifulSoup as bs
import json
import time
from datetime import datetime

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
	i = 0
	while(i < 30):
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

# def go_to_info_page_on_account(browser):
# 	browser.find_element_by_id("userNav").click()
# 	print(2)
# 	return browser

def handle_each_new_friend_in_list(browser):
	#create a new tab
	browser.execute_script("window.open('');")
	browser.switch_to_window(browser.window_handles[-1])
	browser.get("url here")

	#get user info
	scrapy_user_info(browser)

	#get user friend list
	scrapy_friend_list_of_friends(browser)

	#close new tab and switch back to account
	browser.close()
	browser.switch_to_window(browser.window_handles[-1])
	return browser

def scrapy_user_info(browser, uid):
	#go to about tab
	browser.find_element_by_link_text("About").click()
	#browser.find_element_by_xpath("//div[@class='_6_7 clearfix']/a[2]").click()
	
	#obtain information in each section: 
	'''
	Work and Education
	Places Lived
	contact and basic info
	family and relationships
	details about
	''' 
	for index in range(2, 7):
		browser.find_element_by_xpath("//ul[@class='uiList _4kg']/li[{}]/a[@class='_5pwr']".format(index)).click()
		get_info_of_user(browser)
		time.sleep(5)

	#change to log later
	print("get info for {} at {}".format(uid, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def get_info_of_user(browser):
	#locate webElement id based on index
	# element_id = ""
	# if index == 2:
	# 	element_id += "pagelet_eduwork"
	# elif index == 3:
	# 	element_id += "pagelet_hometown"
	# elif index == 4:
	# 	element_id += ""
	# elif index == 5:
	# 	element_id += ""
	# elif index == 6:
	# 	element_id += ""

	#webElement.get_attribute("innnerHTML");
	html_content = browser.find_element_by_id("u_0_3y")
	soup = bs(html_content.get_attribute("innerHTML"))
	

def scrapy_friend_list_of_friends(browser):
	browser.find_element_by_xpath("//div[@class='_6_7 clearfix']/a[3]").click()
	scrapy_friend_list_based_on_account(browser)


def main():
	browser_1 = crawler_config_and_login_account()

	#go to friend lists
	browser_1.find_element_by_link_text("Friend Lists").click()
	browser_1.find_element_by_link_text("See All Friends").click()

	scrapy_friend_list_based_on_account(browser_1)
	browser_1.back()
	
	# browser_2 = go_to_info_page_on_account(browser_1)
	# scrapy_user_info(browser_2)

if __name__ == '__main__':
	main()