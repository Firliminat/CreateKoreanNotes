import csv

DEFAULT_NOTE_TYPE = 'Korean Words Type Answer'
DEFAULT_DECK = 'Coréen::Vocabulaire'

DEFAULT_ATTRIBUTE_LIST_MAPPING = {
  'guid': 0,
  'notetype': 1,
  'deck': 2,
  'korean': 3,
  'french': 4,
  'sound': 5,
  'precision': 6,
  'context': 7,
  'tags': 8,
}

DEFAULT_ANKI_CSV_HEADER_LINES = [
  '#separator:tab',
  '#html:true',
  '#guid column:1',
  '#notetype column:2',
  '#deck column:3',
  '#tags column:9'
]

class Note:
  def __init__(
      self,
      guid: str = '',
      notetype: str = DEFAULT_NOTE_TYPE,
      deck: str = DEFAULT_DECK,
      korean: str = '',
      french: str = '',
      sound: str = '',
      precision: str = '',
      context: str = '',
      tags: str = ''
  ):
    self.guid = guid
    self.notetype = notetype
    self.deck = deck
    self.korean = korean
    self.french = french
    self.sound = sound
    self.precision = precision
    self.context = context
    self.tags = tags

  @classmethod
  def from_list(cls, row: list[str], mapping: dict[str, int]=DEFAULT_ATTRIBUTE_LIST_MAPPING):
    new_note = cls()
    for attr, idx in mapping.items():
      setattr(new_note, attr, row[idx])
    
    return new_note
  
  def to_list(self, mapping: dict[str, int]=DEFAULT_ATTRIBUTE_LIST_MAPPING) -> list[str]:
    new_list = [None] * (max(mapping.values()) + 1)
    for attr, idx in mapping.items():
      new_list[idx] = getattr(self, attr)
    
    return new_list

def from_csv_file(
  file_name: str,
  header_marker: str = '#',
  newline: str = '\n',
  delimiter: str = '\t',
  quotechar:str = '"'
) -> tuple[list[Note], list[str]]:
  notes: list[Note] = []

  with open(file_name, newline=newline) as csv_file:
    input_reader = csv.reader(
      csv_file,
      delimiter=delimiter,
      quotechar=quotechar
    )

    # Skipping header lines
    cursor_pos = csv_file.tell()
    header_lines = []
    while True:
      new_line = csv_file.readline()
      if new_line.startswith(header_marker):
        cursor_pos = csv_file.tell()
        header_lines.append(new_line.strip())
      else:
        break
    csv_file.seek(cursor_pos)
    
    for row in input_reader:
      notes.append(Note.from_list(row))
  
  return notes, header_lines

def to_csv_file(
  notes: list[Note],
  file_name: str,
  header_lines = DEFAULT_ANKI_CSV_HEADER_LINES,
  newline='\n',
  delimiter='\t',
  quotechar='"'
):
  with open(file_name, 'w', newline=newline) as csv_file:
    output_writer = csv.writer(
      csv_file,
      delimiter=delimiter,
      quoting=csv.QUOTE_ALL,
      quotechar=quotechar
    )
    csv_file.write(newline.join(header_lines) + newline)
    for note in notes:
      output_writer.writerow(note.to_list(DEFAULT_ATTRIBUTE_LIST_MAPPING))