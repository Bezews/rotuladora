---
title: "PT260 / XD-210 — Diagnóstico e engenharia reversa de impressora térmica"
date: 2026-11-21
status: discovery
owner: "Projeto pessoal — Inventário"
repository_target: "A definir (possível integração com inventario.caiobezerra.com)"
language: pt-BR
---

# PT260 / XD-210: investigação técnica e continuidade no Claude Code

> **Handoff para Claude Code.** Este documento consolida o relato do proprietário, a comparação preliminar com Phomemo e NIIMBOT, evidências públicas e um roteiro técnico **não destrutivo**. O objetivo não é presumir compatibilidade nem trocar firmware prematuramente.

## 0. Pedido principal ao Claude Code

Atue como engenheiro de software/hardware com experiência em impressoras térmicas, Bluetooth LE/Classic, USB, protocolos de impressão e engenharia reversa. Execute a pesquisa e a implementação por etapas, preservando a segurança do dispositivo. **Primeiro descubra que hardware/protocolo o equipamento realmente usa; só depois proponha um driver.**

**Entregáveis desejados:**

1. Diagnóstico da falha com etiquetas transparentes, incluindo testes que separem problema físico/sensor de problema de comunicação/app.
2. Identificação verificável da PT260/XD-210 (variante, identificadores Bluetooth/USB, transporte e protocolo).
3. Matriz fundamentada de compatibilidade com Phomemo M110/M120/M200/M220 e NIIMBOT D110/B1/B21/B21 Pro.
4. Protótipo de driver/ponte de impressão independente, **somente após identificação do protocolo**.
5. Caminho de integração com `https://inventario.caiobezerra.com` para etiquetas de inventário, texto e QR Code.
6. Relatório de evidências, testes e limitações; nunca concluir que dois aparelhos são iguais por semelhança visual.

## 1. Contexto fornecido pelo proprietário (observações diretas)

- Impressora adquirida: **PT260**; também é identificada/referida como **XD-210**.
- Percepção do proprietário: aparência semelhante à **Phomemo M110**.
- Teste realizado: **conseguiu usar/imprimir em etiqueta transparente uma vez**; nas tentativas posteriores a impressora **não reconheceu a etiqueta transparente**.
- Objetivos: saber se PT260, Phomemo e NIIMBOT compartilham hardware e só mudam o software; avaliar reaproveitamento do app/protocolo Phomemo; investigar engenharia reversa.
- Contexto futuro: geração de etiquetas para o inventário doméstico, incluindo ferramentas, ventiladores e controles remotos, no sistema `inventario.caiobezerra.com`.

**Ainda não fornecido:** foto da etiqueta de identificação, número de série/revisão, foto da bobina, marca/composição do material, modelo do celular/computador, aplicativo em uso, nome anunciado no Bluetooth, VID/PID USB, serviços GATT, mensagens de erro e tamanho da etiqueta. Não inventar nenhum desses dados.

## 2. Conclusões provisórias e graus de certeza

| Questão | Estado | Justificativa/ação |
|---|---|---|
| PT260 e XD-210 são exatamente o mesmo hardware | **Não confirmado** | Nomes comerciais variam; exigem inspeção física/identificadores. |
| PT260 é uma Phomemo M110 com outra marca | **Não confirmado** | Design e 203 dpi não provam placa, protocolo ou firmware idênticos. |
| PT260 usa TSPL | **Hipótese a testar** | Alguns tutoriais/anúncios falam em modo `TSPL`; não extrapolar para todas as unidades. |
| PT260 usa ESC/POS | **Há anúncio de uma variante GS-PT260** | Goldensky GS-PT260 é anunciada como impressora térmica 58 mm, 203 dpi e ESC/POS; pode não ser a unidade do proprietário. |
| Problema da etiqueta transparente é firewall | **Improvável** | Firewall do PC não controla sensor óptico de papel; Bluetooth e impressora precisam ser testados separadamente. |
| Problema é detecção/calibração de mídia | **Hipótese principal** | Transparência pode reduzir contraste óptico entre etiqueta, intervalo e liner. |
| Phomemo tem protocolo estudado publicamente | **Confirmado em projetos abertos** | Ver `phomemo-tools` e `pyphomemo` nas referências. |
| NIIMBOT tem protocolo estudado publicamente | **Confirmado em projeto aberto** | Ver `niimbot-web-bluetooth` nas referências. |
| É seguro instalar firmware Phomemo M110 na PT260 | **Não demonstrado; evitar** | Possível brick por diferenças de bootloader, memória, sensores, pinagem e revisão. |

