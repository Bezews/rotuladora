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
