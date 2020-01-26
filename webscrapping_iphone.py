from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


url = "https://www.flipkart.com/apple-iphone-7-black-32-gb/product-reviews/itmen6daftcqwzeg?pid=MOBEMK62PN2HU7EE&lid=LSTMOBEMK62PN2HU7EEINTGNU&marketplace=FLIPKART"

# Connect to the website and return the html to the variable ‘page’
try:
    page = urlopen(url)
except:
    print("Error opening the URL")


# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Get the number of review pages
pagecnt = soup.find_all('div',{'class':'_2zg3yZ _3KSYCY'})

# current page number
pagenb=int(pagecnt[0].span.text.split(" ")[1])

# last page number
pageend=int(pagecnt[0].span.text.split(" ")[3])

# list to store all the URLs of review pages
superlst=[]


# since the url has just the "&page=2" at the end to select the page
# we iterate through first page number till last page number and build urls
for i in range(1,pageend+1):
    superlst.append(url+"&page="+str(i))

# create empty Data frame to store review data
df=pd.DataFrame()

# to avoid issues related to data collection caused by errors due to http connections
# we shall save the data collected for every 45 pages we scrap
for i in range(1,pageend+1,45):
    for urls in superlst[i:i+45]:
        url=urls
        try:
            page = urlopen(url)
        except:
            print("Error opening the URL")

        soup = BeautifulSoup(page, 'html.parser')
        # has labels - heading of the user review
        Label = soup.find_all('p',{'class':'_2xg6Ul'})

        # name of the user who has written the review
        names=soup.find_all('p',{'class':'_3LYOAd _3sxSiS'})

        # location of the reviewer
        places=soup.find_all('p',{'class':'_19inI8'})

        # Time of review
        years=soup.find_all('p',{'class':'_3LYOAd'})

        # numerical rating of product by customer
        ratings=soup.find_all('div',{'class':['hGSR34 E_uFuv','hGSR34 _1nLEql E_uFuv','hGSR34 _1x2VEC E_uFuv']})

        # review
        Rev = soup.find_all('div',{'class':'qwjRop'})

        # labels
        lbllst=[x.text for x in Label]

        #time
        ylist=[x.text for x in years if(("Today" in x.text) or (" month" in x.text) or (" day" in x.text) or ("," in x.text and len(x.text.split(", "))==2 and ",," not in x.text))==True ]

        #ratings
        rlist=[x.text for x in ratings]

        #names
        nlist=[x.text for x in names]


        #places
        plist=[]
        c=1
        for x in places:
            if(c==0):
                plist.append("")
            c=0
            for y in x:
                if("," in y.text):
                    c=c+1
                    plist.append(y.text.split(", ")[1])
        if(c==0):
            plist.append("")

        Revlst=[x.find_all('div', {'class': ''})[1].text for x in Rev]

        # store the review data from a single page in a dataframe
        # append the dataframe to collection data frame
        df=df.append(pd.DataFrame(np.column_stack([nlist,rlist,lbllst,ylist,plist,Revlst]),columns=['name','rating','label','period','place','review']),ignore_index=True,sort=None)

        # check the status of page being scrapped
        print(url[-3:].replace('=','').replace("e",''),end='\r')

    # save the 45 page review data to csv & replace it for every 45th page
    df.to_csv("D:/Flipcart.csv",mode='w',header=True)
