import configparser

#has_wrote = write_config(file_path = 'settings.ini', section = 'SectionKeyBinds', option = 'restart_key', value = 'f4')
#keybinds = read_config(file_path = 'settings.ini', section = 'SectionKeyBinds')
#print(f'has_wrote: {has_wrote}\nkeybinds: {keybinds}')

def read_config(file_path, section):
    c = configparser.ConfigParser()

    if c.read(file_path) == []:
        print('invalid file given: invalid file name or file is empty')
        return None

    if not section in c.sections():
        print('given section not found in config file')
        return None

    dict = {}

    options = c.options(section)

    for option in options:
        try:
            dict[option] = c.get(section, option)
            if dict[option] == -1:
                print('failed to load option', option)
        except:
            print('exception caught while getting option', option)
            dict[option] = None

    return dict

def write_config(file_path, section, option, value):
    c = configparser.ConfigParser()

    if c.read(file_path) == []:
        print('invalid file given: invalid file name or file is empty')
        return None

    if not section in c.sections():
        print('given section not found in config file')
        return None

    cfgfile = None
    try:
        cfgfile = open(file_path,'w')
    except:
        print('error opening file', file_path)
        return False

    try:
        c.set(section, option, value)
    except:
        print('exception caught while setting option', option)
        return False

    c.write(cfgfile)

    cfgfile.close()
    return True
