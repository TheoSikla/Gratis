import re


class RunLengthEncoder:
    REPEATS_RE = re.compile(r'(.)\1*')
    NUMBERS_RE = re.compile(r'(\d+)(.)')

    def __init__(self):
        self.mode = None
        self.initial_input = ''

    def check_input(self, string: str):
        self.mode = "binary" if all(_ in '01' for _ in string) else "normal"

    @staticmethod
    def to_numbers(match):
        length = len(match.group(0))
        return (
            str(length) + match.group(1)
            if length > 1
            else match.group(1)
        )

    @staticmethod
    def from_numbers(match):
        return int(match.group(1)) * match.group(2)

    def encode(self, string: str):
        self.initial_input = string
        self.check_input(string)
        if self.mode == 'normal':
            return self.REPEATS_RE.sub(self.to_numbers, string)
        string = ''.join([chr(int(char)) for char in string])
        return self.REPEATS_RE.sub(self.to_numbers, string)

    def decode(self, string: str):
        if self.mode == 'normal':
            decoded_string = self.NUMBERS_RE.sub(self.from_numbers, string)
        else:
            decoded_string = ''.join([''.join(str(ord(digit))) for digit in self.NUMBERS_RE.sub(self.from_numbers,
                                                                                                string)])
        if decoded_string != self.initial_input:
            raise Exception("Run Length Decoding Failed.")
        return decoded_string
