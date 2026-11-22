# Análise: backup do firmware e firmware novo "baseado na M110"

Pergunta do proprietário (22/11/2026): fazer backup do firmware atual e criar um firmware novo, baseado na M110, para testar etiqueta colorida.

## 1. A etiqueta colorida precisa de firmware novo?

**Não.** Etiquetas "coloridas" para M110/PT-260 são papel **térmico direto** com fundo pré-colorido (ou camada térmica que escurece em preto/azul). A impressora só aquece pontos; a cor vem do papel. O firmware não sabe nem precisa saber a cor.

O que muda com mídia colorida/transparente é **óptico**: o sensor de gap enxerga contraste diferente. Isso se resolve com:

1. `GAPDETECT` (calibração do sensor) com a bobina colorida — já documentado em `media-tests.md`.
2. `DENSITY` ajustada (fundos coloridos podem exigir mais calor para contraste).
3. Modo contínuo como contorno.

Mesma lógica: o app da Phomemo tem perfis de "etiqueta colorida", mas esses perfis são só tamanho + tipo de gap + densidade. Em TSPL temos os três comandos.

## 2. É possível fazer backup do firmware?

| Via | Viabilidade | Risco |
|---|---|---|
| Bluetooth/TSPL | **Não existe** comando TSPL de leitura de firmware. Ferramentas de fabricante só **gravam**. | — |
| Atualizador do fabricante | Só grava; não lê. | alto |
| Abrir e ligar SWD/JTAG (ST-Link ~R$ 30) | Possível **se** o MCU for STM32/GD32/similar e a proteção de leitura estiver **desligada**. Em produto comercial, normalmente está ligada. | baixo para *tentar ler*; **altíssimo** para desligar a proteção |
| Desligar proteção de leitura (RDP) | Em STM32/GD32, baixar RDP **apaga a flash inteira** por design. Resultado: impressora sem firmware, sem backup. | **destrói o firmware** |
| Glitch/ataque físico na proteção | Técnica de laboratório; exige equipamento e semanas. | alto |

São dois chips programáveis: o **MCU principal** (motor, cabeça, sensor, TSPL) e o **módulo Bluetooth** (dual-mode, serviço ISSC `49535343…` sugere chip Microchip ou clone). Backup "completo" = os dois.

## 3. É possível criar firmware "baseado na M110"?

Não há firmware da M110 publicado. Mesmo que houvesse, seria para outra placa (outro MCU, outra pinagem, cabeça e bateria diferentes — PT-260 usa pack 2S ~7,4 V **[OBSERVADO]**). "Baseado na M110" na prática significa **escrever um firmware de impressora do zero**:

- driver de motor de passo e sincronização com a linha de impressão;
- controle de *strobe* da cabeça térmica com compensação por temperatura (a PT-260 tem sensor de temperatura) e tensão de bateria — erro aqui **queima a cabeça**;
- sensor de gap, botão, LED, carga de bateria, desligamento automático;
- protocolo BLE da Phomemo (proprietário, só parcialmente documentado por engenharia reversa).

Ordem de grandeza: meses de trabalho de firmware embarcado, com hardware de bancada e alta chance de perder a impressora. Resultado final: o app da Phomemo funcionaria — e nada além disso que o TSPL já não faça.

## 4. Custo x benefício

| Opção | Custo | Benefício | Risco |
|---|---|---|---|
| Firmware novo "M110" | meses + equipamento | usar app Phomemo | perder impressora / queimar cabeça |
| Comprar uma M110 | preço de uma rotuladora | app Phomemo nativo | nenhum |
| **TSPL + calibração (atual)** | horas | etiquetas opacas, coloridas e (talvez) transparentes; integração com inventário | nenhum (comandos documentados, denylist) |

## 5. Recomendação

Não fazer backup invasivo nem firmware novo. Testar a etiqueta colorida **hoje** com TSPL (seção 1). Se o interesse for aprendizado em hardware, o caminho seguro é um "laboratório de leitura":

1. Abrir a impressora e fotografar a placa (perde garantia).
2. Identificar MCU, módulo BT e pads de debug (SWD/UART).
3. Tentar **somente leitura** via SWD. Se a proteção estiver ativa: **parar**. Nunca executar "unlock", "mass erase" ou "RDP level 0".
4. Documentar em `docs/hardware.md`.

Nenhuma escrita em flash em qualquer cenário sem backup íntegro verificado e restauração testada.