**Nota sobre fontes comerciais:** foram encontrados anúncios diferentes sob a designação PT260: alguns descrevem etiquetadora de **20–50 mm** com bobina de etiquetas; outro descreve **GS-PT260** com papel de **58 mm**, largura de impressão de **48 mm/384 dots** e ESC/POS. Esta divergência pode representar variantes distintas ou erros dos anúncios. Não consolidar especificações incompatíveis como se fossem uma única ficha técnica.

## 3. Problema das etiquetas transparentes — investigação

### 3.1 Hipóteses ordenadas

1. **Sensor de gap/black-mark inadequado ou descalibrado:** o conjunto etiqueta transparente + liner não oferece contraste suficiente.
2. **Modo de mídia incorreto:** impressora/app configurado como `Gap`, `Continuous` ou `Black Mark` em desacordo com a bobina.
3. **Dimensão/avanço incorretos:** largura, comprimento, deslocamento ou direção de impressão inadequados.
4. **Bobina fora de posição ou sensor sujo:** rolo desalinhado, folga no guia, obstrução de sensor.
5. **Mídia não térmica:** algumas etiquetas transparentes exigem ribbon/transferência térmica, que a impressora térmica direta não possui. Isso explicaria impressão em branco, **não necessariamente erro de reconhecimento**.
6. **Problema no firmware do modelo concreto:** somente investigar após testes de papel/sensor/app.

### 3.2 Plano de teste seguro

- [ ] Fotografar a bobina instalada e a caixa/identificação do material.
- [ ] Confirmar se a impressora imprime **várias** etiquetas opacas em sequência usando configuração atual.
- [ ] Repetir com a etiqueta transparente, registrando: erro exato, avanço físico, luz/LED, conteúdo impresso e necessidade de reiniciar.
- [ ] Conferir se o liner é opaco, translúcido ou transparente, e se há marca preta ou espaço entre etiquetas.
- [ ] Verificar se a **própria mídia** é para *direct thermal* (sem ribbon) e se a camada térmica escurece com calor de forma segura e controlada (não usar chama).
- [ ] Testar `Gap` com bobina realmente separada por gaps; `Black Mark` só com marcas reais; `Continuous` + comprimento fixo **apenas como teste**, se disponível.
- [ ] Procurar rotina de calibração **específica do manual da PT260 exata**. Não reutilizar combinação de botões da M110 sem comprovação.
- [ ] Limpar gentilmente sensor e rolete com equipamento desligado, seguindo manual do fabricante.
- [ ] Registrar resultado de cada combinação em `docs/media-tests.csv` ou `docs/media-tests.md`.

**Interpretação:** se opacas funcionam repetidamente e a transparente perde o posicionamento, suspeita de mídia/sensor aumenta. Se a transparente avança corretamente mas sai em branco, investigar compatibilidade térmica. Se ambas falham, verificar alimentação, bateria, conexão e app.

## 4. Famílias de produtos a comparar

> **Comparação aproximada, não prova de compatibilidade.** Verificar dados sempre em documentação oficial por revisão de modelo.

| Família | Modelos | Razão para investigar | Atenções |
|---|---|---|---|
| PT260/XD-210 | PT260, XD-210; possivelmente GS-PT260 | Dispositivo real, alvo principal | Identidade/protocolo variam entre anúncios |
| Phomemo | M110, M120 | Semelhança visual e largura de etiquetas próximas | Protocolo M110 documentado por comunidade |
| Phomemo | M200, M220 | Impressoras térmicas de etiqueta com maior largura em algumas versões | Mesma marca não implica firmware igual |
| NIIMBOT | D110 | Etiquetadora estreita | Não é substituta 1:1 para 50 mm |
| NIIMBOT | B1, B21 | Concorrentes com uso semelhante e SDK comunitário | Alguns modelos/consumíveis têm identificação RFID |
| NIIMBOT | B21 Pro | Variante de maior resolução declarada (300 dpi) | Divergências de geração/revisão exigem confirmação |

