import csv
from tqdm import tqdm
from notes import Note, from_csv_file, to_csv_file
from dict_api import get_note_from_korean

# notes, header_lines = from_csv_file('ExampleData/Coréen__Nouveau_Vocabulaire.txt')
# to_csv_file(
#   notes,
#   'TestOutput/Coréen__Vocabulaire.txt',
#   header_lines
# )

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

korean_words = get_korean_words_list("./TestInput/NewWords.txt")

errors: list[list[str]] = []
new_notes: list[Note] = []
for word in tqdm(korean_words):
  try:
    new_note = get_note_from_korean(word, True, './TestOutput/Media')
    new_notes.append(new_note)
  except ValueError as e:
    errors.append([word, repr(e)])


with open('./TestOutput/Errors.txt', 'w', newline='\n') as csv_file:
  output_writer = csv.writer(
    csv_file,
    delimiter='\t',
    quoting=csv.QUOTE_ALL,
    quotechar='"'
  )
  output_writer.writerows(errors)

to_csv_file(
  new_notes,
  'TestOutput/Coréen__Vocabulaire_new.txt'
)