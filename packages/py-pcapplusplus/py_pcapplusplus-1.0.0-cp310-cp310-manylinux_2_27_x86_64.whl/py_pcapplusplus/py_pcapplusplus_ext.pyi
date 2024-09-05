from collections.abc import Sequence
import enum
from typing import overload


ConfigurationString: SomeIpSdOptionType = SomeIpSdOptionType.ConfigurationString

ERRORS: SomeIpMsgType = SomeIpMsgType.ERRORS

ERROR_ACK: SomeIpMsgType = SomeIpMsgType.ERROR_ACK

class EthLayer(Layer):
    def __init__(self, src_mac_addr: str = '', dst_mac_addr: str = '') -> None: ...

    @property
    def src_mac_addr(self) -> str: ...

    @src_mac_addr.setter
    def src_mac_addr(self, arg: str, /) -> None: ...

    @property
    def dst_mac_addr(self) -> str: ...

    @dst_mac_addr.setter
    def dst_mac_addr(self, arg: str, /) -> None: ...

    @property
    def ether_type(self) -> int: ...

    @ether_type.setter
    def ether_type(self, arg: bool, /) -> None: ...

FindService: SomeIpSdEntryType = SomeIpSdEntryType.FindService

IPv4Endpoint: SomeIpSdOptionType = SomeIpSdOptionType.IPv4Endpoint

class IPv4Layer(Layer):
    def __init__(self, src_addr: str, dst_addr: str) -> None: ...

    @property
    def src_ip(self) -> str: ...

    @src_ip.setter
    def src_ip(self, arg: str, /) -> None: ...

    @property
    def dst_ip(self) -> str: ...

    @dst_ip.setter
    def dst_ip(self, arg: str, /) -> None: ...

    @property
    def ttl(self) -> int: ...

    @ttl.setter
    def ttl(self, arg: int, /) -> None: ...

    @property
    def ip_identification(self) -> int: ...

    @ip_identification.setter
    def ip_identification(self, arg: int, /) -> None: ...

    def clear_chksum(self) -> None: ...

IPv4Multicast: SomeIpSdOptionType = SomeIpSdOptionType.IPv4Multicast

IPv4SdEndpoint: SomeIpSdOptionType = SomeIpSdOptionType.IPv4SdEndpoint

IPv6Endpoint: SomeIpSdOptionType = SomeIpSdOptionType.IPv6Endpoint

class IPv6Layer(Layer):
    def __init__(self, src_addr: str, dst_addr: str) -> None: ...

    @property
    def src_ip(self) -> str: ...

    @src_ip.setter
    def src_ip(self, arg: str, /) -> None: ...

    @property
    def dst_ip(self) -> str: ...

    @dst_ip.setter
    def dst_ip(self, arg: str, /) -> None: ...

IPv6Multicast: SomeIpSdOptionType = SomeIpSdOptionType.IPv6Multicast

IPv6SdEndpoint: SomeIpSdOptionType = SomeIpSdOptionType.IPv6SdEndpoint

class Layer:
    def __repr__(self) -> str: ...

    def __bytes__(self) -> bytes: ...

class LayerType(enum.Enum):
    """Enum for the different layer types"""

    EthLayer = 1

    IPv4Layer = 2

    IPv6Layer = 3

    TcpLayer = 4

    UdpLayer = 5

    SomeIpLayer = 45

    SomeIpSdLayer = 45

    PayloadLayer = 25

LoadBalancing: SomeIpSdOptionType = SomeIpSdOptionType.LoadBalancing

NOTIFICATION: SomeIpMsgType = SomeIpMsgType.NOTIFICATION

NOTIFICATION_ACK: SomeIpMsgType = SomeIpMsgType.NOTIFICATION_ACK

OfferService: SomeIpSdEntryType = SomeIpSdEntryType.OfferService

