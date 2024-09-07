

class FileError(Exception):
    pass


def read_file(file_name) -> list[str] | bool:
    '''Uses a filepath + filename string to return a list of all the 
    lines in the file, removes newlines in the resulting strings'''
    try:
        return_array = []
        open_file = file_name
        with open(open_file) as f:
            for line in f:
                return_array.append(line.strip().replace('\n', ''))
        return return_array
    except Exception as err:
        raise FileError(f"Error in read_file {err=}, {type(err)=}") from err
