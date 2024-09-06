""" YAML module. Used to read and write in YAML format """

from datetime import datetime
from yaml import dump
import yaml
from ..core.cli import CliOptions


class MyDumper(yaml.Dumper):  # pylint: disable=R0901
    """Ignore aliases when printing dictionaries using YAML"""

    def ignore_aliases(self, _data):  # pylint: disable=W0221,W0237
        """overriding method to return always true."""
        return True


def minimize_paths(paths: list[list[dict[str, object]]]) -> list[list[str]]:
    """
    Exports the minimal set of attribute for paths:

    - "name"
        - To remove "name: ..." from the output, the dict had to be removed and instead
        the "name" attribute was appended to a new list.
    """
    new_paths = []

    for path in paths:
        minimized_path = []
        for link in path:
            minimized_path.append(link["name"])
        new_paths.append(minimized_path)

    return new_paths


def minimize_unis(unis: list[dict[str, object]]) -> list[dict[str, object]]:
    """Export just the minimal set of attributes for UNIs:
    device
    interface_name
    tag:
        value
    """
    new_unis = list()
    for uni in unis:
        new_uni = dict()
        new_uni["device"] = uni["device"]
        new_uni["interface_name"] = uni["interface_name"]
        if uni["tag"]:
            new_uni["tag"] = uni["tag"].copy()
        new_unis.append(new_uni)
        del new_uni
    return new_unis


def minimize(ctks: list[dict[object, object]]) -> list[dict[object, object]]:
    """Export just the minimal set of attributes:
    name,
    unis:
        device
        interface_name
        tag:
            value
    """
    new_ctks = list()

    for ctk in ctks:
        evc_copy = dict()
        evc_copy["name"] = ctk["name"]
        evc_copy["unis"] = minimize_unis(ctk["unis"])
        evc_copy["paths"] = minimize_paths(ctk["paths"])
        new_ctks.append(evc_copy)
        del evc_copy
    return new_ctks


def print_yaml(ctks):
    """Exported function to print in YAML"""
    print(f"Number of Circuits: {len(ctks)}")

    if CliOptions().output_format == "yaml_minimal":
        ctks = minimize(ctks)

    evcs = dict()
    evcs["evcs"] = ctks
    evcs["version"] = "1.0"

    now = datetime.now()
    now.strftime("%Y/%m/%d %H:%M:%S")
    evcs["date"] = now

    with open(CliOptions().destination_file, "w") as yaml_file:
        dump(evcs, yaml_file, default_flow_style=False, Dumper=MyDumper)
        print(f"List of circuits saved on file: {CliOptions().destination_file}")
