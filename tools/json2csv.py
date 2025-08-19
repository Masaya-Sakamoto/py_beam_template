import pandas as pd
import json
import logging
import os
from glob import glob
from argparse import ArgumentParser

def json2dicts(json_file_path:str, encoding:str='utf-8') -> list[dict[str, int|float|str]]:
    with open(json_file_path, 'r', encoding=encoding) as f:
        json_data = json.load(f)
    return json_data

def set_unique_list(new_items:list[str]|str, store_list:list[str]) -> list[str]:
    if type(new_items) != list and type(new_items[0]) == str:
        raise TypeError('new_items must be list[str]')
    if type(new_items) == str:
        new_item = new_items
        if new_item not in store_list:
                store_list.append(new_item)
    elif type(new_items) == list:
        for new_item in new_items:
            if new_item not in store_list:
                store_list.append(new_item)
    else:
        raise TypeError('new_items must be list or str')
    return store_list

def extract_unique_keys_from_json(json_dict_list:list[dict[str, int|float|str]]) -> list[str]:
    """
    Extract unique keys from a list of JSON dictionaries.

    Args:
        json_dict_list (list[dict[str, int|float|str]]): A list of JSON dictionaries.

    Returns:
        list[str]: A list of unique keys.
    """
    unique_keys_list = []
    for json_dict in json_dict_list:
        if set(list(json_dict.keys())) <= set(unique_keys_list):
            unique_keys_list = set_unique_list(list(json_dict.keys()), unique_keys_list)
    return unique_keys_list

def json_dict2df(json_dict_list:list[dict[str, int|float|str]]) -> pd.DataFrame:
    keys = extract_unique_keys_from_json(json_dict_list)
    df = pd.DataFrame.from_records(json_dict_list, columns=keys)
    return df

def json2csv(json_file_path:str, csv_file_path:str, encoding:str='utf-8'):
    df = json_dict2df(json2dicts(json_file_path, encoding))
    df.to_csv(csv_file_path, encoding=encoding, index=False)

def parse_args(args: list[str]):
    parser = ArgumentParser(description="Convert JSON files to CSV format.")
    parser.add_argument("json_dir", help="Path to the input JSON directory.")
    parser.add_argument("csv_dir", help="Path to the output CSV directory.")
    parser.add_argument("--encoding", default='utf-8', help="File encoding (default: utf-8).")
    return parser.parse_args(args)

def main(args: list[str]):
    parsed_args = parse_args(args)
    JSON_DIR = parsed_args.json_dir
    CSV_DIR = parsed_args.csv_dir
    ENCODING = parsed_args.encoding
    json_files = glob(f'{JSON_DIR}/*.json')

    logging.debug("json files list:")
    for i, json_file in enumerate(json_files):
        logging.debug(f"id{i}  name: {json_file.split('/')[-1]}")

    for json_file in json_files:
        csv_file = f'{CSV_DIR}/{json_file.split("/")[-1].split(".")[0]}.csv'
        if os.path.exists(csv_file):
            print(f'{csv_file} already exists')
            continue
        json2csv(json_file, csv_file)
