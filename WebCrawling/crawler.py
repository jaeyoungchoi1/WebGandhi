from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


current_directory = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(current_directory, 'chromedriver')
service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)


# 웹사이트에서 HTML 가져오기
#url = 'https://gall.dcinside.com/board/view/?id=baseball_new11&no=10571167'
board_url = 'https://gall.dcinside.com/board/lists/?id=leagueoflegends5&page=15&exception_mode=recommend'
driver.get(board_url)

wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.gall_tit.ub-word')))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

base_url = 'https://gall.dcinside.com'
post_links = []
for link in soup.find_all('td', class_='gall_tit ub-word'):
    a_tag = link.find('a')
    if a_tag and 'href' in a_tag.attrs and a_tag.attrs['href'].startswith('/board/'):
        post_links.append(base_url + a_tag.attrs['href'])

print(post_links)

csv_file = 'comments.csv'


for link in post_links:
    driver.get(link)
    time.sleep(2)
    print(f"Current page title: {driver.title}")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.usertxt.ub-word')))

    page_html = driver.page_source
    page_soup = BeautifulSoup(page_html, 'html.parser')
    comments = page_soup.find_all('p', class_='usertxt ub-word')

    print(len(comments))

    # 댓글 추출
    extracted_comments = [comment.get_text().strip() for comment in comments]

    df = pd.DataFrame(extracted_comments, columns=['Comment'])

    if os.path.exists(csv_file):
        # 파일이 존재하는 경우, 데이터 누적
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(csv_file, index=False)
    else:
        # 파일이 존재하지 않는 경우, 새로 생성
        df.to_csv(csv_file, index=False)


driver.quit()