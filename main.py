from parsing import TitleSorter
from parsing.Node import Node
from parsing.SaveParser import read_save_file
import pygsheets

from parsing.TitleFormatter import TitleFormatter
from parsing.TitleNames import TitleNames
from sheets.SheetWrapper import *

TEST_SHEET_ID = '1U1_8AsH52t7I9fVvc4QmpiWAG6ioPlM1E_bjcNj7cYc'
LIVE_SHEET_ID = '1nOyDZ1WRqC1-aKH90KDZFb-aZoRJfIoGn0IUnLKprUI'


def get_character_ids_for_houses(character_dict, house_ids):
    character_ids = []
    for character_id, character_data in character_dict.items():
        if 'dynasty_house' in character_data.children and character_data.children['dynasty_house'] in house_ids:
            character_ids.append(character_id)
    return character_ids


def title_was_held(holder, character_ids):
    if isinstance(holder, list):
        for list_item in holder:
            if title_was_held(list_item, character_ids):
                return True
        return False

    if isinstance(holder, Node) and 'holder' in holder.children:
        # Need to drill down into holder nodes which aren't just a literal value
        holder = holder.children['holder']
    return holder in character_ids



def get_historic_titles(title_dict, character_ids):
    title_keys = set()
    for title in title_dict.values():
        if title != 'none' and 'history' in title.children:
            history = title.children['history']
            for holder in history.children.values():
                if title_was_held(holder, character_ids):
                    title_keys.add(title.children['key'])

    return title_keys


if __name__ == '__main__':
    sheet = SheetWrapper(TEST_SHEET_ID)
    # sheet = SheetWrapper(LIVE_SHEET_ID)
    root_node = read_save_file('gamestate')
    title_formatter = TitleFormatter()
    # print('Parsing complete!')


    row = sheet.get_next_row()
    while row is not None:
        historic_character_id = str(int(row[DYNASTY_ID]) + 1)
        character_id = root_node.children['character_lookup'].children[historic_character_id]

        print('Finding character data for ' + row[DYNASTY])
        character_data = None
        if character_id in root_node.children['living'].children:
            character_data = root_node.children['living'].children[character_id]
        elif character_id in root_node.children['dead_unprunable'].children:
            character_data = root_node.children['dead_unprunable'].children[character_id]

        living = 0
        dead = 0
        accumulated_renown = 0
        highest_titles = ''

        if character_data is None:
            print('Could not find character with ID ' + character_id)
        else:
            character_house_id = character_data.children['dynasty_house']
            dynasty_id = root_node.children['dynasties'].children['dynasty_house'].children[character_house_id].children['dynasty']

            house_ids = []
            for house_id, house_data in root_node.children['dynasties'].children['dynasty_house'].children.items():
                if isinstance(house_data, Node) and house_data.children['dynasty'] == dynasty_id:
                    house_ids.append(house_id)

            dynasty_data = root_node.children['dynasties'].children['dynasties'].children[dynasty_id]
            accumulated_renown = int(float(dynasty_data.children['prestige'].children['accumulated']))

            living_character_ids = get_character_ids_for_houses(root_node.children['living'].children, house_ids)
            dead_character_ids = get_character_ids_for_houses(root_node.children['dead_unprunable'].children, house_ids)

            living = len(living_character_ids)
            dead = len(dead_character_ids)

            all_character_ids = living_character_ids + dead_character_ids

            print('Looking up historic titles for ' + ', '.join(all_character_ids))
            historic_titles = get_historic_titles(root_node.children['landed_titles'].children['landed_titles'].children, all_character_ids)
            historic_titles = TitleSorter.get_highest_title_keys(historic_titles)
            print('Found ' + ' '.join(historic_titles))
            highest_titles = title_formatter.titles_to_string(historic_titles)

        row[HIGHEST_TITLE] = highest_titles
        row[GLORY] = str(accumulated_renown)
        row[LIVING] = str(living)
        row[DEAD] = str(dead)
        print('Updating dynasty ' + row[DYNASTY] + '\n')
        sheet.update_current_row(row)

        row = sheet.get_next_row()

    print('Done!')

