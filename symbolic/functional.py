"""Functional programing features for python."""
import inspect
import types
import opcode
import numbers
import dis

from symbolic import core


# cache all constants to improve the performance
OPMAP_LOAD_GLOBAL = opcode.opmap['LOAD_GLOBAL']
OPMAP_LOAD_DEREF = opcode.opmap['LOAD_DEREF']
OPMAP_LOAD_CONST = opcode.opmap['LOAD_CONST']
OPCODE_HAVE_ARGUMENT = opcode.HAVE_ARGUMENT


def _make_closure_cell(val):
    """a nested function just for creating a closure"""
    def nested():
        return val
    return nested.__closure__[0]


def _pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def inject_constants(generator, **constants):
    """Return a copy of of the `generator` parameter. This copy have
    the constants defined in the `constants` map. If a key of
    `constants` share the same name than a global or local object,
    then replace such global or local by the value defined in the
    `constants` argument."""
    # NOTE: all vars with the *new_* name prefix are custom versions of
    # the original attributes of the generator.
    gi_code = generator.gi_code
    new_code = list(gi_code.co_code)
    new_consts = list(gi_code.co_consts)
    new_locals = generator.gi_frame.f_locals.copy()
    new_freevars = list(gi_code.co_freevars)
    new_names = list(gi_code.co_names)

    i = 0
    # through the list of instructions
    while i < len(new_code):
        op_code = new_code[i]
        # Replace global lookups by the values defined in *constants*.
        if op_code == OPMAP_LOAD_GLOBAL:
            oparg = new_code[i + 1] + (new_code[i + 2] << 8)
            # the names of all global variables are stored
            # in generator.gi_code.co_names

            # can't use the new_name variable directly because if I clean the
            # name i get an IndexError.
            name = gi_code.co_names[oparg]
            if name in constants:
                value = constants[name]
                # pos is the position of the new const
                for pos, v in enumerate(new_consts):
                    if v is value:
                        # do nothing  if the value is already stored
                        break
                # add the value to new_consts if such value not exists
                else:
                    pos = len(new_consts)
                    new_consts.append(value)
                new_code[i] = OPMAP_LOAD_CONST
                new_code[i + 1] = pos & 0xFF
                new_code[i + 2] = pos >> 8

        # Here repalce locals lookups by constants lookups with the values
        # defined in *constants*
        if op_code == OPMAP_LOAD_DEREF:
            oparg = new_code[i + 1] + (new_code[i + 2] << 8)
            # !!!: Now the name is sotred in generator.gi_code.co_freevars
            name = new_freevars[oparg]

            # Move the local variable to the `constants` argument
            if  name in generator.gi_frame.f_locals \
            and name in gi_code.co_consts \
            and name in gi_code.co_freevars:
                if name in gi_code.co_consts:
                    _new_key, _new_value = next(
                        (_key, _value) for _key, _value in \
                        _pairwise(gi_code.co_consts) if _key == name
                    )
                    # remove the variable from the local namespace and ...
                    new_locals.pop(_new_key)
                    # ... add such variable to the constants dictionary
                    constants.update({_new_key: _new_value})

            if name in constants:
                value = constants[name]
                # pos is the position of the new const
                for pos, v in enumerate(new_consts):
                    # do nothing  if the value is already stored
                    if v is value:
                        break
                # add the value to new_consts if such value not exists
                else:
                    pos = len(new_consts)
                    new_consts.append(value)
                    # !!!: generator.gi_code.co_locals and
                    # generator.gi_code.co_freevars store the locals names.
                    # I clear this names because if not the generator can't
                    # compile.
                    new_freevars.remove(name)
                    if name in new_locals:
                        del new_locals[name]
                new_code[i] = OPMAP_LOAD_CONST
                new_code[i + 1] = pos & 0xFF
                new_code[i + 2] = pos >> 8
        i += 1
        if op_code >= OPCODE_HAVE_ARGUMENT:
            i += 2

    # NOTE: the lines comented whit the *CUSTOM:* tag mean that such argument
    # is a custom version of the original object

    # new_freevars = [var for var in new_freevars if var != 'a_local']
    # new_locals = {key: value for key, value in new_locals.items() if key != 'a_local'}
    # new_names.append('a_local')

    if '_' in gi_code.co_varnames:
        print()
        print('gi_frame.f_locals', generator.gi_frame.f_locals, new_locals)
        print('gi_code.co_argcount', gi_code.co_argcount)
        print('gi_code.co_kwonlyargcount', gi_code.co_kwonlyargcount)
        print('gi_code.co_nlocals', gi_code.co_nlocals)
        print('gi_code.co_stacksize', gi_code.co_stacksize)
        print('gi_code.co_flags', gi_code.co_flags)
        # print('gi_code.co_code', gi_code.co_code)
        print('gi_code.co_consts', gi_code.co_consts)
        print('gi_code.co_names', gi_code.co_names, new_names)
        print('gi_code.co_varnames', gi_code.co_varnames)
        # print('gi_code.co_filename', gi_code.co_filename)
        print('gi_code.co_name', gi_code.co_name)
        print('gi_code.co_firstlineno', gi_code.co_firstlineno)
        # print('gi_code.co_lnotab', gi_code.co_lnotab)
        print('gi_code.co_freevars', gi_code.co_freevars, new_freevars)
        print('gi_code.co_cellvars', gi_code.co_cellvars)

    # create a new *code object* (like generator.gi_code)
    code_object = types.CodeType(
        gi_code.co_argcount,
        gi_code.co_kwonlyargcount,
        gi_code.co_nlocals,
        gi_code.co_stacksize,
        gi_code.co_flags,
        bytes(new_code),            # CUSTOM: generator.gi_code.co_code
        tuple(new_consts),          # CUSTOM: generator.gi_code.co_consts
        tuple(new_names),           # CUSTOM: generator.gi_code.co_names
        gi_code.co_varnames,
        gi_code.co_filename,
        gi_code.co_name,
        gi_code.co_firstlineno,
        gi_code.co_lnotab,
        tuple(new_freevars),        # CUSTOM: generator.gi_code.co_freevars
        gi_code.co_cellvars)

    if '_' in gi_code.co_varnames:
        print(dis.dis(code_object))

    # Customize the argument of the function object
    _code    = code_object
    _globals = generator.gi_frame.f_globals
    _name    = generator.__name__
    _argdef  = None
    _closure = tuple(_make_closure_cell(var) for var in new_freevars)

    # Make a *generator function*
    # NOTE: the *generator functon* make a *generator object* when is called
    function = types.FunctionType(_code, _globals, _name, _argdef, _closure)

    # return the *generator object*
    return function(**new_locals)       # CUSTOM: generator.gi_frame.f_locals


class Parameters(metaclass=core.IterableMeta):
    pass


_SIGNATURE =     "def {name}{varnames}:\n"
_YIELDED_VALUE = "    yield {expression}"


class Function(core.CallableObject):
    def __init__(self, generator):
        keys = set(generator.gi_code.co_names) - {'where'}
        keys_and_values = generator.gi_code.co_consts[:-1]
        constants = {key: value for value, key in \
                     _pairwise(reversed(keys_and_values)) if
                     key in keys}

        generator = inject_constants(generator, **constants)
        super().__init__(generator)

        varnames = str(self._var_names).replace("'", "").replace(',)', ')')
        signature = _SIGNATURE.format(name='function',
                                      varnames=varnames)

        expression = self._make_expression()
        if type(expression) is list and type(expression[0]) is core.where:
            _, expression = expression
        # CAVEAT: use the repr built-in function to souround the string
        # constants with single quotes.
        yielded_value = _YIELDED_VALUE.format(expression=repr(expression))
        self.__source__ = signature + yielded_value
