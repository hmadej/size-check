
TOLERANCE = 4 # size in kb


def format_diff(master, branch):
    if -TOLERANCE <= (master - branch) <= TOLERANCE:
        return ':heavy_check_mark:'
    elif master < branch:
        return f':warning: +{format_size(branch - master)}'
    else:
        return f':white_check_mark: {format_size(branch - master)}'


def format_size(size):
    if size == 0:
        return '-'
    if abs(size) // 1024 == 0:
        return f'{size}kB'
    else:
        return f'{size//1024:.1f}MB'


def make_table(master, branch):
    table = '<details>\n\n|   | master | branch | change |\n| --- | --- | --- | --- |\n'
    for key, value in master.items():
        if key in branch:
            table += table_row(key, value, branch[key])
        else:
            table += table_row(key, value, 0)
    if (keys := set(branch) - set(master)):
        for key in keys:
            table += table_row(key, 0, branch[key])
    return table + '\n\n</details>\n'


def make_tables(master, branch):
    tables = [make_table(value, branch[key]) for key, value in master.items()]
    return '\n'.join(tables)

def table_row(key, v1, v2):
    return f'| {key} | {format_size(v1)} | {format_size(v2)} | {format_diff(v1, v2)} |\n'
