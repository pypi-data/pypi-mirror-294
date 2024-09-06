""" OESS backend module. """

import sys
import time
import copy
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # pylint: disable=E1101
from ..libs.core.cli import CliOptions
from ..libs.core.log import info
from ..libs.core.log import warn
from ..libs.core.log import debug
from ..libs.models.evc import EthernetVirtualCircuit
from ..libs.models.nni import NNI
from ..libs.models.uni import UNI
from ..libs.models.metrics import Metrics
from ..libs.models.current_config import CurrentConfig
from ..libs.models.mac_address import MacAddress
from .generic_backend import Backend


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # pylint: disable=E1101


class Oess(Backend):
    """OESS backend class."""

    get_existing_circuits = "services/data.cgi?action=get_existing_circuits"
    get_workgroups = "services/data.cgi?action=get_workgroups"
    get_nodes = "services/data.cgi?action=get_nodes"
    get_device_interfaces = "services/data.cgi?action=get_node_interfaces"
    query_vlan_availability = "services/data.cgi?action=is_vlan_tag_available"
    get_path = "services/data.cgi?action=get_shortest_path"
    provision_circuit = "services/provisioning.cgi?action=provision_circuit"
    remove_circuit = "services/provisioning.cgi?action=remove_circuit"

    def authenticate(self):
        """

        :param: use_input_file: if provided, operates offline
        """
        self.user = CliOptions().user  # pylint: disable=W0201
        self.password = CliOptions().password  # pylint: disable=W0201
        self.url = CliOptions().backend_url  # pylint: disable=W0201
        self.tenant = CliOptions().tenant  # pylint: disable=W0201
        self.tenant_id = None  # pylint: disable=W0201
        self._send_get()
        self.get_workgroup()

    def _send_get(self, query=None, payload=None):
        """Send HTTP Request to OESS"""
        if CliOptions().verbose in ["warning", "debug"]:
            return self._send_get_final(query, payload)
        else:
            try:
                return self._send_get_final(query, payload)
            except requests.exceptions.ConnectTimeout as error:
                info(error)
                sys.exit(1)  # Error Code 1 - Connection Timeout.
            except Exception as error:  # pylint: disable=W0703
                info(error)
                sys.exit(2)  # Error Code 2 - Unknown

    def _send_get_final(self, query=None, payload=None):
        """Send HTTP Request to OESS"""

        if not self.session_request:  # pylint: disable=E0203
            # Confirm if authenticated
            self.session_request = requests.Session()  # pylint: disable=W0201
            self.session_request.auth = (self.user, self.password)
            debug(f"URL: {self.url}")
            try:
                request = self.session_request.get(self.url, verify=False, timeout=4)

            except requests.exceptions.ConnectTimeout as exc:
                msg = "ERROR: Not possible to connect to OESS. "
                msg += "Confirm OESS is running."
                raise requests.exceptions.ConnectTimeout(msg) from exc

            except Exception as error:
                raise RuntimeError(error) from error

            debug(f"Query result is {request}")
            if request.status_code == 200:
                return True
            else:
                raise RuntimeError("Error: OESS Authentication Failed!")

        url = self.url + query
        if payload is not None:
            url_ext = ""
            for item in payload:
                url_ext = url_ext + "&" + item + "=" + payload[item]
            url = url + url_ext

        # Try 3 times in case of errors.
        attempt = 0
        while attempt < 4:
            attempt += 1
            error_found = False
            debug(f"URL: {url}")
            request = self.session_request.get(url, verify=False)

            if request.status_code != 200:
                error_found = True
                debug(f"Error Code: {request.status_code}")
                if attempt == 4:
                    raise RuntimeError(f"Error on query: {url}\nStatus Code: {request.status_code}")

            else:
                results = json.loads(request.text)
                debug(f"Query result is {results}")

                if "error" in results:
                    if "path does not connect all endpoints" in results["error"]:
                        return results

                    error_found = True
                    debug(f'Error found: %{results["error"]}')
                    if attempt == 4:
                        if "results" in results and len(results["results"]):
                            info(f'Error: Query result is {results["results"]}')
                        raise RuntimeError(results["error"])

                if "results" not in results:
                    error_found = True
                    debug("Error found. 'results' not found in the reply")
                    if attempt == 4:
                        raise RuntimeError(results)

            if error_found:
                info("Error received. Requesting it again.")
                time.sleep(5)
            else:
                return results["results"]

    def get_evcs(self):
        """Returns a list of all EVCs"""
        query = self.get_existing_circuits
        payload = {"workgroup_id": self.tenant_id}

        return self.process_oess_circuits(self._send_get(query, payload))

    def get_workgroup(self):
        """Get OESS's workgroup/tenant ID using the name provided"""
        query = self.get_workgroups
        groups = self._send_get(query)

        for group in groups:
            if group["name"] == self.tenant:
                self.tenant_id = group["workgroup_id"]  # pylint: disable=W0201

        if not self.tenant_id:
            print("ERROR: OESS workgroup not found!")
            sys.exit(3)

    @staticmethod
    def get_unis(endpoints):
        """

        :param endpoints:
        :return:
        """
        unis = list()
        for endpoint in endpoints:
            uni = UNI()
            uni.device = endpoint["node"]
            uni.interface_name = endpoint["interface"]
            uni.interface_description = endpoint["interface_description"]
            uni.tag.type = "vlan"
            uni.tag.value = endpoint["tag"]
            for mac_addr in endpoint["mac_addrs"]:
                uni.mac_addresses.append(MacAddress(mac_addr["mac_address"]))
            unis.append(copy.deepcopy(uni))
            del uni
        return unis

    @staticmethod
    def process_link(links):
        """

        :param links:
        :return:
        """
        path = list()
        for span in links:
            link = NNI()
            link.device_a = span["node_a"]
            link.interface_a = span["interface_a"]
            link.device_z = span["node_z"]
            link.interface_z = span["interface_z"]
            link.name = span["name"]
            path.append(link)
            del link
        return path

    def get_requested_paths(self, circuit):
        """

        :param circuit:
        :return:
        """
        requested_paths = list()
        requested_paths.append(self.process_link(circuit["links"]))
        if len(circuit["backup_links"]) > 0:
            requested_paths.append(self.process_link(circuit["backup_links"]))
        return requested_paths

    @staticmethod
    def get_metrics(bandwidth):
        """

        :param bandwidth:
        :return:
        """
        metrics = Metrics()
        metrics.min_bw = bandwidth
        return metrics

    @staticmethod
    def is_up(circuit):
        """

        :param circuit:
        :return:
        """
        if circuit["operational_state"] == "up":
            return True
        return False

    def get_current_config(self, oess_circuit, evc):
        """

        :param oess_circuit:
        :param evc
        :return:
        """
        current_config = CurrentConfig()
        current_config.backend = "oess"
        current_config.backend_evc_id = oess_circuit["circuit_id"]
        current_config.is_active = oess_circuit["state"]
        current_config.is_optimized = True
        current_config.is_up = self.is_up(oess_circuit)

        if oess_circuit["active_path"] == "primary":
            current_config.current_path = evc.paths[0]
        else:
            current_config.is_backup = True
            current_config.current_path = evc.paths[1]
        return current_config

    @staticmethod
    def get_time_timestamp(circuit, action="created_on"):
        """

        :param circuit:
        :param action:
        :return:
        """
        p_time = circuit[action] if action in circuit else 0
        if isinstance(p_time, str):
            oess_pattern = "%m/%d/%Y %H:%M:%S"
            p_time = int(time.mktime(time.strptime(p_time, oess_pattern)))
        return p_time

    @staticmethod
    def get_external_identifier(oess_circuit):
        """

        :param oess_circuit:
        :return:
        """
        idx = "external_identifier"
        ext_id = oess_circuit[idx] if idx in oess_circuit else 0
        if not ext_id:
            return 0
        return ext_id

    def process_oess_circuits(self, oess_circuits):
        """

        :param oess_circuits:
        """
        evcs = list()
        for oess_circuit in oess_circuits:
            evcs.append(copy.deepcopy(self.process_oess_circuit(oess_circuit)))

        return evcs

    def process_oess_circuit(self, circuit):
        """

        :param circuit:
        :return:
        """
        evc = EthernetVirtualCircuit()
        evc.name = circuit["description"]
        evc.unis = self.get_unis(circuit["endpoints"])
        evc.paths = self.get_requested_paths(circuit)
        evc.provisioning_time = self.get_time_timestamp(circuit)
        evc.decommissioning_time = 0
        evc.tenant = circuit["workgroup"]["name"]
        evc.metrics = self.get_metrics(circuit["bandwidth"])
        evc.external_id = self.get_external_identifier(circuit)
        evc.current_config = self.get_current_config(circuit, evc)
        return evc

    def add_evc(self, new_evc, change=False):
        """Add or Update EVC based on the provided EVC(s) name(s)

        Args:
            new_evc: EVC class
            change: if it is an EVC change, avoid some evaluations.
        Returns:

        """
        primary_path = None
        backup_path = None
        need_backup = True

        msg = self.evaluate_nodes(new_evc)
        if msg["result"] == "error":
            info(f'Error: {msg["msg"]}')
            return msg

        msg = self.evaluate_unis(new_evc, change=True)
        if msg["result"] == "error":
            info(f'Error: {msg["msg"]}')
            return msg

        warn("Requesting Paths...")
        if new_evc.paths:

            if len(new_evc.paths) == 1:
                need_backup = False

            primary_path = self.oess_get_path(new_evc.unis, requested=new_evc.paths[0])

            if need_backup and primary_path and len(new_evc.paths) >= 2:
                backup_path = self.oess_get_path(new_evc.unis, requested=new_evc.paths[1])

        if not primary_path:
            primary_path = self.oess_get_path(new_evc.unis)

        if need_backup and not backup_path:
            backup_path = self.oess_get_path(new_evc.unis, primary=primary_path)

        debug(f"Primary Path: {primary_path}")
        if need_backup:
            debug(f"Backup Path: {backup_path}")
        else:
            debug("Not Backup Path requested")

        warn("Provisioning circuit...")

        if self.oess_provision_circuit(new_evc, primary_path, backup_path, change=change):
            msg = {"result": "created", "msg": f"EVC {new_evc.name} provisioned."}
            if change:
                msg["result"] = "changed"
            return msg

        return {"result": "error", "msg": f"Error provisioning EVC {new_evc.name}"}

    def evaluate_nodes(self, new_evc):
        """Evaluate if the OESS's switch is up. Otherwise, UNIs are not
        recognized."""

        for uni in new_evc.unis:
            debug("Evaluating each node provided")
            msg = self.oess_evaluate_device(uni.device)
            if msg["result"] == "error":
                return msg

        return {"result": "ok"}

    def evaluate_unis(self, new_evc, change=True):
        """Evaluate if the EVC's params are correct and if the VLANs
        are available.

        Args:
            new_evc: EVC class
        Returns:
            True if ok
            False if not ok
        """
        for uni in new_evc.unis:
            debug("Evaluating each UNI provided")
            msg = self.oess_evaluate_device_interfaces(uni)
            if msg["result"] == "error":
                msg["msg"] = f"{msg['msg']} in EVC {new_evc.name}"
                return msg

            debug("Verifying if VLANs provided are available")
            msg = self.oess_evaluate_vlans_availability(uni)
            if msg["result"] == "error" and not change:
                return msg

        return {"result": "ok"}

    def oess_evaluate_device(self, device):
        """Get existing and UP devices"""
        query = self.get_nodes
        devices = self._send_get(query)

        for found_device in devices:
            if found_device["name"] == device:
                if found_device["operational_state"] == "up":
                    if found_device["in_maint"] == "no":
                        return {"result": "ok"}
        msg = {"result": "error", "msg": f"Device {device} not found, DOWN or in maintenance"}
        return msg

    def oess_evaluate_device_interfaces(self, uni):
        """Get existing interfaces for device"""
        query = self.get_device_interfaces
        payload = {"node": uni.device, "show_down": "1", "show_trunk": "1"}
        device_interfaces = self._send_get(query, payload)

        for device_interface in device_interfaces:
            if device_interface["name"] == uni.interface_name:
                return {"result": "ok"}

        msg = {
            "result": "error",
            "msg": f"Incorrect UNI provided {uni.device}:{uni.interface_name}",
        }
        return msg

    def oess_evaluate_vlans_availability(self, uni):
        """Check if VLAN is available for device and interface provided"""
        query = self.query_vlan_availability
        payload = {"node": uni.device, "interface": uni.interface_name, "vlan": str(uni.tag.value)}
        if self._send_get(query, payload)[0]["available"] in [1]:
            return {"result": "ok"}

        msg = {
            "result": "error",
            "msg": f"VLAN {uni.tag.value} not available on device {uni.device}"
            + f" interface {uni.interface_name}",
        }
        return msg

    def oess_get_path(self, unis, requested=None, primary=None, exclude=None):
        """Process path"""
        query = self.get_path
        path = []

        for uni in unis:
            query += f"&node={uni.device}"

        # Requested is the user-defined FULL path.
        # If we use &link= it means exactly the opposite to OESS (exclude)
        if requested:
            # Expanded to support Blueprint EP005
            for link in requested:

                if isinstance(link, str):
                    # Coming from move_evc
                    path.append(link)

                elif link.name == "Empty":
                    # If link.name == "Empty", it means it is a dynamic path
                    return path

                elif link.name:
                    path.append(link.name)

            return path

        elif primary:
            for link in primary:
                query += f"&link={link}"

        elif exclude:
            if isinstance(exclude, str):
                query += f"&link={exclude}"
            elif isinstance(exclude, list):
                for link in exclude:
                    query += f"&link={link}"

        final_path = self._send_get(query)

        for link in final_path:
            path.append(link["link"])

        return path

    def oess_provision_circuit(self, new_evc, primary_path, backup_path, change=False):
        """Create OESS Provisioning Query"""
        query = self.provision_circuit
        query += f"&workgroup_id={self.tenant_id}"

        try:
            for uni in new_evc.unis:
                query += f"&node={uni.device}&interface={uni.interface_name}&tag={uni.tag.value}"

            for link in primary_path:
                query += f"&link={link}"

            if backup_path:
                for link in backup_path:
                    query += f"&backup_link={link}"

            if not new_evc.provisioning_time:
                query += "&provision_time=-1"
            else:
                query += f"&provision_time={new_evc.provisioning_time}"

            if not new_evc.decommissioning_time:
                query += "&remove_time=-1"
            else:
                query += f"&remove_time={new_evc.decommissioning_time}"

            query += f"&description={new_evc.name}"

            if change:
                query += f"&circuit_id={new_evc.current_config.backend_evc_id}"

            result = self._send_get(query)

            if "error" in result:
                warn(f"ERROR during provisioning of EVC {new_evc.name}: " + result["error"])
                return False

            if result["success"] == 1:
                return True

        except (KeyError, TypeError) as error:
            debug(f"ERROR during provisioning: {error}")
            return False

    def delete_evc(self, evc_to_delete):
        """Delete EVC with the provided EVC(s) name(s)"""
        info(f"Deleting EVC {evc_to_delete.name}:")
        for uni in evc_to_delete.unis:
            info(f"\tUNI device {uni.device}")
            info(f"\tUNI interface {uni.interface_name}")
            info(f"\tUNI vlan {uni.tag.value}")

        try:
            query = self.remove_circuit
            query += "&remove_time=-1"
            query += f"&workgroup_id={self.tenant_id}"
            query += f"&circuit_id={evc_to_delete.current_config.backend_evc_id}"

            result = self._send_get(query)

            if result[0]["success"] == 1:
                return {"result": "deleted", "msg": f"EVC {evc_to_delete.name} deleted."}

            return {"result": "error", "msg": f"EVC {evc_to_delete.name} NOT deleted."}

        except (KeyError, AttributeError, TypeError):
            return {"result": "error", "msg": f"EVC {evc_to_delete.name} NOT deleted."}

    def set_path(self, evc, primary=None, backup=None):
        """Prepare the EVC to move out of a NNI.
        Args:
            evc:
            primary:
            backup:
        Returns:
            self.add_evc
        """

        if primary:
            if isinstance(primary, str):
                primary = list(primary)
            evc.paths.append(primary)
        if backup:
            if isinstance(backup, str):
                backup = list(backup)
            evc.paths.append(backup)
        return self.add_evc(evc, change=True)

    def move_evc(self, evc_to_move, current_primary, current_backup, nni):
        """Move EVC out of a NNI. If the NNI is on the primary path,
        create a new primary without the NNI any request the backup without
        the NNI and the primary.

        Args:
            evc_to_move:
            current_primary:
            current_backup:
            nni:
        Returns:

        """
        current_primary = current_primary.split(" ")
        current_backup = current_backup.split(" ")

        if nni in current_primary:
            # Get a new path without the NNI
            new_primary_path = self.oess_get_path(evc_to_move.unis, exclude=nni)
            if nni in new_primary_path:
                return {
                    "result": "error",
                    "msg": f"EVC {evc_to_move.name}'s primary path NOT changed. No available path.",
                }

            if not current_backup:
                if "result" in self.set_path(evc_to_move, new_primary_path, []):
                    return {
                        "result": "moved",
                        "msg": f"EVC {evc_to_move.name}'s Primary path changed."
                        "No previous backup path existed.",
                    }

            elif current_backup:

                # Copies to create the backup path
                copy_of_new_primary_plus_nni = copy.deepcopy(new_primary_path)
                copy_of_new_primary_plus_nni.append(nni)

                new_backup_path = self.oess_get_path(
                    evc_to_move.unis, primary=copy_of_new_primary_plus_nni
                )

                if new_primary_path == new_backup_path or nni in new_backup_path:
                    debug(
                        "New suggested primary path equals backup path"
                        " or NNI is in the new backup path."
                    )
                    warn("  Changing Primary path. Backup Path won't be changed")
                    # Request OESS to change primary path only. Backup will remain the same.
                    if "result" in self.set_path(evc_to_move, new_primary_path, current_backup):
                        return {
                            "result": "moved",
                            "msg": f"EVC {evc_to_move.name}'s Primary path changed."
                            + " No Backup path available.",
                        }

                elif new_primary_path != new_backup_path and nni not in new_backup_path:
                    warn(f"Moving EVC {evc_to_move.name} out of NNI {nni}")
                    # Request OESS to change primary and backup paths.
                    if "result" in self.set_path(evc_to_move, new_primary_path, new_backup_path):
                        return {
                            "result": "moved",
                            "msg": f"EVC {evc_to_move.name}'s Primary and Backup paths changed.",
                        }

        elif nni in current_backup:

            copy_of_primary_plus_nni = copy.deepcopy(current_primary)
            copy_of_primary_plus_nni.append(nni)

            new_backup_path = self.oess_get_path(evc_to_move.unis, primary=copy_of_primary_plus_nni)

            if nni in new_backup_path:
                warn(f"Path Not Found without NNI {nni}. No changes made.")
                return {"result": "error", "msg": f"Path Not Found without NNI {nni}."}

            if current_primary == new_backup_path:
                warn("Found Backup path is the same as the Primary path.")
                warn("  No changes made.")
                return {
                    "result": "error",
                    "msg": "Primary and Backup paths are the same. No changes made.",
                }

            # Request OESS to change backup path.
            if "result" in self.set_path(evc_to_move, current_primary, new_backup_path):
                return {
                    "result": "moved",
                    "msg": f"EVC {evc_to_move.name}'s Backup path changed with success.",
                }

        else:

            return {
                "result": "error",
                "msg": f"NNI {nni} not part of EVC {evc_to_move.name}. No changes made.",
            }

        # Something wrong happened when changing the path on set_path.
        return {
            "result": "error",
            "msg": f"Error when changing EVC {evc_to_move.name}'s path. Run debug mode to check.",
        }
