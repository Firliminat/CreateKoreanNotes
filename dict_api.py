import re
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from notes import Note
from APIKey import API_KEY

API_URL = 'https://krdict.korean.go.kr/api'

def get_search_soup_from_korean(korean: str) -> BeautifulSoup:
  params = {
    'key': API_KEY,
    'part':'word',
    'q': korean,
    'translated':'y',
    'trans_lang':'3',
    'advanced':'y',
    'method':'exact'
  }
  request_url = API_URL + '/search?' + urlencode(params)

  response = requests.get(request_url)
  response.raise_for_status()

  search_soup = BeautifulSoup(response.content, 'xml')

  error = search_soup.find('error')
  assert error == None, (
    'Error with request to dictionary for ' + korean,
    'error_code: ' + error.find('error_code').text.strip(),
    'message: ' + error.find('message').text.strip()
  )

  return search_soup

def get_french(word: BeautifulSoup) -> str:
  french = ''
  for trans_word in word.find_all('trans_word'):
    main_trans = trans_word.text.split(',', 1)[0].strip().capitalize()
    if main_trans != '':
      french = main_trans
      break

  return french

def get_sound(
  korean: str,
  search_soup: BeautifulSoup,
  download: bool,
  download_folder: str
) -> str:
  file_name = korean + '.mp3'

  if download:
    found_words = search_soup.find_all('item')

    # Trying yo find a pronunciation sound for each found word
    # Stopping as soon as we get one
    for word in found_words:
      # Find url of the word page
      link = word.find('link').text
      page_response = requests.get(link)
      page_response.raise_for_status()

      word_page_soup = BeautifulSoup(page_response.content, 'lxml')

      sound_link_elt = word_page_soup.find('a', class_='sound')
      # No pronunciation sound on this page
      if sound_link_elt == None or not sound_link_elt.has_attr('href'):
         # Jumping to next word
         continue
      
      sound_link: str = sound_link_elt['href']
      # Correctly formatting the link for download
      link_decode_regexp = re.compile(r'.*\(\'(.*?)\'\).*')
      sound_link = link_decode_regexp.sub(r'\1', sound_link).strip()

      # Downloading the pronunciation sound
      out_file = download_folder + '/' + file_name
      with open(out_file, 'wb') as output:
        sound_response = requests.get(sound_link)
        sound_response.raise_for_status()

        # TODO: Check content-type
        # TODO: Check content ?
        # We write the content to the file
        output.write(sound_response.content)
    
      # Once the download is complete we don't need to look on other word pages
      break
  
  return '[sound:' + file_name + ']'

def get_precision(word: BeautifulSoup, french = '') -> str:
  precision = ''
  all_trans_words = [french.lower()]
  for meaning in word.find_all('trans_word'):
    try:
      meaning_str = meaning.text
    except:
      meaning_str = ''

    # Getting the list of translation words for this meaning
    curr_trans_words = list(map(
      lambda trans : trans.strip().lower(),
      meaning.text.split(', ')
    ))

    # Removing all the words already present in a previous meaning
    for trans_word in all_trans_words:
      curr_trans_words = list(filter(
        lambda a: a != trans_word,
        curr_trans_words
      ))

    # Adding the remaining words to the already seen words accumulator
    all_trans_words += curr_trans_words

    # Creating the string for the current meaning
    # And adding it to the return accumulator if not empty
    meaning_str = ', '.join(curr_trans_words).strip().capitalize()
    if meaning_str != '':
      precision += meaning_str + '<br>'

  return precision.removesuffix('<br>')

def get_note_from_korean(
  korean: str,
  download=False,
  download_folder='./'
) -> Note:
  search_soup = get_search_soup_from_korean(korean)
  nb_words_found = len(search_soup.find_all('item'))
  assert nb_words_found > 0, 'No word found for ' + korean

  french = get_french(search_soup)
  assert french != '', 'No french translation found for ' + korean

  precision = get_precision(search_soup, french)

  sound = get_sound(korean, search_soup, download, download_folder)

  new_note = Note(
    korean=korean,
    french=french,
    precision=precision,
    sound=sound
  )

  return new_note

