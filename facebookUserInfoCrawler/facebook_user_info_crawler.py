from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException  
import config
import time
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
from Helper import My_Queue
from Helper import Bloom_Filter

#TODO 
#TODO add dfunctions for collect data into json

#data strcuture to store information obtained
queue = My_Queue()
friend_set = set()
page_bottom = ["medley_header_events", "medley_header_photos", "medley_header_likes"]
#size is descided based on https://hur.st/bloomfilter?n=4&p=1.0E-20
bloom_filter = Bloom_Filter(43132763, 30)

def crawler_config_and_login_account():
	# display = None
	# if config.USE_VIETUAL_SCREEN:
	# 	from pyvirtualdisplay import Display
	# 	display = Display(visible=0, size=(800, 600))
	# 	display.start()

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

def scrapy_friend_list_based_on_account(browser, person_info):
	i = 0
	while(i < 60):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		
		l = []
		page_bottom_flag = False 
		for each in page_bottom:
			try:
				l.append(browser.find_element(By.ID, each))
			except NoSuchElementException:
				pass
			if  len(l) > 0:
				page_bottom_flag = True
		if page_bottom_flag:
			break
		
		time.sleep(0.3)
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
				 	#extract user id from url, this user id is unique for each user
				 	#use this as key to distinguish if two people with same name is the same person
				 	id_url = href_info.split("/")[-1]
				 	fid = ""
				 	if(id_url.startswith("profile.php")):
				 		fid += id_url.split("?")[-1].split("&")[0].split("=")[-1]
				 	else:
				 		fid += id_url.split("?")[0]
				 	
				 	#task
				 	temp = dict()
				 	temp["friend_id"] = fid
				 	temp["url"] = href_info
				 	fl.append(temp)

				 	if fid not in friend_set:
				 		friend_set.add(fid)
				 		if len(friend_set) <= config.THRESHOLD_FOR_MAX_NUMBER_OF_USER_TO_CRWAL:
				 			queue.put(href_info)
	#add list to friend info
	if person_info is not None:
		person_info["friend list"] = fl

def handle_each_new_friend_in_list(browser, next_url, person_info):
	#create a new tab
	browser.execute_script("window.open('');")
	browser.switch_to_window(browser.window_handles[-1])
	#extract next url from list

	# next_url = queue.pop()
	browser.get(next_url)

	id_url = next_url.split("/")[-1]
	fid = ""
	if(id_url.startswith("profile.php")):
		fid += id_url.split("?")[-1].split("&")[0].split("=")[-1]
	else:
		fid += id_url.split("?")[0]

	#get user friend list
	scrapy_friend_list_of_friends(browser, person_info)
	browser.back()

	#get user info
	person_info["user_id"] = fid
	scrapy_user_info(browser, fid, person_info)

	#close new tab and switch back to account
	browser.close()
	browser.switch_to_window(browser.window_handles[-1])
	return browser

def scrapy_friend_list_of_friends(browser, person_info):
	time.sleep(0.2)
	browser.find_element_by_xpath("//div[@class='_6_7 clearfix lfloat _ohe']/a[3]").click()
	#browser.find_element_by_xpath("//div[@id='u_0_o']/a[3]").click()
	scrapy_friend_list_based_on_account(browser, person_info)

