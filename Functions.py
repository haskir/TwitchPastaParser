from collections import Counter
import re

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


if __name__ == "__main__":
    test_string = """Баночка🥫с окурками🚬уже переполнена🤐 То,🟢что крутишься
    с придурками🙃— только🙄твоя👈вина😓
    Баночка🥫с окурками🚬баночка🥫с окурками🚬Уже🧨переполнена😲уже🧨переполнена😲
    Поменялись🔄куртками🧥— Только🎇теперь🕐навсегда😳"""

    print(is_pasta(test_string))
