import string
import random
import requests
from pyquery import PyQuery as pq
from fighterObject import FighterObject as Fighter

# Remember to shuffle arrays before performing loop
def get_id(url):
  id_index = url.find('_/id')
  return url[id_index+5:id_index+12]

def get_url(a):
  return pq(a).attr('href')

def get_fighter_history_url(urlEnd):
  return f'http://espn.com/mma/fighter/history/_/id/{get_id(urlEnd)}'

def parse_list_page(letter):
  url = 'http://espn.com/mma/fighters?search='+letter
  page = requests.get(url)
  html = pq(page.content)
  rows = html('tr.evenrow').find('a') + html('tr.oddrow').find('a')
  return list(map(get_url, rows))

def parse_win_row(tr):
  cells = pq(tr).children()
  loser_id_cell = pq(cells.filter(lambda i, this: pq(this).find('a').length > 0)[0])
  loser_name = loser_id_cell.text()
  return loser_name

def parse_fighter(urlEnd):
  page = requests.get(get_fighter_history_url(urlEnd))
  html = pq(page.content)
  name = ' '.join(html('h1.PlayerHeader__Name').find('span').map(lambda i, this: pq(this).text()))
  nickname = html('div.ttu').filter(lambda i, this: pq(this).text() == 'Nickname').siblings().text()
  winRows = html('div.ResultCell.win-stat').map(lambda i, this: pq(this).parents('tr'))
  wins = list(set(map(parse_win_row, winRows)))
  return { 'name': name, 'nickname': nickname, 'wins': wins }

def get_all_fighters():
  urls = []
  fighters = []
  letters = list(string.ascii_lowercase)
  random.shuffle(letters)
  for letter in letters[0:1]:
    urls.extend(parse_list_page(letter))
  random.shuffle(urls)
  for url in urls[0:9]:
    fighters.extend([parse_fighter(url)])
  return fighters
