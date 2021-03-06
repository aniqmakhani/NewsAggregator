import opengraph
import MySQLdb
import sys
from feedfinding import *
import feedparser
import time

class crawler:
        conn = None
        cursor = None
        def __init__(self):
                pass
        def ConnectDB(self):
                try:
                        self.conn = MySQLdb.connect (host='127.0.0.1', port=3306 , user='root', passwd='', db='mydb', charset="UTF8")
                        self.cursor = self.conn.cursor()
                        return self.cursor

                except Exception as e:
                        print e
                        sys.exit()

        def CommitDB(self):
                self.conn.commit()

        def CloseDB(self):
                self.cursor.close()
                self.conn.close()
                
        def add_web(self, url):

                cursor = self.ConnectDB()

                #format of query to insert data in web.
                insert_to_web = "INSERT INTO web (url) VALUES (%s)"

                try:
                        #Run query to insert data.
                        cursor.execute(insert_to_web, (url))

                
                        #Find Rss/Xml links
                        f = feedfinding()
                        feed_list = f.collect_feeds(url)


                        #category code.
                        CategoryList = ['politic','world','entertainment','sport','business','tech','football','cricket','education','health','europe','asia','america','africa']                      
                        
                        
                        #Save each xml link in Table "XML_PAGE"
                        for link in feed_list:

                                cat = 'others'

                                i = 0
                                while(i < len(CategoryList)):
                                    if CategoryList[i] in link.lower():
                                        if CategoryList[i] == 'europe' or CategoryList[i] == 'asia' or CategoryList[i] =='america' or CategoryList[i] =='africa':
                                            cat = 'world'
                                        elif CategoryList[i] == 'football' or CategoryList[i] == 'cricket':
                                            cat = 'sport'
                                        else:
                                            cat = CategoryList[i]
                                            
                                        break
                                    i = i + 1  
                                
                                #format of query to insert data in web.
                                insert_to_xml = "INSERT INTO xml (url,idWeb,category) VALUES (%s, (SELECT idWeb from web where url = %s),%s)"
                                cursor.execute(insert_to_xml, (link, url,cat))


                        self.CommitDB()
                        self.CloseDB()
                
                        print "Successfully Inserted!"

                except Exception as e:
                        print e
                        self.CloseDB()

        def delete_web(self,link):

                try:
                        cursor = self.ConnectDB()
                
                        #Delete xml
                        delete_xml = "DELETE FROM XML WHERE idWeb = (SELECT idWeb FROM WEB WHERE URL = %s)"
                        cursor.execute(delete_xml, (link))

                        #Delete Web
                        delete_web = "DELETE FROM WEB WHERE URL = %s"
                        cursor.execute(delete_web,(link))

                        #Save and Close
                        self.CommitDB()
                        self.CloseDB()

                        print "Successfully Deleted!"
                        
                except Exception as e:
                        print e
                        self.CloseDB()


        def parse_all(self):

                try:
                        cursor = self.ConnectDB()
                        select = "SELECT url FROM xml"
                        cursor.execute(select)
                        rows = cursor.fetchall()
                        
                        for i in rows:
                                print i[0]
                                self.parse_one(i[0])
                                print "process sleeping for 6 sec."
                                time.sleep(6)
        

                        self.CloseDB()
                        
                except Exception as e:
                        print e
                        self.CloseDB()
                        
                
        def parse_one(self, get_link):
                try:
                        cursor = self.ConnectDB()
                        d = feedparser.parse(get_link)
                except Exception, e:
                        print e

                print len(d.entries)                     
                for entry in d.entries:
                        try:
                                Title = entry.title
                        except Exception, e:
                                Title = None

                        try:
                                Link = entry.link
                        except Exception, e:
                                Link = None

                        try:
                                pub = entry.published
                        except Exception, e:
                                pub = None
                
                        try:
                                summ = BeautifulSoup(entry.get('summary'), 'html.parser').text
                        except Exception, e:
                                summ = None

                        check_existing = "SELECT title from news where title = %s"
                        result = cursor.execute(check_existing, (Title))

                        if (result == 0):
                                print "procees is Sleeping for 6 sec"
                                
                                time.sleep(6)
                                
                                try:
                                        page = opengraph.OpenGraph(url=entry.link, scrape = True)
                                        if page.is_valid():
                                                i = page.get('image', None)
                                                if i == None:
                                                        r = requests.get(entry.link, headers = {'User-Agent' : 'ADDDDD'})
                                                        soup = BeautifulSoup(r.text, 'html.parser') 
                                                        
                                                        for im in soup.findAll('img'):
                                                                if im.has_attr('alt'):
                                                                        if im['src'].endswith('.jpg') == True or im['src'].endswith('.png') == True:
                                                                                img = im['src']
                                                                                break
                                                else:
                                                        img = i
                                        else:
                                                img = None

                                except Exception, e:
                                        print e
                                
                                insert_news = "INSERT INTO NEWS (id_xml, title, date_pub, content, external_link, image) VALUES ((SELECT idxml_page FROM XML WHERE URL = %s),%s,%s,%s,%s,%s)"
                                cursor.execute(insert_news, (get_link, Title, pub, summ, Link, img))

                                self.CommitDB()

        
                self.CloseDB()
                print "News is inserted."
