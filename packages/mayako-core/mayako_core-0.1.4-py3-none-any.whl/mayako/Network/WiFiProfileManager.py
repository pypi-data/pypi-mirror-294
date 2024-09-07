
from typing import TYPE_CHECKING
from ipaddress import IPv4Address
from ..Models.WiFiProfile import WifiProfile

if TYPE_CHECKING:
    from ..Utils.Identity import Identity

class WifiProfileManager:

    profiles: dict[Identity, WifiProfile]
    current_profile: WifiProfile
    
    def __init__(self, profile_config: dict[WifiProfile]) -> None:
        self.profiles = profile_config
        self.current_profile = self.profiles[Identity.WIFI_PROFILE_1]

    def _create() -> Identity:
        raise NotImplementedError

    def _read():
        raise NotImplementedError

    def _select():
        raise NotImplementedError

    def _delete():
        raise NotImplementedError