import abc
import contextlib
import pathlib as p
import shelve
from collections.abc import Callable, Generator
from functools import wraps
from typing import Generic, TypeVar

from tcrutils import Singleton

T = TypeVar('T')

def syncing_method(func: Callable) -> Callable:
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    v = func(self, *args, **kwargs)
    self.sync()
    return v
  return wrapper

class DefaultDictDB(Singleton, Generic[T], shelve.DbfilenameShelf):
  path: p.Path

  @abc.abstractmethod
  def default_factory(self, key: str) -> T: ...

  @staticmethod
  def fix_key(key) -> str:
    return str(key)

  def __init__(self) -> None:
    super().__init__(self.path)

  def __init_subclass__(cls, *, dir: p.Path | str, mkdir: bool = True) -> None:
    dir = p.Path(dir)
    if mkdir:
      dir.mkdir(parents=True, exist_ok=True)
    dir = dir / dir.name
    cls.path = dir
    return super().__init_subclass__()

  def __getitem__(self, key) -> T:
    key = self.fix_key(key)

    if key not in self:
      self[key] = self.default_factory(key)
    return super().__getitem__(key)

  @syncing_method
  def __setitem__(self, key: str, value: T) -> None:
    key = self.fix_key(key)
    return super().__setitem__(key, value)

  @syncing_method
  def __delitem__(self, key: str) -> None:
    key = self.fix_key(key)
    return super().__delitem__(key)

  def __contains__(self, key: str) -> bool:
    key = self.fix_key(key)
    return super().__contains__(key)

  def get(self, key: str, default: None = None) -> T:
    """Get in a default dict is self[key]."""
    return self[key]

  @syncing_method
  def clear(self) -> None:
    return super().clear()

  @syncing_method
  def popitem(self) -> tuple[str, T]:
    return super().popitem()

  @syncing_method
  def update(self, d: dict[str, T]) -> None:
    return super().update(d)

  def setdefault(self, *_, **__):
    """❌ You cannot use setdefault() on a default dict."""
    raise NotImplementedError('You cannot use setdefault() on a default dict.')

  @contextlib.contextmanager
  def cm(self, key: str):
    """Get a context manager for getting, and after the context ends setting the mutable resource at a certain key in this DB."""
    mutable_value = self[key]
    yield mutable_value
    self[key] = mutable_value

  def hard_reset(self) -> None:
    """Permanently delete the DB files. This may get you unstuck if your db is corrupted (and using `.clear()` fails) due to stuff like failed unpickling, though all your data will be lost.

    This will not delete the folder itself, only files in it.
    This action closes the shelf due to it being in a corrupt state if not closed.
    """
    self.close()
    for file in self.path.parent.glob(f'{self.path.name}*'):
      file.unlink()
