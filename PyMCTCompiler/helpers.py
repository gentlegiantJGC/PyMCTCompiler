import glob
import os
import shutil
import subprocess
from typing import Union, List
from urllib.request import urlopen
import json
import amulet_nbt

log_file = open("log.txt", "w")


def load_json_file(path: str) -> Union[dict, list]:
    """Loads and returns the data from the file at prefix/path if it is a json file."""
    with open(path) as f:
        return json.load(f)


def log_to_file(msg: str):
    """Will log the message to the console and the log file.

    :param msg: The message to log
    :type msg: str
    """
    print(msg)
    log_file.write(f"{msg}\n")


def verify_snbt(val):
    nbt_val = amulet_nbt.from_snbt(val)
    if isinstance(nbt_val, amulet_nbt.TAG_String):
        assert val[0] == val[-1] == '"', f"TAG_String {val} not in the strict format"
    elif isinstance(nbt_val, (amulet_nbt.TAG_Compound, amulet_nbt.TAG_List)):
        raise Exception("This function does not work with nested data types")


def verify_string(val):
    assert '"' not in val, f'" character found in {val}'


def check_specification_format(data: dict):
    assert isinstance(data, dict), "Specification must be a dictionary"
    properties = data.get("properties", {})
    defaults = data.get("defaults", {})
    assert isinstance(properties, dict), '"properties" must be a dictionary'
    assert isinstance(defaults, dict), '"defaults" must be a dictionary'
    assert sorted(properties.keys()) == sorted(
        defaults.keys()
    ), 'The keys in "properties" and "defaults" must match'

    for key, val in properties.items():
        assert isinstance(key, str), "Property names must be strings"
        verify_string(key)
        assert isinstance(val, list), "Property options must be a list of strings"
        assert all(
            isinstance(prop, str) for prop in val
        ), "All property options must be strings"
        remove_list_duplicates(val)
        assert isinstance(
            defaults[key], str
        ), "All default property values must be strings"
        assert (
            defaults[key] in val
        ), f"Default property value ({defaults[key]}) must be in the property list ({val})"
        for val_ in val:
            verify_snbt(val_)  # verify that the snbt is valid

    if "snbt" in data:
        assert isinstance(data["snbt"], str), 'Specification "snbt" must be a string'
        while "\n\t" in data["snbt"] or "\n " in data["snbt"]:
            data["snbt"] = data["snbt"].replace("\n\t", "\n").replace("\n ", "\n")
        data["snbt"] = data["snbt"].replace("\n", "")
        try:
            amulet_nbt.from_snbt(data["snbt"])
        except:
            raise Exception(f'Error in snbt: {data["snbt"]}')
        assert (
            "nbt_identifier" in data
            and isinstance(data["nbt_identifier"], list)
            and len(data["nbt_identifier"]) == 2
            and all(isinstance(a, str) for a in data["nbt_identifier"])
        ), 'if "snbt" is defined then "nbt_identifier" must be defined and be [namespace, base_name]'
    else:
        assert (
            "nbt_identifier" not in data
        ), '"nbt_identifier" should only be defined if "snbt" is defined'

    for key in data.keys():
        if key not in ("properties", "defaults", "snbt", "nbt_identifier"):
            log_to_file(f'Extra key "{key}" found')


def unique_merge_lists(list_a: list, list_b: list) -> list:
    """Will return a list of the unique values from the two given lists.

    :param list_a: List of values
    :type list_a: list
    :param list_b: List of values
    :type list_b: list
    :return: List of unique entries from a and b
    """
    merged_list = []
    for entry in list_a + list_b:
        if entry not in merged_list:
            merged_list.append(entry)
    return merged_list


def sort_dict(d: dict) -> dict:
    """
    Sort a dictionary recursively based on its keys
    :param d: The dictionary to sort
    :return: The sorted dictionary
    """
    out = {}
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        out[k] = sort_dict(v) if isinstance(v, dict) else v
    return out


def remove_list_duplicates(val: list):
    # remove duplicates
    i = 0
    while len(val) > i:
        if val[:i].count(val[i]) >= 1:
            del val[i]
        else:
            i += 1


def find_java() -> str:
    """Find the path to java vm."""
    path = os.environ.get("JAVA_PATH", "")
    if not os.path.isfile(path):
        raise Exception("Could not find java")
    return path


def blocks_from_server(version_path: str, version_str: List[str] = None):
    if not os.path.isfile(f"{version_path}/generated/reports/blocks.json"):
        if not os.path.isfile(f"{version_path}/server.jar"):
            download_server_jar(f"{version_path}", version_str)
        # try and find a version of java with which to extract the blocks.json file

        # try the old command
        if subprocess.call(
            [
                find_java(),
                "-cp",
                f"{version_path}/server.jar",
                "net.minecraft.data.Main",
                "--reports",
                "--output",
                f"{version_path}/generated",
            ]
        ):
            # if that errors call the new command
            if subprocess.call(
                [
                    find_java(),
                    "-DbundlerMainClass=net.minecraft.data.Main",
                    "-jar",
                    f"{version_path}/server.jar",
                    "--reports",
                    "--output",
                    f"{version_path}/generated",
                ]
            ):
                raise Exception("Could not extract reports")


try:
    launcher_manifest = json.load(
        urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    )
except:
    launcher_manifest = None


def get_latest_server(path: str):
    if os.path.isfile(os.path.join(path, "latest")):
        with open(os.path.join(path, "latest")) as f:
            last_version = f.read()
    else:
        last_version = ""

    if launcher_manifest is None:
        print("Could not access the internet to check the newest version")
    else:
        new_version = launcher_manifest["latest"]["release"]
        if new_version != last_version:
            download_server_jar(path, new_version.split("."))
            with open(os.path.join(path, "latest"), "w") as f:
                f.write(new_version)
            if os.path.isdir(os.path.join(path, "generated")):
                shutil.rmtree(os.path.join(path, "generated"))


def download_server_jar(path: str, version_str: List[str] = None):
    if version_str is None:
        version_str = launcher_manifest["latest"]["release"].split(".")
    version_str = version_str + ["0"] * (4 - len(version_str))
    version = next(
        (
            v
            for v in launcher_manifest["versions"]
            if v["id"].split(".") + ["0"] * (4 - len(v["id"].split("."))) == version_str
        ),
        None,
    )
    if version is None:
        raise Exception(f'Could not find version "{version_str}"')
    version_manifest = json.load(urlopen(version["url"]))
    if "server" in version_manifest["downloads"]:
        print("\tDownloading server.jar")
        server = urlopen(version_manifest["downloads"]["server"]["url"]).read()
        with open(f"{path}/server.jar", "wb") as f:
            f.write(server)
    else:
        raise Exception(f'Could not find server for version "{version_str}"')
