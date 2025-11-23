#!/usr/bin/env python3
import socket
import ipaddress
from datetime import datetime
from pathlib import Path

DOMAINS = [
    "chatgpt.com",
    "chat.openai.com",
    "cdn.oaistatic.com",
    "oaistatic.com",
    "oaiusercontent.com",
]

OUTPUT_FILE = Path("openai-address-list.rsc")
ADDRESS_LIST_NAME = "openai"


def resolve_ipv4(domain: str) -> set[str]:
    """Резолвим только IPv4-адреса для домена."""
    ips: set[str] = set()
    try:
        results = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
    except socket.gaierror as e:
        print(f"# warn: failed to resolve {domain}: {e}")
        return ips

    for family, _, _, _, sockaddr in results:
        if family == socket.AF_INET:
            ip = sockaddr[0]
            ips.add(ip)
    return ips


def build_networks() -> dict[ipaddress.IPv4Network, set[str]]:
    """
    Возвращаем mapping:
      /24-сеть -> множество доменов, из которых она получилась.
    """
    net_to_domains: dict[ipaddress.IPv4Network, set[str]] = {}

    for domain in DOMAINS:
        ips = resolve_ipv4(domain)
        if not ips:
            continue

        for ip in ips:
            net = ipaddress.IPv4Network(f"{ip}/24", strict=False)
            net_to_domains.setdefault(net, set()).add(domain)

    return net_to_domains


def main() -> None:
    net_to_domains = build_networks()

    if not net_to_domains:
        print("No IPs resolved, nothing to write.")
        return

    networks = sorted(
        net_to_domains.keys(),
        key=lambda n: (int(n.network_address), n.prefixlen),
    )

    lines: list[str] = []


    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append("/ip firewall address-list")
    lines.append(f"remove [find list={ADDRESS_LIST_NAME}]")

    for net in networks:
        domains = ",".join(sorted(net_to_domains[net]))
        line = (
            f'add list={ADDRESS_LIST_NAME} address={net.with_prefixlen} '
            f'comment="{domains}"'
        )
        lines.append(line)

    content = "\n".join(lines) + "\n"
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} with {len(networks)} networks.")


if __name__ == "__main__":
    main()
