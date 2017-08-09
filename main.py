import requests
import csv
from config import token

fanpageID = '557872311000387'
info = []
res = requests.get('https://graph.facebook.com/v2.10/%s/posts?access_token=%s&pretty=1&fields=message,likes,created_time&limit=100' % (fanpageID, token)).json()
n = 0

def isCrawl(inf):
  try:
    return 'message' in inf and len(inf['likes']['data']) > 24
  except:
    return False

def extract(inf):
  return [inf['message'],
          requests.get('https://graph.facebook.com/v2.10/%s/likes?access_token=%s&summary=true' % (inf['id'], token)).json()['summary']['total_count'],
          inf['created_time'][:19]]

while n < 5:
  info.extend([extract(inf) for inf in res['data'] if isCrawl(inf)])
  try:
    res = requests.get(res['paging']['next']).json()
    n += 1
    print('Finish page %d\r' % n, end = '\r')
  except:
    print('')
    break

with open('cowbei.csv', 'w') as file:
  w = csv.writer(file)
  for i in info:
    w.writerow(i)