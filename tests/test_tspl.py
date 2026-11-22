import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import pytest
from pt260.tspl import Label, Media, inventory_label, check_safe, UnsafeCommand


def test_basic_job_structure():
    job = Label().text(10, 10, "A").build()
    lines = job.decode().split("\r\n")
    assert lines[0] == "SIZE 40 mm,30 mm"
    assert lines[1] == "GAP 2 mm,0 mm"
    assert "CLS" in lines
    assert lines[-2] == "PRINT 1,1"
    assert job.endswith(b"\r\n")


def test_black_mark_and_continuous():
    assert b"BLINE 3 mm,0 mm" in Label(media=Media(gap_mm=3, black_mark=True)).build()
    assert b"GAP 0 mm,0 mm" in Label(media=Media(gap_mm=0)).build()


def test_quote_escaping_and_ascii():
    job = Label().text(0, 0, 'a"b').build()
    assert b'"a\\["]b"' in job
    job = Label().text(0, 0, "ação").build()
    job.decode("ascii")  # não lança


def test_inventory_label_has_qr_and_code():
    job = inventory_label("FER-0042", "Furadeira de impacto", "HTTPS://INVENTARIO.CAIOBEZERRA.COM/I/FER-0042/ABCDEFGHIJ")
    assert b"QRCODE 16,16,M,4,A,0,\"HTTPS://INVENTARIO" in job
    assert b'"FER-0042"' in job


@pytest.mark.parametrize("bad", [b"DOWNLOAD \"A.BAS\"\r\n", b"initialprinter\r\n", b"  KILL \"*\"\r\n"])
def test_denylist(bad):
    with pytest.raises(UnsafeCommand):
        check_safe(b"CLS\r\n" + bad)


def test_density_range():
    with pytest.raises(ValueError):
        Label(density=16).build()
