#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
from pysmi.borrower.base import AbstractBorrower


class AnyFileBorrower(AbstractBorrower):
    """Create arbitrary MIB file borrowing object"""
