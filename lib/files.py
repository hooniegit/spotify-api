
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


# send file from local to hdfs
def files_to_hdfs(type, date):
    import subprocess
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, f'../data/{type}/{date}')

    subprocess.run(["hdfs", "dfs", "-mkdir", f"/spotify/{type}/{date}"])
    subprocess.run(["hdfs", "dfs", "-put", f"{data_dir}/", f"/spotify/{type}/"])


# test
if __name__ == "__main__":
    # confirmed - 23.10.06
    # file_dir = "/home/hooniegit/git/personal/spotify-api/data/sample.json"
    # json_data = {"data" : "Hello, World!"}
    # file_json(file_dir, json_data)
    pass