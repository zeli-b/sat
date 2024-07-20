from os import listdir, rename


def main():
    for filename in listdir("."):
        if filename.endswith(".svg"):
            rename(filename, filename[2:])


if __name__ == "__main__":
    main()
