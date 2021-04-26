import os
import hashlib
from pathlib import Path


def compare_strings(v1, v2):
    """Compare two strings."""

    if v1 == v2 and isinstance(v1, str) and isinstance(v2, str):
        return "OK"
    else:
        return "FAIL"


def get_target_file_content(filepath):
    """Get content of the target file."""

    isfile = os.path.isfile(filepath)
    result = Path(filepath).read_text() if isfile else 'NOT FOUND'
    return isfile, result   


def get_hash(content, hash_alg):
    """Check content hash."""

    content = str.encode(content)
    hash_alg = hash_alg.lower()

    ok = True
    if hash_alg == 'md5':
        result = hashlib.md5(content).hexdigest()
    elif hash_alg == 'sha1':
        result = hashlib.sha1(content).hexdigest()
    elif hash_alg == 'sha256':
        result = hashlib.sha256(content).hexdigest()
    else:
        ok = False
        result = 'NOT FOUND'
    
    return ok, result


def check_files_hashes(path_to_dir, target_files_props_dict):
    """Check all target files hashes."""

    results = []

    for i in range(len(target_files_props_dict["filename"])):
        filename = target_files_props_dict["filename"][i]
        hash_alg = target_files_props_dict["hash_alg"][i]
        exp_hash_str = target_files_props_dict["hash_str"][i]

        target_file_path = os.path.join(path_to_dir, filename)
        
        # get target file content
        isfile, result = get_target_file_content(target_file_path)

        if isfile:
            ok, result = get_hash(result, hash_alg)
            if ok:
                result = compare_strings(result, exp_hash_str)

        results.append([filename, result])

    return results


def text_to_data_dict(text):
    """Transform text to dictionary with data."""

    lines_arr = text.split('\n')

    # remove empty strings
    lines_arr = list(filter(None, lines_arr))

    res_dict = {"filename": [], "hash_alg": [], "hash_str": []}
    # transform every line to individual values
    for line in lines_arr:
        props_arr = line.split(' ')        
        res_dict["filename"].append(props_arr[0])
        res_dict["hash_alg"].append(props_arr[1])
        res_dict["hash_str"].append(props_arr[2])

    return res_dict


def print_results(results_arr):
    """Print results."""

    for data in results_arr:
        print(data[0], data[1])