def scrapy_user_info(browser, uid, person_info):
	#go to about tab
	browser.execute_script("window.scrollTo(0, 0);")
	browser.find_element_by_link_text("About").click()
	time.sleep(0.2)
	#browser.find_element_by_xpath("//div[@class='_6_7 clearfix']/a[2]").click()
	
	#obtain information in each section: 
	'''
	Work and Education
	Places Lived
	contact and basic info
	family and relationships
	details about
	''' 
	temp = dict()
	for index in range(2, 7):
		browser.find_element_by_xpath("//ul[@class='uiList _4kg']/li[{}]/a[@class='_5pwr']".format(index)).click()
		time.sleep(1)
		info = get_info_of_user(browser, index)
		if len(info) != 0:
			for each in info:
				temp[each] = info[each]

	person_info["info"] = temp
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
			l2 = []
			#section content
			divs_2_2 = each_div_2_1.find_all("div", class_ = "_2tdc")
			#section might not contain any information
			if (divs_2_2 is None) or (len(divs_2_2) == 0):
				li = each_div_2_1.find_all("li", class_ = "_3pw9 _2pi4")
				if len(li) != 0:
					for each_li in li:
						for each_a in each_li.find_all("a"):
							if each_a is not None:
								l2.append(each_a.text)			
			else:
				for each_div_2_2 in divs_2_2:
					c2 = dict()
					place_info_2 = each_div_2_2.find("div", class_ = "_2lzr _50f5 _50f7").text
					details_2 = each_div_2_2.find("div", class_ = "fsm fwn fcg").text
					#add information to section information
					c2["unit"] = place_info_2
					c2["detail"] = details_2
					l2.append(c2)
			info[title_text_2_1] = l2
	elif index == 3:
		l3 = []
		#divs_3_1 = soup.find_all("div", class_ = "_4qm1")
		#handle number of divs_3_1 has been found
		num = len(divs)
		if num == 0:
			pass
		elif num == 1:
			#only process section 0
			div_3_1a = divs[0].find("div", class_ = "clearfix _h71")
			title_text_3_1a = div_3_1a.text
			divs_3_1a = divs[0].find_all("div", class_ = "_42ef")
			# if (divs_3_1a is None) or (len(divs_3_1a) == 0):
			# 	pass
			# else:
			if len(divs_3_1a) > 0:
				for each_div_3_1a in divs_3_1a:
					c3 = dict()
					div_3_1aa = each_div_3_1a.find("span", class_ = "_50f5 _50f7")
					if div_3_1aa is not None:
						loc_info_3_1a = div_3_1aa.text
						c3["place"] = loc_info_3_1a
					div_3_1c = each_div_3_1a.find("div", class_ = "fsm fwn fcg")
					if div_3_1c is not None:
						detail_loc_3_1a = div_3_1c.text
						c3["detail"] = detail_loc_3_1a
					l3.append(c3)
			#process data with title
			info[title_text_3_1a] = l3
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
					c3 = dict()
					loc_info_3_1b = each_div_3_1b.find("span", class_ = "_50f5 _50f7").text
					c3["place"] = loc_info_3_1b
					div_3_1c = each_div_3_1b.find("div", class_ = "fsm fwn fcg")
					if div_3_1c is not None:
						detail_loc_3_1b = div_3_1c.text
						c3["detail"] = detail_loc_3_1b
					l3.append(c3)
					#detail_loc_3_1b = each_div_3_1b.find("div", class_ = "fsm fwn fcg").text
					#process data with title
				info[title_text_3_1b] = l3
			#section 1
			l3 = []
			div_3_2 = divs[1].find("div", class_ = "clearfix _h71")
			title_text_3_2 = div_3_2.text
			divs_3_2 = divs[1].find_all("div", class_ = "_2tdc")
			if (divs_3_2 is None) or (len(divs_3_2) == 0):
				pass
			else:
				for each_div_3_2 in divs_3_2:
					c3 = dict()
					loc_info_3_2 = each_div_3_2.find("span", class_ = "_50f5 _50f7").text
					c3["place"] = loc_info_3_2
					div_3_2a = each_div_3_2.find("div", class_ = "fsm fwn fcg")
					if div_3_2a is not None:
						detail_loc_3_2 = div_3_2a.text
						c3["detail"] = detail_loc_3_2
					#process data with title
			info[title_text_3_2] = l3
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
				pass
			else:
				for each_div_4_2 in divs_4_2:
					key = each_div_4_2.find("div", class_ = "_4bl7 _3xdi _52ju").text
					value = each_div_4_2.find("div", class_ = "clearfix").text
					_temp_4 = dict()
					_temp_4[key] = value
					l_4.append(_temp_4) 
				#add data with title info
				info[title_text_4_1] = l_4
					
	elif index == 5:
		#this section has two seperate section one of it has div class = "_4qm1 editAnchor"
		#but soup.find_all("div", class_ = "_4qm1") match class partially which can include this class = "_4qm1 editAnchor"
		#no special code need for now
		for i, each_div_5_1 in enumerate(divs):
			l5 = []
			#each div title
			title_text_5_1 = each_div_5_1.find("div", class_="clearfix _h71").text
			divs_5_1 = each_div_5_1.find_all("div", class_ = "_42ef")
			for each_div_5_2 in divs_5_1:
				c5 = dict()
				# u_id = None
				# u_name = None
				# u_relation = None
				a_5_1 = each_div_5_1.find_all("a")
				if len(a_5_1) == 0:
					if i == 0:
						u_stat = each_div_5_2.text
						c5["relationship"] = u_stat  
					elif i == 1:
						u_name = each_div_5_2.find("span", class_ = "_50f5 _50f7").text if each_div_5_2.find("span", class_ = "_50f5 _50f7") is not None else None
						u_relation = each_div_5_2.find_all("div", class_ = "fsm fwn fcg")[1].text if len(each_div_5_2.find_all("div", class_ = "fsm fwn fcg")) > 1 else None
						c5["name"] = u_name
						c5["relationship"] = u_relation

				# 	s_5_1 = each_div_5_1.find_all("span")
				# 	if len(s_5_1) != 0:
				# 		u_name = each_div_5_1.find("span").text
				# 		u_relation = each_div_5_1.find_all("div", class_ = "fsm fwn fcg")[1].text
				# 		#add info with title
				# 		c5["name"] = u_name
				# 		c5["relationship"] = u_relation
				# 		l5.append(c5)	
				else:
					u_id = a_5_1[-1]['href']
					u_name = a_5_1[-1].text
					u_relation = None
					if i == 0:
						u_relation = each_div_5_2.find("div", class_ = "_173e _50f8 _50f3").text
					elif i == 1:
						u_relation = each_div_5_2.find_all("div", class_ = "fsm fwn fcg")[1].text
					#add info with title
					c5["name"] = u_name
					c5["user_id"] = u_id
					c5["relationship"] = u_relation
				l5.append(c5)	
			#process data with title
			info[title_text_5_1] = l5
	elif index == 6:
		for each_div_6_1 in divs:
			l6 = []
			title_text_6_1 = each_div_6_1.find("div", class_ = "clearfix _h71").text
			class_6 = ["_4bl9", "_4bl7", "_2tdc"]
			u_info_div = None
			u_info = None
			for each_class in class_6:
				u_info_div = each_div_6_1.find("div", class_ = each_class)
				if u_info_div is not None:
					if each_class == "_2tdc":
						for each_div_6_2 in each_div_6_1.find_all("li", class_ = "_43c8 _5f6p _3twh"):
							u_info = dict()
							value = each_div_6_2.find("span", class_ = "_50f4").text
							key_div = each_div_6_2.find("div", class_ = "fsm fwn fcg")
							if key_div is not None:
								key = key_div.text
								u_info[key] = value
								l6.append(u_info)	
							else:
								info[title_text_6_1] = value
						info[title_text_6_1] = l6
					else:
						info[title_text_6_1] = u_info_div.text
					break

	#return current information to the person we crawl
	return info

