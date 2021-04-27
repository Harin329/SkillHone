from bs4 import BeautifulSoup
import requests
import csv

## Scrape for skills mentioned in company job descriptions!

baseLink = 'https://jobs.apple.com'
totalPage = 95

## Init total counter
dictionary = dict()

for page in range(1, totalPage + 1):
    print("Page: " + str(page))
    ## Enter base site
    website = requests.get(baseLink + '/en-ca/search?team=apps-and-frameworks-SFTWR-AF+cloud-and-infrastructure-SFTWR-CLD+core-operating-systems-SFTWR-COS+devops-and-site-reliability-SFTWR-DSR+engineering-project-management-SFTWR-EPM+information-systems-and-technology-SFTWR-ISTECH+machine-learning-and-ai-SFTWR-MCHLN+security-and-privacy-SFTWR-SEC+software-quality-automation-and-tools-SFTWR-SQAT+wireless-software-SFTWR-WSFT+machine-learning-infrastructure-MLAI-MLI+deep-learning-and-reinforcement-learning-MLAI-DLRL+natural-language-processing-and-speech-technologies-MLAI-NLP+computer-vision-MLAI-CV+applied-research-MLAI-AR&page=' + str(page))
    soup = BeautifulSoup(website.content, 'html.parser')

    ## Find job table
    id = soup.find(id = 'tblResultSet')

    tbodytags = id.find_all('tbody')
    ## Iterate jobs on each page
    for tag in tbodytags:
        name = tag.find_all('a')
        print(name[0].string)
        job = requests.get(baseLink + name[0]['href'])
        jobSoup = BeautifulSoup(job.content, 'html.parser')
        
        ## Find qualifications
        qualifications = jobSoup.find(class_ = 'jd__list')
        if qualifications != None:
            for trait in qualifications:
                text = trait.find_all('span')
                text = text[0].string
                if text != None:
                    ## Seperate words that have special characters
                    text = text.strip().lower().replace("," , " ").replace("/" , " ").split(" ")
                    for word in text:
                        # print(word)
                        ## Remove special characters
                        w = word.replace("," , "").replace("/" , "").replace(")" , "").replace("(" , "").replace("." , "").replace("!" , "")
                        if w in dictionary:
                            dictionary[w] = dictionary[w] + 1
                        else:
                            dictionary[w] = 1

## Write to csv
with open('./results/Apple.csv', 'w') as f:  
    writer = csv.writer(f)
    for k, v in dictionary.items():
       writer.writerow([k, v])

