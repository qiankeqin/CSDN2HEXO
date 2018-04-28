# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

# 图床
PIC_SOURCE = ''

# watermark
PIC_STYLE = ''

 # 查找图片
def find_pics(article_path, pics):
    # 打开md文件
    f = open(article_path, 'r', encoding='utf-8')
    content = f.read()

    # 匹配正则 match ![]()
    results = re.findall(r"!\[(.+?)\)", content)
    # print('pic len = ', len(results))

    for result in results:
        temp_pic = result.split("](")
        # print(temp_pic)
        # 将图片加入到图片数组当中
        if len(temp_pic) == 2:
            pics.append(temp_pic[1])

    f.close()
    return pics

# 替换链接 添加样式
def replace_url(article_path):
	# 打开md文件
	idx = 0
	f1 = open(article_path, 'r', encoding='utf-8')
	f2 = open('test.md', 'w', encoding='utf-8')
	for line in f1:
		content = line
		# print(content)

		# 去除水印链接
		pattern = re.compile(r'\?watermark(.+?)\)')
		content = re.sub(pattern, ')', content)
		# print(content)

		# 替换图床
		# 第一种形式
		content = content.replace('http://img.blog.csdn.net/',PIC_SOURCE)
		# 第二种形式
		content = content.replace('https://img-blog.csdn.net/',PIC_SOURCE)

		# 添加样式
		# pattern = re.compile(r'http://p7tst3obo.bkt.clouddn.com/(.+?)\)')
		pattern = re.compile(PIC_SOURCE+'(.+?)\)')
		results = re.findall(pattern, content)
		if len(results):
			for result in results:
				content = content.replace(result, result + PIC_STYLE)

		f2.write(content)

	f1.close()	
	f2.close()
	os.remove(article_path)
	os.rename('test.md', article_path)

# 去除水印
def delete_watermark(pics):
	for i in range(0, len(pics)):
		# 第一种形式的水印
		pics[i] = pics[i].split('?watermark')[0]
		# 第二种形式的水印
		pics[i] = pics[i].replace('https://img-blog.csdn.net/','http://img.blog.csdn.net/')


# 下载图片
def download_pic(url):
	r = urllib.request.urlopen(url) 			  # directly access

	content = r.read()
	if content[0] == 0xff and content[1] == 0xd8 :
		pic_type = '.jpg'
	else:
		pic_type = '.png'

	name = url.split('http://img.blog.csdn.net/')[1]+pic_type
	print('downloading ->',name)

	file_path = os.path.join(name)
	# if not os.path.isfile(file_path):

	with open(name, "wb") as code:
	   code.write(content)

	# else:
	# 	print("file exist")			

# 列出文件夹下所有的目录与文件
def get_lists_path(path):
	article_list = os.listdir(path) 
	# print(len(list))
	# for i in range(0,len(article_list)):
	# 	print(article_list[i])
	return article_list

def save_list_to_file(l_name, f_name):
    l_name = sorted(set(l_name), key = l_name.index)     
    # print('l_name = ', l_name)     
    print('l_name len = ', len(l_name))

    with open(f_name, 'w', encoding='utf-8') as file:
        for x in range(0,len(l_name)):
            file.write(str(l_name[x])+'\n')

# module test
if __name__ == '__main__':
	# 获取 hexo 博客文章目录 _post 下的文件
	article_lists = get_lists_path('_posts')
	print(len(article_lists))  

	# 从文件中获取图片链接保存到列表
	pics_lists = list()
	for i in range(0, len(article_lists)):
		find_pics('_posts\\'+article_lists[i], pics_lists)
	print('pics_list len = ', len(pics_lists))	

	# 去除图片链接水印
	delete_watermark(pics_lists)

	# 保存到文件
	save_list_to_file(pics_lists, 'pics_list.txt')	

	# 依次下载
	if not os.path.exists('pic'):
		os.mkdir('pic')
	os.chdir('pic')
	print(os.getcwd())	
	for pics_list in pics_lists:
		if 'blog' in pics_list:
			print(pics_list)
			download_pic(pics_list)

	# 替换图床链接
	for article_list in article_lists:
		print(article_list)
		replace_url('_posts\\'+article_list)