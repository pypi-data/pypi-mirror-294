#!/usr/bin/env python3
"""
Module ENUMTOOLS -- PLIB3 Enum Enhancements
Sub-Package STDLIB of Package PLIB3
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains enhanced Enum support; the main purpose
is to enable user-defined additions to an existing Enum.
"""

import sys
from collections.abc import Mapping
import enum

from plib.stdlib.builtins import first


def _make_new_member(new_func, value_type, use_args):
    # Code cribbed from EnumMeta.__new__, returns a function that
    # constructs a new instance of the appropriate enum class
    if use_args:
        if issubclass(value_type, tuple):
            def get_args(value):
                return value
        else:
            def get_args(value):
                return (value,)
        def new_member(cls, value):
            args = get_args(value)
            member = new_func(cls, *args)
            if not hasattr(member, '_value_'):
                if value_type is object:
                    member._value_ = value
                else:
                    member._value_ = value_type(*args)
            return member
    else:
        def new_member(cls, value):
            member = new_func(cls)
            if not hasattr(member, '_value_'):
                member._value_ = value
            return member
    return new_member


class ExtendableEnumMeta(enum.EnumMeta):
    """Metaclass for extendable enum.
    
    Overrides class construction and ``__call__`` methods to allow new
    instances to be created while still disallowing subclassing once
    the enum has members.
    """
    
    @classmethod
    def __prepare__(meta, name, bases, **kwds):
        # Note: this and what's in __new__ below seems like a lot of boilerplate to
        # handle adding a keyword argument to a class definition (also it's not
        # clear what exactly in EnumMeta.__prepare__ is checking for an unexpected
        # keyword argument since **kwds is neither accessed nor passed in a super call)
        disable_aliases = kwds.pop('disable_aliases', None)
        classdict = enum.EnumMeta.__prepare__(name, bases, **kwds)
        classdict._disable_aliases = disable_aliases
        return classdict
    
    def __new__(meta, name, bases, classdict, **kwds):
        value_types = set(type(classdict[m]) for m in classdict._member_names)
        if len(value_types) > 1:
            raise ValueError("All members of an extendable enum must have the same value type.")
        value_type = value_types.pop() if value_types else None
        member_type, first_enum = meta._get_mixins_(name, bases)
        new_func, _, use_args = meta._find_new_(
            classdict, member_type, first_enum,
        )
        new_member = _make_new_member(new_func, value_type, use_args)
        disable_aliases = classdict._disable_aliases
        del classdict._disable_aliases
        # Note: since we already popped it out of kwds in __prepare__ above,
        # why is it still here?
        assert kwds.pop('disable_aliases', None) is disable_aliases
        enum_class = enum.EnumMeta.__new__(meta, name, bases, classdict, **kwds)
        enum_class._value_type = value_type
        enum_class._new_member = new_member
        enum_class._disable_aliases = disable_aliases
        return enum_class
    
    def __call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=1, disable_aliases=False):
        enum_class = enum.EnumMeta.__call__(cls, value, names, module=module, qualname=qualname, type=type, start=start)
        if names is not None:
            # We created a new enum class
            enum_class._disable_aliases = disable_aliases
        return enum_class


