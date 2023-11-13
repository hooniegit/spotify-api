def create_folders(folder_dir):
    import os

    try:
        os.makedirs(folder_dir)
    except:
        print(f"FOLDER EXISTS: {folder_dir}")


# load file in local
def file_json(file_dir, json_data):
    import json

    try :
        with open(file_dir, "a") as file:
            json.dump(json_data, file, indent=4)
    except:
        with open(file_dir, "w") as file:
            json.dump(json_data, file, indent=4)
    
    print("SUCCEED")


# test
if __name__ == "__main__":
    # confirmed - 23.10.06
    # file_dir = "/home/hooniegit/git/personal/spotify-api/data/sample.json"
    # json_data = {"data" : "Hello, World!"}
    # file_json(file_dir, json_data)
    pass