Distinguir três compatibilidades independentes:

1. **Mecânica/consumíveis:** largura do rolo, diâmetro, liner, tipo de etiqueta e sensor.
2. **Transporte e protocolo:** BLE GATT, Bluetooth Classic SPP, USB serial/USB printer, TSPL, ESC/POS ou protocolo proprietário.
3. **Firmware/hardware:** SoC/MCU, memória, bootloader, GPIO, sensor, cabeça térmica, motorização, bateria e revisão.

`203 dpi`, `Bluetooth` e `50 mm` semelhantes **não** significam firmware intercambiável.

## 5. Evidências públicas localizadas em 21/11/2026

### Código de referência (repositórios)

- **Phomemo / CUPS, comandos M110/M120/M220:** https://github.com/vivier/phomemo-tools
  - O README apresenta controle de velocidade/densidade, modo de mídia (gap/contínuo/marca) e transmissão raster de modelos Phomemo.
  - Esses bytes são **do protocolo documentado para Phomemo**, não comandos validados para PT260.
- **Phomemo M110 / Python e BLE:** https://github.com/mkuhlmann/pyphomemo
  - Documento de implementação via BLE, CLI e API Python para M110; descreve características BLE utilizadas na M110.
  - Usar como referência de engenharia reversa, não executar contra PT260 sem identificação.
- **NIIMBOT / Web Bluetooth:** https://github.com/iscarelli/niimbot-web-bluetooth
  - Implementa/imprime em modelos NIIMBOT validados; diferencia protocolos e versões por identificação do modelo.
  - Particularmente útil como exemplo de *read-only identification*, logs e estrutura de driver com perfil por modelo.
- **Catálogo técnico comunitário:** https://opentlp.github.io/table-of-hardware/index.html
  - Consultar dados de hardware/protocolo por equipamento; não presumir que há registro verificado da PT260.

### Fontes de vendedores PT260 (dados não definitivos)

- Anúncio de **GS-PT260** como térmica 58 mm e protocolo ESC/POS: https://www.magazinevoce.com.br/clubepresidente/mini-etiqueta-termica-58mm-impressora-portatil-bluetooth-goldensky/p/cb43gk44gg/in/ipst/?seller_id=goldenskycombr
- Anúncio de **PT260** como impressora para etiquetas de **20–50 mm**: https://www.magazineluiza.com.br/impressora-bluetooth-10-rolos-etiquetas-adesivas-50x30-titannet/p/hbd60hh16e/in/ipst/

Esses anúncios **não** são documentação oficial da unidade comprada. Exigir evidência física antes de fixar especificações.

## 6. Estratégia de identificação não destrutiva

### Fase A — Inventário de hardware

Coletar, preferencialmente com fotos:

- Face inferior/etiqueta técnica, FCC/ANATEL, fabricante/OEM e código exato.
- Tipo de porta: USB-C, micro-USB, outro; verificar se USB transmite dados ou apenas carrega.
- Nome Bluetooth anunciado e endereço **anonimizado** (não divulgar serial, MAC ou identificadores pessoais em repositório público).
- Aplicativo recomendado na caixa/manual/QR Code; versão do aplicativo e SO.
- Bobina original que funciona e bobina transparente que falha.

### Fase B — Transporte

**Windows / PowerShell (somente consulta):**

```powershell
Get-PnpDevice -PresentOnly | Where-Object {
  $_.FriendlyName -match 'Printer|Bluetooth|USB|Serial|COM'
} | Select-Object Class, FriendlyName, InstanceId, Status

Get-CimInstance Win32_SerialPort | Select-Object Name, DeviceID, PNPDeviceID
```

**macOS (somente consulta):**

```bash
system_profiler SPUSBDataType SPBluetoothDataType
ls /dev/cu.*
```

**Linux (somente consulta):**

```bash
lsusb
bluetoothctl devices
```

