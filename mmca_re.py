from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
from db_manager import DatabaseManager

# CSS 파일 생성
# HEADER = ['제목', '등록일', '조회수', '내용', '첨부파일URL']
# ARGV_COUNT = 2
DATABASE_ID = "local"


base_url= "https://www.mmca.go.kr/main.do"
login_url = "https://www.mmca.go.kr/member/loginForm.do"
board_url= "https://www.mmca.go.kr/educations/eduDataList.do"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def login():    
    driver.get(login_url)

    user_id =""
    password= ""
       
    driver.find_element(By.ID, 'memberEmail').send_keys(user_id) 
    time.sleep(5) 
    driver.find_element(By.ID, 'password').send_keys(password) 
    time.sleep(5) 
    driver.find_element(By.XPATH, '//*[@id="content"]/div/form/div/div/div[2]/div[2]/button').click()
    time.sleep(5)


def crawling():      
    driver.get(board_url)
    time.sleep(5)  
    html = driver.page_source 
    soup = bs(html, 'html.parser')
    
    board_main = soup.find("div",  {"class" : "table scrollNone"})    
    board_body = board_main.find("tbody")
    board_list = board_body.find_all("tr")

    datas = []

    for index, list in enumerate(board_list, start=1):
        
        # list_main = list[0]
        # list_all = list_main.find_all("td")                                  

        # list_type = list_all[0].text                                                # 유형
        # list_category = list_all[1].text                                            # 카데고리

        # print(list_type, list_category)

        bd = "//*[@id='tbody']/tr[{}]/td[3]/a".format(index) 
        
        driver.find_element(By.XPATH, bd).click() 

        datas.append(detail())
        
        driver.get(board_url) 

        time.sleep(5)
        
    if len(datas) > 0:
            db = DatabaseManager(DATABASE_ID)
            db.connection()
            query = '''
                    INSERT INTO board_mmca (TITLE, REG_DATE, READ_COUNT, CONTENT, ATTACH_URL) 
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                '''        

            db.execute_query_bulk(query, datas)               
        

def detail():  
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    view_header = detail_soup.find("div", {"class" : "heading borderX"})
    
    title = view_header.find("h3", {"class" : "title"}).text                          # 제목
        
    reg_date = view_header.find("ul", {"class" : "barList"}).text                       # 등록일

    read_count_all = view_header.find("li", {"class" : "infoViews"})                          
    read_count = read_count_all.find("span", {"class" : "num"}).text                     # 조회수

    content = detail_soup.find("div", {"class" : "bodySection"}).text                # 내용
    
    attach_url= ""    
        
    
    return [title, reg_date, read_count, content , attach_url]
 
     
def main(): 
       
    login()

    crawling()


if __name__ == '__main__':
    main()