#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Homework 2 Solutions
#Name:Jiayi Wang
#UNI: jw4304


# In[ ]:


#Q1 part 1
import requests
from bs4 import BeautifulSoup


# In[ ]:


part_number= 1 
seed_url = "https://press.un.org/en"
response = requests.get(seed_url)
soup = BeautifulSoup(response.content, 'html.parser')

h2_element = soup.find('h2', text='PRESS RELEASES')
press_release_links = h2_element.find_next_sibling()
links = [a['href'] for a in press_release_links.find_all('a')] #extract all the links which are press releases
press_release_homepage = links[-1]
print(press_release_homepage)


# In[ ]:


def extract_links(url):#extract links 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_element = soup.find('div', class_="view-content") 
    all_links = [a['href'] for a in div_element.find_all('a')]#find press release links
    next_page_button = soup.find('a', title='Go to next page') #example: <a class="page-link" href="?page=8" ... </a>
    next_page_link = press_release_homepage + next_page_button['href'] #complete link of the next page
    return next_page_link, all_links #use comma to return 2 items
def find_all_links(target_page): #extract links on this page and continue for the next page
    page = 0 
    current_page = press_release_homepage
    while page < target_page: #return links exactly at the target page. When page = taregt_page, "while" loop will stop.
        next_page, all_links = extract_links(current_page) #name the two things returned from the previous function 
        current_page = next_page #update current page in the loop 
        page += 1
    return all_links


# In[ ]:


#save press release which meets requirements as txt files
part_number= 1 
press_release_number = 1
page = 1

while press_release_number <= 10: #the while loop will stop after 10 txt files are saved (at 11th, break)
    links = find_all_links(page) #it's not the complete link
    for link in links:
        if press_release_number == 11: 
            break
        complete_link= "https://press.un.org" + link 
        response = requests.get(complete_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tag = soup.find('a', href="/en/press-release", hreflang="en", string="Press Release")#check if this is a press release again
        if anchor_tag:
            div_element = soup.find('div', class_="field field--name-body field--type-text-with-summary field--label-hidden field__item")
            content = div_element.text.strip()
            if "crisis" in content.lower(): #check if crisis is included
                filename = f"{part_number}_{press_release_number}.txt" #construct the filename
                with open(filename, 'w', encoding='utf-8') as file:#save the content to the .txt file
                    file.write(content)
                print(complete_link)
                print(f"Saved content to {filename}.")
                press_release_number = press_release_number + 1
                if press_release_number > 10:
                        break
            else:
                continue 
    page += 1


# In[ ]:


#Q1 part 2
import requests
from bs4 import BeautifulSoup


# In[ ]:


part_number = 2
press_release_number = 1
page_number = 0

while press_release_number <= 10:
    seed_url = f"https://www.europarl.europa.eu/news/en/press-room/page/{page_number}"
    response = requests.get(seed_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    press_release_urls = [] #get a list of urls related to plenary sessions
    h3_elements = soup.find_all('h3', class_="ep-a_heading ep-layout_level2")
    for h3 in h3_elements:
        if h3.find('span', class_="ep_name", string="Plenary session"):
            a_tag = h3.find('a', href=True)
            press_release_url = a_tag['href']
            press_release_urls.append(press_release_url)
    for url in press_release_urls: #save press release with crisis included
        press_response = requests.get(url)
        new_soup = BeautifulSoup(press_response.content, 'html.parser')
        p_elements = new_soup.find_all('p', class_="ep-wysiwig_paragraph")
        content = ' '.join(p.text.strip() for p in p_elements) # combine paragraphs
        if "crisis" in content.lower(): 
            filename = f"{part_number}_{press_release_number}.txt" 
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
                print(url)
                print(f"Saved content to {filename}.")
                press_release_number += 1
                if press_release_number > 10:
                    break
    page_number += 1

