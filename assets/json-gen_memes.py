import json

master_list = {}

def main():
    while True:
        meme_object = {}
        try:
            input_file = input()
        except EOFError:
            return
        meme_object["FILE_URL"] = input_file
        meme_name = input()
        meme_object["ACTORS"] = []
        for i in range(int(input())):
            entry = list(map(int, input().split()))
            meme_object["ACTORS"].append((entry[0], entry[1], entry[2]))
        master_list[meme_name] = meme_object

if __name__ == "__main__":
    main()
    print(json.dumps(master_list, indent=2))