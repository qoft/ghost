bypass_fonts = {
    'a': '𝚊',
    'b': '𝚋',
    'c': '𝚌',
    'd': '𝚍',
    'e': '𝚎',
    'f': '𝚏',
    'g': '𝚐',
    'h': '𝚑',
    'i': '𝚒',
    'j': '𝚓',
    'k': '𝚔',
    'l': '𝚕',
    'm': '𝚖',
    'n': '𝚗',
    'o': '𝚘',
    'p': '𝚙',
    'q': '𝚚',
    'r': '𝚛',
    's': '𝚜',
    't': '𝚝',
    'u': '𝚞',
    'v': '𝚟',
    'w': '𝚠',
    'x': '𝚡',
    'y': '𝚢',
    'z': '𝚣'
}

def bypass(text):
    result = ""
    for char in text:
        if char in bypass_fonts:
            result += bypass_fonts[char]
        else:
            result += char
    return result
