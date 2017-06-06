from selenium import webdriver
import config
import time
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
from Helper import My_Queue

#TODO 
#TODO add dfunctions for collect data into json

#data strcuture to store information obtained
queue = My_Queue()
friend_list = set()
user_info_all = []

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

	time.sleep(0.5)

	browser.find_element_by_id("u_0_q").click()

	#broswer in the main page after login
	return browser

def scrapy_friend_list_based_on_account(browser):
	i = 0
	while(i < 30):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.2)
		i += 1

	html = browser.page_source
	soup = bs(html, "lxml")
	
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
				 	#TODO

# def go_to_info_page_on_account(browser):
# 	browser.find_element_by_id("userNav").click()
# 	print(2)
# 	return browser

def handle_each_new_friend_in_list(browser):
	#create a new tab
	browser.execute_script("window.open('');")
	browser.switch_to_window(browser.window_handles[-1])
	#extract next url from list

	next_url = queue.pop()

	browser.get(next_url)

	#get user friend list
	scrapy_friend_list_of_friends(browser)
	browser.back()

	#get user info
	scrapy_user_info(browser)

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
		info = get_info_of_user(browser, index)
		#process info collected with current user info

	#change to log later for debug or check data purposes
	print("get info for {} at {}".format(uid, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def get_info_of_user(browser, index):
	info = dict()
	#webElement.get_attribute("innnerHTML");
	#obtain html source and add into beautifulsoup for process
	html_source = browser.find_element_by_class_name("_4ms4")
	soup = bs(html_source.get_attribute("innerHTML"), "lxml")
	divs = soup.find_all("div", class_ = "_4qm1")

	#process html with beautifulsoup based on index(different page)
	if index == 2:
		#divs_2_1 = soup.find_all("div", class_ = "_4qm1")
		for each_div_2_1 in divs:
			#section title
			title_text_2_1 = each_div_2_1.find("div", class_ = "clearfix _h71").text
			#section content
			divs_2_2 = each_div_2_1.find_all("div", class_ = "_2tdc")
			#section might not contain any information
			if (divs_2_2 is None) or (len(divs_2_2) == 0):
				#add title and empty info to dataset
				continue
			else:
				for each_div_2_2 in divs_2_2:
					place_info_2 = each_div_2_2.find("div", class_ = "_2lzr _50f5 _50f7").text
					details_2 = each_div_2_2.find("div", class_ = "fsm fwn fcg").text
					#add information to section information

	elif index == 3:
		#divs_3_1 = soup.find_all("div", class_ = "_4qm1")
		#handle number of divs_3_1 has been found
		num = len(divs)
		if num == 0:
			#return no information
			pass
		elif num == 1:
			#only process section 0
			div_3_1a = divs[0].find("div", class_ = "clearfix _h71")
			title_text_3_1a = div_3_1a.text
			divs_3_1a = divs[0].find_all("div", class_ = "_4bl0")
			if (divs_3_1a is None) or (len(divs_3_1a) == 0):
				pass
			else:
				for each_div_3_1a in divs_3_1a:
					loc_info_3_1a = each_div_3_1a.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_1a = each_div_3_1a.find("div", class_ = "fsm fwn fcg").text
					#process data with title
		elif num == 2:
			#process section 0 and 1
			#section 0
			div_3_1b = divs[0].find("div", class_ = "clearfix _h71")
			title_text_3_1b = div_3_1b.text
			divs_3_1b = divs[0].find_all("div", class_ = "_4bl0")
			if (divs_3_1b is None) or (len(divs_3_1b) == 0):
				pass
			else:
				for each_div_3_1b in divs_3_1b:
					loc_info_3_1b = each_div_3_1b.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_1b = each_div_3_1b.find("div", class_ = "fsm fwn fcg").text
					#process data with title

			#section 1
			div_3_2 = divs[1].find("div", class_ = "clearfix _h71")
			title_text_3_2 = div_3_2.text
			divs_3_2 = divs[1].find_all("div", class_ = "_2tdc")
			if (divs_3_2 is None) or (len(divs_3_2) == 0):
				pass
			else:
				for each_div_3_2 in divs_3_2:
					loc_info_3_2 = each_div_3_2.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_2 = each_div_3_2.find("div", class_ = "fsm fwn fcg").text
					#process data with title

	elif index == 4:
		#get information div, should be 2 of them
		#divs_4_1 = soup.find_all("div", class_ = "_4qm1")
		#process information in each div
		for each_div_4_1 in divs:
			#each div title
			title_text_4_1 = each_div_4_1.find("div", class_="clearfix _h71").text
			#list of info in each div
			l_4 = []
			divs_4_2 = each_div_4_1.find_all("div", class_ = "clearfix _ikh")
			if (divs_4_2 is None) or (len(divs_4_2) == 0):
				#save only title of the section
				#TODO
				continue
			else:
				for each_div_4_2 in divs_4_2:
					key = each_div_4_2.find("div", class_ = "_4bl7 _3xdi _52ju").text
					value = each_div_4_2.find("div", class_ = "clearfix").text
					_temp_4 = dict()
					_temp_4[key] = value
					l_4.append(_temp_4) 
					#add data with title info
					
	elif index == 5:
		#this section has two seperate section one of it has div class = "_4qm1 editAnchor"
		#but soup.find_all("div", class_ = "_4qm1") match class partially which can include this class = "_4qm1 editAnchor"
		#no special code need for now
		for i, each_div_5_1 in enumerate(divs):
			#each div title
			title_text_5_1 = each_div_5_1.find("div", class_="clearfix _h71").text
			divs_5_1 = each_div_5_1.find_all("div", class_ = "_42ef")
			for each_div_5_2 in divs_5_1:
				# u_id = None
				# u_name = None
				# u_relation = None
				a_5_1 = each_div_5_1.find_all("a")
				if len(a_5_1) == 0:
					s_5_1 = each_div_5_1.find_all("span")
					if len(s_5_1) != 0:
						u_name = each_div_5_1.find("span").text
						u_relation = each_div_5_1.find_all("div", class_ = "fsm fwn fcg")[1].text
						#add info with title
					else:
						#no information
						#combine with title (add empty list {title:[]})
						pass #TODO	
				else:
					for each_a_5_1 in a_5_1:
						u_id = each_a_5_1['href']
						u_name = each_a_5_1.text
						
						if i == 1:
							u_relation = each_a_5_1.find("div", class_ = "_173e _50f8 _50f3").text
						elif i == 2:
							u_relation = each_a_5_1.find_all("div", class_ = "fsm fwn fcg")[1].text
						#add info with title
						#process data with title

	elif index == 6:
		for each_div_6_1 in divs:
			title_text_6_1 = each_div_6_1.find("div", class_ = "clearfix _h71").text

			class_6 = ["_4bl9", "_4bl7", "_2tdc"]
			u_info_div = None
			u_info = None
			flag = None
			for each_class in class_6:
				u_info_div = each_div_6_1.find("div", class_ = each_class)

			if u_info_div is not None:
				if flag == "_2tdc":
					u_info = dict()
					for each_div_6_2 in each_div_6_1.find_all("div", class_ = flag):
						key = each_div_6_2.find("div", class_ = "fsm fwn fcg").text
						value = each_div_6_2.find("span", class_ = "_50f4").text
						u_info[key] = value
				else:
					u_info = u_info_div.text
			#process data with tile

	#return current information to the person we crawl
	return info
	

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