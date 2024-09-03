#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
import sys
import textwrap

try:
    import unittest2 as unittest

except ImportError:
    import unittest

from pyasn1.compat.octets import str2octs
from pysmi.parser.smi import parserFactory
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.codegen.symtable import SymtableCodeGen
from pysnmp.smi.builder import MibBuilder


class ObjectTypeBasicTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "seconds"
        MAX-ACCESS      accessible-for-notify
        STATUS          current
        DESCRIPTION     "Test object"
        REFERENCE       "ABC"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSymbol(self):
        self.assertTrue("testObjectType" in self.ctx, "symbol not present")

    def testObjectTypeName(self):
        self.assertEqual(self.ctx["testObjectType"].getName(), (1, 3), "bad name")

    def testObjectTypeDescription(self):
        self.assertEqual(
            self.ctx["testObjectType"].getDescription(),
            "Test object",
            "bad DESCRIPTION",
        )

    def testObjectTypeStatus(self):
        self.assertEqual(
            self.ctx["testObjectType"].getStatus(), "current", "bad STATUS"
        )

    # TODO:revisit
    #    def testObjectTypeReference(self):
    #        self.assertEqual(
    #            self.ctx['testObjectType'].getReference(), str2octs('ABC'),
    #            'bad REFERENCE'
    #        )

    def testObjectTypeMaxAccess(self):
        self.assertEqual(
            self.ctx["testObjectType"].getMaxAccess(),
            "accessible-for-notify",
            "bad MAX-ACCESS",
        )

    def testObjectTypeUnits(self):
        self.assertEqual(self.ctx["testObjectType"].getUnits(), "seconds", "bad UNITS")

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(123), 123, "bad SYNTAX"
        )

    def testObjectTypeClass(self):
        self.assertEqual(
            self.ctx["testObjectType"].__class__.__name__, "MibScalar", "bad SYNTAX"
        )


class ObjectTypeHyphenTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    test-object-type OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "seconds"
        MAX-ACCESS      accessible-for-notify
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().genCode(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSymbol(self):
        self.assertTrue("test_object_type" in self.ctx, "symbol not present")

    def testObjectTypeLabel(self):
        self.assertEqual(
            self.ctx["test_object_type"].getLabel(), "test-object-type", "bad label"
        )


class ObjectTypeTextTestCase(unittest.TestCase):
    R"""
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        UNITS           "lines per
    text block"
        MAX-ACCESS      accessible-for-notify
        STATUS          current
        DESCRIPTION     "Test
                         object\n"
        REFERENCE       "ABC\"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        docstring = textwrap.dedent(self.__class__.__doc__)
        ast = parserFactory()().parse(docstring)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast,
            {mibInfo.name: symtable},
            genTexts=True,
            textFilter=lambda symbol, text: text,
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeDescription(self):
        self.assertEqual(
            self.ctx["testObjectType"].getDescription(),
            "Test\n                     object\\n",
            "bad DESCRIPTION",
        )

    def testObjectTypeReference(self):
        self.assertEqual(
            self.ctx["testObjectType"].getReference(), "ABC\\", "bad REFERENCE"
        )

    def testObjectTypeUnits(self):
        self.assertEqual(
            self.ctx["testObjectType"].getUnits(), "lines per\ntext block", "bad UNITS"
        )


class ObjectTypeIntegerDefaultTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Integer32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { 123456 }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(self.ctx["testObjectType"].getSyntax(), 123456, "bad DEFVAL")


class ObjectTypeIntegerDefaultZeroTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Integer32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Integer32
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { 0 }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(self.ctx["testObjectType"].getSyntax(), 0, "bad DEFVAL")


class ObjectTypeEnumDefaultTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          INTEGER  {
                            enable(1),
                            disable(2)
                        }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { enable }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(self.ctx["testObjectType"].getSyntax(), 1, "bad DEFVAL")


class ObjectTypeStringDefaultTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { "test value" }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    # TODO: pyasn1 does not like OctetString.defaultValue
    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(), str2octs("test value"), "bad DEFVAL"
        )


class ObjectTypeStringDefaultTextTestCase(unittest.TestCase):
    R"""
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { "\ntest
    value\" }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        docstring = textwrap.dedent(self.__class__.__doc__)
        ast = parserFactory()().parse(docstring)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(),
            str2octs("\\ntest\nvalue\\"),
            "bad DEFVAL",
        )


class ObjectTypeWithIntegerConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Unsigned32 (0..4294967295)
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(123),
            123,
            "bad integer range constrained SYNTAX",
        )


class ObjectTypeWithIntegerSetConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          Unsigned32 (0|2|44)
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(44),
            44,
            "bad multiple integer constrained SYNTAX",
        )


class ObjectTypeWithStringSizeConstraintTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          OCTET STRING (SIZE (0..512))
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(""),
            str2octs(""),
            "bad size constrained SYNTAX",
        )


class ObjectTypeBitsTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE,
      Unsigned32
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          BITS { notification(0), set(1) }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax().clone(("set",)),
            str2octs("@"),
            "bad BITS SYNTAX",
        )


class ObjectTypeBitsDefaultTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          BITS { present(0), absent(1), changed(2) }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { { present, absent } }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(),
            bytes((0xC0,)),
            "bad DEFVAL",
        )


