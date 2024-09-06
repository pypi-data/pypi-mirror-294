from typing import NamedTuple, Any

# sentinel value for marking a deleted object, useful for linear probing
DELETED = object()

class Pair(NamedTuple):
    # tuple that guarantees immutability for any data type
    key: Any
    value: Any

class HashTable:
    def __init__(self, size=8, load_factor_treshold = 0.6):
        # default is small since we have dynamic resize
        if not isinstance(size, int):
            raise TypeError(f"Invalid input type: {type(size).__name__}. Expected int.")
        if not (0 < load_factor_treshold <= 1):
            raise ValueError("Load factor must be a number between (0, 1]")
        if size < 1:
            raise ValueError("Capacity must be a positive number")
        self._size = size
        self._load_factor_treshold = load_factor_treshold
        # initialize empty value slots (key-value pairs)
        # None can be used since we expect tuples as non-empty values
        self._items = [None] * self._size
        # list that preserves the insertion order of the keys
        # this reduces performances, since list search is O(N) vs set O(1)
        self._keys = []

    @property
    def items(self):
        # defensive copying + keep insertion order
        return [(key, self[key]) for key in self.keys
                if self._getpair(key) not in (None, DELETED)]

    @property
    def values(self):
        # list gives me duplicates
        return [self[key] for key in self._keys]

    @property
    def keys(self):
        return self._keys.copy()

    @property
    def size(self):
        return self._size

    @property
    def load_factor(self):
        occupied_or_deleted = [item for item in self._items if item]
        return len(occupied_or_deleted) / self.size

    @classmethod
    def from_dict(cls, dictionary, size=None):
        hash_table = cls(size or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __len__(self):
        return len(self.items)

    def __setitem__(self, key, value):
        # if self._load_factor_treshold == 1, that's a lazy resize
        if self.load_factor >= self._load_factor_treshold:
            self._resize_and_rehash()
            self[key] = value
        # linear probing hash collision resolution
        # look next hashed idx until we find empty slot
        for idx, pair in self._probe(key):
            # DELETED item slot is not replaced
            if pair is DELETED: continue
            # search
            # TODO: string equality test is costly, try hashing equality (cheaper) by storing also the hash
            if pair is None:
                # update, if we have matching key we overwrite
                self._items[idx] = Pair(key, value)
                # new key to be appended
                self._keys.append(key)
                break
            if pair.key == key:
                # update, if we have matching key we overwrite
                self._items[idx] = Pair(key, value)
                break

    def __delitem__(self, key):
        for idx, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._items[idx] = DELETED
                self._keys.remove(key)
                break
            else:
                raise KeyError(key)

    def __getitem__(self, key):
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def _getpair(self, key):
        ''' custom implementation to get the pair from key'''
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair
        raise KeyError(key)

    def __iter__(self):
        yield from self.keys

    def __str__(self):
        pairs = []
        for key, value in self.items:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    def __eq__(self, other):
        ''' two objects are equal if they have the same set of key-value pairs'''
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return set(self.items) == set(other.items)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __or__(self, other):
        if not isinstance(other, HashTable):
            raise TypeError
        new = self.copy()
        new.update(other)
        return new

    def __ror__(self, other):
        ''' right union, in case left object doesn't have __or__ method '''
        if not isinstance(other, HashTable):
            raise TypeError
        new = self.copy()
        new.update(other)
        return new

    def __ior__(self, other):
        ''' in-place union '''
        self.update(other)
        return self

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self):
        ''' create a new dictionary using the same items and size'''
        return self.from_dict(dict(self.items), size=self.size)

    def update(self, other):
        ''' update a dictionary with items from other, in case both have same key, keep other value '''
        if not isinstance(other, HashTable):
            raise TypeError
        if not other:
            return self
        for key, value in other.items:
            self[key] = value

    def _resize_and_rehash(self):
        # resize by creating a local copy
        # sentile value slots are dropped
        new = HashTable(size=self.size * 2)
        for key, value in self.items:
            # set into the new hash table
            new[key] = value
        self._items = new._items
        self._size = new.size

    def _index(self, key):
        return hash(key) % self.size

    def _probe(self, key):
        # you start by using hashed idx, then, loop through all the available slots
        index = self._index(key)
        for _ in range(self.size):
            yield index, self._items[index]
            index = (index + 1) % self.size



