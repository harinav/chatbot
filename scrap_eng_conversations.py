import scrapy
import urllib
import html2text


class BrickSetSpider(scrapy.Spider):
    name = 'eng_conv'
    start_urls = ['https://www.eslfast.com/robot/topics/college/collegelife.htm']
    h = html2text.HTML2Text()
    h.ignore_links = True
    
    def format_data(self,data):
        data = data.replace("b\\\'\\n\\n\\n\\n",'').replace("\\n\\n\\n",'').replace("\\n\\n",'')\
                   .replace("\\n\\n\\n\\n|",'').replace('**Search Images**','').replace('**Translate**','')\
                   .replace("\\n \\n\\n Repeat",'').replace('**','').replace("\\\\\\\'","'").replace('---|---','')\
                   .replace("\\\'","'").replace('\\n','').replace('\n',' ').replace('  ','').replace('Repeat','')\
                   .replace("Practice the Conversations of This Topic with MikeCopyright (C) 2018\\. All rights reserved.eslfast.com\'",'')\
                   .replace(' A:', '\nA:').replace(' B:','\nB:').replace("b\' ",'').replace('|1','')\
                   .replace(' 2','').replace(' 3','')
        return data
    
    def parse(self, response):
        
        questions_file = open('F:\ChatBot\scraping\conv.txt','w')
        
        NAME_SELECTOR = 'li a ::text'
        NEXT_PAGE_SELECTOR = 'li a ::attr(href)'
        
        for category_name,url in zip(response.css(NAME_SELECTOR).extract(),response.css(NEXT_PAGE_SELECTOR).extract()):
            print("{'name': "+str(category_name)+",'url':"+str(url)+"}",file=questions_file)
            response = urllib.request.urlopen('https://www.eslfast.com/robot/topics/college/'+str(url))
            html = response.read()
            
            file = open('F:\ChatBot\scraping\collegelife\\'+str(category_name)+'.txt','w')
            data = self.h.handle(str(html))
            print(self.format_data(data),file=file)
            file.close()
        
        print(40*'-',file=questions_file, end=' ')
        questions_file.close()