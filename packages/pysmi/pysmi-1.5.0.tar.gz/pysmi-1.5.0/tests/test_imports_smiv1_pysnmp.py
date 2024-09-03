#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof; Copyright 2022-2024, others
# License: https://www.pysnmp.com/pysmi/license.html
#
import sys

try:
    import unittest2 as unittest

except ImportError:
    import unittest

from pysmi.parser.smi import parserFactory
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.codegen.symtable import SymtableCodeGen
from pysnmp.smi.builder import MibBuilder


class ImportConversionTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    -- Import one from each conversion category. Note that we cannot test that
    -- the imports "internet", "snmp", and "nullSpecific" can also be used, as
    -- that requires actually parsing SNMPv2-SMI.
    IMPORTS
      internet
        FROM RFC1065-SMI
      Gauge
        FROM RFC1155-SMI
      snmp, nullSpecific
        FROM RFC1158-MIB
      DisplayString, PhysAddress
        FROM RFC1213-MIB
      OBJECT-TYPE
        FROM RFC-1212
      TRAP-TYPE
        FROM RFC-1215;

    testObjectType1 OBJECT-TYPE
        SYNTAX          Gauge
        ACCESS          read-only
        STATUS          mandatory
        DESCRIPTION     "Test object"
      ::= { 1 3 }

    testObjectType2 OBJECT-TYPE
        SYNTAX          DisplayString
        ACCESS          read-only
        STATUS          mandatory
        DESCRIPTION     "Test object"
      ::= { 1 4 }

    testObjectType3 OBJECT-TYPE
        SYNTAX          PhysAddress
        ACCESS          read-only
        STATUS          mandatory
        DESCRIPTION     "Test object"
      ::= { 1 5 }

    trapBase OBJECT IDENTIFIER ::= { 1 6 }

    testTrap TRAP-TYPE
        ENTERPRISE      trapBase
      ::= 2

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

    def testImportedSymbol1(self):
        self.assertTrue("internet" in self.ctx, "imported symbol not present")

    def testImportedSymbol2(self):
        self.assertTrue("Gauge32" in self.ctx, "imported symbol not present")

    def testImportedSymbol3(self):
        self.assertTrue("snmp" in self.ctx, "imported symbol not present")

    def testImportedSymbol4(self):
        self.assertTrue("zeroDotZero" in self.ctx, "imported symbol not present")

    def testImportedSymbol5(self):
        self.assertTrue("DisplayString" in self.ctx, "imported symbol not present")

    def testImportedSymbol6(self):
        self.assertTrue("PhysAddress" in self.ctx, "imported symbol not present")

    def testObjectTypeSyntax1(self):
        self.assertEqual(
            self.ctx["testObjectType1"].getSyntax().__class__.__name__,
            "Gauge32",
            "bad syntax",
        )

    def testObjectTypeSyntax2(self):
        self.assertEqual(
            self.ctx["testObjectType2"].getSyntax().__class__.__name__,
            "DisplayString",
            "bad syntax",
        )

    def testObjectTypeSyntax3(self):
        self.assertEqual(
            self.ctx["testObjectType3"].getSyntax().__class__.__name__,
            "PhysAddress",
            "bad syntax",
        )

    def testTrapTypeName(self):
        self.assertEqual(self.ctx["testTrap"].getName(), (1, 6, 0, 2), "bad name")


class ImportAbsentTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN

    TestType ::= INTEGER

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().genCode(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().genCode(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testTypeClass(self):
        self.assertEqual(
            self.ctx["TestType"].__bases__[0].__name__,
            "Integer32",
            "bad type",
        )


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
