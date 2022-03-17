from parsing.SaveParser import read_save_file
import pygsheets

from sheets.SheetWrapper import *

TEST_SHEET_ID = '1hCy3PKI7VSc0Fh_XyHfipHfiS_EwEO54b-PyVN0b7BE'
LIVE_SHEET_ID = '1nOyDZ1WRqC1-aKH90KDZFb-aZoRJfIoGn0IUnLKprUI'


def count_characters(character_dict, house_ids):
    counter = 0
    for character_data in character_dict.values():
        if 'dynasty_house' in character_data.children and character_data.children['dynasty_house'] in house_ids:
            counter = counter + 1
    return counter


if __name__ == '__main__':
    sheet = SheetWrapper(LIVE_SHEET_ID)
    root_node = read_save_file('gamestate')
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
        prestige = 0

        if character_data is None:
            print('Could not find character with ID ' + character_id)
        else:
            character_house_id = character_data.children['dynasty_house']
            dynasty_id = root_node.children['dynasties'].children['dynasty_house'].children[character_house_id].children['dynasty']

            house_ids = []
            for house_id, house_data in root_node.children['dynasties'].children['dynasty_house'].children.items():
                if house_data.children['dynasty'] == dynasty_id:
                    house_ids.append(house_id)

            dynasty_data = root_node.children['dynasties'].children['dynasties'].children[dynasty_id]
            prestige = int(float(dynasty_data.children['prestige'].children['accumulated']))
            living = count_characters(root_node.children['living'].children, house_ids)
            dead = count_characters(root_node.children['dead_unprunable'].children, house_ids)

        row[PRESTIGE] = str(prestige)
        row[LIVING] = str(living)
        row[DEAD] = str(dead)
        print('Updating dynasty ' + row[DYNASTY] + '\n')
        sheet.update_current_row(row)

        row = sheet.get_next_row()

    print('Done!')

