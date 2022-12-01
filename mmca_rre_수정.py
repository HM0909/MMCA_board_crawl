from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
from db_manager import DatabaseManager

DATABASE_ID = "local"

# 국립현대미술관(MMCA)

base_url = "https://www.mmca.go.kr/main.do"
login_url = "https://www.mmca.go.kr/member/loginForm.do"
board_url = "https://www.mmca.go.kr/educations/eduDataList.do"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def login():
    driver.get(login_url)
    
    user_id = ""
    password = ""
    
    driver.find_element(By.ID, 'memberEmail').send_keys(user_id) 
    time.sleep(5) 
    driver.find_element(By.ID, 'password').send_keys(password) 
    time.sleep(5) 
    driver.find_element(By.XPATH, '//*[@id="content"]/div/form/div/div/div[2]/div[2]/button').click()
    time.sleep(5)
    

def crawling():
    driver.get(board_url)

    html = driver.page_source
    soup = bs(html, 'html.parser')  
        
    board_main = soup.find("tbody",  {"id" : "tbody"}) 
    board_body = board_main.find_all("tr")

    datas =[]
    
    for item in board_body:
        list = item.find_all("td")    
        type = list[0].text                                         # 유형
        category = list[1].text                                     # 카테고리
        
    for index, date in enumerate(board_body, start=1):
        bd = "//*[@id='tbody']/tr[{}]/td[3]/a".format(index)
        driver.find_element(By.XPATH, bd).click()
        
        detail(type,category)
        time.sleep(5)
        
        datas.append(detail(type,category))
        
        driver.get(board_url)
        time.sleep(5)
        

    if len(datas) > 0: 
            db = DatabaseManager(DATABASE_ID) 
            db.connection() 
            query = ''' 
                    INSERT INTO board_mmca (TYPE, CATEGORY, TITLE, REG_DATE, READ_COUNT, CONTENT, ATTACH_URL)  
                    VALUES ( 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s,
                        %s,
                        %s 
                    ) 
                '''         
            db.execute_query_bulk(query, datas)    


def detail(type,category): 
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    title = detail_soup.find("h3", {"class" : "title"}).text.strip()                     # 제목
            
    reg_date = detail_soup.find("ul", {"class" : "barList"}).text.strip()                # 등록일
                  
    read_count = detail_soup.find("span", {"class" : "num"})                             # 조회수                                  
    
    if read_count != None:
            read_count = read_count.text
    else:
        read_count = 0
        
    content = []
    
    content_all = detail_soup.find("div", {"class" : "bodySection"})
    
    if content_all != None:
        content_main = content_all.find_all("span")
        
        for item in content_main:
            content.append(item.text.strip())
            
    attach_url = ""
    
    return [type, category, title, reg_date, read_count, '\r'.join(content), attach_url]
    
            
def main():
    
    login()
    
    crawling()
         
if __name__ == '__main__':
    main()    