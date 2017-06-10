s = '''
<div class="_4ms4" id="u_fetchstream_4_0"><div class="_5h60" id="pagelet_hometown" data-referrer="pagelet_hometown"><div><div class="_4qm1"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Current City and Hometown</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_3pw9 _2pi4 _2ge8" id="current_city"><div class="clearfix _ikh"><div class="_4bl9"><div class="clearfix"><img class="_3-91 _8o _8t lfloat _ohe img" height="36" src="https://external-mia1-2.xx.fbcdn.net/safe_image.php?d=AQAlcY2jp98cSuIX&amp;w=36&amp;h=36&amp;url=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F7%2F76%2FDsg_Gainesville_13th_and_University_Intersection_Approach_20050507.jpg%2F720px-Dsg_Gainesville_13th_and_University_Intersection_Approach_20050507.jpg&amp;cfs=1&amp;fallback=hub_city&amp;f&amp;_nc_hash=AQCoRxe0_RakMMIC" width="36" alt=""><div class="_42ef"><div class="_6a"><div class="_6a _6b" style="height:36px"></div><div class="_6a _6b"><span class="_50f5 _50f7"><a href="https://www.facebook.com/pages/Gainesville-Florida/105630226138026" data-hovercard="/ajax/hovercard/page.php?id=105630226138026" data-hovercard-prefer-more-content-show="1">Gainesville, Florida</a></span><div class="fsm fwn fcg">Current city</div></div></div></div></div></div></div></li><li class="_3pw9 _2pi4 _2ge8" id="hometown"><div class="clearfix _ikh"><div class="_4bl9"><div class="clearfix" id="hometown"><img class="_3-91 _8o _8t lfloat _ohe img" height="36" src="https://external-mia1-2.xx.fbcdn.net/safe_image.php?d=AQC6k21AEaN1LfhH&amp;w=36&amp;h=36&amp;url=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fa%2Fa0%2FHohhot_Central_Square.jpg%2F720px-Hohhot_Central_Square.jpg&amp;cfs=1&amp;fallback=hub_city&amp;f&amp;_nc_hash=AQA8Lg04D_gZAXS9" width="36" alt=""><div class="_42ef"><div class="_6a"><div class="_6a _6b" style="height:36px"></div><div class="_6a _6b"><span class="_50f5 _50f7"><a href="https://www.facebook.com/pages/Hohhot/108601122497020" data-hovercard="/ajax/hovercard/page.php?id=108601122497020" data-hovercard-prefer-more-content-show="1">Hohhot</a></span><div class="fsm fwn fcg">Hometown</div></div></div></div></div></div></div></li></ul></div></div></div></div>
'''
from bs4 import BeautifulSoup as bs
soup = bs(s, "lxml")

divs = soup.find_all("div", class_="_4qm1")

l3 = []

div_3_1a = divs[0].find("div", class_ = "clearfix _h71")
title_text_3_1a = div_3_1a.text
print(title_text_3_1a)


divs_3_1a = divs[0].find_all("div", class_ = "_42ef")
#print(divs_3_1a)
# if (divs_3_1a is None) or (len(divs_3_1a) == 0):
# 	pass
# else:
if len(divs_3_1a) > 0:
	for each_div_3_1a in divs_3_1a:
		c3 = dict()
		#print(each_div_3_1a)
		loc_info_3_1a = each_div_3_1a.find("span", class_ = "_50f5 _50f7").text
		c3["place"] = loc_info_3_1a
		div_3_1c = each_div_3_1a.find("div", class_ = "fsm fwn fcg")
		if div_3_1c is not None:
			detail_loc_3_1a = div_3_1c.text
			c3["detail"] = detail_loc_3_1a
		l3.append(c3)





print(l3)

