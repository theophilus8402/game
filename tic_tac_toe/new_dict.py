
# don't put None key items
# error on setting duplicates
# error if key doesn't exist when deleting

class KeyExists(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "Key, {}, already exists.".format(key)


class PlayerExists(KeyExists):
    def __init__(self, key):
        self.key = key
        self.message = "Player, {}, already exists.".format(key)


class UniqueDict(dict):


    def __init__(self, *args, **kwargs):
        self.error = KeyExists
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        # I don't think we need to change anything here
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):

        # make sure the key is not None
        if key is not None:

            # make sure we don't overwrite keys
            if key in self:
                raise self.error(key)

            dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        # print('update {} : {}'.format(args, kwargs))
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class PlayerDict(UniqueDict):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.error = PlayerExists

