__author__ = 'H.Rouhani'


def get_extension(file_name):
    splitted_file_name = file_name.rsplit('.', 1)
    return splitted_file_name[1]


def get_file_name(file_name):
    splitted_file_name = file_name.rsplit('.', 1)
    return splitted_file_name[0]
