

def tokenize_line(line, tokens):
    if line == '':
        return tokens

    if line[0] == ' ':
        return tokenize_line(line[1:], tokens)

    within_quotes = False
    previous_character = ' '
    for index, character in enumerate(line):
        if character == '"' and previous_character != "\\":
            within_quotes = not within_quotes

        if character == ' ' and not within_quotes:
            # Whitespace found, tokenize here
            token = line[:index]
            tokens.append(token)
            return tokenize_line(line[index + 1:], tokens)

        previous_character = character

    # Whole line must be a token
    tokens.append(line)
    return tokens
