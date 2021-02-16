import configparser
from enum import Enum


class Format(Enum):
    IniFormat = 0,
    MemoryFormat = 1,


def ini_writer(filename: str, key: str, value):
    config = configparser.ConfigParser()
    config.read(filename)

    config['DEFAULT'][key] = value

    with open(filename, 'w') as configfile:
        config.write(configfile)


def ini_reader(filename, key, default_value):
    config = configparser.ConfigParser()
    config.read(filename)

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
        # TODO IMPLEMENT IT
        return self.variables.keys()

    def storage(self):
        return self.storage

    def format(self) -> Format:
        return self.format

    def clear(self):
        # TODO IMPLEMENT IT
        self.variables.clear()

    def set_value(self, key, value):
        self.writer(self.storage, key, value)

    def value(self, key, default_value=None):
        return self.reader(self.storage, key, default_value)

    def remove(self, key):
        # TODO IMPLEMENT IT
        self.variables.pop(key)
