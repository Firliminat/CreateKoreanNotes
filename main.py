import csv
from tqdm import tqdm
from notes import Note
from deck import Deck
from dict_api import get_note_from_korean

DEBUG = True

def get_korean_words_list(file_name: str) -> list[str]:
  words: list[str] = []
  with open(file_name, newline='\n') as csv_file:
    input_reader = csv.reader(
      csv_file,
      delimiter='\t',
      quotechar='"'
    )
    
    for row in input_reader:
      words.append(row[0])
  
  return words


existing_deck, header_lines = Deck.from_csv_file('./TestInput/Coréen__Vocabulaire_Existing.txt')

new_korean_words = get_korean_words_list('./TestInput/NewWords.txt')

errors_csv_file = open('./TestOutput/Errors.txt', 'w', newline='\n')
errors_writer = csv.writer(
  errors_csv_file,
  delimiter='\t',
  quoting=csv.QUOTE_ALL,
  quotechar='"'
)
errors: list[Exception] = []
new_deck = Deck()
for word in tqdm(new_korean_words):
  try:
    new_note = get_note_from_korean(word, True, './TestOutput/Media')

    # Tagging duplicates
    if existing_deck.has_korean(new_note) or new_deck.has_korean(new_note):
      new_note.tags += 'KrDup' + ', '
    if existing_deck.has_french(new_note) or new_deck.has_french(new_note):
      new_note.tags += 'FrDup' + ', '
    new_note.tags = new_note.tags.removesuffix(', ')

    new_deck.update(new_note)
  except Exception as e:
    errors_writer.writerow([word, repr(e)])
    errors.append(e)
errors_csv_file.close()

new_deck.to_csv_file('TestOutput/Coréen__Vocabulaire_new.txt', header_lines)

if DEBUG and len(errors) > 0:
  raise Exception(errors)