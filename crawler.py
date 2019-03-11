# _*_ coding:utf-8 _*_
import os
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re

# 获取内容
def get_content(url):

	html = urllib.request.urlopen(url)
	content= html.read().decode('utf-8',"ignore")
	html.close()
	return content

#获取帖子的页数
def get_page_num(url):
	content = get_content(url)
	# < a href = "/p/2314539885?pn=31" >尾页 < / a >
	pattern = r'<a href="/p/.*?pn=(.*)">尾页</a>'
	return int(re.findall(pattern, content)[0])

# 保存图片
def get_images(info,photo_path,npage,photo_format):

	if not os.path.exists(photo_path):
		os.makedirs(photo_path)
	soup = BeautifulSoup(info)
	#找到所有  img 标签  然后后面跟的class =  BDE_Image
	all_img = soup.find_all('img',class_="BDE_Image")
	#设置计数器
	x=0
	for img in all_img:
		image_name = photo_path+str(npage)+"_"+str(x)+photo_format
		urllib.request.urlretrieve(img['src'],image_name)
		x += 1
		print("find photo page %d NO. %d"%(npage,x))

	return len(all_img)

# 主函数 可改动的参数
# URL——贴吧路径
# photo-path——图片保存的路径
# 图片格式——'.jpg' '.png' '.gif'
if __name__=='__main__':
	url='https://tieba.baidu.com/p/5992489128'
	photo_path="./0311-1/"

	page_num=get_page_num(url)
	for i in range(page_num):
		page_url=url+'?pn='+str(i+1)
		info = get_content(url)
		print(get_images(info,photo_path,i+1,'.gif'))