def output_json(ul): 
	#can choose to output as file or email the zipped data to user 
	if config.EMAIL:
		#call the email class from send_email.py

		print(ul)
	elif config.INTO_DB:
		#output the json into a file 
		pass
	else:
		with open("file", "a") as f:
			for each in ul:
				print(each, file = f, end = "\n")

def task(browser_1):
	#go to friend lists
	browser_1.find_element_by_link_text("Friend Lists").click()
	browser_1.find_element_by_link_text("See All Friends").click()

	id_url = browser_1.current_url.split("/")[3]
	fid = ""
	if(id_url.startswith("profile.php")):
		fid += id_url.split("?")[-1].split("=")[-1]
	else:
		fid += id_url

	#use bloom filter to replace set to import memory efficiency
	friend_set.add(fid)
	scrapy_friend_list_based_on_account(browser_1, None)
	
	user_info_all = []
	while not queue.is_empty():
		time.sleep(2)
		next_url = queue.pop()
		each_info = dict()
		handle_each_new_friend_in_list(browser_1, next_url, each_info)
		#output_json(each_info)
		
		json_file = json.dumps(each_info)
		print(json_file)
		user_info_all.append(json_file)
		if len(user_info_all) > 1000:
			output_json(user_info_all)
			user_info_all = []
	
	if len(user_info_all) != 0:
		output_json(user_info_all)
	#browser_1.back()
	# browser_2 = go_to_info_page_on_account(browser_1)
	# scrapy_user_info(browser_2)
	browser_1.quit()
	# browser_2 = go_to_info_page_on_account(browser_1)
	# scrapy_user_info(browser_2)

def task2(browser_1):
	browser_1.find_element_by_link_text("Friend Lists").click()
	browser_1.find_element_by_link_text("See All Friends").click()

	id_url = browser_1.current_url.split("/")[3]
	
	fid = ""
	if(id_url.startswith("profile.php")):
		fid += id_url.split("?")[-1].split("=")[-1]
	else:
		fid += id_url

	#use bloom filter to replace set to import memory efficiency
	friend_set.add(fid)
	scrapy_friend_list_based_on_account(browser_1, None)
	
	#user_info_all = []
	i = 0
	while not queue.is_empty():
		i += 1
		if i == 100:
			time.sleep(180)
		time.sleep(1)
		next_url = queue.pop()
		#task2_output(next_url)
		#each_info = dict()
		browser_1.execute_script("window.open('');")
		browser_1.switch_to_window(browser_1.window_handles[-1])
		browser_1.get(next_url)

		id_url = next_url.split("/")[-1]
		fid = ""
		if(id_url.startswith("profile.php")):
			fid += id_url.split("?")[-1].split("&")[0].split("=")[-1]
		else:
			fid += id_url.split("?")[0]

		#get user friend list
		scrapy_friend_list_of_friends(browser_1, None)
		browser_1.close()
		browser_1.switch_to_window(browser_1.window_handles[-1])
		#handle_each_new_friend_in_list(browser_1, next_url, each_info)
		

	browser_1.quit()

def recovery():
	pass

def main():
	browser_1 = crawler_config_and_login_account()
	task(browser_1)
	try:
		task()
	except :
		with open("rest_list.txt", "w") as f:
			while not queue.is_empty:
				print(1)
				print(queue.pop(), file=f, end = "\n")



if __name__ == '__main__':
	main()