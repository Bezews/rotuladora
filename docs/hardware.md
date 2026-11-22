# Ficha de evidências — unidade do proprietário

> MAC completo **não** é versionado (aparece na página de autoteste; foto fica fora do repo). Sufixo `FE:9C` já é público no nome Bluetooth.

## Observado em 22/11/2026 (fotos do proprietário)

| Campo | Valor | Fonte | Confiança |
|---|---|---|---|
| Modelo | **PT-260** | etiqueta colada na base + página de autoteste | alta |
| Firmware | **Version 6137** | autoteste (2 impressões) | alta |
| Linguagens de comando | **TSPL + CPCL** (`App: TSPL+CPCL`) | autoteste | alta |
| Teste do app de diagnóstico | TSPL **Support**, CPCL **Support**, ESC1/ESC2 **Not support**, PPLB **Not support** | captura de tela de app de teste de modelo | alta |
| Nome Bluetooth | `PT-260_FE9C` | autoteste + app | alta |
| PIN Bluetooth | `0000` | autoteste | alta |
| MAC | `XX:XX:XX:XX:FE:9C` (anonimizado) | autoteste | alta |
| Densidade (Dark) | 8 em um autoteste, 4 em outro (configurável) | autoteste | alta |
| Tensão bateria | 7745 mV e 8207 mV → pack **2S Li-ion (7,4 V nominal)** | autoteste | alta (inferência elétrica simples) |
| Sensor de temperatura da cabeça | presente (15 °C / 35 °C) | autoteste | alta |
| Marcas regulatórias | CE, FCC (sem FCC ID visível na foto) | foto da base | média |
| Mídia que funciona | etiqueta branca opaca, liner azul-esverdeado, separada por **gap** | foto do rolo | alta |
| Sistema do celular na captura | iOS (barra de status) | captura de tela | alta |
| Bluetooth | **dual-mode (Classic + LE)**; serviços `0x18F0`, `0xFEE7`, `0xFF00`, `e7810a71…`, `49535343…` (ISSC Transparent UART); GATT sem bond | nRF Connect (Android) | alta |

## Implicações

1. **TSPL/CPCL ≠ protocolo Phomemo.** A M110 usa protocolo proprietário estilo ESC/POS com comandos `1F xx` e `1B 4E xx`. A PT-260 recusa ESC no teste do app. São famílias de firmware diferentes: **não** é M110 rebatizada.
2. **TSPL é linguagem aberta e documentada** (TSC TSPL/TSPL2). Não há protocolo a descobrir por engenharia reversa: dá para gerar jobs em texto puro.
3. **PIN 0000** = perfil Bluetooth Classic SPP. nRF Connect confirmou **dual-mode** (Classic + LE) com cinco serviços de dados — ver `transport-observations.md`.
4. Bateria 2S (≈7,4 V) e cabeça com sensor térmico: perfil de impressora "industrial portátil" chinesa genérica com firmware TSPL, não de rotuladora de consumo estilo Phomemo/NIIMBOT.

## Pendente

| Campo | Como obter |
|---|---|
| Características BLE de cada serviço (propriedades) | expandir serviços no nRF Connect ou usar `web/teste-bluetooth.html` |
| Nome do app usado na captura de tela | informar |
| Rolo transparente: marca, medidas, liner, térmico direto? | foto da caixa/rolo |
| Medidas exatas da etiqueta opaca (L×A, gap) | régua |
| USB transmite dados? | ligar no PC e checar Gerenciador de Dispositivos / `lsusb` |
