from selenium import webdriver
import config
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
from Helper import My_Queue

#data strcuture to store information obtained
queue = My_Queue()
friend_set = set()
threshold = True
# user_info_all = []

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
		time.sleep(0.5)
		i += 1

	html = browser.page_source
	soup = bs(html)
	
	# for a in soup.find_all('a', href = True):
	# 	s = str(a['href'])
	#fl = []

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
				 	#fl.append(href_info)
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

				 	if fid not in friend_set:
				 		friend_set.add(fid)
				 		queue.put(href_info)
				 		#make a global flag, if condition meet here set the flag to stop crawling friend list 

				 	if len(friend_set) > config.THRESHOLD_FOR_MAX_NUMBER_OF_USER_TO_CRWAL:
				 		threshold = False
				 	print("Friend id: {}".format(fid))

# def go_to_info_page_on_account(browser):
# 	browser.find_element_by_id("userNav").click()
# 	print(2)
# 	return browser

def handle_each_new_friend_in_list(browser, next_url):
	#create a new tab
	browser.execute_script("window.open('');")
	browser.switch_to_window(browser.window_handles[-1])
	
	#get info for next url in list
	browser.get(next_url)

	id_url = next_url.split("/")[-1]
	fid = ""
	if(id_url.startswith("profile.php")):
		fid += id_url.split("?")[-1].split("&")[0].split("=")[-1]
	else:
		fid += id_url.split("?")[0]

	#get user friend list
	if threshold:
		scrapy_friend_list_of_friends(browser)
		browser.back()

	#get user info
	scrapy_user_info(browser, fid)

	#close new tab and switch back to account
	browser.close()
	browser.switch_to_window(browser.window_handles[-1])
	return browser

