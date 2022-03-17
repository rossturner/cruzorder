from parsing.TitleNames import TitleNames

class TitleFormatter:
    def __init__(self):
        self.name_lookup = TitleNames()

    def titles_to_string(self, titles):
        if not titles:
            return 'Unknown'

        multiple = len(titles) > 1
        translated = list(map(self.name_lookup.get, titles))

        prefix = ''

        if titles[0][0] == 'e':
            prefix = 'Empires of ' if multiple else 'Empire of '
        elif titles[0][0] == 'k':
            prefix = 'Kingdoms of ' if multiple else 'Kingdom of '
        elif titles[0][0] == 'd':
            prefix = 'Duchies of ' if multiple else 'Duchy of '
        elif titles[0][0] == 'c':
            prefix = 'Counties of ' if multiple else 'County of '
        elif titles[0][0] == 'b':
            prefix = 'Baronies of ' if multiple else 'Barony of '

        return prefix + ' and '.join(translated)