class ExtendableEnum(enum.Enum, metaclass=ExtendableEnumMeta):
    """Extendable enum class.
    
    Allows user code to add new members to an existing enum by calling the
    ``add_member`` class method. The ``extend`` class method is also provided
    for convenience to allow adding multiple new members at once. Once an
    extendable enum has members it still cannot be subclassed.
    
    >>> class Color(ExtendableEnum):
    ...     RED = 1
    ...     GREEN = 2
    ...
    >>> Color.add_member('BLUE', 3)
    <Color.BLUE: 3>
    >>> Color.add_member('GREEN', 4)
    Traceback (most recent call last):
    ...
    ValueError: Member name GREEN already exists in enum Color
    >>> Color.add_member('YELLOW', 2)
    <Color.YELLOW: 2>
    >>> class UniqueColor(ExtendableEnum, disable_aliases=True):
    ...     RED = 1
    ...     GREEN = 2
    ...
    >>> UniqueColor.add_member('BLUE', 3)
    <UniqueColor.BLUE: 3>
    >>> UniqueColor.add_member('GREEN', 4)
    Traceback (most recent call last):
    ...
    ValueError: Member name GREEN already exists in enum UniqueColor
    >>> UniqueColor.add_member('YELLOW', 2)
    Traceback (most recent call last):
    ...
    ValueError: Aliases are disabled for enum UniqueColor
    """
    
    @classmethod
    def add_member(cls, name, value):
        """Add new member to an extendable enum.
        
        Raises ``ValueError`` if a new member's value is not of the same type as
        existing members' values, or if the member name already exists. If the
        ``disable_aliases`` keyword argument was used in constructing the extendable
        enum class, existing values cannot be aliased, and ``ValueError`` is raised
        if this is attempted.
        """
        if not isinstance(value, cls._value_type):
            raise ValueError("Invalid value type for extendable enum {}: {}".format(cls.__name__, repr(value)))
        if name in cls.__members__:
            raise ValueError("Member name {} already exists in enum {}".format(name, cls.__name__))
        if cls._disable_aliases and (value in cls._value2member_map_):
            raise ValueError("Aliases are disabled for enum {}".format(cls.__name__))
        existing_member = first(m for m in cls.__members__.values() if m._value_ == value)
        obj = cls._new_member(cls, value)
        obj._name_ = name
        obj._value_ = value
        obj.__objclass__ = cls
        cls._member_map_[name] = existing_member if existing_member is not None else obj
        try:
            # This will fail if value is not hashable, but enum supports that case so suppress exception
            cls._value2member_map_[value] = existing_member if existing_member is not None else obj
        except TypeError:
            pass
        if not existing_member:
            # This list does not contain aliases
            cls._member_names_.append(name)
        return obj
    
    @classmethod
    def extend(cls, members):
        """Add multiple members at once to an extendable enum.
        
        The ``members`` parameter must be an iterable of ``(name, value)`` tuples
        or a mapping of names to values.
        """
        for name, value in (members.items() if isinstance(members, Mapping) else members):
            cls.add_member(name, value)


def _get_transform(name, prefix_classname=False, classname_transform=None):
    if prefix_classname:
        prefix = name
        if classname_transform:
            prefix = classname_transform(prefix)
        f = (lambda s: '{}_{}'.format(prefix, s))
    else:
        f = (lambda s: s)
    return f


def _add_global(mod, s, m, f):
    setattr(mod, f(s), m)


def add_enum_member_global(modname, s, m, prefix_classname=False, classname_transform=None):
    """Add global to module modname for enum member ``m`` with name ``s``.
    """
    f = _get_transform(type(m).__name__, prefix_classname, classname_transform)
    _add_global(sys.modules[modname], s, m, f)


def _add_globals(mod, name, obj, prefix_classname=False, classname_transform=None):
    f = _get_transform(name, prefix_classname, classname_transform)
    for s, m in obj.__members__.items():
        _add_global(mod, s, m, f)


def add_enum_globals(modname, name, obj, prefix_classname=False, classname_transform=None):
    """Add globals to module ``modname`` for all members of enum with class name ``name``.
    """
    return _add_globals(sys.modules[modname], name, obj, prefix_classname, classname_transform)


def add_all_enum_globals(modname, prefix_classname=False, classname_transform=None):
    """Add globals to module ``modname`` for all enums in module.
    """
    mod = sys.modules[modname]
    for name in dir(mod):
        obj = getattr(mod, name)
        if isinstance(obj, type) and issubclass(obj, enum.Enum):
            _add_globals(mod, name, obj, prefix_classname, classname_transform)