def scrapy_user_info(browser, uid):
	#go to about tab
	browser.execute_script("window.scrollTo(0, 0);")
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
		get_info_of_user(browser, index)
		#process info collected with current user info
		
	#change to log later for debug or check data purposes
	print("get info for {} at {}".format(uid, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def get_info_of_user(browser, index):
	#info = dict()
	#webElement.get_attribute("innnerHTML");
	#obtain html source and add into beautifulsoup for process
	html_source = browser.find_element_by_class_name("_4ms4")
	soup = bs(html_source.get_attribute("innerHTML"))
	divs = soup.find_all("div", class_ = "_4qm1")

	#process html with beautifulsoup based on index(different page)
	if index == 2:
		#divs_2_1 = soup.find_all("div", class_ = "_4qm1")
		for each_div_2_1 in divs:
			#section title
			title_text_2_1 = each_div_2_1.find("div", class_ = "clearfix _h71").text
			print(title_text_2_1)
			#section content
			divs_2_2 = each_div_2_1.find_all("div", class_ = "_2tdc")
			print(len(divs_2_2))
			#section might not contain any information
			if (divs_2_2 is None) or (len(divs_2_2)) == 0:
				#add title and empty info to dataset
				print("No info")
			else:
				for each_div_2_2 in divs_2_2:
					place_info_2 = each_div_2_2.find("div", class_ = "_2lzr _50f5 _50f7").text
					details_2 = each_div_2_2.find("div", class_ = "fsm fwn fcg").text
					print("place: {}; detail: {}".format(place_info_2, details_2))
					#add information to section information

	elif index == 3:
		#divs_3_1 = soup.find_all("div", class_ = "_4qm1")
		#handle number of divs_3_1 has been found
		num = len(divs)
		print(num)
		if num == 0:
			#return no information
			print("No info")
		elif num == 1:
			#only process section 0
			div_3_1a = divs[0].find("div", class_ = "clearfix _h71")
			title_text_3_1a = div_3_1a.text
			print(title_text_3_1a)
			divs_3_1a = divs[0].find_all("div", class_ = "_4bl0")
			if (divs_3_1a is None) or (len(divs_3_1a) == 0):
				pass
			else:
				for each_div_3_1a in divs_3_1a:
					loc_info_3_1a = each_div_3_1a.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_1a = each_div_3_1a.find("div", class_ = "fsm fwn fcg").text
					print("loc: {}; detail: {}".format(loc_info_3_1a, detail_loc_3_1a))
					#process data with title
		
		elif num == 2:
			#process section 0 and 1
			#section 0
			div_3_1b = divs[0].find("div", class_ = "clearfix _h71")
			title_text_3_1b = div_3_1b.text
			print(title_text_3_1b)
			divs_3_1b = divs[0].find_all("div", class_ = "_4bl0")
			if (divs_3_1b is None) or (len(divs_3_1b) == 0):
				pass
			else:
				for each_div_3_1b in divs_3_1b:
					loc_info_3_1b = each_div_3_1b.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_1b = each_div_3_1b.find("div", class_ = "fsm fwn fcg").text
					print("loc: {}; detail: {}".format(loc_info_3_1b, detail_loc_3_1b))
					#process data with title

			#section 1
			div_3_2 = divs[1].find("div", class_ = "clearfix _h71")
			title_text_3_2 = div_3_2.text
			print(title_text_3_2)
			divs_3_2 = divs[1].find_all("div", class_ = "_2tdc")
			if (divs_3_2 is None) or (len(divs_3_2) == 0):
				pass
			else:
				for each_div_3_2 in divs_3_2:
					loc_info_3_2 = each_div_3_2.find("span", class_ = "_50f5 _50f7").text
					detail_loc_3_2 = each_div_3_2.find("div", class_ = "fsm fwn fcg").text
					print("loc: {}; detail: {}".format(loc_info_3_2, detail_loc_3_2))
					#process data with title

	elif index == 4:
		#get information div, should be 2 of them
		#divs_4_1 = soup.find_all("div", class_ = "_4qm1")
		#process information in each div
		for each_div_4_1 in divs:
			#each div title
			title_text_4_1 = each_div_4_1.find("div", class_="clearfix _h71").text
			print(title_text_4_1)
			#list of info in each div
			divs_4_2 = each_div_4_1.find_all("div", class_ = "clearfix _ikh")
			if (divs_4_2 is None) or (len(divs_4_2) == 0):
				#save only title of the section
				#TODO
				pass
			else:
				for each_div_4_2 in divs_4_2:
					key = each_div_4_2.find("div", class_ = "_4bl7 _3xdi _52ju").text
					value = each_div_4_2.find("div", class_ = "clearfix").text
					#add data with title info
					print(key + ", " + value)
					
	elif index == 5:
		#this section has two seperate section one of it has div class = "_4qm1 editAnchor"
		#but soup.find_all("div", class_ = "_4qm1") match class partially which can include this class = "_4qm1 editAnchor"
		#no special code need for now
		for i, each_div_5_1 in enumerate(divs):
			#each div title
			title_text_5_1 = each_div_5_1.find("div", class_="clearfix _h71").text
			print(title_text_5_1)
			divs_5_1 = each_div_5_1.find_all("div", class_ = "_42ef")
			for each_div_5_2 in divs_5_1:
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
						print("id: {}; name: {}".format(u_id, u_name))
						print(u_relation)

	elif index == 6:
		for each_div_6_1 in divs:
			title_text_6_1 = each_div_6_1.find("div", class_ = "clearfix _h71").text
			print(title_text_6_1)

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
			print(u_info)
			#process data with tile
	

def scrapy_friend_list_of_friends(browser):
	browser.find_element_by_xpath("//div[@class='_6_7 clearfix']/a[3]").click()
	scrapy_friend_list_based_on_account(browser)


def main():
	browser_1 = crawler_config_and_login_account()

	#go to friend lists
	browser_1.find_element_by_link_text("Friend Lists").click()
	browser_1.find_element_by_link_text("See All Friends").click()

	id_url = browser_1.current_url.split("/")[3]
	fid = ""
	if(id_url.startswith("profile.php")):
		fid += id_url.split("?")[-1].split("=")[-1]
	else:
		fid += id_url
	print("account id: " + fid)
	friend_set.add(fid)

	scrapy_friend_list_based_on_account(browser_1)
	
	while not queue.is_empty():
		next_url = queue.pop()
		handle_each_new_friend_in_list(browser_1, next_url)

	#browser_1.back()
	# browser_2 = go_to_info_page_on_account(browser_1)
	# scrapy_user_info(browser_2)
	print("demo done.")
	browser_1.quit()

if __name__ == '__main__':
	main()