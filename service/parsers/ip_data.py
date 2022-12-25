import ipaddress

from pydantic import BaseModel, validator

from .exceptions import InvalidIPAddress


class ProxyIP(BaseModel):
    ip: str
    port: str

    def __str__(self):
        return f"{self.ip}:{self.port}".upper()

    @validator('ip')
    def check_ip(cls, v, values):
        try:
            ip = ipaddress.ip_address(v)
        except ValueError:
            raise InvalidIPAddress(f"IP address {v} is not valid")
        return v

    @validator("port")
    def check_port(cls, v, values):
        if not (v.isdigit() or 1 <= int(v) <= 65535):
            raise InvalidIPAddress(f"Invalid port of the input IP address: "
                                   f"{values['address']}")
        return v
