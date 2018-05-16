#!/usr/bin/python                                                             
# coding = UTF-8                                                  
import os, sys                                                             
import urllib                                                                  
import time
import PyPDF2
import urllib2
import shutil 
import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO




pdf=['']*1001
web = urllib.urlopen("https://iclr.cc/Conferences/2018/Schedule?type=Poster").read() 

#<a href="content_cvpr_2017/papers/Teney_Graph-Structured_Representations_for_CVPR_2017_paper.pdf">pdf</a>
#print web

i=0      
content=web.find(r'https://openreview.net/forum?id=')   #this is finding the int position of this text    
end=web.find(r'"',content)                                                       
#h1=web.find(r'html/',href)                      
#h2 = web.find(r'">',h1)            
print 'Listing All PDFs...'
time.sleep(1)

while content!=-1 and end!=-1 and i<2000:                       
      initialhtml='https://openreview.net/pdf?id='
      endhtml=web[content+32:end]
      #print endhtml
      pdf[i]=initialhtml+endhtml
      print "final html is: "+pdf[i]                                                         

      content=web.find(r'https://openreview.net/forum?id=',end)                                                       
      end=web.find(r'"',content)                       
      #temp = web.find(r'">',value)                         
      i=i+1                                                               
else:                                                                             
         print '---------------end page------------------'   


print "\nNow print all the organizations..."  
time.sleep(1)                                                   
length= len(pdf)




currentdir= os.path.join(os.getcwd(), 'zlidownload')

## Try to remove tree; if failed show an error using try...except on screen

shutil.rmtree(currentdir,ignore_errors=True,onerror=None)    



os.mkdir('zlidownload')
os.chdir(os.path.join(os.getcwd(), 'zlidownload'))


email=['']*10000
name=['']*10000
org=['']*10000
count=0

for i in xrange(0,200):

	def getFile(url):
	    file_name ="test.pdf"
	    u = urllib2.urlopen(url)
	    f = open(file_name, 'wb')

	    block_sz = 8192
	    while True:
	        buffer = u.read(block_sz)
	        if not buffer:
	            break

	        f.write(buffer)
	    f.close()
        
	 #   print "Sucessful to download" + " " + file_name
    
	
	
	#print"what the hell the url is: "+ pdf[i]


	myfile="test.pdf"
	if os.path.isfile(myfile):
                 os.remove(myfile)

	else:    ## Show an error ##
          print("Notice: %s file not found, no need to delete\n" % myfile)
            
	getFile(pdf[i])

	with open("test.pdf", "rb") as f:
	  
		  input1 = PdfFileReader(f)
		  #print input1
		# print how many pages input1 has:
		#print("document1.pdf has %d pages." % input1.getNumPages())

		  page1 = input1.getPage(0)

		  a = page1.extractText().encode('UTF-8','ignore')
    
	  
	point = 0
	i=0

	
	s=a.find("@")
	point=a.find(".",s)	
	#i=a.find("\n")

	
	while s != -1:

		for x in xrange(i,s): 
				   #print "now s="+str(s)
				   
			   #print "HERE IS A:  "+a   
			   s1=a.find("\n",i+1,s)
			   #print"this is s1"+str(s1)
			   if s1 == -1:
			    #print "something"
					 end = a.find("\n",point)
					 end1 = a.find(",",point)

					 if end1 < end:
					 	end=end1


					 #print "the initial point is: " + str(point)

					 for x in xrange(point,end):

						  endpoint=a.find(".",point,end)

						  if endpoint == -1:
						  	endpoint=point-1
						  	#print "the endpoint is: "+ str(endpoint)
						  	break

						  else:
						    point=endpoint+1#remember plus one to prevent repeating


					 if a[i]==",":
					 	i=i+1
					 print"email: "+ a[i:end]
					 print "person: "+ a[i:s]
					 print "organization: "+ a[s+1:endpoint]+"\n"

					 email[count]=  a[i:end]
					 name[count]=  a[i:s]
					 org[count]= a[s+1:endpoint]+"\n"
                     
					 count = count+1
                     #print "check count now, should increase: "+ str(count)



					 break

			   else:
			   #print "s1="+str(s1)
			   #print "s="+str(s)
				 i=s1+1 #avoid repeat searching

		i= a.find("\n",point)#does not avoid repeat searching here
		i1= a.find(",",point)
		if i1 < i:
			i=i1+1  #id detect "," first, then search the first "," from the point, plus one to hide it from printing
		s=a.find("@",point)
		point=a.find(".",s)
	    
dataframe = pd.DataFrame({'email:': email,'person:': name,'organization:': org})
dataframe.to_csv("resultx.csv",index=False,sep=',')

		#i=i+1 #i saves value of s1,just the last \n statement, increases one step
		#print"i's value check: "+ str(i)
	#print "\nnew i: "+str(i)
	    #s=a.find(r"@",s+1)
	    #n=a.find("\n",s)


	






	
    
	#print"s is: "+ s
	#print"a is this: "+ a[0:120]
	#i=0
	
	    # break 

	  # else:
	 #print "s1="+str(s1)
	 #print "s="+str(s)
	    #s=s1
	   # continueas

	 #i=point+1
	#print "\nnew i: "+str(i)

	   





	

