

def from_hex_string(text):
    return str(bytearray.fromhex(text.replace('\n', ' ')))

def from_extended_string(text):
    return text.strip('\n').replace('\\n', '\n').replace('\\r', '\r')

def to_hex_prefix_string(text):
    result = ''
    hex_part = ''
    str_part = ''
    bytes_index = 0
    while bytes_index < len(text):
        ch = text[bytes_index]
        if ch == '\n':
            hex_part += '0A' + ' '
            str_part += '.'

            result += hex_part.ljust(52) + str_part + '\n'
            hex_part = ''
            str_part = ''
        elif ch == '\r':
            hex_part += '0D' + ' '
            str_part += '.'

            if ((bytes_index + 1) < len(text)) and (text[bytes_index + 1] == '\n'):
                hex_part += '0A' + ' '
                str_part += '.'
                bytes_index += 1

            result += hex_part.ljust(52) + str_part + '\n'
            hex_part = ''
            str_part = ''
        else:
            hex_part += '{:02X}'.format(ord(ch)) + ' '
            if ch < '\x20' or ch > '\x7F':
                ch = '.'
            str_part += ch

        if len(str_part) >= 16:
            result += hex_part.ljust(52) + str_part + '\n'
            hex_part = ''
            str_part = ''

        bytes_index += 1

    if str_part:
        result += hex_part.ljust(52) + str_part + '\n'

    return result
