# rotuladora — PT260 / XD-210 lab

Investigação técnica, diagnóstico e futuro driver para a rotuladora térmica **PT260** (também referida como **XD-210**), visualmente semelhante à **Phomemo M110**. Objetivo final: imprimir etiquetas (texto + QR Code) a partir do inventário doméstico `inventario.caiobezerra.com`.

> **Status:** `discovery` — nenhuma afirmação sobre a unidade real foi verificada fisicamente ainda.
> Toda afirmação neste repositório é marcada como **[OBSERVADO]** (visto na unidade), **[REFERENCIADO]** (fonte pública citada) ou **[HIPÓTESE]**.

## Pedido original e decisão de escopo

O pedido inicial foi *"alterar o firmware ou hardware da PT260 para que ela funcione como se fosse uma M110"*. Após análise, a decisão é:

| Caminho | Veredito | Motivo resumido |
|---|---|---|
| Cross-flash do firmware M110 na PT260 | **Rejeitado (alto risco)** | Sem dump, sem bootloader conhecido, sem prova de placa idêntica; risco real de *brick*. O SDK Marklife documenta até um comando de entrada em BOOT (`1F A0 BE 66 88`), prova de que existe caminho de atualização — e de que um byte errado pode acioná-lo. |
| Trocar a placa da PT260 por uma placa M110 | **Inviável economicamente** | Exige comprar uma M110 para canibalizar; mais barato usar a própria M110. |
| **Driver nativo PT260** (software externo, reversível) | **Recomendado** | Zero risco ao hardware; cobre o caso real (inventário). |
| Ponte BLE "finge ser M110" (ex.: ESP32) | **Opcional, fase futura** | Só se for indispensável usar o app Phomemo. Reversível, mas depende de conhecer os dois protocolos. |

Detalhes e justificativas: [`docs/00-escopo-e-decisao.md`](docs/00-escopo-e-decisao.md).

## Achado-chave da pesquisa (22/11/2026)

- Manuais públicos da PT260 indicam o app **DLabel / Marklife** **[REFERENCIADO]**, não o Print Master da Phomemo.
- O SDK oficial Marklife (npm `marklife-label-printer-web-kit`) usa **GATT `0xFF02` (escrita) + `0xFF03` (crédito/fluxo)** e comandos da família **`0x1F xx`** (mídia em `1F 80 01 <tipo>`, posicionamento em `1F 11 …`) **[REFERENCIADO]**.
- A Phomemo M110 (projetos `phomemo-tools`/`pyphomemo`) também escreve em `0xFF02` e usa `1F 11 <modo>` para mídia **[REFERENCIADO]**.
- **Porém a semântica diverge**: o mesmo `1F 11` define mídia na Phomemo e move papel na Marklife; códigos de mídia também diferem (Marklife `0x10/0x20/0x30`; Phomemo `0x0A/0x0B/0x26`). Mesmo layout GATT e mesmo prefixo **não** significam compatibilidade byte a byte — sugere uma linhagem OEM comum com dialetos diferentes **[HIPÓTESE]**.

Análise completa: [`docs/protocol-notes.md`](docs/protocol-notes.md) e [`docs/compat-matrix.md`](docs/compat-matrix.md).

## Mapa do repositório

```text
README.md
docs/
  00-escopo-e-decisao.md     # por que não cross-flash; caminhos avaliados
  hardware.md                # ficha de evidências da unidade (a preencher)
  transport-observations.md  # BLE/USB observado (a preencher)
  protocol-notes.md          # Phomemo vs Marklife; denylist de comandos perigosos
  compat-matrix.md           # PT260 x Phomemo x NIIMBOT x Marklife
  media-tests.md             # diagnóstico da etiqueta transparente
  risk-register.md           # riscos e mitigação
  inventario-integracao.md   # arquitetura com inventario.caiobezerra.com
  roadmap.md                 # sprints e critérios de aceite
  research-links.md          # fontes
  fonte/handoff-original-2026-11-21.md
tools/
  ble_inspect.py             # inspeção BLE SOMENTE LEITURA (scan + GATT)
captures/  (gitignored)      # capturas privadas
fixtures/                    # amostras anonimizadas
```

## Regras de segurança do projeto

1. **Nunca** enviar bytes à impressora antes de identificar o protocolo (Sprint 2).
2. **Nunca** enviar comandos da denylist (`docs/protocol-notes.md#denylist`), em especial BOOT/fábrica.
3. **Nunca** versionar MAC, serial, capturas brutas ou tokens.
4. Firmware: fora de escopo até existirem backup integral + recuperação comprovada (ver `docs/risk-register.md`).

## Próximo passo (bloqueante)

Preencher [`docs/hardware.md`](docs/hardware.md) — principalmente: etiqueta inferior, app que acompanha, nome Bluetooth e saída de `tools/ble_inspect.py`.
