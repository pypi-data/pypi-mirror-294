# SPDX-FileCopyrightText: © 2024 Shaun Wilson
# SPDX-License-Identifier: MIT

from .ConfigurationException import ConfigurationException
import json
import re
import types
from typing import Any, ForwardRef, get_type_hints
import unicodedata

type any = Any

class Configuration:
    """A configuration class which creates a layer of indirection between configuration providers and configuration consumers."""

    __key_scrub_re:re.Pattern
    __keys:dict[str, str]
    __normalize:bool

    def __init__(self, *, normalize:bool = False, scrubkeys:bool = False):
        """By default keys are ingest as-is, pass `True` for `normalize` to normalize kets to lower case."""
        self.__keys = {}
        self.__normalize = normalize
        self.__key_scrub_re = None if not scrubkeys else re.compile(r'[^A-Za-z0-9_]', re.IGNORECASE | re.UNICODE)

    def __delitem__(self, key:str) -> None:
        key = key.upper()
        k = self.__keys.get(key)
        if k != None:
            delattr(self, k)
            self.__keys.pop(key)

    def __getitem__(self, key:str) -> any:
        parts = key.replace(':', '__').split('__')
        o = self
        for part in parts:
            if o == self:
                k = self.__keys.get(part.upper())
                if k == None:
                    raise KeyError()
                else:
                    o = getattr(o, self.__scrub_key(k))
            else:
                o = o[part]
        return o

    def __iter__(self):
        return iter(self.__keys.values())

    def __len__(self) -> int:
        return len(self.__keys)

    def __recursiveBind(self, target:object, source:ForwardRef('Configuration')|dict) -> any:
        targetTypeHints = get_type_hints(target)
        for aname in dir(target):
            if aname.startswith('_'):
                continue
            lval = getattr(target, aname)
            if isinstance(lval, types.FunctionType) or isinstance(lval, types.MethodType):
                continue
            ahint = targetTypeHints.get(aname)
            rval = source.get(aname)
            if rval == None:
                setattr(target, aname, None)
            elif ahint is float:
                v = float(rval)
                setattr(target, aname, v)
            elif ahint is int:
                v = int(rval)
                setattr(target, aname, v)
            elif ahint is str:
                v = str(rval)
                setattr(target, aname, v)
            elif isinstance(rval, Configuration):
                if hasattr(ahint, '__origin__') and issubclass(ahint.__origin__, dict):
                    lval = rval.toDictionary()
                    setattr(target, aname, lval)
                else:
                    if lval == None:
                        lval = ahint()
                        setattr(target, aname, lval)
                    self.__recursiveBind(lval, rval)
            else:
                if hasattr(ahint, '__origin__') and issubclass(ahint.__origin__, list):
                    elementType = ahint.__args__[0]
                    l = ahint()
                    for e in rval:
                        v = self.__recursiveBindType(elementType, e)
                        l.append(v)
                    setattr(target, aname, l)
                else:
                    # naive behavior
                    setattr(target, aname, rval)
        return target

    def __recursiveBindType(self, elementType:type, source:any) -> any:
        if isinstance(source, elementType):
            return source
        elif elementType is float:
            return float(source)
        elif elementType is int:
            return int(source)
        elif elementType is str:
            return str(source)
        elif isinstance(source, Configuration | dict):
            v = elementType()
            return self.__recursiveBind(v, source)       
        else:
            raise ConfigurationException(f'Recursive bind to type `{elementType}` from `{type(source)}` is not supported.')

    def __scrub_key(self, key:str) -> str:
        """Scrubs a key for use as an attribute/identifier according to the Python lexer/standard."""
        key = key.replace(':', '__').replace('.', '_')
        return key if None == self.__key_scrub_re else \
            self.__key_scrub_re.sub(
                self.__scrub_uc,
                unicodedata.normalize(
                    'NFKC',
                    key))

    def __scrub_uc(self, m:re.Match) -> str:
        match unicodedata.category(m[0]):
            case 'Lu' | 'Ll' | 'Lt' | 'Lm' | 'Lo' | 'Nl' | 'Mn' | 'Mc' | 'Nd' | 'Pc' :
                return m[0]
            case _:
                return '_'

    def __setitem__(self, key:str, value:any) -> None:
        self.set(key, value)

    def __str__(self) -> str:
        return json.dumps(self.toDictionary())

    def bind(self, target:object, key:str|None = None) -> any:
        """Binds the configuration values into the target object.
        
        Can optionally specify a configuration key to bind from."""
        if not target:
            raise ConfigurationException('Missing required argument: target')
        if key == None:
            return self.__recursiveBind(target, self)
        else:
            source = self.get(key)
            sourceType = type(source)
            if sourceType is Configuration or sourceType is dict:
                return self.__recursiveBindFromConfig(target, source)
            else:
                raise ConfigurationException(f'Bind of source type `{type(source)}` is not supported.')

    def clear(self) -> None:
        while len(self.__keys) > 0:
            t = self.__keys.popitem()
            delattr(self, t[1])

    @staticmethod
    def fromDictionary(source:dict, *, normalize:bool = False, scrubkeys:bool = False) -> 'Configuration':
        config:Configuration = Configuration(normalize=normalize, scrubkeys=scrubkeys)
        for kvp in source.items():
            v = kvp[1]
            if issubclass(type(v), dict):
                v = Configuration.fromDictionary(v, normalize=normalize, scrubkeys=scrubkeys)
            config.set(kvp[0], v)
        return config

    def get(self, key:str, default:any = None) -> any:
        """Gets the configuration element associated with the specified key."""
        parts = key.replace(':', '__').split('__')
        o = self
        for part in parts:
            if o == self:
                k = self.__keys.get(part.upper())
                if k == None:
                    return default
                else:
                    o = getattr(o, self.__scrub_key(k))
            else:
                o = o.get(part, default)
        return o

    def has_key(self, key:str) -> bool:
        return self.__keys.get(key.upper()) != None

    def items(self) -> list[tuple[str,any]]:
        it = []
        for k in self.keys():
            v = self.get(k)
            it.append((k, v))
        return it

    def keys(self) -> list[str]:
        return self.__keys.values()

    def pop(self, key:str) -> any:
        value = self[key]
        del self[key]
        return value

    def set(self, key:str, value:any) -> None:
        """Sets the configuration element for the specified key."""
        if self.__normalize:
            key = key.upper()
        parts = key.replace(':', '__').split('__')
        o = self
        for i in range(len(parts) - 1):
            if o == self:
                k = self.__keys.get(parts[i].upper())
                if k == None:
                    c = Configuration(normalize=self.__normalize, scrubkeys=(None != self.__key_scrub_re))
                    setattr(o, self.__scrub_key(parts[i]), c)
                    self.__keys[parts[i].upper()] = parts[i]
                    o = c
                else:
                    o = getattr(self, self.__scrub_key(k))
            else:
                if not o.has_key(parts[i]):
                    c = Configuration(normalize=self.__normalize, scrubkeys=(None != self.__key_scrub_re))
                    o.set(parts[i], c)
                    o = c
                else:
                    o = o.get(parts[i])
        vtype = type(value)
        if issubclass(vtype, dict):
            value = Configuration.fromDictionary(value, normalize=self.__normalize, scrubkeys=self.__key_scrub_re != None)
        elif issubclass(vtype, list):
            l = []
            for e in value:
                if issubclass(type(e), dict):
                    l.append(Configuration.fromDictionary(e, normalize=self.__normalize, scrubkeys=self.__key_scrub_re != None))
                else:
                    l.append(e)
            value = l
        key = parts[-1]
        if o == self:
            k = self.__keys.get(key.upper())
            if k != None:
                setattr(self, self.__scrub_key(k), value)
            else:
                self.__keys[key.upper()] = key
                setattr(self, self.__scrub_key(key), value)
        else:
            o.set(key, value)

    def toDictionary(self) -> dict:
        """Projects a dictionary from the configuration object."""
        result = {}
        for k in self.__keys.values():
            v = getattr(self, self.__scrub_key(k))
            if isinstance(v, Configuration):
                result[k] = v.toDictionary()
            elif issubclass(type(v), list):
                tmp = []
                for e in v:
                    if isinstance(e, Configuration):
                        tmp.append(e.toDictionary())
                    else:
                        tmp.append(e)
                result[k] = tmp
            else:
                result[k] = v
        return result

    def values(self) -> list[any]:
        values = []
        for k in self.__keys.values():
            v = getattr(self, self.__scrub_key(k))
            values.append(v)
        return values
