""" Module responsible for hosting all EVC imported from backend
or from YAML file. Any operation performed by evc_manager over an EVC
has to pass through this module to guarantee we have the right EVC. """

import re
from typing import Optional
from .cli import CliOptions
from .evc_to_dict import convert_class
from ..outputs.to_table import filter_per_nni
from ...libs.models.uni import UNI
from ...libs.models.evc import EthernetVirtualCircuit


class EvcsList(object):
    """List of EVCs"""

    def __init__(self, evc_list=None):
        """Init method"""
        self._evcs = list()
        if evc_list:
            self.evcs = evc_list

    @property
    def evcs(self):
        """Getter"""
        return self._evcs

    @evcs.setter
    def evcs(self, evc_list):
        """Setter"""
        # TODO: Validate input
        self._evcs = self.filter(evc_list)

    def to_dict(self):
        """Convert to self to dictionary"""
        return convert_class(self.evcs)

    def find(self, target_evc):
        """Return True if a specific EVC already exists"""
        for evc in self.evcs:
            if target_evc == evc:
                return evc
        return False

    @staticmethod
    def evc_list_after_nni_filter(nni_name, nni_type, evc_list):
        """Create the final list of EVCs after filtering per NNI
        Args:
            nni_name: NNI Name
            nni_type: type of NNI (any, primary, backup)
            evc_list: list of EVCs
        Returns:
            list of evcs
        """
        evcs_to_add = list()
        for evc in evc_list:
            if filter_per_nni(evc, target_nni=nni_name, filter_per_type=nni_type):
                evcs_to_add.append(evc)
        return evcs_to_add

    def has_nni_filters(self, evc_list):
        """Used to filter per NNI's name. NNI could be part of the primary, backup,
        or both paths.
        Args:
            evc_list: list of evcs
        Return:
            list of EVCs (original or filtered by NNI)
        """
        if not CliOptions().has_nni_filters:
            return evc_list

        if CliOptions().has_nni_name:
            # It doesn't matter if it is primary or backup
            return self.evc_list_after_nni_filter(CliOptions().has_nni_name, "any", evc_list)
        else:
            if CliOptions().has_nni_name_primary:
                evc_list = self.evc_list_after_nni_filter(
                    CliOptions().has_nni_name_primary, "primary", evc_list
                )

            if CliOptions().has_nni_name_backup:
                return self.evc_list_after_nni_filter(
                    CliOptions().has_nni_name_backup, "backup", evc_list
                )
            return evc_list

    def filter(self, evc_list):
        """Apply filters if any."""
        if CliOptions().has_evc_filters or CliOptions().has_partial_evc_filters:
            evc_list = self.filter_evc(evc_list)

        if not CliOptions().has_uni_filters and not CliOptions().has_nni_filters:
            return evc_list

        evcs = self.filter_unis(evc_list)
        return self.has_nni_filters(evcs)

    @staticmethod
    def filter_uni(
        uni: UNI,
        filter_uni_device: Optional[str],
        filter_uni_interface: Optional[str],
        filter_uni_tag_value: Optional[int],
        filter_uni_tag_values: Optional[list[int]],
    ) -> bool:
        """Apply UNI filters. All filters are applied per UNI to guarantee consistency.
        It works like this:
        if user hasn't provided a filter, consider it True
        if user has provided a filter, compare with the UNI's. If matches, consider it True
        otherwise, false.
        Args:
            uni: UNI class
            filter_uni_device: if --has-uni-device is provide, this is the value of it
            filter_uni_interface: if --has-uni-interface is provide, this is the value of it
            filter_uni_tag_value: if --has-uni-tag-value is provide, this is the value of it
        Return:
            bool
        """

        tag_value_verified = False
        interface_verified = False
        device_verified = False

        if filter_uni_device and uni.device == filter_uni_device:
            device_verified = True
        elif not filter_uni_device:
            device_verified = True

        if filter_uni_interface and uni.interface_name == filter_uni_interface:
            interface_verified = True
        elif not filter_uni_interface:
            interface_verified = True

        if uni.tag and filter_uni_tag_value and uni.tag.value == filter_uni_tag_value:
            tag_value_verified = True
        elif uni.tag and filter_uni_tag_values and uni.tag.value in filter_uni_tag_values:
            tag_value_verified = True
        elif uni.tag and not filter_uni_tag_value and not filter_uni_tag_values:
            tag_value_verified = True

        return tag_value_verified and interface_verified and device_verified

    def filter_unis(self, evc_list):
        """Loop to go through each UNI of each EVC.
        Args:
            evc_list: current valid list of EVCs
        Returns:
            final list of EVCs after all UNI filters are checked.
        """
        if not CliOptions().has_uni_filters:
            return evc_list

        evcs_to_add = list()
        for evc in evc_list:
            for uni in evc.unis:
                if self.filter_uni(
                    uni,
                    CliOptions().has_uni_device,
                    CliOptions().has_uni_interface,
                    CliOptions().has_uni_tag_value,
                    CliOptions().has_uni_tag_values,
                ):
                    evcs_to_add.append(evc)
                    break

        return evcs_to_add

    @staticmethod
    def filter_evc_has_name(evc, name):
        """Apply EVC name filter
        Args:
            evc: EVC object
            name: if --has-evc-name is provide, this is the value of it
        Return:
            bool
        """
        return evc.name == name

    @staticmethod
    def filter_evc_partially_has_name(evc: EthernetVirtualCircuit, pattern: str) -> bool:
        """
        Loop through the EVC list and use regex to find matches. It

        Args:
            evc: EthernetVirtualCircuit object
            name: A subsequence (such as vlan) that is provided after --has-evc-name. It can
                be a regular expression.
        """
        try:
            return re.search(pattern, evc.name) is not None
        except re.error as exc:
            raise ValueError(
                "Incorrect pattern usage.", "Must use either a simple string or regular expression"
            ) from exc
        except Exception as exc:
            raise ValueError("Unknown error.") from exc

    def filter_evc(self, evc_list):
        """Loop through the EVC list and apply specific filters.
        Args:
            evc_list: current valid list of EVCs
        Returns:
            final list of EVCs after all specific filters are applied.
        """
        if not CliOptions().has_evc_filters and not CliOptions().has_partial_evc_filters:
            return evc_list

        new_evc_list = list()

        if CliOptions().has_evc_filters:
            for evc in evc_list:
                if self.filter_evc_has_name(evc, CliOptions().has_evc_name):
                    new_evc_list.append(evc)

        else:
            for evc in evc_list:
                if self.filter_evc_partially_has_name(evc, CliOptions().has_partial_evc_name):
                    new_evc_list.append(evc)

        return new_evc_list
