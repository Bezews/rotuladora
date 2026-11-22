#!/usr/bin/env python3
"""Inspeção BLE SOMENTE LEITURA para a PT260 / XD-210.

O que faz:
  --scan          lista dispositivos BLE próximos (nome, RSSI, UUIDs anunciados)
  --name NOME     conecta ao primeiro dispositivo cujo nome contém NOME e lista
                  serviços/características GATT com propriedades. Lê apenas o
                  Device Information Service (0x180A), que é padrão e inofensivo.

O que NÃO faz (por design):
  - nunca escreve em característica alguma (sem write / write-without-response)
  - nunca assina notificações
  - nunca lê características proprietárias (ex.: 0xFF0x), só lista

Endereços MAC são anonimizados por padrão (use --show-mac só localmente).

Requer: python -m pip install bleak
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

try:
    from bleak import BleakClient, BleakScanner
except ImportError:  # pragma: no cover
    sys.exit("Instale a dependência: python -m pip install bleak")

DEVICE_INFO_SERVICE = "0000180a-0000-1000-8000-00805f9b34fb"
DEVICE_INFO_CHARS = {
    "00002a29-0000-1000-8000-00805f9b34fb": "manufacturer_name",
    "00002a24-0000-1000-8000-00805f9b34fb": "model_number",
    "00002a25-0000-1000-8000-00805f9b34fb": "serial_number",
    "00002a26-0000-1000-8000-00805f9b34fb": "firmware_revision",
    "00002a27-0000-1000-8000-00805f9b34fb": "hardware_revision",
    "00002a28-0000-1000-8000-00805f9b34fb": "software_revision",
}
SENSITIVE = {"serial_number"}


def anon(addr: str, show: bool) -> str:
    if show or not addr:
        return addr
    parts = addr.replace("-", ":").split(":")
    if len(parts) == 6:
        return "XX:XX:XX:XX:" + ":".join(parts[-2:])
    return addr[:4] + "…" + addr[-4:]  # macOS usa UUID em vez de MAC


async def scan(timeout: float, show_mac: bool) -> list[dict]:
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    out = []
    for dev, adv in found.values():
        out.append({
            "name": adv.local_name or dev.name,
            "address": anon(dev.address, show_mac),
            "rssi": adv.rssi,
            "service_uuids": adv.service_uuids,
            "manufacturer_data_ids": [hex(k) for k in adv.manufacturer_data],
        })
    return sorted(out, key=lambda d: d["rssi"] or -999, reverse=True)


async def inspect(name: str, timeout: float, show_mac: bool, show_serial: bool) -> dict:
    dev = await BleakScanner.find_device_by_filter(
        lambda d, a: name.lower() in ((a.local_name or d.name or "").lower()),
        timeout=timeout,
    )
    if dev is None:
        raise SystemExit(f"Nenhum dispositivo com nome contendo '{name}' encontrado.")

    report: dict = {"name": dev.name, "address": anon(dev.address, show_mac),
                    "services": [], "device_information": {}}
    async with BleakClient(dev) as client:
        for svc in client.services:
            entry = {"uuid": svc.uuid, "description": svc.description, "characteristics": []}
            for ch in svc.characteristics:
                entry["characteristics"].append({
                    "uuid": ch.uuid,
                    "handle": ch.handle,
                    "properties": ch.properties,
                    "description": ch.description,
                })
            report["services"].append(entry)

            if svc.uuid.lower() == DEVICE_INFO_SERVICE:
                for ch in svc.characteristics:
                    key = DEVICE_INFO_CHARS.get(ch.uuid.lower())
                    if not key or "read" not in ch.properties:
                        continue
                    try:
                        raw = await client.read_gatt_char(ch)
                        val = raw.decode("utf-8", errors="replace").strip("\x00 ")
                    except Exception as exc:  # leitura pode ser negada
                        val = f"<erro: {exc}>"
                    if key in SENSITIVE and not show_serial:
                        val = "<oculto; use --show-serial localmente>"
                    report["device_information"][key] = val
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--scan", action="store_true")
    g.add_argument("--name")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--show-mac", action="store_true", help="não anonimizar (não publique a saída)")
    ap.add_argument("--show-serial", action="store_true", help="exibir serial (não publique a saída)")
    args = ap.parse_args()

    if args.scan:
        result = asyncio.run(scan(args.timeout, args.show_mac))
    else:
        result = asyncio.run(inspect(args.name, args.timeout, args.show_mac, args.show_serial))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
