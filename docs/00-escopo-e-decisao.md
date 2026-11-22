# Escopo e decisão: "fazer a PT-260 funcionar como M110"

## 1. Pedido original

Alterar firmware ou hardware da PT-260 para que ela opere como uma Phomemo M110 (aparência semelhante).

## 2. Evidência que decide a questão

**[OBSERVADO 22/11/2026]** autoteste: `Model PT-260 · Version 6137 · App: TSPL+CPCL`. App de teste: TSPL/CPCL suportados, ESC/PPLB não.

**[REFERENCIADO]** M110: protocolo proprietário estilo ESC/POS via BLE `0xFF02` (`phomemo-tools`, `pyphomemo`).

Aparência semelhante vem de carcaça genérica (molde OEM comum em Shenzhen). Por dentro, firmwares de famílias diferentes.

## 3. Avaliação dos caminhos

| Caminho | Análise | Veredito |
|---|---|---|
| Cross-flash firmware M110 | Exige mesmo MCU, pinagem, cabeça, sensor, bateria (PT-260 usa pack 2S ~7,4 V **[OBSERVADO]**; arquitetura de alimentação da M110 não confirmada), dump e recuperação via SWD. Nenhum disponível. Resultado provável: *brick*. Ganho: trocar padrão aberto (TSPL) por proprietário. | **Rejeitado** |
| Trocar placa | Precisa M110 doadora; incompatibilidade mecânica/elétrica provável. | **Rejeitado** |
| Ponte BLE "M110 → TSPL" (ESP32) | Tecnicamente possível, mas só serviria para usar o app Phomemo. Sem benefício real. | **Arquivado** |
| **Driver TSPL próprio** | Linguagem documentada, QR nativo, texto puro, testável sem hardware. | **Adotado** |

## 4. Plano

1. Confirmar transporte (nRF Connect; Serial Bluetooth Terminal) — `android-ferramentas.md`.
2. Imprimir etiqueta de teste TSPL manual.
3. Diagnosticar etiqueta transparente com `GAPDETECT`/modos de mídia — `media-tests.md`.
4. Integrar gerador TSPL ao inventário (Web Bluetooth no Android ou agente local) — `inventario-integracao.md`.

## 5. Fora do escopo

Flash de firmware, ferramentas de atualização do fabricante, `DOWNLOAD`/`INITIALPRINTER`/`KILL`, abertura do equipamento.
