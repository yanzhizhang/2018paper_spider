#!/usr/bin/python                                                             
# -*- coding: latin-1 -*-                                                     
import os, sys                                                             
import urllib                                                                  
import time


 
#j=0  
#while j<2:

author=['']*3200
web = urllib.urlopen("http://openaccess.thecvf.com/CVPR2017.py").read() 


i=0             
form=web.find(r'<form id=')                                                       
value=web.find(r'value=',form)  #从form位置开始搜索最近value=                    
temp = web.find(r'">',value)    #从value位置开始搜素最近">                      
print 'Listing All Authors...'
time.sleep(3)
                           
while form!=-1 and value!=-1 and temp!=-1 and i<3200:                       
      author[i]=web[value+7:temp+0]                                                          
      print author[i]                                                         

      form=web.find(r'<form id=',temp)                                                       
      value=web.find(r'value=',form)  #从form位置开始搜索最近value=                     
      temp = web.find(r'">',value)    #从value位置开始搜素最近">                      
      i=i+1                                                               
else:                                                                             
         print '---------------end page------------------'                                       
#j=j+1                                                     


form=web.find(r'<form id=')                                                       
value=web.find(r'value=',form)  #从form位置开始搜索最近value=                    
temp = web.find(r'">',value)    #从value位置开始搜素最近">      
temp='http://blog.sina.com.cn/s/articlelist_1191258123_0_'+str(page)+'.html'












