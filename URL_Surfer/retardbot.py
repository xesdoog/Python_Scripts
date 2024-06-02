import sys
import os
import random
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
count = 1200
os.system("apt install toilet")
color1 = ["\033[1;31;40m", "\033[1;32;40m", "\033[1;33;40m", "\033[1;34;40m", "\033[1;35;40m", "\033[1;36;40m"]
def color():
 return str(random.choice(color1))
def banner():
 os.system("clear")
 os.system("toilet -fmono12 -F Cunt Bot")
 print("    \033[1;36;40m Written by  : \033[1;32;40m SAMURAI")
 print("    \033[1;36;40m Github      : \033[1;32;40m www.github.com/xesdoog")
 print("        \033[1;31;40m!NOTE: Most Modern Websites Can Detect This Bot.")
 print("\n\n") 
def req(proxy_url, target_url, timeo, stay_time):
 r = requests.get(proxy_url)
 soup = BeautifulSoup(r.content, 'html.parser')
 list = soup.find(class_= 'table table-striped table-bordered')
 list1 = list.findAll('td')
 iplist = []
 portlist = []
 j = 0
 while (j < (8 * count)):
  try:
   a = str (list1[j].contents[0])
   iplist.append(a)
   j = j + 8
  except:
   break
 j = 1
 while (j < (8 * count)):
  try:
   a = str(list1[j].contents[0])
   portlist.append(a)
   j = j + 8
  except:
   break
 for index in range (0, (len(iplist) - 1)):
  try:   
   PROXY = iplist[index] + ":" + portlist[index]
   print("\033[1;32;40mTrying From " + color() + str(PROXY))
   webdriver.DesiredCapabilities.FIREFOX['proxy'] = {"httpProxy":PROXY, "ftpProxy":PROXY, "sslProxy":PROXY, "proxyType":"MANUAL"}
   driver=webdriver.Firefox()
   driver.set_page_load_timeout(timeo)
   driver.get(target_url)
   time.sleep(stay_time)
   driver.close()
  except Exception as e:
   driver.close()
banner()
target = input("\033[1;33;40mEnter The Target URL:")
timeout = int(input("\033[1;33;40mEnter The Timeout (in seconds) (recommended 100):"))
stay = int(input("\033[1;33;40mEnter The Task Duration (How long you want to stay on the page in seconds):"))
urllist = ["https://www.sslproxies.org", "https://us-proxy.org", "https://free-proxy-list.net/uk-proxy.html", "https://free-proxy-list.net/anonymous-proxy.html", "https://free-proxy-list.net", "https://www.socks-proxy.net"]
for purl in urllist:
 banner()
 req(purl, target, timeout, stay)
 print("\033[1;32;40mSleeping For 10 Seconds...")
 time.sleep(10)
