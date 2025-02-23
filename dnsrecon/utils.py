import logging
import json
import csv
import xml.etree.ElementTree as ET


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()

def load_wordlist(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Failed to load wordlist: {e}")
        return []

def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def save_to_xml(data, file_path):
    root = ET.Element("results")
    for item in data:
        record = ET.SubElement(root, "record")
        for key, value in item.items():
            ET.SubElement(record, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write(file_path)
