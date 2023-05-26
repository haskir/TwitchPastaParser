from collections import Counter
import difflib, re
from progress.bar import IncrementalBar
from twitchio import Message


def skip(message: Message) -> bool:
    if len(message.content) < 40:
        return True
    if "bot" in message.author.name or "streamelements" in message.author.name:
        return True
    if "@" in message.content and message.channel.name not in message.content:
        return True
    return False


def is_pasta(string: str) -> int:
    loop: bool = False
    smiles: int = 0
    for key, item in enumerate(string):
        if ord(item) > 100000:
            print(f"{item} -> {ord(item)}")
            smiles += 1
            string = string[:key] + " " + string[key + 1:]
    if smiles > 5:
        return True


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


if __name__ == "__main__":
    strings = open("messages.txt", "r", errors="ignore", encoding="utf-8").readlines()
    bar = IncrementalBar('Countdown', max=len(strings))
    dictionary = dict()
    bar.start()
    for key, string in enumerate(strings):
        bar.next()
        try:
            dictionary[string] = \
            max(similarity(string, t_string) for t_string in strings[key + 1:-10:])
        except ValueError:
            ...
    with open("test.txt", "w", errors="ignore") as file:
        for item in sorted(dictionary.items(), key=lambda x: x[1])[:10:]:
            file.write(item[0])
    bar.finish()