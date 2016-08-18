def join_sentence(tokens):
    sentence = tokens[0] + ' '
    for token in tokens[1:]:
        sentence += token
        if token.isalpha() or token == ')':
            sentence += ' '

    return sentence.strip()
