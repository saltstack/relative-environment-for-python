"""
The ``relenv build`` command.
"""
from . import linux, darwin, windows

from ..common import host_arch, python_version

import sys


def platform_module():
    if sys.platform == "darwin":
        return darwin
    elif sys.platform == "linux":
        return linux
    elif sys.platform == "win32":
        return windows


def setup_parser(subparsers):
    """
    Setup the subparser for the ``build`` command.

    :param subparsers: The subparsers object returned from ``add_subparsers``
    :type subparsers: argparse._SubParsersAction
    """
    mod = platform_module()
    build_subparser = subparsers.add_parser(
        "build", description="Build Relenv Python Environments from source"
    )
    build_subparser.set_defaults(func=main)
    build_subparser.add_argument(
        "--arch",
        default=host_arch(),
        choices=mod.ARCHES,
        type=str,
        help="The host architecture [default: %(default)s]",
    )
    build_subparser.add_argument(
        "--version",
        default=python_version(),
        type=str,
        help="The version of python to build [default: %(default)s]",
    )
    build_subparser.add_argument(
        "--clean",
        default=False,
        action="store_true",
        help=(
            "Clean up before running the build. This option will remove the "
            "logs, src, build, and previous tarball."
        ),
    )
    build_subparser.add_argument(
        "--no-cleanup",
        default=False,
        action="store_true",
        help=(
            "By default the build directory is removed after the build "
            "tarball is created. Setting this option will leave the build "
            "directory in place."
        ),
    )
    # XXX We should automatically skip downloads that can be verified as not
    # being corrupt and this can become --force-download
    build_subparser.add_argument(
        "--no-download",
        default=False,
        action="store_true",
        help="Skip downloading source tarballs",
    )
    build_subparser.add_argument(
        "--step",
        dest="steps",
        metavar="STEP",
        action="append",
        default=[],
        help=(
            "A step to run alone, can use multiple of this argument. When this option is used to "
            "invoke builds, depenencies of the steps are ignored.  This option "
            "should be used with care, as it's easy to request a situation that "
            "has no chance of being succesful. "
        ),
    )


def main(args):
    """
    The entrypoint to the ``build`` command.

    :param args: The arguments to the command
    :type args: ``argparse.Namespace``
    """
    mod = platform_module()
    if not mod:
        print("Unsupported platform")
        sys.exit(1)
    mod.main(args)
