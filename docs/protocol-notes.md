# Notas de protocolo

## 0. Resultado (22/11/2026)

**[OBSERVADO]** Autoteste da unidade: `App: TSPL+CPCL`, firmware `6137`. App de diagnóstico: TSPL e CPCL suportados; ESC/POS e PPLB não.

Consequência: a PT-260 usa **TSPL** (linguagem da TSC, texto ASCII, documentada publicamente) e **CPCL** (linguagem estilo Zebra móvel). Não usa o protocolo proprietário da Phomemo M110 nem o dialeto `0x1F` da Marklife. A hipótese "família Marklife" da primeira versão destas notas está **descartada**.

## 1. TSPL — subconjunto usado pelo driver

Referência: manual TSPL/TSPL2 da TSC **[REFERENCIADO]**. Clones implementam subconjuntos: cada comando precisa ser confirmado na unidade.

| Comando | Função | Persistente? |
|---|---|---|
| `SIZE w mm,h mm` | tamanho da etiqueta | sim (em muitos firmwares) |
| `GAP g mm,o mm` | etiqueta com gap; `GAP 0,0` = contínuo | sim |
| `BLINE b mm,o mm` | marca preta | sim |
| `DIRECTION d,m` | orientação | não |
| `REFERENCE x,y` | origem | não |
| `DENSITY 0..15` | escurecimento | sim |
| `SPEED n` | velocidade (portáteis costumam ignorar) | sim |
| `CLS` | limpa buffer de imagem | não |
| `TEXT x,y,"font",rot,mx,my,"txt"` | texto (fontes `"1"`..`"8"`) | não |
| `QRCODE x,y,ECC,cell,A,rot,"dados"` | QR Code nativo (sem rasterizar) | não |
| `BITMAP x,y,wBytes,h,mode,dados` | imagem 1-bit | não |
| `BOX`, `BAR` | linhas/retângulos | não |
| `PRINT m,n` | imprime m conjuntos, n cópias | não |
| `FORMFEED`, `HOME` | avança uma etiqueta / acha início | não |
| `GAPDETECT [x,y]` | **calibra sensor de gap** (avança papel) | sim (calibração) |
| `AUTODETECT` | detecção automática de mídia (TSPL2) | sim |
| `SELFTEST` | imprime autoteste | não |
| `<ESC>!?` (`1B 21 3F`) | status 1 byte em tempo real | não |
| `~!T` | nome do modelo | não |

Coordenadas em dots: 203 dpi = 8 dots/mm. Etiqueta 40×30 mm = 320×240 dots.

## 2. Denylist (implementada em `src/pt260/tspl.py`)

| Comando | Motivo |
|---|---|
| `DOWNLOAD` | grava arquivo/programa na flash |
| `KILL`, `MOVE`, `RUN` | apaga/move/executa arquivos armazenados |
| `INITIALPRINTER` | reset de fábrica |
| `SET COUNTER`, `SET RESPONSE`, `SET COM1`, `SET KEY`, `SET HEAD`, `SET PRINTKEY`, `SET REPRINT` | configuração persistente fora do escopo |
| qualquer ferramenta de atualização de firmware do fabricante | risco de *brick* |

## 3. Referência histórica: dialetos que **não** são o da PT-260

Mantido para a matriz de compatibilidade e para uma eventual ponte.

| Função | Phomemo M110 [REFERENCIADO: phomemo-tools/pyphomemo] | Marklife [REFERENCIADO: SDK npm 1.1.4] |
|---|---|---|
| Transporte | BLE, escrita `0xFF02` | BLE, escrita `0xFF02`, créditos `0xFF03` |
| Mídia | `1F 11 <0A gap / 0B contínuo / 26 marca>` | `1F 80 01 <10/20/30>` |
| Densidade | `1B 4E 04 <d>` | `1F 70 01 <1..15>` |
| Raster | `1D 76 30 00 wL wH hL hH` + bitmap | bitmap com compressão proprietária |
| BOOT/firmware | não documentado | `1F A0 BE 66 88` (entra em modo BOOT) |

## 4. CPCL

Suportado pela unidade. Não será usado na v1 (TSPL cobre tudo e tem QR nativo). Registrar caso TSPL apresente limitação.
