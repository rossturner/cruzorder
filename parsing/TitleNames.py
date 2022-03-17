

class TitleNames:
    def __init__(self):
        self.key_map = {}
        with open('titles_l_english.yml', 'r', encoding="utf8") as titles_file:
            line = titles_file.readline()
            # skip a line
            line = titles_file.readline()
            while line:
                if line.count(':0') > 0 or line.count(':1') > 0:
                    line = line.strip()
                    key = line[:line.index(':')]
                    value = line[line.index('"')+1:len(line) - 1]
                    self.key_map[key] = value

                line = titles_file.readline()


    def get(self, title_key):
        return self.key_map[title_key]