class ObjectTypeBitsDefaultMultiOctetTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          BITS { a(0), b(1), c(2), d(3), e(4), f(5), g(6), h(7), i(8), j(9), k(10), l(11), m(12), n(13), o(14), p(15), q(16) }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { { b, c, m } }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(),
            bytes((0x60, 0x08)),
            "bad DEFVAL",
        )


class ObjectTypeBitsDefaultEmptySetTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          BITS { present(0), absent(1), changed(2) }
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { { } }
     ::= { 1 3 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(),
            bytes((0x00,)),
            "bad DEFVAL",
        )


class ObjectTypeObjectIdentifierTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testTargetObjectType OBJECT-TYPE
        SYNTAX          Integer32
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test target object"
     ::= { 1 3 }

    testObjectType OBJECT-TYPE
        SYNTAX          OBJECT IDENTIFIER
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { testTargetObjectType }
     ::= { 1 4 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeSyntax(self):
        self.assertEqual(
            self.ctx["testObjectType"].getSyntax(),
            (1, 3),
            "bad DEFVAL",
        )


class ObjectTypeObjectIdentifierInvalidTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

    testObjectType OBJECT-TYPE
        SYNTAX          OBJECT IDENTIFIER
        MAX-ACCESS      read-only
        STATUS          current
        DESCRIPTION     "Test object"
        DEFVAL          { { 0 0 } }
     ::= { 1 3 }

    END
    """

    def testObjectTypeSyntax(self):
        # The "{{0 0}}" type notation is invalid and currently not supported.
        # This test verifies that such notations can be parsed at all, which
        # is why the parsing is part of the actual test, and why successful
        # instantiation of the syntax is enough here.
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

        self.ctx["testObjectType"].getSyntax()


class ObjectTypeMibTableTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER,
            testValue   OCTET STRING
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testValue OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 2 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )

    def testObjectTypeTableColumnClass(self):
        self.assertEqual(
            self.ctx["testIndex"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"),),
            "bad table index",
        )


class ObjectTypeMibTableImpliedIndexTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { IMPLIED testIndex }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((1, "TEST-MIB", "testIndex"),),
            "bad IMPLIED table index",
        )


class ObjectTypeMibTableMultipleIndicesTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex, testValue }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER,
            testValue   OCTET STRING
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testValue OBJECT-TYPE
        SYNTAX          OCTET STRING
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 2 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"), (0, "TEST-MIB", "testValue")),
            "bad multiple table indices",
        )


class ObjectTypeAurmentingMibTableTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 3 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

      testTableExt OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntryExt
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 4 }

      testEntryExt OBJECT-TYPE
        SYNTAX          TestEntryExt
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        AUGMENTS        { testEntry }
      ::= { testTableExt 3 }

      TestEntryExt ::= SEQUENCE {
            testIndexExt   INTEGER
      }

      testIndexExt OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntryExt 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableRowAugmention(self):
        # TODO: provide getAugmentation() method
        try:
            augmentingRows = self.ctx["testEntry"].augmentingRows

        except AttributeError:
            augmentingRows = self.ctx["testEntry"]._augmentingRows

        self.assertEqual(
            list(augmentingRows)[0],
            ("TEST-MIB", "testEntryExt"),
            "bad AUGMENTS table clause",
        )


# This case verifies that pysmi provides leniency for a type name mismatch in
# "SEQUENCE OF" syntaxes for conceptual-table object types, as long as the
# corresponding table entry object type is correct.
class ObjectTypeMibTableMismatchedSequenceOfTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TypoEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          Test-Entry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      Test-Entry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().genCode(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )

    def testObjectTypeTableColumnClass(self):
        self.assertEqual(
            self.ctx["testIndex"].__class__.__name__,
            "MibTableColumn",
            "bad table column class",
        )

    def testObjectTypeTableRowIndex(self):
        self.assertEqual(
            self.ctx["testEntry"].getIndexNames(),
            ((0, "TEST-MIB", "testIndex"),),
            "bad table index",
        )


class ObjectTypeMibTableAndColumnTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI;

      Overview ::= SEQUENCE {
            testTable   TestEntry
      }

      testTable OBJECT-TYPE
        SYNTAX          SEQUENCE OF TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test table"
      ::= { 1 3 }

      testEntry OBJECT-TYPE
        SYNTAX          TestEntry
        MAX-ACCESS      not-accessible
        STATUS          current
        DESCRIPTION     "Test row"
        INDEX           { testIndex }
      ::= { testTable 1 }

      TestEntry ::= SEQUENCE {
            testIndex   INTEGER
      }

      testIndex OBJECT-TYPE
        SYNTAX          INTEGER
        MAX-ACCESS      read-create
        STATUS          current
        DESCRIPTION     "Test column"
      ::= { testEntry 1 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().genCode(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeTableClass(self):
        self.assertEqual(
            self.ctx["testTable"].__class__.__name__, "MibTable", "bad table class"
        )

    def testObjectTypeTableRowClass(self):
        self.assertEqual(
            self.ctx["testEntry"].__class__.__name__,
            "MibTableRow",
            "bad table row class",
        )


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
