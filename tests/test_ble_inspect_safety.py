"""Garante que a ferramenta de inspeção nunca escreve nem assina notificações."""
import ast
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "tools" / "ble_inspect.py"
FORBIDDEN = {"write_gatt_char", "write_gatt_descriptor", "start_notify"}


def test_no_write_calls():
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    called = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert not (called & FORBIDDEN), f"chamadas proibidas: {called & FORBIDDEN}"


def test_mac_anonymized_by_default():
    ns: dict = {}
    code = SRC.read_text(encoding="utf-8").split("try:\n    from bleak")[0]
    exec(code, ns)  # só imports da stdlib
    src_anon = SRC.read_text(encoding="utf-8")
    fn_src = src_anon[src_anon.index("def anon"):src_anon.index("async def scan")]
    exec(fn_src, ns)
    assert ns["anon"]("12:34:56:78:9A:BC", False) == "XX:XX:XX:XX:9A:BC"
    assert ns["anon"]("12:34:56:78:9A:BC", True) == "12:34:56:78:9A:BC"
