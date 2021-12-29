import json
import requests

from snipssonos.entities.device import Device
from snipssonos.services.device.discovery_service import DeviceDiscoveryService
from snipssonos.exceptions import DeviceParsingException, NoReachableDeviceException, ExternalDeviceDiscoveryUnreachable


class NodeDeviceDiscoveryService(DeviceDiscoveryService):
    SERVICE_NAME = "node_device_discovery"

    def __init__(self, CONFIGURATION=None):
        super(NodeDeviceDiscoveryService, self).__init__(CONFIGURATION)

    def get(self):
        devices = self.get_devices()
        if len(devices):
            return devices[0]
        else:
            raise NoReachableDeviceException("Couldn't find any reachable device")

    def get_devices(self):
        response = self.execute_query()
        return self.parse_devices(response)

    def execute_query(self):
        query_url = self.generate_get_query()

        try:
            req = requests.get(query_url)
        except requests.RequestException as e:
            raise ExternalDeviceDiscoveryUnreachable("External Node REST API is unreachable")

        if req.ok:
            return req.text
        raise NoReachableDeviceException("Could not reach your Sonos devices")

    def generate_get_query(self):
        return "{}{}:{}/zones/".format(self.PROTOCOL, self.HOST, self.PORT)

    def parse_devices(self, json_response):
        parsed_response = json.loads(json_response)

        try:
            members_section = self.extract_member_section_from_json_payload(parsed_response)
            devices = [self.parse_device_object_from_json_member_payload(member) for member in members_section]
        except KeyError as e:
            raise DeviceParsingException(e.message)

        return devices

    def parse_device_object_from_json_member_payload(self, member):
        return Device(member['uuid'], member['roomName'], int(member['state']['volume']))

    def extract_member_section_from_json_payload(self, json_payload):
        return json_payload[0]['members']
