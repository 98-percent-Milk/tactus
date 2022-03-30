from json import loads
from time import sleep


def main():
    word_data = load_file('witch')
    display_single(word_data)


def wait_for_answer() -> None:
    input("Think for an answer and Press Enter to see possible answers")


def get_option(data: dict) -> str:
    temp = list(enumerate(data, start=-1))[1:]
    index = [x[0] for x in temp]
    print(f"{'Available options':-^30}")
    [print(f"{i + 1}.{val}") for i, val in temp].remove(None)
    while True:
        try:
            if (choice := int(input("Enter option number: ")) - 1) in index:
                return temp[choice][1]
            else:
                print("\tTry again!!! Invalid option")
        except ValueError:
            print("\tTry again!!! Invalid input")


def display_single(data: dict) -> None:
    option = get_option(data)
    wait_for_answer()
    title = f"{option.title()} of a {data['word'].upper()}"
    print(f"\n{title:^120}\n")
    count = -1
    for val in data[option]:
        if (count := count + 1) == 4:
            print()
            count = 0
        print(f"{val:<30}", end='', flush=True)
        sleep(0.4)
        # print()


def display_all(data: dict) -> None:
    print(f"\n{data['word'].upper():^120}\n")
    for key in list(data)[1:]:
        count = -1
        print(f"{key:-^120}")
        for val in data[key]:
            if (count := count + 1) < 4:
                print(f"{val:<30}", end='', flush=True)
                sleep(0.2)
            else:
                print()
                count = -1
        print()


def load_file(filename: str) -> dict:
    with open(f"files/{filename}.json", 'r') as f:
        data = loads(f.read())
    return data


if __name__ == "__main__":
    main()
