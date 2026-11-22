# Notas de protocolo

> Nada aqui foi validado contra a PT260 do proprietário. São dialetos **de referência** para confronto com capturas futuras.

## 1. Comparativo de dialetos conhecidos

| Função | Phomemo M110 **[REFERENCIADO: phomemo-tools / pyphomemo]** | Marklife (DLabel) **[REFERENCIADO: SDK npm oficial 1.1.4]** |
|---|---|---|
| Serviço / escrita BLE | `0xFF00` / escrita `0xFF02` (blocos ~128 B) | escrita `0xFF02` (blocos 90 B) |
| Controle de fluxo | não documentado nos projetos | créditos via notify `0xFF03` |
| Tipo de mídia | `1F 11 <m>` — `0A` gap, `0B` contínuo, `26` marca preta | `1F 80 01 <t>` (set) — `10` contínuo, `20` gap, `30` marca preta; `1F 12 <m> 00` = localizar gap/marca |
| Velocidade | `1B 4E 0D <v>` | `1F 60 01 <0..2>` |
| Densidade | `1B 4E 04 <d>` | `1F 70 01 <1..15>` |
| Raster | `1D 76 30 00 wL wH hL hH` + bitmap (estilo ESC/POS) | bitmap com compressão proprietária |
| Início/fim de job | rodapé `1F F0 05 00`, `1F F0 03 00` | `1F C0 01 00` / `1F C0 01 01` |
| Alinhar papel | — | `1F 11 51` (início) / `1F 11 50` (fim); `1F 11 <m> dH dL` = avanço/recuo manual |
| Aprender papel (calibração) | — | `1F 30 60` |
| Ler sensor óptico | — | `1F 30 02` (reflexão) |
| Status / bateria / versão | — | `1F 20 00`, `10 FF 50 F1`, `10 FF 20 F1` |

Observação: os bytes da M110 vêm da documentação comunitária (README do `phomemo-tools`); **conferir a versão atual do repositório antes de usar**. Os bytes Marklife vêm do pacote npm oficial (licença restritiva: citamos fatos, não copiamos código).

## 2. Leitura analítica

- **Mesmo layout GATT (`FF00/FF02/FF03`)** aparece em muitas térmicas chinesas baratas porque vem do módulo/firmware BLE de referência do fabricante do chip — **não** identifica o fabricante da impressora.
- **Prefixo `0x1F`** comum sugere SDK OEM de mesma origem **[HIPÓTESE]**, mas a semântica do mesmo opcode diverge (`1F 11` = "definir mídia" na Phomemo; "ajustar posição/avançar papel" na Marklife). Enviar comandos de um dialeto ao outro pode ter efeito **diferente do esperado**.
- Consequência para o "modo M110": uma ponte teria de **traduzir** comandos, não só repassá-los.
- Para a etiqueta transparente, o dialeto Marklife expõe exatamente o que interessa: **aprender papel** e **ler valor do sensor óptico**. Se a PT260 for Marklife, dá para medir o contraste do sensor com mídia opaca vs transparente — teste objetivo. Só após confirmação do dialeto por captura.

## 3. Denylist

Comandos que o driver deste projeto **nunca** enviará, independentemente do perfil:

| Bytes | Significado referenciado | Risco |
|---|---|---|
| `1F A0 BE 66 88` | Entrar em modo BOOT (Marklife) | *brick* / bootloader |
| `1F 50 BE` | Reset de fábrica (Marklife) | perda de calibração |
| `10 FF 12 ..` | Alterar tempo de desligamento | alteração persistente |
| qualquer opcode não observado em captura do app original | desconhecido | escrita em flash |

O driver deve operar com **allowlist** por perfil (só bytes vistos em captura) e checar a denylist como segunda barreira.

## 4. Como confirmar o dialeto da PT260 (sem risco)

1. Android → Opções do desenvolvedor → *Ativar registro de snoop HCI Bluetooth*.
2. Abrir o app que acompanha a PT260, conectar, imprimir **uma** etiqueta simples (ex.: texto "A").
3. Gerar *bug report* e extrair `btsnoop_hci.log` → salvar em `captures/` (gitignored).
4. Abrir no Wireshark, filtro `btatt.opcode == 0x52 || btatt.opcode == 0x12` (Write Command/Request).
5. Comparar os primeiros bytes com a tabela acima e registrar em `transport-observations.md` — bytes **observados** separados de interpretação.
