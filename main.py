from requests import get
# from nltk.corpus import wordnet as wn
# from datamuse import Datamuse
from bs4 import BeautifulSoup as bs
from pprint import pprint
from json import dumps, loads
from filteration import if_animal

# API = Datamuse()


def main():
    """How to use it
    Step.1 Run the command -> python ./main.py
    Step.2 Enter a word you would like to search -> Example: cat
    Step.3 It will collect words that are either associated or describes the
           'word' and will save it to files directory as a json file with same
           filename as the 'word'
    Step.4 Use display function to output the collected words.
    """
    word = input("Enter a word you would like to search: ")
    category = input("Enter category: ")
    collect_words(word, category)


def key_change(data: dict, word: str) -> None:
    """Replace part of dictionary key with given word

    Args:
        data (dict): data containing replaceable part
        word (str): new word to replace the part
    """
    new_keys = [x.replace('{blank}', word) for x in data]
    new_keys.reverse()
    old_keys = [x for x in data]
    for key in old_keys:
        data[new_keys.pop()] = data.pop(key)


def collect_words(word: str = '', category: str = '') -> None:
    """Collect words that either associated or describes the 'word'

    Args:
        word (str, optional): Search word. Defaults to ''.
    """
    if word == '':
        print("Word can't be an empty string!!!")
        return
    search_terms = load_file('new_template')
    word_template = load_file('word_template')
    key_change(search_terms, word)
    key_change(word_template, word)
    word_template['word'] = word
    soup = get_soup(word)
    divs = get_divs(soup)
    category_sets = separate_categories(soup)
    for key in search_terms:
        word_template[key] = get_list(
            word, search_terms[key], divs, category_sets)
    if category == "animal":
        key = "What type of thing is it?"
        word_template[key] = if_animal(word_template[key], word)
    save_file(word, word_template)


def separate_categories(soup: bs) -> list:
    """Separate div elements into 2 lists. One with more items and one without.

    Args:
        soup (bs): BeautifulSoup object

    Returns:
        list: lists containing div Beautiful Soup object
    """
    divs = get_divs(soup)
    divs = list(enumerate(get_categories(divs)))
    divs_more = [divs.pop(divs.index(x))
                 for x in divs[:] if x[1] in is_there_more(soup)]
    return divs, divs_more


def get_list(word: str, search_t: list, divs: list, category_sets: list) -> list:
    """Extract information about the 'word' from div elements using search terms

    Args:
        word (str): Main word to generate the list
        search_t (list): list containing search terms
        divs (list): list containing div BeautifulSoup object
        category_sets (list): Names of div elements seperated into 2 lists

    Returns:
        list: list of words that are associated with the 'word'
    """
    search_t = [x.replace("{blank}", word) for x in search_t]
    without = category_sets[0]
    with_more = category_sets[1]
    without_category = [x[1] for x in without]
    with_category = [x[1] for x in with_more]
    items = []
    for term in search_t:
        try:
            i = without_category.index(term)
            items.extend(get_items(divs[without[i][0]]))
        except ValueError:
            try:
                # We can further extract additional possible answers if we want
                # But for now I'm just removing the "more" link
                i = with_category.index(term)
                items.extend(get_items(divs[with_more[i][0]]))
            except ValueError:
                print(f"Category: {term} -> Not Found")
    return list(set(items))


def get_items(div: list) -> list:
    """Extract list items from div element

    Args:
        div (list): div element containing unordered list element

    Returns:
        list: list of items
    """
    items = [x.a.text.lower().strip() for x in div.find_all('li')]
    try:
        items.remove("more »")
    except ValueError:
        pass
    return items


def get_categories(divs: list) -> list:
    """Extract Text of h2 element from div element

    Args:
        divs (list): div elements

    Returns:
        list: Concept names extracted from the div elements
    """
    return [x.h2.text.strip().lower().replace('…', '') for x in divs]


def get_divs(soup: bs) -> list:
    """Extract div elements from BeautifulSoup object

    Args:
        soup (bs): BeautifulSoup object

    Returns:
        list: div elements
    """
    return soup.find_all(
        'div', class_="pure-u-1 pure-u-md-1-2 pure-u-lg-1-3 pure-u-xl-1-4 feature-box")


def is_there_more(soup: bs) -> list:
    """Extract names of div elements that has more items to display

    Args:
        soup (bs): BeautifulSoup object

    Returns:
        list: Text of h2 elements of div elements
    """
    more = soup.find_all('li', class_='more')
    return [x.parent.parent.h2.text.strip().lower().replace('…', '') for x in more]


def get_soup(search_term: str, url: str = "https://conceptnet.io/c/en/{}") -> bs:
    """Retrieves URL as request object and converts it into BeautifulSoup object

    Args:
        search_term (str): Term/object/item to search
        url (_type_, optional): URL link. Defaults to "https://conceptnet.io/c/en/{}".

    Returns:
        bs: BeautifulSoup object
    """
    return bs(get(url.format(search_term)).text, 'html.parser')


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


# def lexnames(word: str, category: str) -> list:
#     temp = word.split(' ')
#     if category in temp:
#         return True
#     if len(temp) == 1:
#         return True if category in [x.lexname().split('.')[1] for x in wn.synsets(word)] else False
#     for t in temp:
#         if category in [x.lexname().split('.')[1] for x in wn.synsets(t)]:
#             return True
#     return False


# def ml(search_word: str, look_word: str) -> list:
#     return True if look_word in [x['word'] for x in API.words(ml=f"{search_word}")] else False


if __name__ == "__main__":
    main()
