
def format_diff(master, branch):
    if -4 < (master - branch) < 4:
        return ':heavy_check_mark:'
    elif master < branch:
        return f':warning: +{format_size(branch - master)}'
    else:
        return f':white_check_mark: {format_size(branch - master)}'


def format_size(number):
    if number == 0:
        return '-'
    if abs(number) // 1024 == 0:
        return f'{number}kB'
    else:
        return f'{number//1024:.1f}MB'


def make_table(master, branch):
    table = ''
    for key, value in master.items():
        if type(value) is dict:
            table += '|   | master | branch | change |\n| --- | --- | --- | --- |\n'
            table += make_table(value, branch[key])
        else:
            if key in branch:
                table += table_row(key, value, branch[key])
            else:
                table += table_row(key, value, 0)
    if (keys := set(branch) - set(master)):
        for key in keys:
            table += table_row(key, 0, branch[key])
    return table + '\n'


def table_row(key, v1, v2):
    return f'| {key} | {format_size(v1)} | {format_size(v2)} | {format_diff(v1, v2)} |\n'