class Packet:
    """Represent a network packet"""

    def __init__(self) -> None: ...

    def get_layer(self, type: LayerType) -> Layer:
        """
        Extract layer of requested type from a packet, none type if no such layer exists in the packet
        """

    def add_layer(self, new_layer: Layer) -> bool:
        """Add a new layer as the last layer in the packet"""

    def insert_layer(self, prev_layer: Layer, new_layer: Layer) -> bool:
        """Insert a new layer after an existing layer in the packet."""

    def __repr__(self) -> str: ...

    def __bytes__(self) -> bytes: ...

class PayloadLayer(Layer):
    def __init__(self, data: bytes) -> None: ...

REQUEST: SomeIpMsgType = SomeIpMsgType.REQUEST

REQUEST_ACK: SomeIpMsgType = SomeIpMsgType.REQUEST_ACK

REQUEST_NO_RETURN: SomeIpMsgType = SomeIpMsgType.REQUEST_NO_RETURN

REQUEST_NO_RETURN_ACK: SomeIpMsgType = SomeIpMsgType.REQUEST_NO_RETURN_ACK

RESPONSE: SomeIpMsgType = SomeIpMsgType.RESPONSE

RESPONSE_ACK: SomeIpMsgType = SomeIpMsgType.RESPONSE_ACK

class RawSocket:
    def __init__(self, if_name: str) -> None: ...

    def send_packet(self, packet: Packet) -> bool: ...

    def receive_packet(self, blocking: bool = True, timeout: float = -1) -> Packet: ...

    def sniff(self, timeout: float = 1) -> list[Packet]: ...

    def send_packets(self, packets: Sequence[Packet]) -> int:
        """Sends a list of packets over the specified network interface"""

class Reader:
    """Device for reading and parsing .pcap files"""

    def __init__(self, pcap_path: str) -> None:
        """Initializes device and open requested pcap file"""

    def __next__(self) -> Packet:
        """Get next packet"""

    def __iter__(self) -> Reader:
        """Get an iterator"""

SD_TCP: SomeIpSdProtocolType = SomeIpSdProtocolType.SD_TCP

SD_UDP: SomeIpSdProtocolType = SomeIpSdProtocolType.SD_UDP

class SomeIpLayer(Layer):
    def __init__(self, service_id: int = 0, method_id: int = 0, client_id: int = 0, session_id: int = 0, interface_version: int = 0, msg_type: SomeIpMsgType = SomeIpMsgType.REQUEST, return_code: int = 0, payload: bytes = ...) -> None: ...

    @staticmethod
    def from_bytes(raw_data: bytes) -> SomeIpLayer: ...

    @property
    def service_id(self) -> int: ...

    @service_id.setter
    def service_id(self, arg: int, /) -> None: ...

    @property
    def method_id(self) -> int: ...

    @method_id.setter
    def method_id(self, arg: int, /) -> None: ...

    @property
    def client_id(self) -> int: ...

    @client_id.setter
    def client_id(self, arg: int, /) -> None: ...

    @property
    def session_id(self) -> int: ...

    @session_id.setter
    def session_id(self, arg: int, /) -> None: ...

    @property
    def interface_version(self) -> int: ...

    @interface_version.setter
    def interface_version(self, arg: int, /) -> None: ...

    @property
    def message_type(self) -> SomeIpMsgType: ...

    @message_type.setter
    def message_type(self, arg: SomeIpMsgType, /) -> None: ...

    @property
    def return_code(self) -> int: ...

    @return_code.setter
    def return_code(self, arg: int, /) -> None: ...

    @property
    def protocol_version(self) -> int: ...

    @protocol_version.setter
    def protocol_version(self, arg: int, /) -> None: ...

