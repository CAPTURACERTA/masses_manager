import os



def main():
    p = os.path.dirname(__file__)
    for s in "..\\database\\masses.db".split("\\"):
        p = os.path.join(p, s)
    print(os.path.exists(p))


if __name__ == "__main__":
    main()
