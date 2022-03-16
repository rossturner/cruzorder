# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from LineTokenizer import tokenize_line
from Node import Node
from ParserState import ParserState


def parse_value(identifier, line, state):
    if line.count('"') >= 2 and line[0] == '"' and line[len(line) - 1] == '"':
        # TODO treat this as a literal value
        line = line[1:len(line)-1]
        state.current_node.children[identifier] = line
    elif line[0] == '{':
        # Starting a new Node
        child_node = Node(state.current_node)
        if identifier in state.current_node.children:
            list_name = identifier + '_list'
            if list_name not in state.current_node.children:
                state.current_node.children[list_name] = [state.current_node.children[identifier]]
            state.current_node.children[list_name].append(child_node)
        else:
            state.current_node.children[identifier] = child_node
        state.current_node = child_node
        parse_line(line[1:], state)
    else:
        state.current_node.children[identifier] = line


def parse_line(line, state):
    line = clean(line)
    if len(line) == 0:
        pass
    elif line.count('=') > 0:
        identifier = line[:line.index('=')]
        line = line[line.index('=') + 1:]
        parse_value(identifier, line, state)
    elif line[0] == '{':
        # Starting a new Node
        child_node = Node(state.current_node)
        state.current_node.values.append(child_node)
        state.current_node = child_node
        parse_line(line[1:], state)
    elif line[0] == '}':
        # Closing node
        state.current_node = state.current_node.parent
    else:
        # Just a value for the current node
        state.current_node.values.append(line)


def clean(line):
    return line.strip().replace('\r', '').replace('\n', '').replace('\t', ' ')


def read_save_file(filename):
    state = ParserState()
    root_node = state.current_node

    with open(filename, 'r', encoding="utf8") as save_file:

        line = save_file.readline()
        line_number = 1
        while line:
            if len(line) < 3000:
                # Just skipping long lines at the moment like static_dynasties={...
                line = clean(line)
                lines = tokenize_line(line, [])
                for token in lines:
                    parse_line(token, state)

            line = save_file.readline()
            line_number = line_number + 1

            if line_number % 100000 == 0:
                print('Parsing line ' + str(line_number))

        ross_value = root_node.children['ross']
        print('Parsing complete!')




if __name__ == '__main__':
    read_save_file('gamestate')
    # read_save_file('religions_test.txt')

