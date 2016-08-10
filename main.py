import os
from pprint import pprint

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


def main():
    files = get_txt_files()

    try:
        date_extractor = DateExtractor(files[1])
    except Exception as e:
        print 'Could not instantiate date extractor: %r' % e

    dates = date_extractor.extract_dates()

    pprint(dates)


if __name__ == '__main__':
    main()
