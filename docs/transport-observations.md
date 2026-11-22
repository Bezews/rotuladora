# Observações de transporte

> Somente dados **[OBSERVADO]** desta unidade. MAC anonimizado (`XX:XX:XX:XX:FE:9C`).

## Bluetooth — nRF Connect (Android), 22/11/2026

| Campo | Valor |
|---|---|
| Nome anunciado | `PT-260_FE9C` (Complete Local Name) |
| Device type | **CLASSIC and LE** (dual-mode confirmado) |
| Flags | `0x0A` — LE General Discoverable; LE + BR/EDR capable (controller) |
| Advertising | Legacy, intervalo ~185 ms, RSSI -49/-55 dBm a curta distância |
| UUIDs anunciados | 16-bit `0x18F0`; 128-bit `e7810a71-73ae-499d-8c15-faa9aef0c3f2` |
| Manufacturer data | Company ID `0x5A47` (reservado/não atribuído pelo SIG) + 6 bytes = próprio MAC |
| Bonding | conexão GATT funcionou **sem pareamento** (NOT BONDED) |

### Serviços GATT primários (conectado)

| UUID | Leitura técnica | Confiança |
|---|---|---|
| `0x1800` | Generic Access (padrão) | observado |
| `0x18F0` | Serviço de impressão comum em módulos BLE de impressoras térmicas chinesas; costuma ter `0x2AF1` (write) e `0x2AF0` (notify) | serviço observado; características **[HIPÓTESE]** |
| `0xFEE7` | Serviço atribuído à Tencent (WeChat/AirSync) — presente em firmwares de módulo BLE chinês | observado |
| `0xFF00` | Serviço genérico de fornecedor; costuma ter `0xFF01`/`0xFF02`/`0xFF03` | serviço observado; características **[HIPÓTESE]** |
| `e7810a71-73ae-499d-8c15-faa9aef0c3f2` | UUID muito difundido em impressoras térmicas genéricas; característica típica `bef8d6c9-9c21-4c9e-b632-bd58c1009f9f` (write + notify) | serviço observado; característica **[HIPÓTESE]** |
| `49535343-fe7d-4ae5-8fa9-9fafd205e455` | **Microchip/ISSC Transparent UART** (módulos IS1678/BM7x e clones). TX `49535343-8841-43f4-a8d4-ecbe34729bb3` (write), RX `49535343-1e4d-4bd9-ba61-23c647249616` (notify) | serviço observado; características **[REFERENCIADO]** pela documentação Microchip |

Aba SERVER mostra só `0x1800`/`0x1801` do próprio celular — irrelevante.

### Leitura

- Quatro serviços de dados diferentes no mesmo aparelho = firmware de módulo BLE "universal" que expõe todos os perfis que os apps chineses procuram. Qualquer um deles provavelmente leva ao mesmo UART interno, que entrega bytes ao interpretador TSPL/CPCL.
- Conexão sem bond → **Web Bluetooth no Chrome Android funciona sem pareamento prévio**.
- `49535343…` (Transparent UART) é o candidato mais seguro: documentação pública do fabricante do chip.

### Pendente

Expandir no nRF Connect cada serviço (`0x18F0`, `0xFF00`, `e7810a71…`, `49535343…`) e fotografar as características com propriedades (WRITE, WRITE NO RESPONSE, NOTIFY). Ou usar `web/teste-bluetooth.html`, que lista tudo automaticamente.

## USB

| SO | VID:PID | Classe | Observação |
|---|---|---|---|
| | | | não testado |

## Testes de impressão

| Data | Transporte | Serviço/característica | Job | Resultado |
|---|---|---|---|---|
| | | | | |
