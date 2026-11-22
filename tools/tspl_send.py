#!/usr/bin/env python3
"""Gera e (opcionalmente) envia um job TSPL para a PT-260.

Padrão: --dry-run (só imprime o job na tela / salva .prn). Envio real exige --send.

Transportes:
  --port COM5 | /dev/rfcomm0 | /dev/cu.PT-260_XXXX   Bluetooth Classic (SPP, PIN 0000)
  (BLE: usar após descobrir UUIDs com tools/ble_inspect.py)

Exemplos:
  python tools/tspl_send.py --text "TESTE"                       # dry-run
  python tools/tspl_send.py --text "TESTE" --out teste.prn        # salva arquivo
  python tools/tspl_send.py --text "TESTE" --port COM5 --send     # imprime
  python tools/tspl_send.py --status --port COM5 --send           # consulta status (<ESC>!?)
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from pt260.tspl import Label, Media, check_safe, inventory_label, status_query  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--text")
    ap.add_argument("--item", nargs=3, metavar=("CODIGO", "NOME", "URL"))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--width", type=float, default=40)
    ap.add_argument("--height", type=float, default=30)
    ap.add_argument("--gap", type=float, default=2, help="0 = contínuo")
    ap.add_argument("--black-mark", action="store_true")
    ap.add_argument("--density", type=int, default=8)
    ap.add_argument("--out", help="salvar job em arquivo .prn")
    ap.add_argument("--port", help="porta serial SPP")
    ap.add_argument("--send", action="store_true", help="enviar de fato (sem isso, dry-run)")
    a = ap.parse_args()

    media = Media(a.width, a.height, a.gap, 0, a.black_mark)
    if a.status:
        job = status_query()
    elif a.item:
        job = inventory_label(*a.item, media=media)
    elif a.text:
        job = Label(media=media, density=a.density).text(16, 16, a.text, font="3", mult=2).build()
    else:
        ap.error("use --text, --item ou --status")
    check_safe(job)

    if a.out:
        pathlib.Path(a.out).write_bytes(job)
    if not a.send:
        print(job.decode("ascii", errors="replace").replace("\x1b", "<ESC>"))
        print("\n[dry-run] nada enviado. Use --port ... --send para imprimir.", file=sys.stderr)
        return
    if not a.port:
        ap.error("--send exige --port")
    try:
        import serial  # pyserial
    except ImportError:
        sys.exit("python -m pip install pyserial")
    with serial.Serial(a.port, 9600, timeout=2) as s:
        s.write(job)
        s.flush()
        if a.status:
            time.sleep(0.5)
            resp = s.read(8)
            print("status bytes:", resp.hex(" ") or "<sem resposta>")


if __name__ == "__main__":
    main()