class SomeIpMsgType(enum.Enum):
    """Enum for the different SOME/IP msg types"""

    REQUEST = 0

    REQUEST_ACK = 64

    REQUEST_NO_RETURN = 1

    REQUEST_NO_RETURN_ACK = 65

    NOTIFICATION = 2

    NOTIFICATION_ACK = 66

    RESPONSE = 128

    RESPONSE_ACK = 192

    ERRORS = 129

    ERROR_ACK = 193

    TP_REQUEST = 32

    TP_REQUEST_NO_RETURN = 33

    TP_NOTIFICATION = 34

    TP_RESPONSE = 160

    TP_ERROR = 161

class SomeIpSdEntry:
    @overload
    def __init__(self, entry_type: SomeIpSdEntryType, service_id: int, instance_id: int, major_version: int, ttl: int, minor_version: int) -> None:
        """Construct a new SOME/IP-SD Service Entry Type"""

    @overload
    def __init__(self, entry_type: SomeIpSdEntryType, service_id: int, instance_id: int, major_version: int, ttl: int, counter: int, event_group_id: int) -> None:
        """Construct a new SOME/IP-SD Service Entry Type"""

    @property
    def service_id(self) -> int: ...

    @service_id.setter
    def service_id(self, arg: int, /) -> None: ...

    @property
    def instance_id(self) -> int: ...

    @instance_id.setter
    def instance_id(self, arg: int, /) -> None: ...

    @property
    def major_version(self) -> int: ...

    @major_version.setter
    def major_version(self, arg: int, /) -> None: ...

    @property
    def minor_version(self) -> int: ...

    @minor_version.setter
    def minor_version(self, arg: int, /) -> None: ...

    @property
    def ttl(self) -> int: ...

    @ttl.setter
    def ttl(self, arg: int, /) -> None: ...

    @property
    def counter(self) -> int: ...

    @counter.setter
    def counter(self, arg: int, /) -> None: ...

    @property
    def event_group_id(self) -> int: ...

    @event_group_id.setter
    def event_group_id(self, arg: int, /) -> None: ...

    @property
    def type(self) -> SomeIpSdEntryType: ...

    @property
    def index_1(self) -> int: ...

    @property
    def index_2(self) -> int: ...

    @property
    def n_opt_1(self) -> int: ...

    @property
    def n_opt_2(self) -> int: ...

class SomeIpSdEntryType(enum.Enum):
    """Types of entries that can occur in SOME/IP-SD"""

    FindService = 0

    OfferService = 1

    StopOfferService = 2

    SubscribeEventgroup = 3

    StopSubscribeEventgroup = 4

    SubscribeEventgroupAck = 5

    SubscribeEventgroupNack = 6

class SomeIpSdIPv4Option(SomeIpSdOption):
    def __init__(self, option_type: SomeIpSdIPv4OptionType, ipv4_addr: str, port: int, protocol_type: SomeIpSdProtocolType) -> None: ...

    @property
    def addr(self) -> str: ...

    @property
    def port(self) -> int: ...

    @property
    def protocol_type(self) -> SomeIpSdProtocolType: ...

class SomeIpSdIPv4OptionType(enum.Enum):
    """Types of options which are implemented with SomeIpSdIPv4Option"""

    IPv4Endpoint = 0

    IPv4Multicast = 1

    IPv4SdEndpoint = 2

class SomeIpSdIPv6Option(SomeIpSdOption):
    def __init__(self, option_type: SomeIpSdIPv6OptionType, ipv6_addr: str, port: int, protocol_type: SomeIpSdProtocolType) -> None: ...

    @property
    def addr(self) -> str: ...

    @property
    def port(self) -> int: ...

    @property
    def protocol_type(self) -> SomeIpSdProtocolType: ...

class SomeIpSdIPv6OptionType(enum.Enum):
    """Types of options which are implemented with SomeIpSdIPv6Option"""

    IPv6Endpoint = 0

    IPv6Multicast = 1

    IPv6SdEndpoint = 2

