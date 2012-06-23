"""Test the interfaces module."""

from unittest2 import TestCase
import interfaces


@interfaces.define
class StringInterface(object):

    @interfaces.require
    def execute(self, argument):
        """Execute must be implemented with an 'argument' option."""
        pass


@interfaces.define
class NumberInterface(object):

    @interfaces.require
    def add(self, number1, number2):
        """Add must be implemented with an 'argument' option."""
        pass


@interfaces.define
class InheritableInterface(object):

    def __init__(self, name):
        self._name = name

    @interfaces.require
    def run(self):
        """Run must be implemented."""
        pass

    def retrieve(self):
        return self._name


@interfaces.define
class FinalInterface(object):

    @interfaces.final
    def test(self):
        return "original"


class TestInterfaces(TestCase):

    def test_implement(self):
        """Test implementing an interface."""

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            @interfaces.implement(StringInterface)
            class Obstinate(object):
                pass


        @interfaces.implement(StringInterface)
        class Broifier(object):

            def execute(self, argument):
                return "%s, bro." % argument

        broifier = Broifier()
        self.assertEqual("5, bro.", broifier.execute(5))

        # should just work, through the magic of inheritance.
        @interfaces.implement(StringInterface)
        class PassThrough(Broifier):
            pass

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            # should fail, because it's actually not really implemented...
            @interfaces.implement(StringInterface)
            class InterfaceSubclass(StringInterface):
                pass

        @interfaces.implement(StringInterface)
        class Inclusifier(Broifier):

            def execute(self, argument):
                result = super(Inclusifier, self).execute(argument)
                return result.replace("bro", "ladies and gentlemen")

        inclusifier = Inclusifier()
        self.assertEqual("5, ladies and gentlemen.", inclusifier.execute(5))

    def test_implement_not_interface(self):
        """Test implementing a not defined interface."""
        class BadInterface(object):
            pass

        with self.assertRaises(interfaces.InvalidInterface):
            @interfaces.implement(BadInterface)
            class Foo(object):
                pass

    def test_multiple_interfaces(self):
        """Test that we can use multiple interfaces."""

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            @interfaces.implement(StringInterface, NumberInterface)
            class UberThing(object):
                pass

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            @interfaces.implement(StringInterface, NumberInterface)
            class UberThing(object):

                def execute(self, argument):
                    return argument

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            @interfaces.implement(StringInterface, NumberInterface)
            class UberThing(object):

                def add(self, number1, number2):
                    return number1 + number2

        @interfaces.implement(StringInterface, NumberInterface)
        class UberThing(object):

            def execute(self, argument):
                return argument

            def add(self, number1, number2):
                return number1 + number2

        uber = UberThing()
        self.assertEqual("foo", uber.execute("foo"))
        self.assertEqual(10, uber.add(4, 6))

    def test_interface_inheritance(self):
        """Test that interfaces can inherit from each other, gaining rules."""
        @interfaces.define
        class InheritedInterface(StringInterface):
            @interfaces.require
            def run(self):
                """Must implement run."""
                pass

        with self.assertRaises(interfaces.MissingRequiredAttribute):
            @interfaces.implement(InheritedInterface)
            class UsesInheritedInterface(object):
                def run(self):
                    pass

    def test_implement_inheritance(self):
        """Test that we don't break any normal inheritance rules."""

        @interfaces.implement(InheritableInterface)
        class Task(InheritableInterface):

            def run(self):
                self._name = "FOOBAR!"

        task = Task("whatever")
        self.assertEqual("whatever", task.retrieve())
        task.run()
        self.assertEqual("FOOBAR!", task.retrieve())

    def test_final(self):
        """Test that the final keyword works in various scenarios."""

        with self.assertRaises(interfaces.CannotOverrideFinal):
            @interfaces.implement(FinalInterface)
            class Belligerent(object):
                def test(self):
                    # should not be able to do this
                    pass

        with self.assertRaises(interfaces.CannotOverrideFinal):
            @interfaces.implement(FinalInterface)
            class Belligerent(FinalInterface):
                def test(self):
                    # shouldn't be able to through inheritance either
                    pass

        @interfaces.implement(FinalInterface)
        class Respectful(FinalInterface):
            pass

        respect = Respectful()
        self.assertEqual("original", respect.test())

        # trying to 'sneak' in an overwrite with a mixin
        class SneakyMixin(object):
            def test(self):
                pass

        with self.assertRaises(interfaces.CannotOverrideFinal):
            @interfaces.implement(FinalInterface)
            class SneakyBelligerent(SneakyMixin):
                pass

        # the final decorator should be usable on any base class
        # or mixin used by an @implement class.

        class FinalMixin(object):

            @interfaces.final
            def run(self):
                pass

        with self.assertRaises(interfaces.CannotOverrideFinal):
            @interfaces.implement(FinalInterface)
            class MixinBelligerent(FinalMixin):
                def run(self):
                    pass

    def test_strict(self):
        """Test the strict checker for final, etc."""

        @interfaces.strict
        class FinalMixin(object):

            @interfaces.final
            def run(self):
                pass

        with self.assertRaises(interfaces.CannotOverrideFinal):
            @interfaces.strict
            class MixinBelligerent(FinalMixin):
                def run(self):
                    pass

