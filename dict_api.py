import re
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from notes import Note

API_URL = "https://krdict.korean.go.kr/api"
API_KEY = "DUMMY_APY_KEY"

def get_word_soup_from_korean(korean: str) -> BeautifulSoup:
  params = {
    "key": API_KEY,
    "part":"word",
    "q": korean,
    "translated":"y",
    "trans_lang":"3",
    "advanced":"y",
    "method":"exact"
  }
  request_url = API_URL + "/search?" + urlencode(params)
  response = requests.get(request_url)

  word_soup = BeautifulSoup(response.content, "xml")
  items = word_soup.find_all('item')

  if len(items) > 0:
    return word_soup
  else:
    raise ValueError('No word found for ' + korean)

def get_korean(word_soup: BeautifulSoup) -> str:
  for word in word_soup.find_all('word'):
    korean = word.text.strip()
    if korean != '':
      return korean
    
  raise TypeError('No korean found')

def get_french(word: BeautifulSoup) -> str:
  french = ''
  for trans_word in word.find_all('trans_word'):
    main_trans = trans_word.text.split(',', 1)[0].strip().capitalize()
    if main_trans != '':
      french += main_trans + ', '

  return french.removesuffix(', ')

def get_sound(word: BeautifulSoup,
  download: bool,
  download_folder: str
) -> str:
  korean = get_korean(word)
  file_name = korean + '.mp3'

  if download:
    link = word.find('item').find('link').text

    response = requests.get(link)
    soup = BeautifulSoup(response.content, "lxml")
    regexp = re.compile(r".*\(\'(.*?)\'\).*")
    try:
      href = soup.find("a", class_="sound")['href']
    except Exception as e:
      raise ValueError('No sound found for ' + korean + ' | ' + repr(e))
      
    sound_link = regexp.sub(r'\1', href)

    out_file = download_folder + '/' + file_name
    with open(out_file, 'wb') as output:
      response = requests.get(sound_link)
      output.write(response.content)
  
  return '[sound:' + file_name + ']'

def get_precision(word: BeautifulSoup) -> str:
  precision = ''
  for trans_word in word.find_all('trans_word'):
    try:
      remaining_trans = trans_word.text.split(',', 1)[1].strip().capitalize()
    except:
      remaining_trans = ''
    if remaining_trans != '':
      precision += remaining_trans + '<br>'

  return precision.removesuffix('<br>')

def get_note_from_korean(korean: str, download=False, download_folder='./') -> Note:
  word_soup = get_word_soup_from_korean(korean)
  note = Note()
  note.notetype = 'Korean Words Type Answer'
  note.deck = 'Coréen::Vocabulaire'
  note.korean = get_korean(word_soup)
  note.french = get_french(word_soup)
  note.precision = get_precision(word_soup)
  note.sound = get_sound(word_soup, download, download_folder)

  return note

