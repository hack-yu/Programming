# written by hackyu
# eamils of stack_exchange leagues crawling
# usage python 3.x
# -*-encoding:utf-8-*-
# Function Call Flow : main -> request_links -> request_emails

import re
import requests
import unicodedata
from bs4 import BeautifulSoup

total_count = 0                                             # found email count increment.

# Function request_emails
def request_emails(email_request_link, page_number):                 # start function requests_emails
    global total_count                                      # global variable
    urls = email_request_link                               # request links in index ex) pages of 1/week, pages of 2/week
    result_list_check = ""                                  # findall email regular expression in requests page.
    emails = ""                                             # result emails. 
    i = 0
    user_numbers = 1                                             # Try Numbers.
    
    while i < len(urls):
        url = str(urls[i])[1:]                              # byte object to string
        url = url.replace("'","") 
    
        try:
            print ("[Try Page:%d User:%d]" % (page_number, user_numbers), "  ", url)
            res2 = requests.get(url)
            result_list_check = re.findall(r"(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)", res2.text) #regular expression email form
            user_numbers = user_numbers+1
            
            # if not result_list_check:                           # not exist email form in page
            #     print ("not exist")
            
            if result_list_check:
                if "png" or "icon" in result_list_check:        # not email form delete
                    del result_list_check[0]

                if result_list_check:                           # exist email form in page
                    total_count = total_count + 1               # Found It!
                    count = 0                                   # recombination

                    for index in range(0, len(result_list_check)):
                            result_list = result_list_check[index]

                    for index in range(0, len(result_list)):                    
                        '''
                        example
                        print mail -> ('hackyu','naver','com')

                        case count == 0
                            result ->>>> hackyu@
                        case count == 1
                            result ->>>> hackyu@naver
                        case count == 2 
                            result ->>>> hackyu@naver.com     
                        '''
                        if count == 0:
                            result = result_list[index]+"@"
                    
                        elif count == 1:
                            result = result+result_list[index]
                        
                        elif count == 2:
                            result = result+"."+result_list[index]
                            emails = emails+result+", "
                            if result != "team@stackexchange.com":
                                print ("\nFound It!!:", result, "Found Count: ", total_count, "\n")
                                with open('a.txt','a') as f:
                                    f.write(result+"\n")           
                        count = count+1
            i += 1
        except Exception as e:
            print(e)
            print("Error! Continue Retry request_emails")
            continue                                        





# Function request_links
def request_links(url, params, page_number):
    res = requests.get(url, params=params)  
    soup = BeautifulSoup(res.text, "html.parser")
    link = soup.select("#leagueUserList > div > div.user.user > a")
    email_request_link = []

    for i in range(0, len(link)):
        j = link[i]            
        href_tags = j.get("href")
        result = unicodedata.normalize('NFKD', href_tags).encode('ascii','ignore')
        email_request_link.append(result)
    request_emails(email_request_link, page_number)                                      # end function requests_links





if __name__ == "__main__":    
    leagues_list = []
    
    url = "https://stackexchange.com/leagues/"
    res = requests.get(url) 
    soup = BeautifulSoup(res.text, "html.parser")   # response content or text html prase
    link = soup.select(".league-list > div > a")    # tag base select
     
    # find leagues list
    for i in link:
        href_tags = i.get("href")
        result = unicodedata.normalize('NFKD', href_tags).encode('ascii','ignore') 
        leagues_list.append(result)
    

    for i in leagues_list:
        a = str(i)[1:]              # byte object to string
        a = a.replace("'", "")

        j = 1
        
        url = "https://stackexchange.com" + a   # url setting
        print("url: ", url)
        
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")   # response content or text html parse
        
        page_numbers = soup.find_all('span', {'class': 'page-numbers'}) # tag base find_all
        page_numbers = int(str(page_numbers[7]).replace("<span class=\"page-numbers\">", "").replace("</span>", "")) # find max page_numbers
        print("page_numbers: ", page_numbers)

      
        while j <= page_numbers:
            params = { "page" : j }
            print ("\n===========================url: %s page: %d===========================\n" % (url, j))
            email_requests_link = []
        
            try:
                request_links(url, params, j) # call request_links
                j += 1

            except Exception as e:
                print(e)
                print("Error! Continue Retry main")
                #j -= 1
                continue