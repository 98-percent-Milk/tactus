from pprint import pprint
from utils import lexnames, ml, load_file
# cat = 2121620


def main():
    # animal = animal_to_synset('cat')
    data = load_file('cat')
    a = data['What type of thing is it?']
    pprint(if_animal(a))


def if_animal(data: list, animal: str) -> None:
    data = [x.replace(',', '') for x in data]
    temp = [data.pop(data.index(x)) for x in data[:] if lexnames(x, 'animal')]
    temp.extend([x for x in data[:] if ml('_'.join(x.split(' ')), animal)])
    return temp


if __name__ == "__main__":
    main()
