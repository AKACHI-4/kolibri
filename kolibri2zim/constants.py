#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import multiprocessing
import os
import pathlib

from zimscraperlib.logging import getLogger as lib_getLogger

ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name

with open(ROOT_DIR.joinpath("VERSION")) as fh:
    VERSION = fh.read().strip()

SCRAPER = f"{NAME} {VERSION}"

STUDIO_DEFAULT_BASE_URL = "https://studio.learningequality.org"
STUDIO_URL = os.getenv("STUDIO_URL", STUDIO_DEFAULT_BASE_URL)


def is_running_inside_container():
    fpath = pathlib.Path("/proc/self/cgroup")
    if not fpath.exists():
        return False
    try:
        with open(fpath) as fh:
            for line in fh.readlines():
                if line.strip().rsplit(":", 1)[-1] != "/":
                    return True
    finally:
        pass
    return False


class Global:
    debug = False
    inside_container = is_running_inside_container()
    nb_available_cpus: int


Global.nb_available_cpus = (
    1 if Global.inside_container else multiprocessing.cpu_count() - 1 or 1
)


def set_debug(debug):
    """toggle constants global DEBUG flag (used by getLogger)"""
    Global.debug = bool(debug)


def get_logger():
    """configured logger respecting DEBUG flag"""
    return lib_getLogger(NAME, level=logging.DEBUG if Global.debug else logging.INFO)
