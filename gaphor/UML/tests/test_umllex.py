"""
Parsing of UML model elements from string tests.
"""

import unittest
from gaphor.application import Application
from gaphor.UML.elementfactory import ElementFactory
from gaphor.UML import *
from gaphor.UML.umllex import parse
from gaphor.UML.umllex import attribute_pat, operation_pat, parameter_pat

def dump_prop(prop):
    m = attribute_pat.match(prop)
    #print m.groupdict()

def dump_oper(oper):
    m = operation_pat.match(oper)
    if m:
        g = m.group
    else:
        # set name to oper
        return
    #print g('vis'), g('name'), g('type'), g('mult_l'), g('mult_u'), g('tags')
    if g('params'):
        params = g('params')
        while params:
            m = parameter_pat.match(params)
            g = m.group
            #print ' ', g('dir') or 'in', g('name'), g('type'), g('mult_l'), g('mult_u'), g('default'), g('tags')
            params = g('rest')

dump_prop('#/name')
dump_prop('+ / name : str[1..*] = "aap" { static }')
dump_prop('+ / name : str[*] = "aap" { static }')

dump_oper('myfunc(aap:str = "aap", out two): type')
dump_oper('   myfunc2 ( ): type')
dump_oper('myfunc(aap:str[1] = "aap" { tag1, tag2 }, out two {tag3}): type')


factory = ElementFactory()

class AttributeTestCase(unittest.TestCase):

    def setUp(self):
        factory.init(Application)
        factory.flush()


    def tearDown(self):
        factory.shutdown()


    def test_parse_property_1(self):
        #log.set_log_level(log.INFO)

        #print 'testing parse_property()...'
        a = factory.create(Property)
        assert len(factory.values()) == 1

        # Very simple:

        parse_property(a, 'myattr')
        #assert a.visibility == 'protected', a.visibility
        assert a.isDerived == False, a.isDerived
        assert a.name == 'myattr', a.name
        assert a.typeValue.value is None, a.typeValue.value 
        assert a.lowerValue.value is None, a.lowerValue.value 
        assert a.upperValue.value is None, a.upperValue.value 
        assert a.defaultValue.value is None, a.defaultValue.value 
        s = render_property(a)
        parse_property(a, s)
        assert s == render_property(a)

        a.unlink()

    def test_parse_property_2(self):
        # All features:
        a = factory.create(Property)

        parse_property(a,'+ / name : str[0..*] = "aap" { static }')
        assert a.visibility == 'public'
        assert a.isDerived == True, a.isDerived
        assert a.name == 'name', a.name
        assert a.typeValue.value == 'str', a.typeValue.value 
        assert a.lowerValue.value == '0', a.lowerValue.value 
        assert a.upperValue.value == '*', a.upperValue.value 
        assert a.defaultValue.value == '"aap"', a.defaultValue.value 
        s = render_property(a)
        parse_property(a, s)
        assert s == render_property(a)
        #print render_property(a)

        a.unlink()

    def test_parse_property_3(self):
        # Invalid syntax:
        a = factory.create(Property)

        parse_property(a, '+ name = str[*] = "aap" { static }')
        #assert a.visibility == 'protected'
        assert a.isDerived == False, a.isDerived
        assert a.name == '+ name = str[*] = "aap" { static }', a.name
        assert not a.typeValue or a.typeValue.value is None, a.typeValue.value 
        assert not a.lowerValue or a.lowerValue.value is None, a.lowerValue.value 
        assert not a.upperValue or a.upperValue.value is None, a.upperValue.value 
        assert not a.defaultValue or a.defaultValue.value is None, a.defaultValue.value 
        s = render_property(a)
        parse_property(a, s)
        assert s == render_property(a)
        #print render_property(a)

        # Cleanup

        a.unlink()
        assert len(factory.values()) == 0

    def test_parse_property_4(self):
        # Association end:

        a = factory.create(Association)

        p = factory.create(Property)
        p.association = a
        parse_property(p, 'end')
        #assert p.visibility == 'protected', p.visibility
        assert p.name == 'end', p.name
        assert not p.typeValue or p.typeValue.value is None, p.typeValue.value 
        assert not p.lowerValue or p.lowerValue.value is None, p.lowerValue.value 
        assert not p.upperValue or p.upperValue.value is None, p.upperValue.value 
        assert not p.defaultValue or p.defaultValue.value is None, p.defaultValue.value 
        p.unlink()
        a.unlink()

    def test_parse_property_5(self):
        a = factory.create(Association)
        p = factory.create(Property)
        p.association = a
        parse_property(p, 'end')
        #assert p.visibility == 'protected', p.visibility
        assert p.name == 'end', p.name
        assert not p.typeValue or p.typeValue.value is None, p.typeValue.value 
        assert not p.lowerValue or p.lowerValue.value is None, p.lowerValue.value 
        assert not p.upperValue or p.upperValue.value is None, p.upperValue.value 
        assert not p.defaultValue or p.defaultValue.value is None, p.defaultValue.value 
        p.unlink()
        a.unlink()

    def test_parse_property_6(self):
        a = factory.create(Association)
        p = factory.create(Property)
        p.association = a
        parse_property(p, '0..2 { tag }')
        #assert p.visibility == 'protected', p.visibility
        assert p.name is None, p.name
        assert not p.typeValue or p.typeValue.value is None, p.typeValue.value 
        assert p.lowerValue.value == '0', p.lowerValue.value 
        assert p.upperValue.value == '2', p.upperValue.value 
        assert not p.defaultValue or p.defaultValue.value is None, p.defaultValue.value 
        p.unlink()
        a.unlink()

    def test_parse_property_7(self):
        a = factory.create(Association)
        p = factory.create(Property)
        p.association = a
        parse_property(p, '''0..2 { tag1,
        tag2}''')
        #assert p.visibility == 'protected', p.visibility
        assert p.name is None, p.name
        assert not p.typeValue or p.typeValue.value is None, p.typeValue.value 
        assert p.lowerValue.value == '0', p.lowerValue.value 
        assert p.upperValue.value == '2', p.upperValue.value 
        assert not p.defaultValue or p.defaultValue.value is None, p.defaultValue.value 
        p.unlink()
        a.unlink()

    def test_parse_property_8(self):
        a = factory.create(Association)
        p = factory.create(Property)
        p.association = a
        parse_property(p, '-/end[*] { mytag}')
        assert p.visibility == 'private', p.visibility
        assert p.isDerived is True
        assert p.name == 'end', p.name
        assert not p.typeValue or p.typeValue.value is None, p.typeValue.value 
        assert not p.lowerValue or p.lowerValue.value is None, p.lowerValue.value 
        assert p.upperValue.value == '*', p.upperValue.value 
        assert not p.defaultValue or p.defaultValue.value is None, p.defaultValue.value 
        p.unlink()

        a.unlink()


