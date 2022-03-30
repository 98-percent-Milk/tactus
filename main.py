from requests import get
from bs4 import BeautifulSoup as bs
from pprint import pprint
from json import dumps, loads


# get_list(word, search_t, divs)
# dont_need = ['synonyms', "related terms", "derived terms", "word forms", "etymological", ""]
# location = ["location of {blank}"]
# type of thing = ["{blank} is a type of"]
# material = ["{blank} is made of"]
# can be = ["{blank} can be..."]
# what is it used for = ["{blank} is capable of...", "{blank} is used for..."]
# what does it do = ["{blank} wants...", "{blank} is capable of", "{blank} is a way of"]
# make you think of = ["types of {blank}", "{blank} is a type of...", "things located at {blank}",
#                      "parts of {blank}", "things that want {blank}", "things used for {blank}"]
# doesn't want = ["{blank} doesn't want...", ]
# parts = ["{blank} has...", "parts of {blank}"]
# properties = ["properties of {blank}"]
def main():
    search_terms = load_file('search_template')
    word_template = load_file('word_template')
    word = 'witch'
    word_template['word'] = word
    soup = get_soup(word)
    divs = get_divs(soup)
    category_sets = separate_categories(soup)
    # pprint(category_sets[0])
    # pprint(category_sets[1])
    for key in search_terms:
        word_template[key] = get_list(
            word, search_terms[key], divs, category_sets)

    pprint(word_template)
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
                print("Category Not Found")
    return items


def get_items(div: list) -> list:
    """Extract list items from div element

    Args:
        div (list): div element containing unordered list element

    Returns:
        list: list of items
    """
    items = [x.a.text.strip() for x in div.find_all('li')]
    try:
        items.remove("More »")
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


if __name__ == "__main__":
    main()