class SomeIpSdLayer(SomeIpLayer):
    def __init__(self, service_id: int = 65535, method_id: int = 33024, client_id: int = 0, session_id: int = 1, interface_version: int = 1, msg_type: SomeIpMsgType = SomeIpMsgType.NOTIFICATION, return_code: int = 0, flags: int = 128) -> None: ...

    @staticmethod
    def from_bytes(raw_data: bytes) -> SomeIpSdLayer: ...

    @property
    def flags(self) -> int: ...

    @flags.setter
    def flags(self, arg: int, /) -> None: ...

    def add_entry(self, entry: SomeIpSdEntry) -> int: ...

    def add_option_to(self, index: int, option: SomeIpSdOption) -> bool: ...

    def get_entries(self) -> list[SomeIpSdEntry]: ...

    def get_options(self) -> list[SomeIpSdOption]: ...

class SomeIpSdOption:
    @property
    def type(self) -> SomeIpSdOptionType: ...

class SomeIpSdOptionType(enum.Enum):
    """Types of options currently available for the SOME/IP-SD protocol"""

    Unknown = 0

    ConfigurationString = 1

    LoadBalancing = 2

    IPv4Endpoint = 4

    IPv6Endpoint = 6

    IPv4Multicast = 20

    IPv6Multicast = 22

    IPv4SdEndpoint = 36

    IPv6SdEndpoint = 38

class SomeIpSdProtocolType(enum.Enum):
    """Types of protocols that can be referenced in SOME/IP-SD"""

    SD_TCP = 6

    SD_UDP = 17

StopOfferService: SomeIpSdEntryType = SomeIpSdEntryType.StopOfferService

StopSubscribeEventgroup: SomeIpSdEntryType = SomeIpSdEntryType.StopSubscribeEventgroup

SubscribeEventgroup: SomeIpSdEntryType = SomeIpSdEntryType.SubscribeEventgroup

SubscribeEventgroupAck: SomeIpSdEntryType = SomeIpSdEntryType.SubscribeEventgroupAck

SubscribeEventgroupNack: SomeIpSdEntryType = SomeIpSdEntryType.SubscribeEventgroupNack

TP_ERROR: SomeIpMsgType = SomeIpMsgType.TP_ERROR

TP_NOTIFICATION: SomeIpMsgType = SomeIpMsgType.TP_NOTIFICATION

TP_REQUEST: SomeIpMsgType = SomeIpMsgType.TP_REQUEST

TP_REQUEST_NO_RETURN: SomeIpMsgType = SomeIpMsgType.TP_REQUEST_NO_RETURN

TP_RESPONSE: SomeIpMsgType = SomeIpMsgType.TP_RESPONSE

class TcpLayer(Layer):
    def __init__(self, src_port: int, dst_port: int) -> None: ...

    def clear_chksum(self) -> None: ...

    @property
    def src_port(self) -> int: ...

    @property
    def dst_port(self) -> int: ...

    @property
    def syn_flag(self) -> int: ...

    @syn_flag.setter
    def syn_flag(self, arg: bool, /) -> None: ...

    @property
    def ack_flag(self) -> int: ...

    @ack_flag.setter
    def ack_flag(self, arg: bool, /) -> None: ...

    @property
    def rst_flag(self) -> int: ...

    @rst_flag.setter
    def rst_flag(self, arg: bool, /) -> None: ...

class UdpLayer(Layer):
    def __init__(self, src_port: int, dst_port: int) -> None: ...

    def clear_chksum(self) -> None: ...

    @property
    def src_port(self) -> int: ...

    @property
    def dst_port(self) -> int: ...

Unknown: SomeIpSdOptionType = SomeIpSdOptionType.Unknown

def send_eth_packets(eth_interface: str, packets: Sequence[Packet], dst_ipv4_addr: str) -> int:
    """Sends a list of packets over the specified network interface"""

def sniff_eth(eth_interface: str, timeout: float) -> list[Packet]:
    """
    Sniff over the provided interface and capture packets up to provided timeout
    """
