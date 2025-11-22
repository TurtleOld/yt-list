from __future__ import annotations

import socket
import sys
from pathlib import Path
from typing import Iterable, Set

LIST_NAME = "openai"

OUTPUT_PATH = Path("openai-address-list.rsc")

DEFAULT_DOMAINS = [
    "api.openai.com",
    "chat.openai.com",
    "chatgpt.com",
]


def resolve_domain(domain: str) -> Set[str]:
    """Резолвим домен в множество IPv4-адресов."""
    ips: Set[str] = set()
    try:
        for family, _, _, _, sockaddr in socket.getaddrinfo(domain, None):
            if family == socket.AF_INET:  # только IPv4
                ip, *_ = sockaddr
                ips.add(ip)
    except socket.gaierror as e:
        print(f"# failed to resolve {domain}: {e}", file=sys.stderr)
    return ips


def generate_rsc(domains: Iterable[str], list_name: str = LIST_NAME) -> str:
    """Формируем текст rsc-скрипта для MikroTik."""
    lines = [
        "/ip firewall address-list",
        f"remove [find list={list_name}]",
    ]

    seen: Set[str] = set()

    for domain in domains:
        for ip in sorted(resolve_domain(domain)):
            if ip in seen:
                continue
            seen.add(ip)
            lines.append(
                f'add list={list_name} address={ip}'
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    domains = sys.argv[1:] or DEFAULT_DOMAINS

    content = generate_rsc(domains)
    OUTPUT_PATH.write_text(content, encoding="utf-8")

    addr_count = max(len(content.splitlines()) - 2, 0)
    print(f"Wrote {OUTPUT_PATH} with {addr_count} addresses")


if __name__ == "__main__":
    main()
