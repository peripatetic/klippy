# Based on https://github.com/tswicegood/pyKindle
# Updated to work with the Kindle Paperwhite (changes to date, location formats)
# Updated to handle all data as unicode

import datetime, time, re

__all__ = ['parse', 'join_notes']

KINDLE_FIRST_LINE_NOISE = '\xef\xbb\xbf'
KINDLE_DIVIDER = '=' * 10
KINDLE_DATE_FORMAT = '%A, %B %d, %Y %I:%M:%S %p' # Updated for the Paperwhite
LINE_BREAK = "\r\n"

def filter_title(title_meta):
    return title_meta[:title_meta.rfind(' (')]

def filter_author(title_meta):
    return title_meta[title_meta.rfind(' (')+2:title_meta.rfind(')')]

def filter_type(meta):
    return meta[meta.find('Your ')+5:meta.find(' Location')]

def filter_location(meta):
    return meta[meta.find('Location ')+9:meta.find(' | ')]

def filter_date(meta):
    text_date = meta[meta.find('Added on ')+9:]
    return datetime.datetime(*time.strptime(text_date, KINDLE_DATE_FORMAT)[:-3]) # -3 gets rid of trailing zeroes

def filter_tags(meta):
    x = meta[meta.find('.'):meta.find(' .... ')]
    y = re.findall(r'''
    \.      # find the dot character
    \w      # find any alphanumerical character
    {2,4}   # of 2 to 4 characters in length
    ''', x, re.VERBOSE)
    return y

def note_tags_stripped(note):
    comment = re.sub(r'^.* \.\.\.\. |^.* \.\.\.\.', '', note)
    comment.strip()
    return comment

def assign_tags(meta):

    tags_dict = {
        'cmt' : 'comments',
        'econ' : 'economics',
        'int' : 'interesting',
        'ma' : 'more attention',
        'mo' : 'motif',
        'pol' : 'politics',
        'soc' : 'society',
        'race' : 'race',
        'thm' : 'theme',
        'vote' : 'disenfranchisement',
        'ws' : 'quotable'
    }

    tags = [] 
    for shorthand in meta:
        tags.append(tags_dict[shorthand[1:]]) # the [1:] skips the first character in the string, in this case the dot
    return tags


def parse(filename,
          title_filter=filter_title,
          author_filter=filter_author,
          type_filter=filter_type,
          location_filter=filter_location,
          date_filter=filter_date):
    fp = open(filename, 'rb')
    contents = fp.read().lstrip(KINDLE_FIRST_LINE_NOISE)
    fp.close()

    contents = contents.strip().rstrip(KINDLE_DIVIDER)
    blocks = contents.split(KINDLE_DIVIDER)

    ret = []
    for block in blocks:
        title_meta, meta, _empty_line, notes, _empty_line = block.lstrip().split(LINE_BREAK)
        title = title_filter(title_meta)
        author = author_filter(title_meta)
        type = type_filter(meta)
        location = location_filter(meta)
        date = date_filter(meta)

        ret.append({
            'title': title,
            'type': type,
            'location': location,
            'date': date,
            'highlight': notes.strip() if notes.strip() else None,
            'author': author,
            'note': '',
            'tag': '',
        })
    return ret

def join_notes(parsed_data, new_dataset):
    ''' This function joins a note with its respective highlight. It inserts the note into a "comment" key in the dictionary, and inserts the stripped tag from the original note into the "tag" key for the highlight's array item. '''
    
    for index, clipping in enumerate(parsed_data):  # iterate over the clippings
        if clipping['type'] == 'Note':
            note = clipping['highlight']
            clean_note = note_tags_stripped(note)
            tags = assign_tags(filter_tags(note))
            tags.append('kindle')

            parsed_data[index + 1]['tag'] = tags
            parsed_data[index + 1]['note'] = clean_note
    
    for clipping in parsed_data:
        if clipping['type'] == 'Highlight':
            new_dataset.append(clipping)

