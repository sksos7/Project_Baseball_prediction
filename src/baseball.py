import requests
from bs4 import BeautifulSoup

kbo_url = 'https://www.koreabaseball.com/'
ranking_url = 'TeamRank/TeamRank.aspx'
page = requests.get(kbo_url+ranking_url)
soup = BeautifulSoup(page.content, 'html.parser')

rank_element = soup.find_all('table', class_='tData')

# 순위
print(rank_element[0].find_all('th'))

# 상대 전적
# print(rank_element[1])