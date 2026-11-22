# rotuladora — PT-260 lab

Diagnóstico e driver da rotuladora térmica **PT-260** para imprimir etiquetas (texto + QR Code) do inventário doméstico `inventario.caiobezerra.com`.

> **Status:** protocolo identificado por evidência física; driver TSPL experimental pronto, sem teste em hardware ainda.
> Marcadores: **[OBSERVADO]** (visto na unidade), **[REFERENCIADO]** (fonte pública), **[HIPÓTESE]**.

## Achado decisivo (22/11/2026)

Página de autoteste da unidade **[OBSERVADO]**:

```text
Model: PT-260   Version: 6137   App: TSPL+CPCL
BT NAME: PT-260_FE9C   PIN: 0000
```

App de diagnóstico: **TSPL suportado, CPCL suportado, ESC/POS não suportado**.

Conclusões:

1. A PT-260 **não** é uma Phomemo M110 rebatizada. A M110 usa protocolo proprietário (`1F xx`, `1B 4E xx`, raster ESC/POS); a PT-260 roda firmware **TSPL/CPCL**, outra família.
2. **TSPL é uma linguagem aberta e documentada** (TSC). Não há protocolo a descobrir: o driver gera texto ASCII (`SIZE`, `GAP`, `TEXT`, `QRCODE`, `PRINT`).
3. "Transformar em M110" deixa de fazer sentido: seria trocar um padrão aberto por um proprietário. Firmware e hardware **não serão alterados**.
4. Bluetooth **dual-mode confirmado** (nRF Connect): Classic SPP (PIN `0000`) + LE com serviços `0x18F0`, `0xFF00`, `e7810a71…` e `49535343…` (Microchip Transparent UART). GATT conecta sem pareamento → Web Bluetooth viável.
5. Firmware novo/backup avaliado em [`docs/firmware-analise.md`](docs/firmware-analise.md): etiqueta colorida **não** depende de firmware; backup exige abrir a placa e quase sempre esbarra em proteção de leitura.

## Decisão de escopo

| Caminho | Veredito |
|---|---|
| Cross-flash do firmware M110 | **Rejeitado** — famílias de firmware diferentes, risco de *brick*, ganho nulo |
| Trocar placa por placa M110 | **Rejeitado** — inviável e desnecessário |
| **Driver TSPL próprio** | **Adotado** — `src/pt260/tspl.py` |
| Ponte "finge ser M110" | **Arquivado** — sem motivo, TSPL já é aberto |

Detalhes: [`docs/00-escopo-e-decisao.md`](docs/00-escopo-e-decisao.md).

## Uso rápido

```bash
python tools/tspl_send.py --item FER-0042 "Furadeira de impacto" "HTTPS://INVENTARIO.CAIOBEZERRA.COM/I/FER-0042/TOKEN"
```

Sem `--send`, só mostra o job (dry-run). Para imprimir pelo PC via Bluetooth Classic (porta serial pareada):

```bash
python tools/tspl_send.py --text "TESTE" --port COM5 --send
```

No Android: [`docs/android-ferramentas.md`](docs/android-ferramentas.md). Teste direto pelo Chrome: [`web/teste-bluetooth.html`](web/teste-bluetooth.html) (precisa de HTTPS — ex.: GitHub Pages).

## Mapa

```text
docs/
  00-escopo-e-decisao.md     decisão e alternativas
  hardware.md                ficha de evidências da unidade (observado)
  android-ferramentas.md     nRF Connect, HCI log, Serial Bluetooth Terminal
  firmware-analise.md        backup/firmware novo: viabilidade e riscos
  protocol-notes.md          TSPL usado + denylist; dialetos Phomemo/Marklife como referência
  compat-matrix.md           PT-260 x Phomemo x NIIMBOT x Marklife
  media-tests.md             diagnóstico da etiqueta transparente (GAPDETECT etc.)
  transport-observations.md  BLE/SPP observado (a preencher)
  inventario-integracao.md   integração com inventario.caiobezerra.com
  risk-register.md, roadmap.md, research-links.md
  fonte/handoff-original-2026-11-21.md
src/pt260/tspl.py            gerador TSPL + denylist
tools/tspl_send.py           dry-run / .prn / envio SPP
tools/ble_inspect.py         inspeção BLE somente leitura
web/teste-bluetooth.html     Web Bluetooth: lista GATT, imprime TSPL, GAPDETECT, status
tests/                       pytest (sem hardware)
```

## Regras de segurança

1. Denylist TSPL ativa no código: `DOWNLOAD`, `KILL`, `MOVE`, `RUN`, `INITIALPRINTER`, `SET COUNTER` etc.
2. Nunca usar ferramenta de atualização de firmware.
3. Nunca versionar MAC completo, serial, capturas ou tokens (`captures/` no `.gitignore`).
