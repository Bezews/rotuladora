# Ferramentas no Android

Ordem de uso. As duas primeiras são **somente leitura**; a terceira envia comandos TSPL documentados.

## 1. nRF Connect for Mobile (Nordic Semiconductor) — descobrir BLE

Play Store: "nRF Connect for Mobile". Gratuito, padrão da indústria.

1. Ligar a PT-260. **Desconectar** do app de impressão (BLE aceita uma conexão por vez).
2. Aba **Scanner** → procurar `PT-260_FE9C` → anotar se aparece (se não aparecer, o BLE pode estar desligado ou o aparelho só fala Classic).
3. **Connect** → aba do dispositivo → expandir cada serviço.
4. Para cada característica anotar: UUID e propriedades (READ, WRITE, WRITE NO RESPONSE, NOTIFY).
5. **Não** tocar nas setas de escrita (↑). Leitura (↓) só no serviço *Device Information* (0x180A).
6. Tirar prints e mandar. Preencher `transport-observations.md`.

Interesse: achar a característica com WRITE / WRITE NO RESPONSE — é por ela que o TSPL entra. Candidatos comuns em módulos chineses: serviço `0x18F0` (caract. `0x2AF1`), `0xFF00` (`0xFF02`), `0xFFE0` (`0xFFE1`), `0xAE30` (`0xAE01`), `49535343-FE7D-…` (módulo Microchip/ISSC). Isso é referência, não observação.

## 2. Registro HCI do Android — capturar o app original (opcional agora)

Com TSPL confirmado, captura deixou de ser obrigatória. Útil só para ver quais comandos TSPL o app manda (tamanho, gap, densidade).

1. Configurações → Sobre o telefone → tocar 7× em "Número da versão".
2. Opções do desenvolvedor → **Ativar registro de rastreamento HCI Bluetooth**.
3. Desligar e ligar o Bluetooth. Imprimir uma etiqueta "A" pelo app.
4. Opções do desenvolvedor → **Relatório de bug** → compartilhar o ZIP para o PC.
5. No ZIP: `FS/data/log/bt/btsnoop_hci.log` (varia por fabricante). Abrir no Wireshark.
6. Guardar em `captures/` (não versionado).

## 3. Serial Bluetooth Terminal (Kai Morich) — primeiro teste TSPL

Play Store: "Serial Bluetooth Terminal". Fala Bluetooth **Classic (SPP)** e **BLE**.

1. Parear a PT-260 nas configurações do Android (PIN `0000`).
2. No app: menu → Devices → aba *Bluetooth Classic* → `PT-260_FE9C`.
3. Settings → Send → *Newline* = **CR+LF**; *Character encoding* = UTF-8/ASCII.
4. Conectar e colar, linha por linha (ou como macro):

```text
SIZE 40 mm,30 mm
GAP 2 mm,0 mm
DIRECTION 1,0
CLS
TEXT 16,16,"3",0,2,2,"TESTE PT-260"
QRCODE 16,90,M,4,A,0,"HTTPS://INVENTARIO.CAIOBEZERRA.COM"
PRINT 1,1
```

Ajustar `SIZE`/`GAP` à etiqueta real (medir com régua). Se imprimir, o transporte e o dialeto estão confirmados na prática.

**Não enviar**: `DOWNLOAD`, `KILL`, `INITIALPRINTER`, `SET COUNTER`, nada de atualização de firmware. Lista completa em `protocol-notes.md`.

## Web (futuro)

Chrome no Android suporta **Web Bluetooth (só BLE)**. Com os UUIDs do passo 1, `inventario.caiobezerra.com` pode imprimir direto do navegador. iPhone: Safari não tem Web Bluetooth (alternativa: navegador Bluefy ou agente local).
