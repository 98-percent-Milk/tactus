from nltk.corpus import wordnet as wn
from datamuse import Datamuse
from json import loads
from pprint import pprint
# cat = 2121620

API = Datamuse()


def main():
    # animal = animal_to_synset('cat')
    animal = 2121620
    data = load_file('cat')
    a = data['What type of thing is it?']
    if_animal(a)


def if_animal(data: list, animal: str) -> None:
    data = [x.replace(',', '') for x in data]
    temp = [data.pop(data.index(x)) for x in data[:] if lexnames(x, 'animal')]
    temp.extend([x for x in data[:] if ml('_'.join(x.split(' ')), animal)])
    return temp


def lexnames(word: str, category: str) -> list:
    temp = word.split(' ')
    if category in temp:
        return True
    if len(temp) == 1:
        return True if category in [x.lexname().split('.')[1] for x in wn.synsets(word)] else False
    for t in temp:
        if category in [x.lexname().split('.')[1] for x in wn.synsets(t)]:
            return True
    return False


def ml(search_word: str, look_word: str) -> list:
    return True if look_word in [x['word'] for x in API.words(ml=f"{search_word}")] else False


def names(synsets: list) -> list:
    return [x.name().split('.')[0] for x in synsets]


def parents(word_synset: wn.synset) -> list:
    return list(set(word_synset.closure(lambda x: x.hypernyms())))


def animal_to_synset(animal: str) -> wn.synset:
    index = [v[0] + 1 for v in list(enumerate(x.lexname()
                                              for x in wn.synsets(animal))) if 'noun.animal' in v]
    if not index:
        print(f"{animal} is not an animal")
        return
    return wn.synset(f"{animal}.n.0{index[0]}")


def off_to_syn(offset: int, pos: str = 'n') -> wn.synset:
    return wn.synset_from_pos_and_offset(pos, offset)


def load_file(filename: str) -> dict:
    """Load json file from files directory

    Args:
        filename (str): Name of the json file

    Returns:
        dict: return json file as dictionary object
    """
    with open(f"files/{filename}.json", 'r') as f:
        data = loads(f.read())
    return data


if __name__ == "__main__":
    main()
