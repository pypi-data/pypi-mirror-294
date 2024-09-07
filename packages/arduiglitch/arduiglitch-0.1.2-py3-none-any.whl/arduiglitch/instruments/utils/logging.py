""""
Part of EM induced Arduino fault injection formation
Original author: Hugo PERRIN (h.perrin@emse.fr).
License: check the LICENSE file.
"""

from logging import Formatter
from blessed import Terminal


class CleanFormatter(Formatter):
    """
    A Formatter that removes ANSI color codes from the log messages.
    """

    def format(self, record):
        msg = super().format(record)
        msg = Terminal().strip_seqs(msg)
        return msg
