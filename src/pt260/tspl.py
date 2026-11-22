"""Gerador de jobs TSPL para a PT-260.

Fonte do dialeto: página de autoteste da unidade ("App: TSPL+CPCL", firmware 6137)
e manual público TSPL/TSPL2 da TSC. Clones baratos implementam subconjuntos do
TSPL; cada comando abaixo deve ser confirmado na unidade antes de uso em volume.

Nada aqui fala com hardware: só monta bytes. O envio fica em tools/tspl_send.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field

DOTS_PER_MM = 8  # 203 dpi

# Comandos que alteram firmware/flash/fábrica ou contadores persistentes.
DENYLIST_PREFIXES = (
    "DOWNLOAD",       # grava arquivo/programa na memória da impressora
    "KILL",           # apaga arquivos da memória
    "MOVE",           # move arquivos entre memórias
    "RUN",            # executa programa armazenado
    "INITIALPRINTER", # reset de fábrica
    "SET COUNTER",
    "SET RESPONSE",
    "SET COM1",
    "SET KEY",
    "SET HEAD",
    "SET PRINTKEY",
    "SET REPRINT",
    "~!F",            # lista/gerência de arquivos (dialetos)
)


class UnsafeCommand(ValueError):
    pass


def check_safe(job: bytes) -> None:
    for raw in job.split(b"\n"):
        line = raw.strip().decode("ascii", errors="replace").upper()
        if any(line.startswith(p) for p in DENYLIST_PREFIXES):
            raise UnsafeCommand(f"comando bloqueado pela denylist: {line[:40]!r}")


def _q(text: str) -> str:
    """Aspas TSPL: aspas internas viram \\["] (sintaxe TSPL2)."""
    if any(ord(c) > 126 for c in text):
        text = text.encode("ascii", "replace").decode("ascii")  # fontes 1..8 só ASCII
    return '"' + text.replace('"', '\\["]') + '"'


@dataclass
class Media:
    width_mm: float = 40
    height_mm: float = 30
    gap_mm: float = 2          # 0 => contínuo
    gap_offset_mm: float = 0
    black_mark: bool = False   # True => BLINE em vez de GAP

    def commands(self) -> list[str]:
        cmds = [f"SIZE {self.width_mm:g} mm,{self.height_mm:g} mm"]
        if self.black_mark:
            cmds.append(f"BLINE {self.gap_mm:g} mm,{self.gap_offset_mm:g} mm")
        else:
            cmds.append(f"GAP {self.gap_mm:g} mm,{self.gap_offset_mm:g} mm")
        return cmds


@dataclass
class Label:
    media: Media = field(default_factory=Media)
    density: int = 8           # 0..15
    direction: int = 1
    body: list[str] = field(default_factory=list)

    def text(self, x: int, y: int, value: str, font: str = "3", mult: int = 1) -> "Label":
        self.body.append(f"TEXT {x},{y},{_q(font)},0,{mult},{mult},{_q(value)}")
        return self

    def qrcode(self, x: int, y: int, data: str, cell: int = 4, ecc: str = "M") -> "Label":
        self.body.append(f"QRCODE {x},{y},{ecc},{cell},A,0,{_q(data)}")
        return self

    def box(self, x0: int, y0: int, x1: int, y1: int, thick: int = 2) -> "Label":
        self.body.append(f"BOX {x0},{y0},{x1},{y1},{thick}")
        return self

    def build(self, copies: int = 1) -> bytes:
        if not 0 <= self.density <= 15:
            raise ValueError("density fora de 0..15")
        lines = [
            *self.media.commands(),
            f"DIRECTION {self.direction},0",
            "REFERENCE 0,0",
            f"DENSITY {self.density}",
            "CLS",
            *self.body,
            f"PRINT 1,{int(copies)}",
        ]
        job = ("\r\n".join(lines) + "\r\n").encode("ascii")
        check_safe(job)
        return job


def inventory_label(code: str, name: str, url: str, media: Media | None = None) -> bytes:
    """Layout do inventário: QR à esquerda, código e nome à direita."""
    media = media or Media()
    w = int(media.width_mm * DOTS_PER_MM)
    h = int(media.height_mm * DOTS_PER_MM)
    margin = 2 * DOTS_PER_MM
    qr_cell = 4 if h >= 200 else 3
    lbl = Label(media=media)
    lbl.qrcode(margin, margin, url, cell=qr_cell)
    # URL ~60 chars alfanuméricos + ECC M => QR versão 4 (33 módulos) => 33*cell dots
    tx = margin + 33 * qr_cell + 12
    lbl.text(tx, margin, code, font="3")
    words, line, y = name.split(), "", margin + 40
    max_chars = max(6, (w - tx - margin) // 12)
    for word in words:
        cand = f"{line} {word}".strip()
        if len(cand) > max_chars and line:
            lbl.text(tx, y, line, font="2")
            y += 28
            line = word
            if y > h - margin - 24:
                line = ""
                break
        else:
            line = cand
    if line:
        lbl.text(tx, y, line, font="2")
    return lbl.build()


# Diagnóstico de mídia (enviar só após o teste de autoteste/etiqueta opaca passar)
def gap_calibration() -> bytes:
    """GAPDETECT: a impressora avança papel e aprende o gap (TSPL2)."""
    return b"GAPDETECT\r\n"


def status_query() -> bytes:
    """<ESC>!? — status em tempo real (1 byte) em TSPL2. Só leitura."""
    return b"\x1b!?"
