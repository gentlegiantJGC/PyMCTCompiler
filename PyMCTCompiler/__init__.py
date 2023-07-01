from typing import Dict
import os
import time
from PyMCTCompiler import code_functions

from PyMCTCompiler.compilers.base_compiler import BaseCompiler

from PyMCTCompiler import version_compiler
from PyMCTCompiler.helpers import log_to_file
from PyMCTCompiler.disk_buffer import disk_buffer

compiled_dir = "./build"
path = os.path.dirname(__file__)


def build(compiled_dir_):
    global compiled_dir
    compiled_dir = compiled_dir_
    """Will remove all files from compiled_dir and generate them from uncompiled_dir"""
    t2 = time.time()

    # sort versions into order by version number
    versions: Dict[str, BaseCompiler] = {}

    vc_dir = os.path.join(os.path.dirname(__file__), "version_compiler")
    for version_name in os.listdir(vc_dir):
        if os.path.isdir(os.path.join(vc_dir, version_name)):
            if hasattr(version_compiler, version_name) and hasattr(
                getattr(version_compiler, version_name), "compiler"
            ):
                versions[version_name] = getattr(
                    version_compiler, version_name
                ).compiler
                versions[version_name].version_name = version_name
            else:
                log_to_file(
                    f"Could not find compiler for {version_name} This version has been skipped"
                )

    # iterate through all versions in the uncompiled directory
    for version_name, compiler in sorted(
        versions.items(),
        key=lambda x: (
            "" if x[1].platform == "universal" else x[1].platform,
            x[1].version,
        ),
    ):
        compiler: BaseCompiler
        log_to_file(f"Compiling {version_name} ...")
        t = time.time()
        compiler.build()
        log_to_file(f"\tFinished in {round(time.time() - t, 2)} seconds")

    code_functions.save(os.path.join(compiled_dir, "code_functions"))

    disk_buffer.save()

    try:
        with open(os.path.join(compiled_dir, "build_number.json")) as f:
            last_build_number = int(f.read())
    except:
        last_build_number = -1
    with open(os.path.join(compiled_dir, "build_number.json"), "w") as f:
        f.write(str(last_build_number + 1))

    log_to_file(f"\nFinished compiling all versions in {round(time.time() - t2, 2)}")
