from twittersql.database import init_db
from twittersql.utils import find_json_files, load_json
from twittersql.database import write_tweet

def main():
    print("Starting")
    init_db()

    for index, file in enumerate(find_json_files()):
        data = load_json(file)
        print("{} - loaded: {}".format(index, file))
        write_tweet(data)



if __name__ == '__main__':
    main()