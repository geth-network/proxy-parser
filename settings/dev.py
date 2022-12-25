from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_url: str
    redis_proxy_key: str = "proxy"
    tasks_module: str
    parse_interval: float = 60.0 * 10  # seconds
    check_interval: float = 60.0 * 5  # seconds
    check_url: str = "https://httpbin.org/ip"
    bs_parser: str = "lxml"
    checker_timeout: float = 30.0


settings = Settings()
