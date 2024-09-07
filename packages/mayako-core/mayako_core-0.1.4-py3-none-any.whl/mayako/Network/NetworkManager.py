from enum import Enum
from .WiFiUDP import WiFiUDP
from .BLE import BLE
from .IntegrityMiddleware import IntegrityMiddleware
from .NetworkInterface import NetworkInterface

#https://stackoverflow.com/a/51976841
class NetworkProtocol(str, Enum):
    WIFIUDP = "WIFIUDP"
    BLE = "BLE"
    SERIAL = "SERIAL"

class NetworkManager:

    _protocol_name: NetworkProtocol
    _protocol: NetworkInterface
    _integrity_middelware: IntegrityMiddleware

    def __init__(self, protocol_name: NetworkProtocol, config: dict = None) -> None:
        self._protocol_name = protocol_name
        self._protocol = self._define_protocol(self._protocol_name)
        
        self._integrity_middelware = IntegrityMiddleware(self._protocol)

    def _define_protocol(self, protocol_name: NetworkProtocol) -> NetworkInterface:
        protocol: NetworkInterface = None

        if type(protocol_name) is not NetworkProtocol:
            raise TypeError(f"protocol_name must be of type NetworkProtocol")

        if protocol_name == NetworkProtocol.WIFIUDP:
            protocol = WiFiUDP()

        elif protocol_name == NetworkProtocol.BLE:
            protocol = BLE()

        else:
            raise NotImplementedError(f"{protocol_name.value} is not implemented")

        return protocol
    
    def send_data(self):
        self.integrity_middelware.write()
    
    def read_data(self):
        self.integrity_middelware.read()
    
