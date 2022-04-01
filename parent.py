from utils import load_file, all_parents


def main():
    word = 'eagle'
    animal = load_file('animal')
    categories = list(animal)
    found = all_parents(word, categories)
    print(found)


if __name__ == "__main__":
    main()
