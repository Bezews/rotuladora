# Escopo e decisão: "fazer a PT260 funcionar como M110"

## 1. O que o pedido realmente significa

"Funcionar como M110" pode ter três significados diferentes, cada um com solução distinta:

| Interpretação | O que o usuário ganha | Solução adequada |
|---|---|---|
| A. Usar o **app Phomemo (Print Master)** com a PT260 | Interface/templates da Phomemo | Ponte BLE ou nada; o app precisa reconhecer o aparelho |
| B. Usar **ferramentas abertas da M110** (`phomemo-tools`, `pyphomemo`) | Impressão pelo PC/script | Driver nativo PT260 (mais simples que imitar M110) |
| C. Obter **qualidade/recursos** de M110 | Ex.: sensor melhor p/ transparente | Nenhum firmware resolve limite físico de sensor |

O objetivo real declarado (etiquetas do inventário com QR) é atendido por **B**, sem tocar na impressora.

## 2. Por que não trocar o firmware

**[REFERENCIADO]** Projetos abertos da M110 documentam apenas protocolo (sniffing BLE). Não há dump público de firmware, identificação de MCU, nem teardown da M110 localizados em 22/11/2026.

Para um cross-flash ser sequer avaliável seriam necessários, **todos**:

1. Mesmo MCU/SoC e mesma memória flash nas duas placas (exige abrir ambas).
2. Mesma pinagem para cabeça térmica, motor de passo, sensor de gap, bateria, LED e botão.
3. Mesma cabeça térmica (largura em dots, resistência, *strobe*) — senão sobreaquece ou imprime falho.
4. Backup integral do firmware original (SWD/UART), com restauração testada.
5. Formato da imagem de atualização e eventual assinatura/checksum conhecidos.

Hoje temos **zero de cinco**. Além disso:

- **[REFERENCIADO]** O SDK Marklife (família provável da PT260) expõe `1F A0 BE 66 88` = *Enter BOOT mode*. Isso confirma que o firmware é atualizável via BLE — e que um envio errado pode deixar a impressora em modo bootloader sem imagem válida.
- Firmware M110 dentro da PT260 teria **outro dialeto de comandos** (ver `protocol-notes.md`), logo só o app Phomemo passaria a funcionar; o DLabel deixaria de funcionar.
- Mesmo funcionando, não resolveria o problema da etiqueta transparente se a causa for óptica (sensor/mídia).

**Conclusão:** risco alto, ganho baixo. Fora do escopo.

## 3. Por que não trocar o hardware

Trocar a placa-mãe exige uma M110 doadora. Custo ≥ comprar uma M110, com risco de incompatibilidade mecânica (conectores, flat da cabeça, bateria). Não faz sentido econômico.

## 4. Caminho escolhido

1. **Diagnóstico de mídia** (etiqueta transparente) — `media-tests.md`.
2. **Identificação passiva** (fotos, nome BLE, GATT) — `hardware.md`, `tools/ble_inspect.py`.
3. **Captura do app original** (Android *HCI snoop log*) imprimindo uma etiqueta conhecida.
4. **Confronto** da captura com os dialetos Marklife e Phomemo já documentados.
5. **Driver nativo** com perfil `pt260` e denylist embutida.
6. **Integração** com o inventário via agente local.
7. *(Opcional)* **Ponte M110** em ESP32: anuncia-se como M110, traduz, por exemplo, "mídia gap" Phomemo `1F 11 0A` → Marklife `1F 80 01 20`. Só se o item A da tabela for de fato desejado.

## 5. Fora do escopo (explicitamente)

- Flash de firmware, entrada em BOOT, reset de fábrica.
- Varredura cega de opcodes (*fuzzing*).
- Abrir a impressora antes do Sprint 2 (perde garantia; só se o proprietário autorizar para fotografar a placa).