class OperationTestCase(unittest.TestCase):

    def setUp(self):
        factory.flush()

    def tearDown(self):
        factory.flush()

    def test_parse_operation_1(self):
        o = factory.create(Operation)
        assert len(factory.values()) == 1

        # Very simple procedure:

        parse_operation(o, 'myfunc()')
        #assert o.visibility == 'protected'
        assert o.name == 'myfunc', o.name
        assert o.returnResult[0].typeValue.value is None, o.returnResult[0].typeValue.value
        assert not o.formalParameter, o.formalParameter
        # 1 operation, 1 parameter, 4 literal strings.
        assert len(factory.values()) == 5, len(factory.values())
        s = render_operation(o)
        #print render_operation(o)
        parse_operation(o, s)
        assert s == render_operation(o)

        # Procedure with return value:

        parse_operation(o, '+ myfunc(): myType')
        assert o.name == 'myfunc', o.name
        assert o.returnResult[0].typeValue.value == 'myType', o.returnResult[0].typeValue.value
        assert o.visibility == 'public'
        assert not o.formalParameter, o.formalParameter
        assert len(factory.values()) == 5, factory.values()
        s = render_operation(o)
        parse_operation(o, s)
        assert s == render_operation(o), render_operation(o)

    def test_parse_operation_2_params(self):
        # Change the operation to support two parameters:

        o = factory.create(Operation)
        parse_operation(o, '# myfunc2 (a: str, b: int = 3 {  static}): myType2')
        assert o.name == 'myfunc2', o.name
        assert o.returnResult[0].typeValue.value == 'myType2', o.returnResult[0].typeValue.value
        assert o.visibility == 'protected'
        assert len(o.formalParameter) == 2, o.formalParameter
        assert o.formalParameter[0].name == 'a', o.formalParameter[0].typeValue
        assert o.formalParameter[0].typeValue.value == 'str', o.formalParameter[0].typeValue.value
        assert o.formalParameter[0].defaultValue.value is None, o.formalParameter[0].defaultValue.value
        assert o.formalParameter[1].name == 'b', o.formalParameter[1].name
        assert o.formalParameter[1].typeValue.value == 'int', o.formalParameter[1].typeValue.value
        assert o.formalParameter[1].defaultValue.value == '3', o.formalParameter[1].defaultValue.value
        # 1 operation, 3 parameters, 4 + 5*2 literal strings
        assert len(factory.lselect(lambda e: isinstance(e, LiteralSpecification))) == 11, len(factory.lselect(lambda e: isinstance(e, LiteralSpecification)))
        assert len(factory.values()) == 15, len(factory.values())
        s = render_operation(o)
        parse_operation(o, s)
        assert s == render_operation(o)

        #print render_operation(o)

        # Change the operation to own one parameter:

        parse_operation(o, '- myfunc2 (a: node): myType2')
        assert o.name == 'myfunc2', o.name
        assert o.returnResult[0].typeValue.value == 'myType2', o.returnResult[0].typeValue.value
        assert o.visibility == 'private'
        assert len(o.formalParameter) == 1, o.formalParameter
        assert o.formalParameter[0].name == 'a', o.formalParameter[0].typeValue
        assert o.formalParameter[0].typeValue.value == 'node', o.formalParameter[0].typeValue.value
        assert o.formalParameter[0].defaultValue.value is None, o.formalParameter[0].defaultValue.value
        # 1 operation, 2 parameters, 4 + 5 literal strings
        assert len(factory.lselect(lambda e: isinstance(e, Operation))) == 1, len(factory.values())
        assert len(factory.lselect(lambda e: isinstance(e, Parameter))) == 2, len(factory.values())
        assert len(factory.lselect(lambda e: isinstance(e, LiteralSpecification))) == 7, len(factory.lselect(lambda e: isinstance(e, LiteralSpecification)))
        assert len(factory.values()) == 10, len(factory.values())
        #print render_operation(o)
        s = render_operation(o)
        parse_operation(o, s)
        assert s == render_operation(o)

        # Invalid syntax

        parse_operation(o, '- myfunc2: myType2')

        #print 'done'
