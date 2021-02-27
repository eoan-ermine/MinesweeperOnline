import configparser
from enum import Enum


class Format(Enum):
    IniFormat = 0,
    MemoryFormat = 1,


def get_ini_config(filename: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def get_config(storage, format):
    if format == Format.MemoryFormat:
        return storage
    elif format == Format.IniFormat:
        return get_ini_config(storage)


def update_ini_file(filename, config):
    with open(filename, 'w') as configfile:
        config.write(configfile)


def ini_writer(filename: str, key: str, value):
    config = get_ini_config(filename)
    config['DEFAULT'][key] = value
    update_ini_file(filename, config)


def ini_reader(filename, key, default_value):
    config = get_ini_config(filename)
    return config.get('DEFAULT', key, fallback=default_value)


def memory_writer(storage: dict, key: str, value):
    storage[key] = value


def memory_reader(storage: dict, key: str, default_value):
    return storage.get(key, default_value)


class Settings:
    """ The Setting class provides persistent platform-independent application settings """

    def __init__(self, format: Format, filename: str = ""):
        self.formats = {Format.IniFormat: (ini_writer, ini_reader, filename),
                        Format.MemoryFormat: (memory_writer, memory_reader,
                                              {})}
        self.writer, self.reader, self.storage = self.formats[format]
        self.format = format

    def all_keys(self):
        config = get_config(self.storage, self.format)
        if self.format == Format.MemoryFormat:
            return list(config.keys())
        elif self.format == Format.IniFormat:
            return list(config['DEFAULT'].keys())

    def storage(self):
        return self.storage

    def format(self) -> Format:
        return self.format

    def clear(self):
        config = get_config(self.storage, self.format)
        if self.format == Format.MemoryFormat:
            config.clear()
        elif self.format == Format.IniFormat:
            for key in self.all_keys():
                del config['DEFAULT'][key]
            update_ini_file(self.storage, config)

    def set_value(self, key, value):
        self.writer(self.storage, key, value)

    def value(self, key, default_value=None):
        return self.reader(self.storage, key, default_value)

    def remove(self, key):
        config = get_config(self.storage, self.format)
        if self.format == Format.MemoryFormat:
            del config[key]
        elif self.format == Format.IniFormat:
            del config['DEFAULT'][key]
            update_ini_file(self.storage(), config)
