import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, f'../lib')
sys.path.append(lib_dir)

from files import files_to_hdfs

# send artist files from local to hdfs
def artists_to_hdfs(date):
    files_to_hdfs("artists", date)

# send album files from local to hdfs
def albums_to_hdfs(date):
    files_to_hdfs("albums", date)

# send track files from local to hdfs
def tracks_to_hdfs(date):
    files_to_hdfs("tracks", date)


if __name__ == "__main__":
    # confirmed - 23.10.16
    # artists_to_hdfs("2023-10-16")

    # confirmed - 23.10.16
    # albums_to_hdfs("2023-10-16")

    # confirmed - 23.10.16
    # tracks_to_hdfs("2023-10-16")
    pass