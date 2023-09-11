#!/usr/bin/python
"""
MIT License

Copyright (c) 2022 EdvinAlvarado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import annotations
from typing import Callable, Generic, TypeVar, Optional


T = TypeVar('T')
U = TypeVar('U')

class Option(Generic[T]):
    def __init__(self, value: T, is_some: bool) -> None:
        self._val = value
        self._is_some = is_some
        self._type = type(value)
    
    @classmethod
    def Some(cls, value: T) -> Option[T]:
        return cls(value, True)
    @classmethod
    def NONE(cls) -> Option[T]:
        return cls(None, False)
    @classmethod
    def maybe(cls, val: Optional[T]) -> Option[T]:
        return cls.NONE() if val is None else cls.Some(val)
    
    def __bool__(self) -> bool:
        return self._is_some

    @property
    def is_some(self) -> bool:
        return self._is_some
    @property
    def is_none(self) -> bool:
        return not self._is_some
    
    def expect(self, msg: str) -> T:
        if self._is_some:
            return self._val
        raise ValueError(msg)
    def unwrap(self) -> T:
        if self._is_some:
            return self._val
        raise ValueError
    def unwrap_or(self, default: T) -> T:
        if self._is_some:
            return self._val
        return default
    # Need to somehow know what type it could had been
#     def unwrap_or_default(self) -> T:
#         if self._is_some:
#             return self._val
#         return type(self._val)()
    def map(self, f: Callable[[T], U]) -> Option[U]:
        match self._is_some:
            case True: return Option.Some(f(self._val))
            case False: return Option.NONE() # type: ignore
    def map_or(self, f: Callable[[T], U], default: U) -> Option[U]:
        match self._is_some:
            case True: return Option.Some(f(self._val))
            case False: return Option.Some(default)
    # def map_or_else(self, f: Callable, default: Callable) -> Option[U]:
    #     match self._is_some:
    #         case True: return Option.Some(f(self._val))
    #         case False: return Option.Some(default)
    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        if self._is_some:
            match f(self._val):
                case True: return self
                case False: return Option.NONE()
        return Option.NONE()
    def insert(self, val: T) -> T:
        self = Option.Some(val)
        return val
    def get_or_insert(self, val: T) -> T:
        if not self._is_some:
            self = Option.Some(val)
        return self._val
    def take(self) -> Option[T]:
        if self._is_some:
            v = self
            self = Option.NONE()
            return v
        return self
    def replace(self, val: T) -> Option[T]:
        v = self
        self = Option.Some(val)
        return v
    def contains(self, v: T) -> bool:
        if self._is_some:
            return self._val == v
        return False
    def zip(self, opt: Option[U]) -> Option[tuple[T, U]]:
        if self._is_some and opt._is_some:
            return Option.Some((self._val, opt.unwrap()))
        return Option.NONE() # type: ignore

    def __str__(self) -> str:
        if self._is_some:
            return f"Some({self._val})"
        return "NONE()"



if __name__ == "__main__":
    t = Option.Some(2)
    f = Option.NONE()
    print(t.is_some)
    print(f.is_some)
