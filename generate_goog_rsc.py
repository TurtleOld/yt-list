#!/usr/bin/env python3
import json
import urllib.request

URL = "https://www.gstatic.com/ipranges/goog.json"
LIST_NAME = "youtube"            # имя address-list на MikroTik
OUTPUT_FILE = "google_youtube.rsc"


def main() -> None:
    # Скачиваем JSON
    with urllib.request.urlopen(URL) as resp:
        data = json.load(resp)

    prefixes = data.get("prefixes", [])

    lines: list[str] = []
    lines.append("/ip firewall address-list")
    lines.append(f"remove [find list={LIST_NAME}]")

    count = 0
    for p in prefixes:
        ipv4 = p.get("ipv4Prefix")
        if not ipv4:
            continue
        lines.append(f"add list={LIST_NAME} address={ipv4}")
        count += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Готово: записано {count} префиксов в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
