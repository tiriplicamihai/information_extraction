import json
import os
from pprint import pprint

import chardet

from constants import DATA_SET_PATH
from date_extractor import DateExtractor


def get_txt_files():
    """Extract file paths from data set. """
    files = []
    for file in os.listdir(DATA_SET_PATH):
        current_path = '%s/%s' % (DATA_SET_PATH, file)
        if os.path.isfile(current_path) and file.endswith('.txt'):
            files.append(current_path)
            continue

        if not os.path.isdir(current_path):
            continue

        # It is safe to look into the first to leveles because this is how data is structured
        for inner_file in os.listdir(current_path):
            file_path = '%s/%s' % (current_path, inner_file)

            if os.path.isfile(file_path) and inner_file.endswith('.txt'):
                files.append(file_path)

    return files


def get_text_content(filename):
    with open(filename, 'r') as f:
        text = f.read()

    if 'UTF-16' in chardet.detect(text).get('encoding', ''):
        text = text.decode('utf-16')

    return text


def main():
    files = get_txt_files()

    date_extractor = DateExtractor()
    #filename = files[140]
    result = {}
    for filename in files:
        print 'Date extractor for file %s' % filename

        try:
            dates = date_extractor.extract_dates(get_text_content(filename))
        except Exception as e:
            print 'Could not extract dates: %r' % e
            continue

        result[filename.split('/')[-1]] = dates

    #pprint(dates)
    with open('output.json', 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
