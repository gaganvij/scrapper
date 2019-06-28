def scrape(input):
    from bs4 import BeautifulSoup
    import requests
    import re
    import pandas as pd
    import os
    
    
 
    text = input
    
    url = 'http://google.com/search?q=' + text
    
    #url='https://www.bing.com/search?q=gaganvij'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    #soup.prettify()
    
    
    hyper_links=[] 
    
    
    
    all_links = soup.find_all("a")
    for link in all_links:
        print(link.get("href"))
        hyper_links.append(link.get("href"))
        
    
    hyper_links_relevant=[]
    b='/url?q'
    d='webcache'
    for a in hyper_links:
        if b in a and d not in a:
            hyper_links_relevant.append(a)
    
    
    clean_link=[]
    for c in hyper_links_relevant:
        result= re.findall(r'url.q.(.*).sa',c) #### focus on the first link from search result
        if "preferences" not in result[0]:
            clean_link.append(result[0])
        
    
    
    data1=[]
    
    
    for d in clean_link:
        
        
        try:
        
            request = requests.get(d)
            
            soup = BeautifulSoup(request.text, 'lxml')
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
        
            data1.append(soup.get_text())
            
        except:
             data1.append('cant be extracted')
            

        
    ouput_path=z['Value'][0]
       
    final_df = pd.DataFrame(
        {'Links': clean_link,'Data': data1})
    
    os.chdir(ouput_path)
   
    writer = pd.ExcelWriter('test_data.xlsx')
    final_df.to_excel(writer,'Sheet1')
    writer.save() 


#################
input=AI
scrape(input)