**BLE:** usar ferramentas de descoberta GATT (nRF Connect, LightBlue ou `bleak`) para listar nome, UUIDs de serviços e características de leitura/notificação/escrita. Neste estágio **não enviar payloads**. Se Bluetooth Classic SPP, identificar porta serial e configurações sem enviar comandos indiscriminados.

### Fase C — Determinação do protocolo

Avaliar evidências em ordem:

1. Documentação/SDK/QR do fabricante da **mesma** revisão.
2. Identificador USB/Bluetooth e UUIDs GATT, confrontados com drivers conhecidos.
3. Captura do tráfego gerado pelo **app original** em ações normais (conectar, consultar status, imprimir etiqueta de teste).
4. Identificação de enquadramento, cabeçalhos, checksum, comandos de raster, feed, config e respostas.
5. Teste de comandos benignos **apenas com suporte/validação de modelo**.

**Não realizar varredura cega de opcodes**: um comando desconhecido pode iniciar escrita em flash, atualização de firmware, avanço contínuo ou alteração persistente. Salvar capturas anonimizadas e distinguir bytes observados de inferências.

### Fase D — Prototipação de driver

Preferir **driver nativo para PT260** em vez de fazer o hardware se passar por M110:

- Camada `transport` (BLE / SPP / USB, conforme o real).
- Camada `protocol` (frames, handshake, status, mídia, raster, impressão).
- Camada `renderer` (texto/imagem/QR Code para bitmap em resolução real).
- Camada `profiles` (PT260 revisão X, variantes separadas e nunca misturadas sem teste).
- Logs hexdump configuráveis, **desligados por padrão**, com anonimização.
- Testes unitários com fixtures de capturas locais, sem necessidade de hardware.
- Teste de impressão real **só após identificação robusta de protocolo**.

Considerar uma ponte `M110 -> PT260` apenas se algum consumidor realmente exigir protocolo/app Phomemo; a ponte depende da tradução bem documentada de ambos. **Bluetooth advertised name não substitui protocolo.**

## 7. Firmware: limites de segurança

**Não tentar cross-flash do firmware M110 na PT260** neste projeto inicial. Para sequer considerar isso futuramente, seriam necessários:

- identificação física da placa e dos chips;
- backup integral do firmware original e verificação de restauração;
- entendimento do bootloader e da assinatura/verificação de imagens;
- diagrama ou mapeamento dos GPIOs dos sensores/cabeça/motor;
- possibilidade comprovada de recuperação em bancada (UART/SWD/JTAG, quando aplicável);
- autorização clara do proprietário para aceitar risco de perda permanente do equipamento.

Sem isso, classificar a troca de firmware como **alto risco e não recomendada**. Foco em solução reversível por software externo.

## 8. Possível integração com inventario.caiobezerra.com

**Visão:** ao cadastrar um objeto no inventário, emitir etiqueta física com seu identificador e QR Code.

Proposta preliminar (depende do sistema real e das permissões):

```text
[inventario.caiobezerra.com]
           |
    pedido de etiqueta
           v
 [serviço local/bridge]
           |
     layout + QR Code
           v
 [renderer 203 dpi*]
           |
   [driver PT260 detectado]
           |
       BLE / USB
           v
        [PT260]

* resolução e largura dependem da variante efetiva
```

- Evitar expor o dispositivo diretamente na internet; o serviço local deve fazer a impressão sob comando autenticado.
- Prever modo sem conectividade com nuvem, reimpressão, calibração e visualização prévia.
- Estruturar objetos como `tipo`, `categoria`, `prefixo`, `identificador`, `nome`, `URL/QR`, `tamanho_da_etiqueta` e `impressora`.
- Não gravar serial Bluetooth/MAC ou token de API em logs ou arquivos públicos.
- Se utilizar navegador, verificar disponibilidade de Web Bluetooth no SO/navegador e origem HTTPS; alternativa: agente local.

## 9. Roadmap e critérios de aceite

### Sprint 0 — Reunir dados

- [ ] Fotos e dados do hardware e bobinas.
- [ ] App atual, versão e SO.
- [ ] Cenário reproduzível de erro e mídia opaca de controle.

