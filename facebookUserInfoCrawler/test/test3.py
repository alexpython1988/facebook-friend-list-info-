s ='''
<div class="_4ms4" id="u_fetchstream_4_0"><div><div class="_5h60" id="pagelet_bio" data-referrer="pagelet_bio"><div class="_4qm1"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">About Xi</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_3pw9 _2pi4 _2ge8 profileText"><div class="clearfix _ikh"><div class="_4bl9"><span class="_c24 _50f4">I like DOTA,Chemistry and Rock music!</span></div></div></li></ul></div></div><div class="_5h60" id="pagelet_pronounce" data-referrer="pagelet_pronounce"><div class="_4qm1"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Name Pronunciation</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_43c8 _5f6p" id="u_1a_0"><div class="_2tdc"><div class="clearfix _ikh"><div class="_4bl7"><span class="_3-90" id="u_1a_1"><span class="_d2c __3e" tabindex="0" role="button"><i class="_4brm img sp_Qt3aYVGesyX sx_742cd2" height="16" width="16" alt=""></i><audio preload="auto"><source src="/tts/?flavor=echo&amp;text=[%23%22Si%3A%23]%20[%23%22jA%3AN%23]&amp;id=100003086045405&amp;format=mp3" type="audio/mpeg"></audio></span></span></div><div class="_4bl7"><span class="_50f4">SHEE YAHNG</span></div></div></div></li></ul></div></div><div class="_5h60" id="pagelet_nicknames" data-referrer="pagelet_nicknames"><div class="_4qm1"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Other Names</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_43c8 _5f6p _3twh" id="1261842173928639"><div class="_2tdc"><span class="_50f4">asd</span></div><div class="fsm fwn fcg">Nickname</div></li><li class="_43c8 _5f6p _3twh" id="1261821153930741"><div class="_2tdc"><span class="_50f4">Xy</span></div><div class="fsm fwn fcg">Alternate Spelling</div></li></ul></div></div><div class="_5h60" id="pagelet_quotes" data-referrer="pagelet_quotes"><div class="_4qm1"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Favorite Quotes</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_3pw9 _2pi4 _2ge8 profileText"><div class="clearfix _ikh"><div class="_4bl9"><span class="_c24 _50f4">aaaa</span></div></div></li></ul></div></div><div class="_5h60" id="pagelet_profile_field_with_options" data-referrer="pagelet_profile_field_with_options"></div></div></div>
'''

from bs4 import BeautifulSoup as bs
soup = bs(s, "lxml")

info = dict()
divs = soup.find_all("div", class_="_4qm1")

class_6 = ["_4bl9", "_4bl7", "_2tdc"]
# for each_class in class_6:
for each_div_6_1 in divs:
	l6 = []
	title_text_6_1 = each_div_6_1.find("div", class_ = "clearfix _h71").text
		# div_1 = each_div_6_1.find_all("div", class_ = each_class)
		# if div_1 is not None:
		# 	if each_class  == "_2tdc":
		# 		for each_div_6_2 in each_div_6_1.find_all("li", class_ = "_43c8 _5f6p _3twh"):
		# 			value = each_div_6_2.find("span", class_ = "_50f4").text
		# 			print(value)
		# 			key = each_div_6_2.find("div", class_ = "fsm fwn fcg").text
		# 			print(key)
		# 	else:

	u_info_div = None
	u_info = None
	for each_class in class_6:
		u_info_div = each_div_6_1.find("div", class_ = each_class)
		if u_info_div is not None:
			if each_class == "_2tdc":
				u_info = dict()
				for each_div_6_2 in each_div_6_1.find_all("li", class_ = "_43c8 _5f6p _3twh"):
					print(each_div_6_2)
					value = each_div_6_2.find("span", class_ = "_50f4").text
					print(value)
					key_div = each_div_6_2.find("div", class_ = "fsm fwn fcg")
					#print(key_div)
					if key_div is not None:
						key = key_div.text
						print(key)
						u_info[key] = value
						l6.append(u_info)	
					else:
						info[title_text_6_1] = value
				info[title_text_6_1] = l6
			else:
				info[title_text_6_1] = u_info_div.text
			break

print(info)