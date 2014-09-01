import pycurl, threading, time, urllib2
from bs4 import BeautifulSoup

url_list = ['http://www.bostonfanfavorites.com/redwings/',
            'http://www.bostonfanfavorites.com/bruins/', 
            'http://www.detroitfanfavorites.com/trigers/',
            'http://www.detroitfanfavorites.com/redwings/'
             'http://www.fanfavorites.com']

#url_list = ['http://google.com',
#            'http://google.com',
#            'http://google.com',
#            'http://google.com',
#            'http://google.com']

proxy_list = ['127.0.0.1']

link_list = []
link_dict = dict()

max_runs = 10

def make_url_request(url, proxy=None):
    if proxy:
        proxy = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
    req = urllib2.Request(str(url))
    req.add_header('User-Agent',
         'Chrome/37.0.2049.0')
    
    # Add try block here

    res = urllib2.urlopen(req)
    data = res.read().decode("UTF-8")
    soup = BeautifulSoup(data)

    return soup 

def find_links(url, soup):
    link_dict.update({url: []}) 

    for link in soup.find_all('a'):
        link_url = link.get('href')
        link_list.append(link_url)

        if url in link_dict.keys():
            link_dict[url].append(link_url)
        else:
            link_dict.update({url:  []})

class getterThread(threading.Thread):
    def __init__(self, threadID, url, threadname=None, proxies=[]):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.runcount = 0
        if(len(proxies) > 0):
            self.proxies = proxies
		else:
			self.proxies = [None]
        if threadname:
            self.name =  threadname


    def run(self):
        print "Starting " + self.name + " ID: " + str(self.threadID)
        
        sleeptime = 3
        soup = make_url_request(self.url)
        find_links(self.url, soup)
        
        print "URL is %s - %s ID: %s" % (self.url, self.name, self.threadID)

		for self.runcount in xrange(0, max_runs / len(self.proxies)):
			for proxy in self.proxies:
				make_url_request(self.url, proxy)
				time.sleep(sleeptime) 
				if self.runcount <= 100:
					sleeptime += .2
				elif self.runcount > 100 and self.runcount < 10000:
					sleeptime += .1
				elif self.runcount >= 1000 and self.runcount < 5000:
					sleeptime +=.05
				elif self.runcount >= 5000:
					sleeptime +=.025
            
        print "Exiting " + self.name + " ID: " + str(self.threadID)

def execute():
    threads = create_threadlist()
    start_threads(threads)
    end_threads(threads)

def create_threadlist():
    i = 1
    threadlist = []
    for url in url_list:
        threadname = "Getter Thread"
        print "Initializing %s, ID: %d" % (threadname, i)
        newthread = getterThread(i, url, threadname, proxy_list)
        threadlist.append(newthread)
        i+=1
    return threadlist

def start_threads(threadlist):
    for thread in threadlist:
        thread.start()    

def end_threads(threadlist):
    for thread in threadlist:
        thread.join()

def main():
    execute()

if __name__ == '__main__':
    main()
