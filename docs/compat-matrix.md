# Matriz de compatibilidade

> Três compatibilidades independentes: **mecânica/consumível**, **transporte/protocolo**, **firmware/hardware**. Semelhança visual não prova nenhuma delas.

| Modelo | Largura de etiqueta | Resolução | App oficial | Transporte | Protocolo público | Compat. c/ PT260 |
|---|---|---|---|---|---|---|
| **PT-260 (unidade)** | rolo com gap, opaco funciona [OBSERVADO]; largura a medir | 203 dpi [HIPÓTESE] | app de teste multi-linguagem [OBSERVADO] | BT Classic SPP (PIN 0000) + provável BLE | **TSPL + CPCL** [OBSERVADO, fw 6137] | — alvo |
| Marklife P50/P50S | ~50 mm | 203 dpi | DLabel/Marklife | BLE `FF02/FF03` | SDK npm oficial (dialeto `0x1F`) | Não — hipótese inicial descartada pelo autoteste |
| Phomemo M110 | 20–50 mm | 203 dpi | Print Master | BLE `FF02` + USB | `phomemo-tools`, `pyphomemo` (proprietário) | Carcaça semelhante; **firmware/protocolo de outra família** |
| Phomemo M120 | 20–50 mm | 203 dpi | Print Master | BLE | mesmo protocolo da M110 (phomemo-tools) | idem M110 |
| Phomemo M200/M220 | até 75/80 mm | 203 dpi | Print Master | BLE | phomemo-tools (M220) | Consumível maior; não intercambiável |
| NIIMBOT D110 | 12–15 mm | 203 dpi | NIIMBOT | BLE | `niimbot-web-bluetooth` | Não — outra mecânica |
| NIIMBOT B1/B21 | 20–50 mm | 203 dpi | NIIMBOT | BLE | protocolo NIIMBOT (frames `55 55 … AA AA`) | Não — protocolo próprio; rolos com RFID |
| NIIMBOT B21 Pro | 20–50 mm | 300 dpi (declarado) | NIIMBOT | BLE | parcial | Não |

## Conclusões

1. **Consumível**: rolos de 40–50 mm com gap tendem a servir mecanicamente em PT260 e M110 se o diâmetro do rolo couber — testar, não presumir. NIIMBOT B-series exige RFID no rolo original.
2. **Protocolo**: PT-260 = TSPL/CPCL (padrão aberto TSC/Zebra-like). Phomemo, Marklife e NIIMBOT usam protocolos proprietários distintos. Qualquer software que gere TSPL (BarTender, drivers TSC, bibliotecas `tspl`) é candidato a funcionar com a PT-260.
3. **Firmware**: sem dados. Nenhuma combinação é considerada intercambiável.

Fontes: ver `research-links.md`.
