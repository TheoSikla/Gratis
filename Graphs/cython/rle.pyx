def encode(input_string):
    count = 1
    prev = ''
    lst = []
    out = ''
    for character in input_string:
        if character != prev:
            if prev:
                # entry = (prev, count)
                # lst.append(entry)
                out += f'{str(count)}{prev}'
                # print lst
            count = 1
            prev = character
        else:
            count += 1
    else:
        try:
            # entry = (character, count)
            # lst.append(entry)
            out += f'{str(count)}{character}'
            return out
        except Exception as e:
            print("Exception encountered {e}".format(e=e))
            return e


def decode(lst):
    q = ""
    for (count, character) in zip(lst[0::2], lst[1::2]):
        q += int(count) * character
    return q

REPEATS_RE = re.compile(r'(.)\1*')
NUMBERS_RE = re.compile(r'(\d+)(.)')


def to_numbers(match):
    length = len(match.group(0))
    return (
        str(length) + match.group(1)
        if length > 1
        else match.group(1)
    )


def from_numbers(match):
    return int(match.group(1)) * match.group(2)


# def encode(string):
#     return REPEATS_RE.sub(to_numbers, string)


def decode(string):
    return NUMBERS_RE.sub(from_numbers, string)


# Method call
init_string = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
value = encode(init_string)

print("Encoded value is {}".format(value))
assert decode(value) == init_string

