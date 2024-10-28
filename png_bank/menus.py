from simple_term_menu import TerminalMenu


def list_menu(choices):
    terminal_menu = TerminalMenu(choices)
    choice_index = terminal_menu.show()
    return choices[choice_index]


def get_ser(vault):
    items = []
    for ser, pas in vault.items():
        if len(pas) > 1:
            items.append(f"{ser} ({len(pas)})")
            continue
        items.append(ser)
    return list_menu(items).split(' ')[0]


def get_pass_from_vault(vault):
    ser = get_ser(vault)
    items = []
    for i, pas in enumerate(vault[ser]):
        items.append(f'{i+1}: {pas[0]}')
    return vault[ser][int(list_menu(items).split(':')[0])-1][1]


def yn(nomen=None, true=0):
    if nomen is None:
        nomen = ['yes', 'no']
    return list_menu(nomen) == nomen[true]
