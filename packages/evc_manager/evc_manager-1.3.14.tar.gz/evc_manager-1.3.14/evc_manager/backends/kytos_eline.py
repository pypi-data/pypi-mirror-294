""" Kytos MEF E-Line application's backend """

# pylint: disable=broad-exception-caught,broad-exception-raised


import copy
import datetime
import time
import traceback
import requests
from .generic_backend import Backend
from ..libs.core.cli import CliOptions
from ..libs.models.evc import EthernetVirtualCircuit
from ..libs.models.uni import UNI
from ..libs.models.nni import NNI
from ..libs.models.tag import Tag
from ..libs.models.current_config import CurrentConfig
from ..libs.core.log import debug, info, warn


class KytosEline(Backend):
    """Kytos MEF E-Line application's backend. Kytos does not have authentication yet."""

    auth = None
    timeout = 30
    mef_eline_api = "/kytos/mef_eline/v2/evc/"
    topology_api = "/kytos/topology/v3/"

    def _get(self, url, evc=""):
        """Submit a get request to the mef_eline"""
        response = requests.get(f"{url}{evc}", auth=self.auth, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception("Status code is not 200. Error: " + response.text)

        return response.json()

    def _get_topo(self):
        """Get the Kytos topology to have access to metadata values for better
        naming and representation of ports and switches."""
        response = requests.get(self.url + self.topology_api, auth=self.auth, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception("Status code is not 200. Error: " + response.text)
        self.topology = response.json()["topology"]  # pylint: disable=W0201

    def authenticate(self):
        """Kytos is not requiring authentication"""
        self.url = CliOptions().backend_url  # pylint: disable=W0201
        self.auth = (CliOptions().user, CliOptions().password)  # pylint: disable=W0201

    def get_evcs(self, topology=None):
        """Get all EVCs from Kytos MEF E-Line napp"""
        if not topology:
            self._get_topo()
        return self.process_kytos_evcs(self._get(url=self.url + self.mef_eline_api))

    def delete_evc(self, evc_to_delete: EthernetVirtualCircuit):
        """Delete EVC with the provided EVC name"""
        info(f"Deleting EVC {evc_to_delete.name}:")
        for uni in evc_to_delete.unis:
            info(f"\tUNI device {uni.device}")
            info(f"\tUNI interface {uni.interface_name}")
            if uni.tag is not None:  # Check for EPL
                info(f"\tUNI vlan {uni.tag.value}")

        try:
            self._send_delete(evc_to_delete.current_config.backend_evc_id)
        except Exception as e:
            return {"result": "error", "msg": str(e)}

        return {"result": "deleted", "msg": f"EVC {evc_to_delete.name} deleted."}

    def move_evc(self, evc_to_move, current_primary, current_backup, nni):
        """Move EVC out of a provided NNI. The provided nni is actually a
        link name or link ID"""
        links_idx = self.get_links_with_indexes()
        link = links_idx.get(nni)
        if not link:
            return {
                "result": "error",
                "msg": f"could not find valid Link for NNI {nni}",
            }

        evc_payload = dict()
        evc_payload["primary_constraints"] = {"undesired_links": [link["id"]]}
        evc_payload["secondary_constraints"] = {"undesired_links": [link["id"]]}

        try:
            self._send_patch(evc_to_move.current_config.backend_evc_id, evc_payload)
        except Exception as err:
            warn(
                f"Error on PATCH EVC {evc_to_move.name}: {err}. Traceback: "
                + traceback.format_exc()
            )
            return {"result": "error", "msg": str(err)}

        msg = {"result": "changed", "msg": f"EVC {evc_to_move.name} updated."}

        return msg

    def process_kytos_evcs(self, kytos_evcs):
        """Convert each Kytos_evc in an EVC and add them to a list
        Args:
            kytos_evcs: list of Kytos EVC dictionaries
        """
        evcs = list()
        for kytos_evc in kytos_evcs.values():
            evcs.append(copy.deepcopy(self.process_kytos_evc(kytos_evc)))
        return evcs

    def process_kytos_evc(self, kytos_evc):
        """Convert from Kytos EVC format to the EthernetVirtualCircuit() data model
        Args:
            kytos_evc: a Kytos EVC in dictionary
        """
        evc = EthernetVirtualCircuit()
        evc.name = kytos_evc["name"]
        evc.unis = self.get_unis([kytos_evc["uni_a"], kytos_evc["uni_z"]])
        evc.paths = self.get_requested_paths(kytos_evc)

        evc_start_date = datetime.datetime.strptime(
            kytos_evc["start_date"], "%Y-%m-%dT%H:%M:%S"
        ).timetuple()
        evc.provisioning_time = int(time.mktime(evc_start_date))

        if kytos_evc["end_date"]:
            evc_end_date = datetime.datetime.strptime(
                kytos_evc["end_date"], "%Y-%m-%dT%H:%M:%S"
            ).timetuple()
            evc.decommissioning_time = int(time.mktime(evc_end_date))

        if "metadata" in kytos_evc:
            if "metrics" in kytos_evc["metadata"]:
                if "min_bw" in kytos_evc["metadata"]["min_bw"]:
                    evc.metrics.min_bw = kytos_evc["metadata"]["metrics"]["min_bw"]

            if "external_id" in kytos_evc["metadata"]:
                evc.external_id = kytos_evc["metadata"]["external_id"]

        evc.current_config = self.get_current_config(kytos_evc, evc)
        return evc

    def get_switches(self):
        """Returns all switches in the kytos topology napp"""
        return self.topology["switches"].values()

    def get_switch_names(self, dpid):
        """Get the switch name from metadata using the DPID.
        Args:
            dpid: switch's dpid in the format xx:xx:xx:xx:xx:xx:xx:xx
        """
        for switch in self.get_switches():
            if dpid == switch["id"]:
                if "node_name" in switch["metadata"]:
                    return switch["metadata"]["node_name"]
        return dpid

    def get_interface_name(self, dpid_port):
        """Get the interface name from the topology.
        Args:
            interface in the format xx:xx:xx:xx:xx:xx:xx:xx:NN
        switch is xx:xx:xx:xx:xx:xx:xx:xx or xx:xx:xx:xx:xx:xx:xx:xx:NN[0:23]
        interface is NN or xx:xx:xx:xx:xx:xx:xx:xx:NN[24:]
        """
        # to make things easier, when exporting an EVC we export the interface
        # name as the port_number (instead of the description, datapath name, or
        # even metadata.port_name). Heads up: when reading from user input we will
        # continue to accept metadata.port_name, description or port_number.
        # for switch in self.get_switches():
        #    if dpid_port[0:23] == switch["id"]:
        #        for interface in switch["interfaces"].values():
        #            if dpid_port == interface["id"]:
        #                if "port_name" in interface["metadata"]:
        #                    return interface["metadata"]["port_name"]
        #                else:
        #                    return interface["name"]
        return dpid_port[24:]

    def get_interface_description(self, dpid_port):
        """Get the interface description from the topology.
        Args:
            interface in the format xx:xx:xx:xx:xx:xx:xx:xx:NN
        switch is xx:xx:xx:xx:xx:xx:xx:xx or xx:xx:xx:xx:xx:xx:xx:xx:NN[0:23]
        interface is NN or xx:xx:xx:xx:xx:xx:xx:xx:NN[24:]
        """
        for switch in self.get_switches():
            if dpid_port[0:23] == switch["id"]:
                for interface in switch["interfaces"].values():
                    if dpid_port == interface["id"]:
                        if "description" in interface["metadata"]:
                            return interface["metadata"]["description"]
                        else:
                            return interface["name"]
        return dpid_port[24:]

    def get_uni(self, kytos_uni):
        """ "Convert Kytos UNI to UNI class
        Args:
            kytos_uni: a Kytos uni dictionary
        """
        uni = UNI()

        uni.device = self.get_switch_names(kytos_uni["interface_id"][0:23])
        uni.interface_name = self.get_interface_name(kytos_uni["interface_id"])
        uni.interface_description = self.get_interface_description(kytos_uni["interface_id"])

        if "tag" in kytos_uni:
            uni.tag.type = "vlan"
            uni.tag.value = kytos_uni["tag"]["value"]
        else:
            uni.tag = None
        return uni

    def get_unis(self, kytos_unis):
        """Creates a list of UNI() objects
        Args:
            kytos_unis: list with Kytos uni_a and uni_b
        """
        unis = list()
        for kytos_uni in kytos_unis:
            unis.append(self.get_uni(kytos_uni))
        return unis

    def get_links(self):
        """Returns all links in the kytos topology napp"""
        return self.topology["links"].values()

    def get_link_name(self, span):
        """Get the link name from the topology.
        Args:
            span: a segment of the end-to-end path or a connection between two switches
        """
        for link in self.get_links():
            if (
                link["endpoint_a"]["id"] == span["endpoint_a"]["id"]
                and link["endpoint_b"]["id"] == span["endpoint_b"]["id"]
            ) or (
                link["endpoint_a"]["id"] == span["endpoint_b"]["id"]
                and link["endpoint_b"]["id"] == span["endpoint_a"]["id"]
            ):
                if "link_name" in link["metadata"]:
                    return link["metadata"]["link_name"]

        # If there is an error with the links (issue #72), add NOT_A_LINK to the name
        msg = ""
        if span["endpoint_a"]["switch"] == span["endpoint_b"]["switch"]:
            msg = "NOT_A_LINK--"

        return f"{msg}{span['endpoint_a']['name']}--{span['endpoint_b']['name']}"

    def process_path(self, links):
        """Convert from Kytos links to a list of NNI() objects
        Args:
            links: Kytos list of links.
        """
        path = list()
        for span in links:
            link = NNI()

            link.device_a = span["endpoint_a"]["name"].split("-")[0]
            if "port_name" in span["endpoint_a"]["metadata"]:
                link.interface_a = span["endpoint_a"]["metadata"]["port_name"]
            else:
                link.interface_a = span["endpoint_a"]["name"]

            link.device_z = span["endpoint_b"]["name"].split("-")[0]
            if "port_name" in span["endpoint_b"]["metadata"]:
                link.interface_z = span["endpoint_b"]["metadata"]["port_name"]
            else:
                link.interface_z = span["endpoint_b"]["name"]
            link.name = self.get_link_name(span)
            path.append(link)
            del link
        return path

    def get_requested_paths(self, evc):
        """Create the list of paths based on primary, backup, or
        none (dynamic). requested_paths, if empty, must be a list with one list.
        As kytos has dynamic path, do this in case neither primary or backup
        paths are provided.
        Args:
            evc: kytos evc as dictionary
        """
        requested_paths = list()
        if len(evc["primary_path"]) > 0:
            requested_paths.append(self.process_path(evc["primary_path"]))
        if len(evc["backup_path"]) > 0:
            requested_paths.append(self.process_path(evc["backup_path"]))
        if evc["dynamic_backup_path"]:
            requested_paths.append(list())
        if (
            not evc["dynamic_backup_path"]
            and len(evc["primary_path"]) == 0
            and len(evc["backup_path"]) == 0
        ):
            requested_paths.append(list())
        return requested_paths

    @staticmethod
    def compare_current_with_primary(current, primary):
        """Compare the current path with the primary path provided
        Returns:
            True if they are not the same
            False if they are the same
        """

        if len(current) != len(primary):
            return True

        i = 0
        while i < len(current):
            if current[i].__dict__ != primary[i].__dict__:
                return True
            i += 1

        return False

    def get_current_config(self, kytos_evc, evc):
        """Instantiate the CurrentConfig object
        Args:
            kytos_evc: a Kytos EVC dict.
            evc: the instantiated EVC object
        """
        current_config = CurrentConfig()
        current_config.backend = "kytos"
        current_config.backend_evc_id = kytos_evc["id"]
        current_config.is_active = kytos_evc["active"]
        current_config.is_up = kytos_evc["enabled"]
        current_config.current_path = self.process_path(kytos_evc["current_path"])
        current_config.is_optimized = True  # Not supported since Kytos doesn't support it.

        if len(evc.paths) > 0:
            # If a primary_path was requested and it is diferent from current_path, is backup
            current_config.is_backup = self.compare_current_with_primary(
                current_config.current_path, evc.paths[0]
            )

        if int(datetime.datetime.now().timestamp()) > evc.decommissioning_time:
            current_config.is_expired = True

        return current_config

    def _send_post(self, payload):
        """send a post request to kytos api"""
        api_url = self.url + self.mef_eline_api
        try:
            response = requests.post(api_url, json=payload, auth=self.auth, timeout=self.timeout)
        except Exception as err:
            raise Exception(f"Error connecting to Kytos API: {err}") from err

        if response.status_code != 201:
            raise Exception(
                f'Failed sending POST for EVC {payload["name"]}:'
                + f" status_core = {response.status_code}"
                + f" response = {response.text}"
            )

        return response.json()

    def _send_delete(self, evc_id):
        """Send a request to delete an EVC"""
        api_url = self.url + self.mef_eline_api + evc_id
        try:
            response = requests.delete(api_url, auth=self.auth, timeout=self.timeout)
        except Exception as err:
            raise Exception(f"Error connecting to Kytos API: {err}") from err

        if response.status_code != 200:
            raise Exception(f"Failed to delete circuit {evc_id}: {response.text}")

        return response.json()

    def _send_patch(self, evc_id, payload):
        """Send a request to PATCH an EVC"""
        debug(f"Submit request to patch EVC: evc_id={evc_id} payload={payload}\n")
        api_url = self.url + self.mef_eline_api + evc_id
        try:
            response = requests.patch(api_url, json=payload, auth=self.auth, timeout=self.timeout)
        except Exception as err:
            raise Exception(f"Error connecting to Kytos API: {err}") from err

        if response.status_code != 200:
            raise Exception(f"Failed to patch circuit {evc_id}: {response.text}")

        data = response.json()
        data["circuit_id"] = next(iter(data))
        return data

    def get_interface_id(self, switch_interfaces, interface):
        """Look up for an interface in the switch interfaces."""

        debug(f"Looking for interface {interface} in {switch_interfaces}\n")
        for switch_interface in switch_interfaces.values():
            if "port_name" in switch_interface["metadata"]:
                if switch_interface["metadata"]["port_name"] == interface:
                    return switch_interface["id"]

            if interface.isdigit() and switch_interface["port_number"] == int(interface):
                return switch_interface["id"]

            if switch_interface["name"] == interface:
                return switch_interface["id"]

            if switch_interface["id"] == interface:
                return switch_interface["id"]

        return None

    def evaluate_uni(self, device, interface):
        """to do: check status, state, maintenance?"""
        for switch in self.get_switches():
            debug(f"Looking for switch {device} in {switch}\n")
            if "node_name" in switch["metadata"]:
                if switch["metadata"]["node_name"] == device:
                    debug(f"Found switch: {switch['id']}. Looking for interfaces\n")
                    return self.get_interface_id(switch["interfaces"], interface)

            # 5/9/2024 Fix: Add functionality does not accept the id if
            # "node_name" is in "metadata".
            if switch["name"] == device:
                debug(f"Found switch: {switch['id']}. Looking for interfaces\n")
                return self.get_interface_id(switch["interfaces"], interface)

        return None

    def evaluate_unis(self, new_evc):
        """Process EVC UNIs to create proper UNI dict."""
        kytos_interface_ids = list()
        for uni in new_evc.unis:
            debug(f"Evaluating each node provided: {uni.device}:{uni.interface_name}\n")
            kytos_interface_id = self.evaluate_uni(uni.device, uni.interface_name)
            if kytos_interface_id:
                kytos_interface_ids.append(kytos_interface_id)

        return kytos_interface_ids

    def prepare_uni(self, interface_id, tag: Tag):
        """Create an UNI dict from interface dict"""
        uni = dict()
        uni["interface_id"] = interface_id
        if tag:
            uni["tag"] = dict()
            uni["tag"]["tag_type"] = 1
            uni["tag"]["value"] = tag.value
        return uni

    def get_links_with_indexes(self):
        """Return a dict of links indexed by link id."""
        links_idx = {}
        for link in self.get_links():
            link_name = link["metadata"].get("link_name")
            if link_name:
                links_idx[link_name] = link
            links_idx[link["id"]] = link
        return links_idx

    def evaluate_paths(self, evc):
        """Evaluate each path of an EVC."""
        links_idx = self.get_links_with_indexes()
        for path in evc.paths:
            self.evaluate_path(path, links_idx)

    def evaluate_nni(self, nni, links_idx):
        """Process link and update a NNI."""
        link = links_idx.get(nni.name)
        if not link:
            raise ValueError(f"could not find valid Link for NNI {nni.name}")
        nni.device_a = link["endpoint_a"]["switch"]
        nni.interface_a = link["endpoint_a"]["port_number"]
        nni.device_z = link["endpoint_b"]["switch"]
        nni.interface_z = link["endpoint_b"]["port_number"]

    def evaluate_path(self, path, links_idx):
        """Process individual links in a path."""
        for nni in path:
            if nni.name == "Empty":
                continue
            self.evaluate_nni(nni, links_idx)

    def prepare_path(self, uni_a, uni_z, path):
        """Prepare path in Kytos format: list of dict containing interface
        IDs. To be considered a valid path, each NNI's endpoint should match
        the next item. Example: ([a, b],[b, c]) is valid; [b,a],[b,c] is
        invalid."""
        formatted_path = []
        path_copy = path[:]
        previous = ":".join(uni_a.split(":")[:-1])
        last_sw = ":".join(uni_z.split(":")[:-1])

        debug(f"uni_a={uni_a} uni_z={uni_z} path={path}\n")
        for _ in range(len(path)):
            found_nni = None
            for idx, nni in enumerate(path_copy):
                iface_a = f"{nni.device_a}:{nni.interface_a}"
                iface_z = f"{nni.device_z}:{nni.interface_z}"
                if nni.device_a == previous:
                    formatted_path.append(
                        {"endpoint_a": {"id": iface_a}, "endpoint_b": {"id": iface_z}}
                    )
                    previous = nni.device_z
                    found_nni = idx
                    break
                if nni.device_z == previous:
                    formatted_path.append(
                        {"endpoint_a": {"id": iface_z}, "endpoint_b": {"id": iface_a}}
                    )
                    previous = nni.device_a
                    found_nni = idx
                    break
            else:
                raise ValueError(f"Invalid path: there is no link from {previous}. Path: {path}")
            path_copy.pop(found_nni)

        if previous != last_sw:
            raise ValueError(f"Invalid path: last link is different from uni_z. Path: {path}")

        return formatted_path

    def provision_evc(
        self, new_evc: EthernetVirtualCircuit, interface_ids: list[int], change: bool = False
    ) -> dict[str, object]:
        """Create OESS Provisioning Query"""
        debug(f"provision_evc new_Evc: {new_evc.paths}\n")

        kytos_evc = dict()
        kytos_evc["name"] = new_evc.name
        kytos_evc["uni_a"] = self.prepare_uni(interface_ids[0], new_evc.unis[0].tag)
        kytos_evc["uni_z"] = self.prepare_uni(interface_ids[1], new_evc.unis[1].tag)
        kytos_evc["primary_path"] = []
        kytos_evc["backup_path"] = []

        if change:
            kytos_evc["dynamic_backup_path"] = False

        # primary_path, backup_path, dynamic_backup_path
        # possible values:
        # 1) no paths
        # 2) one path and it is Empty
        # 3) one path and it is not Empty
        # 4) two paths and they are all Empty
        # 5) two paths and the first is not Empty
        # 6) two paths and the first and second are not Empty
        # 7) three paths and they are all Empty
        # 8) three paths and the first one is not Empty (similar to 5)
        # 9) three paths and the first and second are not Empty
        # 10) three paths or more and they are not Empty

        if len(new_evc.paths) == 0:
            kytos_evc["dynamic_backup_path"] = True

        if len(new_evc.paths) >= 1:
            if new_evc.paths[0][0].name == "Empty":
                kytos_evc["dynamic_backup_path"] = True
            else:
                kytos_evc["primary_path"] = self.prepare_path(
                    interface_ids[0], interface_ids[1], new_evc.paths[0]
                )
        if len(new_evc.paths) >= 2:
            if new_evc.paths[1][0].name == "Empty":
                kytos_evc["dynamic_backup_path"] = True
            else:
                kytos_evc["backup_path"] = self.prepare_path(
                    interface_ids[0], interface_ids[1], new_evc.paths[1]
                )
        if len(new_evc.paths) >= 3:
            kytos_evc["dynamic_backup_path"] = True

        if change:
            result = self._send_patch(new_evc.current_config.backend_evc_id, kytos_evc)
        else:
            result = self._send_post(kytos_evc)

        return result["circuit_id"]

    def add_evc(self, new_evc, change=False):
        """Add/Change EVC based on the provided EVC name"""
        interface_ids = self.evaluate_unis(new_evc)
        if len(interface_ids) != len(new_evc.unis):
            return {"result": "error", "msg": f"UNIs not found in EVC {new_evc.name}"}

        warn("Requesting Paths...")

        try:
            self.evaluate_paths(new_evc)
        except ValueError as err:
            return {"result": "error", "msg": f"Invalid path: {err}"}

        warn("Provisioning circuit...")

        try:
            self.provision_evc(new_evc, interface_ids, change=change)
        except Exception as err:
            warn(
                f"ERROR during provisioning EVC {new_evc.name}: {err}. Traceback:"
                + traceback.format_exc()
            )
            return {
                "result": "error",
                "msg": f"Error provisioning EVC {new_evc.name}",
            }

        msg = {"result": "created", "msg": f"EVC {new_evc.name} provisioned."}
        if change:
            msg["result"] = "changed"
        return msg
