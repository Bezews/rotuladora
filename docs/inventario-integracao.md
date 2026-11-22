# Integração com inventario.caiobezerra.com

## Arquitetura proposta

```text
[inventario.caiobezerra.com]  (nuvem, HTTPS)
        │  usuário clica "Imprimir etiqueta"
        ▼
 Opção A: Web Bluetooth no próprio navegador (Chrome/Edge desktop/Android)
          site → renderer canvas → bytes do perfil pt260 → BLE → PT260
 Opção B: agente local (PC/Raspberry na LAN)
          site → POST http://localhost:PORT/print (token) → renderer → BLE → PT260
```

| Critério | A — Web Bluetooth | B — Agente local |
|---|---|---|
| Instalação | nenhuma | serviço Python/Node |
| iPhone/Safari | **não suporta** | funciona (agente faz o BLE) |
| Impressão em lote | sim | sim, com fila |
| Segurança | permissão por gesto do usuário | token + bind em localhost |

Recomendação: começar por **A** (zero infraestrutura, testes rápidos), manter a camada `protocol` isolada para reaproveitar em **B**.

## Modelo de dados da etiqueta

```json
{
  "tipo": "ferramenta",
  "categoria": "elétricas",
  "prefixo": "FER",
  "identificador": "FER-0042",
  "nome": "Furadeira de impacto",
  "url": "https://inventario.caiobezerra.com/i/FER-0042",
  "tamanho_da_etiqueta": "40x30",
  "impressora": "pt260"
}
```

## Template 40×30 mm @ 203 dpi (≈ 320 × 240 px)

```text
┌──────────────────────────────┐
│ ┌────────┐  FER-0042         │
│ │ QR     │  Furadeira de     │
│ │ (URL)  │  impacto          │
│ └────────┘  ferramenta       │
└──────────────────────────────┘
```

- QR com correção **M**, módulo ≥ 4 px (legível em 203 dpi).
- Bitmap 1-bit, largura alinhada a 8 px; largura máxima a confirmar pela variante (384 px = 48 mm é típico).
- Pré-visualização obrigatória antes de enviar.

## Requisitos

- Nunca gravar MAC/token em logs.
- Reimpressão e impressão em lote (vários itens).
- Funciona sem internet no modo B (fila local).

## Atualização 22/11/2026 — rota TSPL

O repositório `inventario` hoje exporta **SVG** (`src/lib/label.ts`, perfil padrão 40×30 mm, margem 2 mm) e delega a impressão ao app da impressora (PRD, RF-13/RF-16). Com TSPL confirmado, há caminho melhor:

1. **Nova rota** `GET /itens/[code]/etiqueta.prn` gerando TSPL com `QRCODE` nativo (o firmware desenha o QR; nitidez máxima, payload de ~400 bytes contra imagem rasterizada).
2. **Botão "Imprimir na PT-260"** (Chrome Android, Web Bluetooth): conecta no serviço BLE descoberto pelo nRF Connect e escreve o `.prn` em blocos (≤ MTU-3, tipicamente 20 B sem negociação).
3. **Lote**: concatenar jobs; um `PRINT` por item.
4. SVG continua como reserva (iPhone/Safari, outras impressoras).

Porte de `src/pt260/tspl.py` para TypeScript é direto (montagem de strings). Mudanças no `inventario` ficam para quando o transporte BLE estiver confirmado; não alterado nesta etapa.
