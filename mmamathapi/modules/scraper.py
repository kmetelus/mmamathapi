import string
import sys
import random
import requests
# from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
from pyquery import PyQuery as pq

# Remember to shuffle arrays before performing loop
# all_fighters = []

def get_id(url):
  id_index = url.find('_/id')
  return url[id_index+5:id_index+12]

def get_url(a):
  return pq(a).attr('href')

def get_fighter_history_url(urlEnd):
  return f'http://espn.com/mma/fighter/history/_/id/{get_id(urlEnd)}'

def parse_list_page(letter, session):
  url = 'http://espn.com/mma/fighters?search='+letter
  page = session.get(url)
  if page.ok:
    html = pq(page.content)
    rows = html('tr.evenrow').find('a') + html('tr.oddrow').find('a')
    return list(map(get_url, rows))
  return []

def parse_win_row(tr):
  cells = pq(tr).children()
  loser_id_cell = pq(cells.filter(lambda i, this: pq(this).find('a').length > 0))
  if len(loser_id_cell) == 0:
    return ''
  loser_name = pq(loser_id_cell[0]).text()
  return loser_name

def parse_fighter(urlEnd, session):
  page = session.get(get_fighter_history_url(urlEnd))
  response = { 'name': '', 'nickname': '', 'wins': [] }
  if page.ok:
    html = pq(page.content)
    response['name'] = ' '.join(html('h1.PlayerHeader__Name').find('span').map(lambda i, this: pq(this).text()))
    response['nickname'] = html('div.ttu').filter(lambda i, this: pq(this).text() == 'Nickname').siblings().text()
    winRows = html('div.ResultCell.win-stat').map(lambda i, this: pq(this).parents('tr'))
    response['wins'] = list(set(map(parse_win_row, winRows)))
    return response
  return response

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

def try_get_group_of_fighters(letter, session):
  start = time.time()
  fighters = []
  print(f'Starting with "{letter}"')
  try:
    # print(parse_list_page(letter))
    urls = parse_list_page(letter, session)
    for url in urls:
      fighters.append(parse_fighter(url, session))
      # print('Finished with one url')
    print(f'Finished "{letter}" in {time.time() - start}s')
    return fighters
  except:
    print(f'An error occured while getting fighter data on page "{letter}"')
    print(sys.exc_info())

async def get_all_fighters_async(letters):
  res = []
  with ThreadPoolExecutor() as executor:
    with requests.Session() as session:
      loop = asyncio.get_event_loop()
      tasks = [
        loop.run_in_executor(executor, try_get_group_of_fighters, *(letter, session)) for letter in letters
      ]
      for response in await asyncio.gather(*tasks):
        res.append(response)
  return res

def try_get_all_fighters():
  letters = list(string.ascii_lowercase)
  random.shuffle(letters)
  start = time.time()

  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(get_all_fighters_async(letters))
  res = loop.run_until_complete(future)
  end = time.time()
  elapsed = end - start
  print(f'Finished all in {elapsed}s')
  return res

def main():
  try_get_all_fighters()


if __name__ == "__main__":
  main()