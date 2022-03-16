from parsing.SaveParser import read_save_file


if __name__ == '__main__':
    root_node = read_save_file('gamestate')
    # root_node = read_save_file('religions_test.txt')

    print('Parsing complete!')

    historic_characters = {
        'orenog': '777101',
        'Gengar': '777301',
        'Kaosubaloo': '777401',
        'majorbyte': '777201',
        'PhageForge': '777601',
        'AussieVikingr': '777701',
        'Cobra1297': '777801',
        'Harringzord': '777901',
        'Bazik': '7771001',
        'zsinj001': '7771201',
        'Metal': '7771301',
        'Razta': '7771401'
    }

    current_characters = {}
    for player_name, historic_id in historic_characters.items():
        current_characters[player_name] = root_node.children['character_lookup'].children[historic_id]

    players_data = []

    for played_character in root_node.children['played_character_list']:
        if played_character.children['player'] != '-1':
            current_characters[played_character.children['name']] = played_character.children['character']

    for player_name, character_id in current_characters.items():
        player = {
            'name': player_name,
            'character_id': character_id
        }
        character_data = None
        if player['character_id'] in root_node.children['living'].children:
            character_data = root_node.children['living'].children[character_id]
        elif player['character_id'] in root_node.children['dead_unprunable'].children:
            character_data = root_node.children['dead_unprunable'].children[character_id]

        if character_data is None:
            print('Could not find character ' + character_id)
            player['character_name'] = 'Unknown'
            player['renown'] = 0
            player['prestige_accumulated'] = 0
        else:
            player['character_name'] = character_data.children['first_name']
            player['dynasty_house_id'] = character_data.children['dynasty_house']

            player['dynasty_id'] = root_node.children['dynasties'].children['dynasty_house'].children[player['dynasty_house_id']].children['dynasty']
            if 'localized_name' in root_node.children['dynasties'].children['dynasty_house'].children[player['dynasty_house_id']].children:
                player['dynasty_name'] = root_node.children['dynasties'].children['dynasty_house'].children[player['dynasty_house_id']].children['localized_name']
            else:
                player['dynasty_name'] = root_node.children['dynasties'].children['dynasty_house'].children[player['dynasty_house_id']].children['name']

            dynasty_data = root_node.children['dynasties'].children['dynasties'].children[player['dynasty_id']]
            player['renown'] = int(float(dynasty_data.children['prestige'].children['currency']))
            player['prestige_accumulated'] = int(float(dynasty_data.children['prestige'].children['accumulated']))

        players_data.append(player)

    players_data = sorted(players_data, key=lambda p:  p['prestige_accumulated'], reverse=True)

    print('\n')
    print('Player,Character,Dynasty,Renown,Prestige (accumulated renown)')
    for player_data in players_data:
        print(player_data['name'] + ',' + player_data['character_name'] + ',' + player_data['dynasty_name'] + ',' + player_data['renown'] + ',' + player_data['prestige_accumulated'])


