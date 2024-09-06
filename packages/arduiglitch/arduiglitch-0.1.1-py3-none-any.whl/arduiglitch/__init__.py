"""
This is an entry point script that runs the main menu of the program.
"""

import sys
from argparse import ArgumentParser
from logging import Logger
from blessed import Terminal
import logging
from .term.synchronization import synchronized
from .term.inputter import Inputter
from .term.selectable import Selectable
from .term.selectable_menu import SelectableMenu
from .term.tab_menu import TabMenu
from .term.tab_text import TabText
from .term.tab_log import TabLog
from .experiment.target_gui import TargetGUI
from .experiment.glitcher_gui import GlitcherGUI
from .experiment.pfa_campaign import PfaCampaign
from .guis import basic_gui, cmds_base, cmds_base_campaigns
from instruments.utils.logging import CleanFormatter


def test(args):
    # Initialize logging
    level = logging.DEBUG if args.verbose else logging.INFO
    log = logging.getLogger("__main__")
    log.setLevel(level)
    # Create file log handler
    logf = logging.FileHandler("sandbox.log")
    logf.setLevel(logging.DEBUG)
    logf.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s",
                          "%H:%M:%S"))
    log.addHandler(logf)
    # Create clean log file handler
    logf_clean = logging.FileHandler("sandbox_clean.log")
    logf_clean.setLevel(logging.DEBUG)
    logf_clean.setFormatter(
        CleanFormatter("%(asctime)s | %(levelname)s | %(message)s",
                       "%H:%M:%S"))
    log.addHandler(logf_clean)

    # Initialize terminal
    term = Terminal()

    if args.verbose:
        log.debug(term.green("Verbose mode enabled by user."))

    # Clear screen
    with synchronized(term):
        print(term.home + term.clear + term.move_y(term.height // 2))

    # Create Arduino target connection
    target = TargetGUI(log, args.target_port, 38400, timeout_s=1.0)
    glitcher = GlitcherGUI(log, args.glitcher_port, 9600, 1.0, 100, target)

    # Create PFA campaign (needs to save data between multiple callbacks)
    #pfa_campaign = PfaCampaign(log,
    #                           glitcher,
    #                           target,
    #                           "./static/data/data.csv",
    #                           batch_size=20)

    # Initialize interface

    # Add user input box
    inputter = Inputter((0, 27), width=50)
    inputter.render(term)

    menu, _ = basic_gui(log, term, cmds_base(term, glitcher, target, inputter),
                        inputter)

    # Main loop
    menu.main_loop(term)

    # Clear screen before exiting
    with synchronized(term):
        print(term.home + term.clear + term.move_y(term.height // 2))

    target.close_instrument()
    glitcher.close_instrument()


def campaigns(args):
    # Initialize logging
    level = logging.DEBUG if args.verbose else logging.INFO
    log = logging.getLogger("__main__")
    log.setLevel(level)
    # Create file log handler
    logf = logging.FileHandler("sandbox.log")
    logf.setLevel(logging.DEBUG)
    logf.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s",
                          "%H:%M:%S"))
    log.addHandler(logf)
    # Create clean log file handler
    logf_clean = logging.FileHandler("sandbox_clean.log")
    logf_clean.setLevel(logging.DEBUG)
    logf_clean.setFormatter(
        CleanFormatter("%(asctime)s | %(levelname)s | %(message)s",
                       "%H:%M:%S"))
    log.addHandler(logf_clean)

    # Initialize terminal
    term = Terminal()

    if args.verbose:
        log.debug(term.green("Verbose mode enabled by user."))

    # Clear screen
    with synchronized(term):
        print(term.home + term.clear + term.move_y(term.height // 2))

    # Create Arduino target connection
    target = TargetGUI(log, args.target_port, 38400, timeout_s=1.0)
    glitcher = GlitcherGUI(log, args.glitcher_port, 9600, 1.0, 100, target)

    # Initialize interface

    # Add user input box
    inputter = Inputter((0, 27), width=50)
    inputter.render(term)

    menu, _ = basic_gui(log, term,
                        cmds_base_campaigns(term, glitcher, target, inputter),
                        inputter)

    # Main loop
    menu.main_loop(term)

    # Clear screen before exiting
    with synchronized(term):
        print(term.home + term.clear + term.move_y(term.height // 2))

    target.close_instrument()
    glitcher.close_instrument()


def main():
    # Parse terminal user arguments
    parser_main = ArgumentParser(
        prog="Arduiglitch",
        description=
        "This is the entry point script that runs the main menu of the program",
    )
    parser_main.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Shows debug level logs in the terminal.",
    )
    parser_main.add_argument(
        "-t",
        "--target-port",
        action="store",
        type=str,
        help=
        "Serial com port or url for the target board (ie. `/dev/ttyACM0` or `COM1`)",
        required=True,
    )
    parser_main.add_argument(
        "-g",
        "--glitcher-port",
        action="store",
        type=str,
        help=
        "Serial com port or url for the attacker board (ie. `/dev/ttyACM0` or `COM1`)",
        required=True,
    )
    subparsers = parser_main.add_subparsers(required=True)

    parser_test = subparsers.add_parser("test")
    parser_test.set_defaults(func=test)

    parser_campaigns = subparsers.add_parser("campaigns")
    parser_campaigns.set_defaults(func=campaigns)

    parser_main_args = parser_main.parse_args()
    parser_main_args.func(parser_main_args)
