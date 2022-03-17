import pygsheets

# Column indices - could be done dynamically
DYNASTY_ID = 0
DYNASTY = 1
TYPE = 2
BELONGS_TO = 3
CHAR_NAME = 4
STARTING_TITLE = 5
HIGHEST_TITLE = 6
FATE = 7
GLORY = 8
LIVING = 9
DEAD = 10


class SheetWrapper:
    def __init__(self, sheet_key):
        gclient = pygsheets.authorize(service_file='cruzorder-53a12d76f66a.json')
        self.sheet = gclient.open_by_key(sheet_key)
        self.work_sheet = self.sheet.sheet1
        self.row_cursor = 1

        headers = self.work_sheet.range('A1:K1')
        # Checking column names match up
        assert headers[0][DYNASTY_ID].value == 'Dynasty ID'
        assert headers[0][DYNASTY].value == 'Dynasty'
        assert headers[0][TYPE].value == 'Type'
        assert headers[0][BELONGS_TO].value == 'Belongs To...'
        assert headers[0][CHAR_NAME].value == 'Primary Character Name'
        assert headers[0][STARTING_TITLE].value == 'Starting Primary Title'
        assert headers[0][HIGHEST_TITLE].value == 'Highest Title Held by Dynasty'
        assert headers[0][FATE].value == 'Fate'
        assert headers[0][GLORY].value == 'Glory'
        assert headers[0][LIVING].value == 'Living'
        assert headers[0][DEAD].value == 'Dead'

    def get_next_row(self):
        self.row_cursor = self.row_cursor + 1

        row = self.work_sheet.get_row(self.row_cursor)
        if row[0] == '':
            return None
        else:
            return row

    def update_current_row(self, row_data):
        self.work_sheet.update_row(self.row_cursor, row_data)
