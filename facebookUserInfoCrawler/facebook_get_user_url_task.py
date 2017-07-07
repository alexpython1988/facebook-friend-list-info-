from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import config
import time
from bs4 import BeautifulSoup as bs
from Helper import My_Queue
from Helper import Bloom_Filter
from Helper import Counter
import random
import logging
import mmap
import sys
from config import get_account_pwd

#data strcuture to store information obtained
queue = My_Queue()
page_bottom = ["medley_header_events", "medley_header_photos", "medley_header_likes"]
bloom_filter = Bloom_Filter(575103503 , 40)
count = Counter()
FORMAT = '%(asctime)-20s %(name)-5s %(levelname)-10s %(message)s'
logging.basicConfig(filename='get_user_url.log',level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("task")

def reset(browser_1, index):
	browser_1.quit()
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
	k1 = None
	k2 = None
	if index % 3 == 0:
		k1,k2 = get_account_pwd(0)
	elif index % 2 == 0:
		k1,k2 = get_account_pwd(1)
	else:
		k1,k2 = get_account_pwd(2)
	
	email = browser.find_element_by_id("email")
	email.clear()
	email.send_keys(k1)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(k2)

	submit = browser.find_element_by_xpath("//input[@id='u_0_r']")
	time.sleep(0.5)
	submit.click()

	#broswer in the main page after login
	return browser

def resume():
	logger.info("resume from previous backup point...")

	bcount = 0
	bqueue = 0
	with open("backup.txt", "r") as f:
		for i, each in enumerate(f):
			if i == 0:
				bcount = int(each)
			else:
				bqueue = int(each)
	backup_point = bcount - bqueue

	with open("url_list.txt", "r") as f:
		for i, each in enumerate(f):
			id_url = each.split("/")[-1]
			fid = None
			if(id_url.startswith("profile.php")):
				fid = id_url.split("?")[-1].split("&")[0].split("=")[-1]
			else:
				fid = id_url.split("?")[0]
			bloom_filter.add(fid)		

			if i >= backup_point:
				queue.put(each)
			count.increase()
	
	browser_1, display = crawler_config_and_login_account()
	
	i = 0
	flag = 0
	while not queue.is_empty() and count.size() < config.THRESHOLD_FOR_MAX_NUMBER_OF_USER_TO_CRWAL:
		new_url_list = []
		i += 1
		if i % 99 == 0:
			logger.info("reset the browser")
			browser_1 = reset(browser_1, i)

		if i % 5 == 0:
			t = random.random()*1200
			logger.info("sleep {}s".format(t))
			time.sleep(t)
			logger.info(count.size())

		time.sleep(1)
		next_url = queue.pop()
		
		try:
			browser_1.execute_script("window.open('');")
			browser_1.switch_to_window(browser_1.window_handles[-1])
		
			browser_1.get(next_url)
		
			new_url_list = scrapy_friend_list_of_friends(browser_1, None)
			
			browser_1.close()
			browser_1.switch_to_window(browser_1.window_handles[-1])
		except:
			logger.error("Exception happen")
			flag += 1
			if flag > 100:
				sys.exit(1)
			queue.put(next_url)
			if len(browser_1.window_handles) > 1:
				browser_1.switch_to_window(browser_1.window_handles[-1])
				browser_1.close()
			browser_1.switch_to_window(browser_1.window_handles[-1])
			browser_1.refresh()
			continue
		task2_output(new_url_list)
	
	browser_1.quit()


def crawler_config_and_login_account():
	display = None
	if config.USE_VIETUAL_SCREEN:
		from pyvirtualdisplay import Display
		display = Display(visible=0, size=(1080, 720))
		display.start()

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
	k1,k2 = get_account_pwd(0)
	email.send_keys(k1)

	pwd = browser.find_element_by_id("pass")
	pwd.clear()
	pwd.send_keys(k2)

	submit = browser.find_element_by_xpath("//input[@id='u_0_r']")
	time.sleep(0.5)
	submit.click()

	#broswer in the main page after login
	return browser, display

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
		
		time.sleep(0.5)
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
				 	#task2
				 	if not bloom_filter.contains(fid):
				 		count.increase()
				 		bloom_filter.add(fid)
				 		fl.append(href_info)
				 		queue.put(href_info)
	logger.info("get {} urls.".format(len(fl)))			 			 			
	return fl

def scrapy_friend_list_of_friends(browser, person_info):
	time.sleep(0.5)
	browser.find_element(By.XPATH, "//div[@id='fbTimelineHeadline'][@class='clearfix']/div[2]/ul/li[3]/a").click()
	
	#browser.find_element_by_xpath("//div[@id='u_0_o']/a[3]").click()
	return scrapy_friend_list_based_on_account(browser, person_info)

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
	bloom_filter.add(fid)
	new_url_list = scrapy_friend_list_based_on_account(browser_1, None)
	task2_output(new_url_list)

	i = 0
	flag = 0
	while not queue.is_empty() and count.size() < 1000000:
		new_url_list = []
		i += 1

		if i % 5 == 0:
			t = random.random()*1200
			logger.info("sleep {}s".format(t))
			time.sleep(t)
			i = 0
			logger.info(get_output_size())
		
		time.sleep(1)
		next_url = queue.pop()
		
		try:
			browser_1.execute_script("window.open('');")
			browser_1.switch_to_window(browser_1.window_handles[-1])
		
			browser_1.get(next_url)
		
			new_url_list = scrapy_friend_list_of_friends(browser_1, None)
			
			browser_1.close()
			browser_1.switch_to_window(browser_1.window_handles[-1])
		except:
			logger.error("Exception happen")
			flag += 1
			if flag > 100:
				sys.exit(1)
			queue.put(next_url)
			if len(browser_1.window_handles) > 1:
				browser_1.switch_to_window(browser_1.window_handles[-1])
				browser_1.close()
			browser_1.switch_to_window(browser_1.window_handles[-1])
			browser_1.refresh()
			continue
		task2_output(new_url_list)
	
	browser_1.quit()

def get_output_size():
	lines = 0
	with open("url_list.txt", "r+") as f:
		buf = mmap.mmap(f.fileno(), 0)
		readline = buf.readline
		while readline():
			lines += 1
	return "No. of total urls: {}".format(lines)
	
def task2_output(url):
	if len(url) != 0:
		with open("url_list.txt", "a") as f:
			for each in url:
				print(each, file = f, end = "\n")

def left_task():
	with open("backup.txt", "w") as f:
		while not queue.is_empty():
			print(queue.pop(), file=f, end='\n')
		print("*************************************", file=f, end='')

def main():
	#browser_1, display = crawler_config_and_login_account()
	# try:
	# 	task2(browser_1)
	# finally:
	# 	left_task()
	# 	if display is not None:
	# 		display.stop()
	try:
		resume()
	finally:
		left_task()
		


if __name__ == '__main__':
	main()