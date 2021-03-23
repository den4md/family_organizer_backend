import string


def camel_case_to_snake_case(camel_str: str) -> str:
    word_list = []
    while True:
        found_upper = False
        for i in range(1, len(camel_str)):
            if camel_str[i] in string.ascii_uppercase:
                word_list.append(camel_str[:i].lower())
                camel_str = camel_str[i:]
                found_upper = True
                break
        if not found_upper:
            break
    word_list.append(camel_str.lower())
    return '_'.join(word_list)


def snake_case_to_camel_case(snake_str: str) -> str:
    return ''.join([word[:1].upper() + word[1:] for word in snake_str.split('_')])
