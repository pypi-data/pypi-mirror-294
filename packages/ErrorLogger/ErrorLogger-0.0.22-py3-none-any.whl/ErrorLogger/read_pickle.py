import pickle
 
def read_pickle_file(pickle_file):
    try:
        with open(pickle_file, 'rb') as file:
            data = pickle.load(file)
            print("Data from pickle file:", data)
            return data
    except FileNotFoundError:
        print(f"File {pickle_file} not found.")
    except Exception as e:
        print(f"An error occurred while reading the pickle file: {e}")
 
# Example usage
pickle_data = read_pickle_file('logs.pkl')