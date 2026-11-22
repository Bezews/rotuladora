# Diagnóstico: etiqueta transparente imprimiu uma vez e depois "não foi reconhecida"

## 1. Por que transparente é difícil para esse tipo de impressora

Rotuladoras de 50 mm usam em geral um **sensor óptico de transmissão** (LED de um lado, fototransistor do outro) para achar o **gap** entre etiquetas: etiqueta + liner bloqueia mais luz que só o liner. Com etiqueta **transparente**, a diferença de opacidade entre "etiqueta+liner" e "só liner" cai muito → o firmware não encontra o gap, avança papel procurando, e declara erro ou desalinha.

Por que **funcionou uma vez**: provavelmente o primeiro job usou a posição já alinhada (sem precisar procurar gap) ou a calibração anterior ainda era da mídia opaca; nos seguintes, a impressora tentou reaprender/localizar o gap e falhou **[HIPÓTESE principal]**.

Firewall/PC **não** influenciam: o sensor é local na impressora.

## 2. Árvore de decisão

```text
Etiqueta opaca imprime 5x seguidas sem erro?
├── NÃO → problema de conexão/app/bateria, não de mídia. Parar e investigar transporte.
└── SIM → trocar para transparente
     ├── Avança várias etiquetas e para com erro/LED → sensor não acha gap (H1/H2)
     ├── Avança certo mas sai em branco → mídia não é térmica direta (H5)
     ├── Imprime mas desalinhado → calibração/tamanho (H3)
     └── Nem puxa papel → rolo mal posicionado/sensor obstruído (H4)
```

## 3. Ações por ordem (todas reversíveis)

1. Conferir se a bobina transparente é **térmica direta** (diz "direct thermal"/"sem tinta"; arranhar com a unha deixa marca escura). Se exigir ribbon, é incompatível.
2. Verificar se o **liner** (papel de fundo) é opaco/branco. Liner transparente + etiqueta transparente = praticamente indetectável.
3. No app da impressora, escolher tipo de papel **"etiqueta com gap"** e tamanho exato (ex.: 40×30).
4. Executar **calibração/aprendizado de papel** pelo próprio app ou rotina do manual da PT-260 ou `GAPDETECT` (seção 4) (não usar combinação de botões da M110).
5. Teste de contorno: modo **contínuo** + comprimento fixo — se imprimir, confirma que só a detecção de gap falha.
6. Limpar sensor (desligada, cotonete seco/álcool isopropílico) e conferir guia lateral do rolo.
7. Contorno definitivo, se nada resolver: usar etiquetas transparentes **com marca preta** no verso, ou etiquetas BOPP "clear" de fabricantes que declaram compatibilidade com o sensor (a Phomemo vende transparentes específicas para M110 — o que reforça que é questão de mídia, não de firmware).

## 4. Sequência TSPL para a transparente (PT-260 confirmada TSPL)

Enviar pelo Serial Bluetooth Terminal (CR+LF), com a bobina transparente instalada. Medir antes largura, altura e gap.

**Passo A — calibrar sensor de gap**

```text
SIZE 40 mm,30 mm
GAP 2 mm,0 mm
GAPDETECT
```

A impressora avança algumas etiquetas e aprende o limiar. Depois:

```text
CLS
TEXT 16,16,"3",0,2,2,"CLEAR A"
PRINT 1,1
```

Repetir o `PRINT` 3×. Se alinhar sempre → calibração resolveu (causa: limiar aprendido com mídia opaca).

**Passo B — se A falhar: modo contínuo (contorno)**

```text
SIZE 40 mm,32 mm
GAP 0 mm,0 mm
CLS
TEXT 16,16,"3",0,2,2,"CLEAR B"
PRINT 1,1
```

`SIZE` = altura da etiqueta + gap (passo). Imprime sem procurar gap; desalinhamento acumula, mas confirma se o problema é só o sensor.

**Passo C — voltar ao normal com a opaca**

```text
SIZE 40 mm,30 mm
GAP 2 mm,0 mm
GAPDETECT
```

`SIZE`/`GAP` costumam persistir: sempre restaurar após testes.

Se `GAPDETECT` for ignorado (clone sem o comando), testar `AUTODETECT` e registrar o resultado.

## 5. Registro de testes

| Data | Mídia (marca, tamanho, liner) | Modo no app | Calibrou? | Resultado observado | LED/erro | Conclusão |
|---|---|---|---|---|---|---|
| | | | | | | |
