from unicodedata import category
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import time
from webdriver_manager.chrome import ChromeDriverManager    # Mac

# 국립현대미술관(MMCA)

base_url = "https://www.mmca.go.kr/main.do"
board_url = "https://www.mmca.go.kr/educations/eduDataList.do"
login_url = "https://www.mmca.go.kr/member/loginForm.do"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')    # Windows


def login():

    driver.get(login_url)
    
    # 로그인
    user_id = ""
    password = ""

    driver.find_element_by_id('memberEmail').send_keys(user_id)
    time.sleep(5)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="content"]/div/form/div/div/div[2]/div[2]/button').click()
    time.sleep(5)
 

def crawling():
    driver.get(board_url)
    soup = bs(ur.urlopen(board_url).read(), 'html.parser')   

    board_main = soup.find("div",  {"class" : "table scrollNone"})
    board_body = board_main.find("tbody")
    board_list = board_body.find_all("tr")
    print(board_list)

    # for list_all in board_list: 
    #     list = list_all.find_all("td")
    #     print(list)
    #     if len(list) > 2:
    #         category = list[1].text                                                       # 카테고리
    #     else:   
    #         type = list[0].text                                                           # 유형

    # data = board_list.find("td", {"class":"title"})
    # link = data.find("a")
    # link_url = link.get("href")                                                           # 상세 URL ... 자바스크립트

    # print(type)
    # print(category)
    # print(link_url)


#상세 크롤링
def detail(link_url):
    driver.get(link_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    view_header = detail_soup.find("div", {"class" : "heading borderX"})
    title = view_header.find("h3", {"class" : "title"})                                 # 제목
    
    reg_date = view_header.find("ul", {"class" : "barList"})                            # 등록일

    read_count_all = view_header.find("li", {"class" : "infoViews"})                          
    read_count = read_count_all.find("span", {"class" : "num"})                         # 조회수
    
    content_all = view_header.find("div", {"class" : "bodySection"})
    content = content_all.find("p")                                                     # 내용
    
    attach = detail_soup.find("div", {"class" : "btnDownList"})
    attach_url = attach.get("href")                                                     # 첨부파일 URL ... 자바스크립트
            

    print(title)
    print(reg_date)
    print(read_count)
    print(content)
    print(attach_url)


def main():
    
    login()
    
    crawling()
    
    driver.quit()
         

if __name__ == '__main__':
    main()