**Aceite:** evidências suficientes para classificar o problema como mídia/sensor, app ou conexão sem especulação.

### Sprint 1 — Identificar o transporte

- [ ] BLE vs SPP vs USB (ou combinação).
- [ ] UUIDs/características ou VID/PID, conforme aplicável.
- [ ] Captura de conexão e impressão pelo software original.

**Aceite:** ficha de hardware/transport com origem e confiança de cada achado.

### Sprint 2 — Compreender o protocolo

- [ ] Documentar mensagens observadas e comandos presumidos separados.
- [ ] Identificar fluxos de status, mídia, raster e fim da impressão.
- [ ] Testes com fixtures e hexdumps anonimizados.

**Aceite:** um caso de impressão do app oficial explicado com evidências; sem operações destrutivas.

### Sprint 3 — Driver experimental

- [ ] Implementar transporte e renderização modular.
- [ ] Imprimir etiqueta opaca de teste e receber status de erro.
- [ ] Testar mídia transparente em modo correto se houver suporte.

**Aceite:** impressão repetida e previsível em hardware real, com logs e passo de restauração/rollback.

### Sprint 4 — Inventário

- [ ] API/integração com inventário.
- [ ] Template 50x30 mm (somente se suportado), com ID e QR Code.
- [ ] Serviço local seguro e teste end-to-end.

**Aceite:** criar objeto no inventário e gerar etiqueta corretamente de forma repetível.

## 10. Organização sugerida para o repositório

```text
pt260-lab/
├── README.md
├── docs/
│   ├── hardware.md
│   ├── research-links.md
│   ├── media-tests.md
│   ├── transport-observations.md
│   ├── protocol-notes.md
│   └── risk-register.md
├── captures/                # privadas; nunca publicar sem sanitizar
├── fixtures/                # amostras anonimizadas
├── src/
│   ├── transport/
│   ├── protocol/
│   ├── renderer/
│   └── printer_profiles/
└── tests/
```

Criar `.gitignore` para `captures/`, `secrets/`, `*.pcap`, `*.pcapng`, identificadores sensíveis, logs com endereço Bluetooth e backups de firmware.

## 11. Perguntas abertas que ainda bloqueiam conclusões

1. Qual é a **referência literal** impressa na parte inferior: PT260, XD-210, GS-PT260 ou outra?
2. O dispositivo **tem visor**? É etiquetadora ou impressora de recibos com rolo 58 mm?
3. Qual é o **app original**, instalado ou fornecido pelo vendedor?
4. Qual é o **nome Bluetooth exato**, tipo de conexão e eventual USB VID/PID?
5. Qual o **material transparente** (marca, `direct thermal`, BOPP, PET, liner, gap/black mark e dimensões)?
6. O que exatamente significa “não reconheceu”: erro de papel, avança várias etiquetas, imprime em branco, desalinha ou não conecta?
7. A etiqueta opaca continua imprimindo várias vezes sem falha?
8. Qual é o SO de execução desejado para o driver e qual arquitetura do site de inventário?

## 12. Prompt curto para iniciar uma nova sessão no Claude Code

> Tenho uma impressora térmica PT260, possivelmente denominada XD-210. Ela se parece com a Phomemo M110, mas NÃO sabemos se tem o mesmo hardware ou protocolo. Use este documento como contexto. Quero um plano investigativo com ferramentas e scripts **somente de leitura** para descobrir hardware, BLE/USB e protocolo da minha unidade; também quero diagnosticar uma bobina transparente que imprimiu uma vez e depois deixou de ser reconhecida. Não faça flash de firmware, não envie comandos desconhecidos e não assuma compatibilidade com a Phomemo. Comece propondo a estrutura de repositório, fichas de evidências e comandos seguros de inspeção para meu sistema operacional. Após evidências do transporte, proponha a arquitetura de um driver/bridge e futura integração com inventario.caiobezerra.com. Identifique todos os achados como observados, referenciados ou hipóteses.

---

*Preparado em 21/11/2026. Esta é uma especificação de pesquisa, não um relatório de testes práticos da unidade PT260 do proprietário. Os dados públicos não substituem inspeção do equipamento real.*
