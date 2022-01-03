#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import ijson
import json
import sys

def save(values, append = False):
    with open('ca-terms.json', 'w') as outfile:
        json.dump(values, outfile, skipkeys=True, indent=4, ensure_ascii=False)

def get_ca_label(item):
    label = ''

    try:
        if 'ca' not in item['labels']:
            return label

        label = item['labels']['ca']['value']

    except:
        #print("Error")
        pass

    return label

def save_items(total_items, items_saved, items_processed, values):
    psaved = items_saved * 100 / items_processed
    pprocessed = items_processed * 100 / total_items
    print(f"Items processed {items_processed} ({pprocessed:.2f}%), saved {items_saved} ({psaved:.2f}%)")
    save(values)

def main():

    items_processed = 0
    items_saved = 0
    total_items = 96386518
    
    with open('words.txt', 'w') as fh_words:
        items = ijson.items(sys.stdin, 'item', use_float=True)

        values = []
        for item in items:
            ca_label = get_ca_label(item)
            items_processed += 1

            if items_processed % 1000000 == 0:
                save_items(total_items, items_saved, items_processed, values)

            if ca_label is None or len(ca_label) == 0:
                continue

            identifier = item['id']

            text =f"{identifier} - {ca_label}"
            fh_words.write(text + "\n")

            values.append(value)
            items_saved += 1

        save_items(total_items, items_saved, items_processed, values)

if __name__ == "__main__":
    print("Extracts from Wikidata dump only the items that have the Catalan label")
    main()
