# Roadmap

| Sprint | Entrega | Aceite | Status |
|---|---|---|---|
| 0 — Dados | Fotos, app, bobinas, cenário de erro | Problema classificado como mídia/sensor, app ou conexão | ⏳ aguardando proprietário |
| 1 — Transporte | `ble_inspect.py` + nRF Connect, VID/PID | Ficha `transport-observations.md` preenchida | ⏳ |
| 2 — Protocolo | Captura HCI do app oficial imprimindo "A" | Dialeto confirmado (Marklife? outro?) com bytes observados | ⏳ |
| 3 — Driver | `transport/`, `protocol/`, `renderer/`, perfil `pt260`, allowlist+denylist | 10 etiquetas opacas seguidas, previsíveis | ⏳ |
| 4 — Inventário | Web Bluetooth ou agente local; template 40×30 com QR | Criar item → etiqueta impressa, repetível | ⏳ |
| 5 — Opcional | Ponte ESP32 "M110" | App Phomemo imprime via ponte | ❔ só se desejado |

## Perguntas abertas (bloqueiam Sprint 0)

1. Texto literal da etiqueta inferior (PT260, XD-210, GS-PT260?).
2. App que acompanha (DLabel/Marklife? MLabel? outro?).
3. Nome Bluetooth exato.
4. Rolo transparente: marca, tamanho, liner, térmico direto?
5. "Não reconheceu" = erro, avança várias, sai branco, desalinha?
6. Opaca imprime várias vezes seguidas sem falhar?
7. SO preferido para o driver (Windows/macOS/Linux/Android).
