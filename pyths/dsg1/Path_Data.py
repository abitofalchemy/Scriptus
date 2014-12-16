import pandas
import os

# Class that grabs data from data files
class Path_Data:

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.path_data = dict()
        self.limit = 1 # limits the number of files processed, for testing purposes
        i = 0
        for filename in os.listdir(self.directory_path):
            if filename[0] is '.':
                continue
            print 'Processing file: ' + filename
            f = open(self.directory_path + filename)
            ID = self.get_ID_from_name(filename)
            for line in f:
                self.path_data[ID + '_to_' + line[0]] = line[1]
            i += 1
            if i >= self.limit:
                break
        return

    # Grabs the node ID from the filename
    def get_ID_from_name(self, filename):
        start = -1
        end = int()
        for i in range(0, len(filename)):
            if filename[i].isdigit():
                start = i
            if start != -1 and filename[i].isalpha:
                end = i
                break
        return filename[start:end]


if __name__ == '__main__':
    """
    Path_Data
    """
     
    # Grab shortest path data
    print 'Fetching shortest path data'
    shortest_path_data = Path_Data('/data/zliu8/sssp/')

    # Grab cat_path data
    print 'Fetching category path data'
    cat_path_data = Path_Data('/data/zliu8/our_algo/')

    # Process data to produce correlation
    print 'Processing data'

    sp_df = pandas.DataFrame(shortest_path_data.path_data.values, shortest_path_data.path_data.keys)
    cp_df = pandas.DataFrame(cat_path_data.path_data.values, cat_path_data.path_data.keys)

    # sp_df = pandas.DataFrame({'key': shortest_path_data.path_data.keys, 'SP': shortest_path_data.path_data.values})
    # cp_df = pandas.DataFrame({'key': cat_path_data.path_data.keys, 'CP': cat_path_data.path_data.values})

    data = pandas.DataFrame()
    data = pandas.merge(sp_df, cp_df, on='key')

    print data['SP'].corr(data['CP'])

