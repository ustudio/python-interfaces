Interfaces
==========

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

A simple example:

```python
    @interfaces.define
    class DuckInterface(object):

    @interfaces.require
    def quack(self):
        """All Ducks must implement a 'quack' method."""
        pass

    @interfaces.implement(DuckInterface)
    class Tree(object):

        @interfaces.final
        def quack(self):
            return "the tree appears to quack."

    def in_the_forest(duck):
        print duck.quack()

    tree = Tree()
    in_the_forest(tree)
```

Additionally, if you are interested in using the `final` method decorator
outside of an interface, you can do so using the `strict` class decorator
around any class you want to check:

```python
    @interfaces.strict
    class BaseClass(object):

        @interfaces.final
        class method(self):
            return "Old functionality!"

    # the following will raise an exception at import:

    @interfaces.strict
    class SubClass(object):

        class method(self):
            return "New functionality!"
```
