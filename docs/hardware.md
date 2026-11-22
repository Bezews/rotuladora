# Ficha de evidências — unidade do proprietário

> Preencher com o que for **[OBSERVADO]**. Não publicar MAC completo nem serial: usar `XX:XX:XX:XX:AB:CD`.

| Campo | Valor | Fonte (foto/app/comando) | Confiança |
|---|---|---|---|
| Texto literal da etiqueta inferior | | | |
| Fabricante/OEM, ANATEL/FCC ID | | | |
| Nome comercial na caixa | PT260 / XD-210 (relato) | relato do proprietário | baixa |
| Tem visor? Botões? LEDs? | | | |
| Porta (USB-C/micro) — dados ou só carga? | | | |
| App indicado (caixa/QR/manual) | | | |
| Versão do app e SO do celular | | | |
| Nome anunciado no Bluetooth | | nRF Connect / `ble_inspect.py` | |
| Serviços GATT | | `ble_inspect.py` | |
| Device Information (0x180A): fabricante/modelo/firmware | | `ble_inspect.py` | |
| USB VID:PID (se houver dados) | | `lsusb` / Gerenciador de Dispositivos | |
| Largura máx. do rolo / diâmetro | | régua | |
| Rolo opaco que funciona (marca, tamanho) | | | |
| Rolo transparente que falha (marca, tamanho, liner) | | | |

## Comandos de inspeção (somente leitura)

**Android (recomendado):** app *nRF Connect* → Scanner → anotar nome, serviços, características (propriedades R/W/N). Não usar "Write".

**PC (Linux/macOS/Windows) com Python:**

```bash
python -m pip install bleak
```

```bash
python tools/ble_inspect.py --scan
```

```bash
python tools/ble_inspect.py --name PT260
```

**Windows (PowerShell):**

```powershell
Get-PnpDevice -PresentOnly | Where-Object { $_.FriendlyName -match 'Printer|Bluetooth|USB|Serial|COM' } | Select-Object Class, FriendlyName, InstanceId, Status
```

**Linux:** `lsusb` e `bluetoothctl devices`. **macOS:** `system_profiler SPUSBDataType SPBluetoothDataType`.
