import sys
from pathlib import Path
from hashapp.fileHashChecker import text_to_data_dict, check_files_hashes, print_results


def main(args):

    # get args
    path_to_input_file = args[1]
    path_to_target_files = args[2]

    # read content of the input file
    data = Path(path_to_input_file).read_text()

    # transform text to matrix
    target_files_props_dict = text_to_data_dict(data)

    # check all mentioned in the input file files hashes
    results_arr = check_files_hashes(path_to_target_files, target_files_props_dict)

    # print results 
    print_results(results_arr)
        

if __name__ == '__main__':
    main(sys.argv)
