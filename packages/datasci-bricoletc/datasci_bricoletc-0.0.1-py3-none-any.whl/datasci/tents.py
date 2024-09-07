from typing import List, Optional
from pathlib import Path
from itertools import starmap, repeat


class UnsetFieldsException(Exception):
    pass


class UnsupportedFieldsException(Exception):
    pass


class Tent:
    _UNSET = "NA"

    def __init__(self, h: list, r_h: list, immutable: bool, unset = None):
        self._headers = h
        self._headers_set = set(h)
        self._required_headers = r_h
        self._required_headers_set = set(r_h)
        self._set_headers = set()
        self._immutable = immutable
        if unset is not None:
            self._UNSET = unset
        for key in self._headers:
            setattr(self, key, self._UNSET)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setattr__(self, key, value):
        if not key.startswith("_"):
            self._check_fields_are_supported({key})
            if key in self._set_headers and self._immutable:
                raise ValueError(f"{key} is already set")
            self._set_headers.add(key)
        super().__setattr__(key, value)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        missing_fields = self._required_headers_set.difference(self._set_headers)
        if len(missing_fields) > 0:
            raise UnsetFieldsException(
                f"Missing unset fields: {missing_fields}. Entry can only be serialised with all of the following fields set: {self._required_headers}"
            )
        values = starmap(getattr, zip(repeat(self), self._headers))
        return "\t".join(map(str, values))

    def _check_fields_are_supported(self, field_names):
        if not self._headers_set.issuperset(field_names):
            raise UnsupportedFieldsException(
                f"Supported fields: {self._headers}"
            )

    def update(self, **fields):
        self._check_fields_are_supported(fields.keys())
        for key, val in fields.items():
            self[key] = val


class Tents:
    """
    [TODO] Description
    [TODO] Usage
    """

    @classmethod
    def from_tsv(self, fname: str, headers: List[str] = None) -> "Tents":
        with Path(fname).open("r") as fin:
            if headers is None:
                while True:
                    headers = next(fin).strip()
                    if not headers.startswith("#"):
                        headers = headers.split("\t")
                        break
            result = Tents(headers=headers)
            for line in fin:
                elements = line.strip().split("\t")
                new_tent = result.new()
                new_tent.update(**dict(zip(headers, elements)))
                result.add(new_tent)
        return result


    def __init__(self, headers: list, required_headers: list = [], immutable: bool = False, unset_value = None):
        self._headers = headers
        self._required_headers = required_headers
        self._entries = list()
        self._immutable = immutable
        self._unset = unset_value

    def __repr__(self, with_header: bool = True):
        return self.get_header() + "\n".join(map(repr, self._entries))

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, idx):
        return self._entries[idx]

    def add(self, entry: Tent):
        repr(entry)
        assert entry._headers == self._headers
        self._entries.append(entry)

    def new(self) -> Tent:
        return Tent(self._headers, self._required_headers, self._immutable, self._unset)

    def get_header(self):
        return "\t".join(self._headers) + "\n"

