# Roadmap

| Sprint | Entrega | Aceite | Status |
|---|---|---|---|
| 0 — Dados | Fotos, autoteste, app | Unidade identificada | ✅ 22/11 (modelo, fw 6137, TSPL+CPCL, BT) |
| 1 — Transporte | nRF Connect (UUIDs BLE) + Serial Bluetooth Terminal (SPP) | `transport-observations.md` preenchido | 🟡 serviços BLE observados; faltam características e 1ª impressão |
| 2 — Protocolo | TSPL confirmado por autoteste | Etiqueta manual TSPL impressa | 🟡 identificado; falta teste prático |
| 3 — Driver | `src/pt260/tspl.py` + `tools/tspl_send.py` + denylist + testes | 10 etiquetas opacas seguidas, previsíveis | 🟡 código pronto, sem hardware |
| 3b — Mídia | Sequência GAPDETECT/contínuo (`media-tests.md`) | Transparente alinha 3× ou limite físico documentado | ⏳ |
| 4 — Inventário | Rota TSPL no inventário + Web Bluetooth (Android Chrome) | Criar item → etiqueta impressa, repetível | ⏳ protótipo em `web/teste-bluetooth.html` |
| — Firmware | Backup/firmware novo | — | ❌ não recomendado (`firmware-analise.md`) |
| 5 — Ponte M110 | — | — | ❌ arquivado (TSPL aberto torna desnecessário) |

## Perguntas abertas (bloqueiam Sprint 0)

1. ~~Texto da etiqueta inferior~~ → PT-260, fw 6137 (respondido).
2. Nome do app usado na captura de tela.
3. ~~Nome Bluetooth~~ → PT-260_FE9C (respondido). Falta: UUIDs BLE.
4. Rolo transparente: marca, tamanho, liner, térmico direto?
5. "Não reconheceu" = erro, avança várias, sai branco, desalinha?
6. Opaca imprime várias vezes seguidas sem falhar?
7. SO preferido para o driver (Windows/macOS/Linux/Android).
