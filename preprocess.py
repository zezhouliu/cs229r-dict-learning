import argparse
import collections
import csv
import json

def read_and_write_file(json_file_path, json_out_path, column_names):
    """Read in the json dataset file:
        Strip out only the fields that are interesting (reviews, stars), given the column names,
        and then write back out as a condensed json
    """
    with open(json_out_path, 'wb+') as fout:
        with open(json_file_path) as fin:
            count = 0
            for line in fin:
                count += 1
                if count < 500000:
                    continue
                elif count == 510000:
                    break
                if count % 10000 == 0:
                    print count
                line_contents = json.loads(line)
                data = {"text" : line_contents["text"].lower(), "stars" : line_contents["stars"]}
                d = json.dumps(data, fout)
                fout.write(d + "\n")


def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names given a dict.

    Example:

        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }

        will return: ['a.b', 'a.c']

    These will be the column names for the eventual csv file.

    """
    column_names = []
    for k, v in line_contents.iteritems():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            column_names.extend(
                    get_column_names(v, column_name).items()
                    )
        else:
            column_names.append((column_name, v))
    return dict(column_names)

def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.
    Example:

        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'

        will return: 2
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )
        if isinstance(line_value, unicode):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    parser = argparse.ArgumentParser(
            description='Condenses Yelp Dataset Challenge data to smaller JSON.',
            )

    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert.',
            )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = 'test.json'

    column_names = ["text", "stars"]
    read_and_write_file(json_file, csv_file, column_names)
