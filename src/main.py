from data.table_classes import ClientColumns
from typing import get_args


def main():
    d = {"a":"a", "b":"", "c":""}
    if any(d.values()):
        print("any!")
    if not any(d.values()):
        print("NOT any!")


if __name__ == "__main__":
    main()
