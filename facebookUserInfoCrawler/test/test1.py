from bs4 import BeautifulSoup as bs

s = '''<div class="_4ms4" id="u_0_1u"><div class="_5h60" id="pagelet_relationships" data-referrer="pagelet_relationships"><div class="_4qm1 editAnchor" id="u_d_0"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Relationship</span></div><ul class="uiList fbProfileEditExperienc
4kg _4ks"><li class="_3pw9 _2pi4 _2ge8" data-privacy-fbid="8787550733" id="u_d_1" data-pnref="rel"><div class="clearfix _ikh"><div class="_4bl9"><div class="clearfix"><a class="_3-91 _8o lfloat _ohe" href="https://www.facebook.com/huiyuan.hu.1" tabindex="-1" aria-hidden="true"><img class="img" h
t="36" src="https://scontent-iad3-1.xx.fbcdn.net/v/t1.0-1/p40x40/11698356_895272513867599_6661363165978346886_n.jpg?oh=6ccfb7f3c86b2933978656d1fa35b894&amp;oe=59DE635B" width="36" alt=""></a><div class="_42ef"><div class="_6a"><div class="_6a _6b" style="height:36px"></div><div class="_6a _6b"><
class="_2lzr _50f5 _50f7"><a href="https://www.facebook.com/huiyuan.hu.1" data-hovercard="/ajax/hovercard/user.php?id=100001545752021" data-hovercard-prefer-more-content-show="1">Michelle Hu</a></div><div class="_173e _50f8 _50f3">Married since May 17, 2014</div></div></div></div></div></div></d
/li></ul></div><div class="_4qm1" data-pnref="family"><div class="clearfix _h71"><span class="_h72 lfloat _ohe _50f8 _50f7">Family Members</span></div><ul class="uiList fbProfileEditExperiences _4kg _4ks"><li class="_3pw9 _2pi4"><div class="clearfix _4bbo" role="button" tabindex="0"><div class="
w _3-91 _8o lfloat _ohe"><i class="_5rsx img sp_fTLpXpK1dse sx_966b7b"></i></div><div class="_42ef"><div class="_6a"><div class="_6a _6b" style="height:36px"></div><div class="_6a _6b"><span class="_50f8 _50f4">No family members to show</span></div></div></div></div></li></ul></div></div></div>'''

soup = bs(s, "lxml")
divs = soup.find_all("div", class_ = "_4qm1")

for i, each_div_5_1 in enumerate(divs):
	#each div title
	title_text_5_1 = each_div_5_1.find("div", class_="clearfix _h71").text
	print(title_text_5_1)
	divs_5_1 = each_div_5_1.find_all("div", class_ = "_42ef")
	#print(len(divs_5_1))
	for each_div_5_2 in divs_5_1:
		a_5_1 = each_div_5_1.find_all("a")
		print(a_5_1)
		if len(a_5_1) == 0:
			# s_5_1 = each_div_5_1.find_all("span")
			# if len(s_5_1) != 0:
			# 	u_name = each_div_5_1.find("span").text
			# 	#index out of range
			# 	u_relation = each_div_5_1.find_all("div", class_ = "fsm fwn fcg")[1].text
			# 	#add info with title
			# else:
			# 	#no information
			# 	#combine with title (add empty list {title:[]})
			if i == 0:
				u_stat = each_div_5_2.text
				print("stats: " + u_stat)
			elif i == 1:
				u_name = each_div_5_2.find("span", class_ = "_50f5 _50f7").text if each_div_5_2.find("span", class_ = "_50f5 _50f7") is not None else None
				u_relation = each_div_5_2.find_all("div", class_ = "fsm fwn fcg")[1].text if len(each_div_5_2.find_all("div", class_ = "fsm fwn fcg")) > 1 else None
				print("name: {} rel: {}".format(u_name, u_relation) )
		else:
			u_id = a_5_1[-1]['href']
			u_name = a_5_1[-1].text
			if i == 0:
				u_relation = each_div_5_2.find("div", class_ = "_173e _50f8 _50f3").text
			elif i == 1:
				u_relation = each_div_5_2.find_all("div", class_ = "fsm fwn fcg")[1].text
			print("id: {}; name: {}".format(u_id, u_name))
			print(u_relation)
