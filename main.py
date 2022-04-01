from requests import get
from bs4 import BeautifulSoup as bs
from filtration import if_animal
from utils import load_file, save_file, all_parents
from pprint import pprint
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
    word_template = collect_words(word, category)
    if category == "animal":
        new_categories = list(load_file('animal'))
        new_word = all_parents(word, new_categories)[0].split('.')[0]
    collect_additional(new_word, word, category, word_template)


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


def collect_additional(new_word: str, old_word: str, category: str, word_template: dict) -> None:
    search_terms = load_file('new_template')
    if category == "animal":
        add_template = load_file("additional")
        key_change(add_template, new_word)
        key_change(search_terms, new_word)
        soup = get_soup(new_word)
        divs = get_divs(soup)
        category_sets = separate_categories(soup)
        for key in search_terms:
            word_template[key.replace(new_word, old_word)] = get_list(
                new_word, search_terms[key], divs, category_sets)
        pprint(word_template)
        save_file(old_word, word_template)


def collect_words(word: str = '', category: str = '') -> dict:
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
    soup = get_soup(word)
    divs = get_divs(soup)
    word_template['word'] = word
    category_sets = separate_categories(soup)
    for key in search_terms:
        word_template[key] = get_list(
            word, search_terms[key], divs, category_sets)
    if category == "animal":
        key = "What type of thing is it?"
        word_template[key] = if_animal(word_template[key], word)
    save_file(word, word_template)
    return word_template


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


if __name__ == "__main__":
    main()
