from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException  
import config
import time
from bs4 import BeautifulSoup as bs
from Helper import My_Queue
from Helper import Bloom_Filter
from Helper import Counter
import random
#TODO 
#TODO add dfunctions for collect data into json

#data strcuture to store information obtained
queue = My_Queue()
page_bottom = ["medley_header_events", "medley_header_photos", "medley_header_likes"]
bloom_filter = Bloom_Filter(43132763, 30)
count = Counter()
display = None
def crawler_config_and_login_account():
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
		
		time.sleep(1)
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
				 		#print(count.size()		 			
	task2_output(fl)

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

	#close new tab and switch back to account
	browser.close()
	browser.switch_to_window(browser.window_handles[-1])
	return browser

def scrapy_friend_list_of_friends(browser, person_info):
	time.sleep(1)
	browser.find_element_by_xpath("//div[@class='_6_7 clearfix lfloat _ohe']/a[3]").click()
	#browser.find_element_by_xpath("//div[@id='u_0_o']/a[3]").click()
	scrapy_friend_list_based_on_account(browser, person_info)

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
	scrapy_friend_list_based_on_account(browser_1, None)

	i = 0
	while not queue.is_empty() and count.size() < 1000000:
		i += 1
		if i % 5:
			time.sleep(random.random()*1000)
		time.sleep(1)
		next_url = queue.pop()
		browser_1.execute_script("window.open('');")
		browser_1.switch_to_window(browser_1.window_handles[-1])
		browser_1.get(next_url)
		scrapy_friend_list_of_friends(browser_1, None)
		browser_1.close()
		browser_1.switch_to_window(browser_1.window_handles[-1])
	browser_1.quit()
	
def task2_output(url):
	if len(url) != 0:
		with open("new_list.txt", "a") as f:
			for each in url:
				print(each, file = f, end = "\n")

def main():
	browser_1 = crawler_config_and_login_account()
	try:
		task2(browser_1)
	except:
		browser_1.switch_to_window(browser_1.window_handles[-1])
		browser_1.back()
		browser_1.refresh()
		task2(browser_1)

if __name__ == '__main__':
	main()