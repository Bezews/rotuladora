# Fontes pesquisadas (22/11/2026)

## Protocolos e código de referência

- Phomemo M110/M120/M220 — CUPS/Linux: https://github.com/vivier/phomemo-tools (fork: https://github.com/taylorjdlee/phomemo-tools)
- Phomemo M110 — Python/BLE (escrita em `0xFF02`, blocos de 128 B): https://github.com/mkuhlmann/pyphomemo
- Marklife — SDK oficial BLE (P50S, protocolos `0x1F`/`0x10`, `FF02`/`FF03`): https://www.npmjs.com/package/marklife-label-printer-web-kit · https://gitlab.com/marklife/marklife-label-printer-web-kit
- LaBLEr — app Android aberto para Marklife P15/P12/L13: https://f-droid.org/en/packages/io.github.toolicious.labler/
- NIIMBOT — Web Bluetooth: https://github.com/iscarelli/niimbot-web-bluetooth
- Catálogo comunitário de hardware: https://opentlp.github.io/table-of-hardware/index.html
- Metodologia de engenharia reversa BLE em térmicas similares:
  - Fichero/AiYin D11: https://hackaday.com/2026/03/09/reverse-engineering-the-bluetooth-fichero-thermal-label-printer-protocol
  - Cat printer: https://werwolv.net/blog/cat_printer
  - https://parzivail.github.io/ble-thermal-printer

## PT260 — fontes comerciais (não definitivas)

- Manuais PT260 citando app **Marklife/DLabel**: https://manuals.plus/ae/1005008871929138 · https://manuals.plus/ae/1005008087721332 (não acessíveis deste ambiente; conteúdo via resultado de busca)
- Listagens PT-260 (58 mm, iOS/Android/Windows): https://officesolution.al/en/label-printers/9186-pt-260-bluetooth-label-printer.html · https://www.gamers-stop.com/products/pt-260-bluetooth-portable-label-thermal-printer-compatible-with-ios-android-windows
- GS-PT260 (58 mm, ESC/POS): https://www.magazinevoce.com.br/clubepresidente/mini-etiqueta-termica-58mm-impressora-portatil-bluetooth-goldensky/p/cb43gk44gg/in/ipst/?seller_id=goldenskycombr
- PT260 20–50 mm: https://www.magazineluiza.com.br/impressora-bluetooth-10-rolos-etiquetas-adesivas-50x30-titannet/p/hbd60hh16e/in/ipst/
- ETIKEZ PM260 (app Labelnize; modelo relacionado, não igual): https://www.amazon.com/ETIKEZ-PM260-Bluetooth-Portable-Organization/dp/B0FPCC1829

## Phomemo M110 — oficial

- https://phomemo.com/pages/m110-support-center
- https://phomemo.com/collections/labels-for-m110-m120

## Lacunas

- Nenhum teardown público da M110 ou PT260 (MCU desconhecido).
- Nenhuma documentação oficial do protocolo PT260.
