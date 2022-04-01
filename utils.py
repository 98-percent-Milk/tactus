from nltk.corpus import wordnet as wn
from datamuse import Datamuse
from json import loads, dumps

API = Datamuse()


def save_file(filename: str, data: dict) -> None:
    """Save 'data' dictionary object as json file in files directory

    Args:
        filename (str): Name of the json file
        data (dict): 'data' dictionary object that is being saved
    """
    with open(f"files/{filename}.json", 'w') as f:
        f.write(dumps(data, indent=4))


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


def all_parents(word: str, categories: list) -> list:
    temp = set(categories)
    for syn in wn.synsets(word, 'n'):
        p_temp = set(x.name() for x in parents(syn))
        found = temp.intersection(p_temp)
        if found:
            return list(found)
    return []


def animal_to_synset(animal: str) -> wn.synset:
    index = [v[0] + 1 for v in list(enumerate(x.lexname()
                                              for x in wn.synsets(animal))) if 'noun.animal' in v]
    if not index:
        print(f"{animal} is not an animal")
        return
    return wn.synset(f"{animal}.n.0{index[0]}")


def off_to_syn(offset: int, pos: str = 'n') -> wn.synset:
    return wn.synset_from_pos_and_offset(pos, offset)
