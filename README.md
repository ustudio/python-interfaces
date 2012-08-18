Interfaces
==========

Overview
--------

This library is a trivial implementation of an interface in Python,
with the following aspects / features:

* It fails at import time, not at construction, so you know
  immediately when you have a problem.
* It's quite simple (very few LOC) and lenient where it counts
* It exclusively uses decorators, so...
* It does not require inheritance (reducing 'forced' subclassing)
* It does not enforce any typing checks
* It is intended to 'enhance' duck typing by avoiding common
  pitfalls (forgot to implement something on your fake duck class,
  overwrote something fundamental, etc.)

Usage
-----

Given a simple interface like:

```python
@interfaces.define
class DuckInterface(object):

    @interfaces.require
    def quack(self):
        """All Ducks must implement a 'quack' method."""
        pass
```

...the following will raise a MissingRequiredAttribute exception
at import time:

```python
@interfaces.implement(DuckInterface)
class Silent(object):
    # no quack method
    pass
```

This, however works:

```python
@interfaces.implement(DuckInterface)
class Tree(object):

    @interfaces.final
    def quack(self):
        return "the tree appears to quack."

tree = Tree()
tree.quack()
```

Additionally, if you are interested in using the `final` method decorator
outside of an interface, you can do so using the `strict` class decorator
around any class you want to check:

```python
@interfaces.strict
class BaseClass(object):

    @interfaces.final
    def method(self):
        return "Old functionality!"

# the following will raise an exception at import:

@interfaces.strict
class SubClass(BaseClass):

    def method(self):
        return "New functionality!"
```

It will also check to make sure your arguments match in your implemented
methods. For example:

```python
@interfaces.define
class Base(object):
    @interfaces.require
    def foo(self, a, b, *args):
        pass

@interfaces.implements(Base)
class Sub(object):
    def foo(self, a):
        pass
```

...will raise an `InvalidMethodSignature` error. It checks arguments (and
argument names) as well as the presence of *args and **kwargs.

Limitations
-----------

Obviously, this does nothing for enforcing interfaces on the calling side.
I've contemplated something like:

```python
def get_json(instance):
    # raises an exception if instance does not implement
    # JSONViewInterface
    interfaces.expects(instance, JSONViewInterface)
    return instance.to_json()
```

...but that's just plain type checking, and the only thing you gain over isinstance
is a more explicit exception at runtime. Feedback welcome.
