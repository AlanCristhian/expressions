"""A module that let you define functions with generator expressions."""

import dis


class _Iterator:
    """This class store many base class. Is an helper class that 
    will be returned bye the _IterableMeta.__itert__() method.

    The value stored in self.bases will be used by 
    Object._find_arguments_classes() to find the type of
    each argument of the function.
    """
    def __init__(self, bases):
        self.bases = bases

    def __iter__(self):
        pass

    def __next__(self):
        pass


class _IterableMeta(type):
    """The *generator expression* need that *for statement* be
    iterable. Because that the *class object* should be iterable.
    """
    def __init__(cls, name, bases, namespace):
        cls.bases = bases
        return super().__init__(name, bases, namespace)

    def __iter__(cls):
        return _Iterator(cls.bases)


class Object(object, metaclass=_IterableMeta):
    def __init__(self, generator):
        self.generator = generator

        # the functions below find objects in the differents scopes
        self._locals = lambda _, name: self.generator.gi_frame.f_locals[name]
        self._globals = lambda _, name: self.generator.gi_frame.f_globals[name]
        self._attributes = lambda obj, name: getattr(obj, name)

        # associate one finder function to each instruction name
        self._lookup = {
            'LOAD_FAST':    self._locals,
            'LOAD_GLOBAL':  self._globals,
            'LOAD_ATTR':    self._attributes,
            'LOAD_DEREF':   self._locals,
        }

        self._find_arguments_classes()
    
    def _find_arguments_classes(self):
        # The arguments name is stored in self.generator.gi_code.co_varnames
        # but also the '.0' name is of the first iterable of the for statement
        argument_amount = len(self.generator.gi_code.co_varnames) - 1
        instructions_type = []
        group = []

        # El bytecode es una sucesion de instrucciones. Si hay una serie
        # ininterrumpida de instrucciones LOAD_*, entonces se refiere a un
        # solo objeto. En el bucle siguiente
        for instruction in dis.Bytecode(self.generator.gi_code):
            if instruction.opname.startswith('LOAD_'):
                group.append(instruction)
            else:
                if len(group) != 0:
                    instructions_type.append(group)
                    group = []
            if len(instructions_type) == argument_amount:
                break

        self._arguments_classes = []
        for group in instructions_type:
            # everything the first value is '.0'
            value = '.0'
            for instruction in group:
                # obtain the value from the memory
                value = self._lookup[instruction.opname]\
                    (value, instruction.argval)
            self._arguments_classes.append(value.bases)
