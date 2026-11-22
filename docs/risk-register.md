# Registro de riscos

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| R1 | *Brick* por flash de firmware incompatível | alta se tentado | perda do aparelho | Fora de escopo. Denylist TSPL bloqueia `DOWNLOAD`/`RUN`/`KILL`. Nunca usar utilitário de firmware. |
| R2 | Comando desconhecido grava config persistente | média | calibração perdida/comportamento estranho | Allowlist por perfil, apenas bytes vistos em captura do app oficial. |
| R3 | Reset de fábrica acidental | baixa | perda de calibração | Denylist `INITIALPRINTER`. |
| R4 | Vazamento de MAC/serial em repositório público | média | privacidade | `.gitignore` em `captures/`; anonimizar fixtures; revisão antes de commit. |
| R5 | Confundir variantes (PT260 50 mm vs GS-PT260 58 mm ESC/POS) | alta | driver errado | Perfis separados; identificação por GATT + resposta de modelo antes de imprimir. |
| R6 | Sobreaquecimento da cabeça por densidade máxima contínua | baixa | desgaste | Limitar densidade padrão a valor médio; pausas entre jobs longos. |
| R7 | Mídia transparente incompatível com sensor (limite físico) | alta | feature impossível | Testes de `media-tests.md`; alternativa: mídia com marca preta. |
| R8 | Expor impressora/agente local à internet | média | abuso remoto | Agente só em `localhost`/LAN, token, sem porta aberta no roteador. |
| R9 | Clone TSPL implementar subconjunto (comando ignorado ou interpretado diferente) | média | layout errado | Testar cada comando na unidade; registrar em `transport-observations.md`. |
| R10 | `SIZE`/`GAP`/`DENSITY` persistem na flash | alta | app original passa a usar outro tamanho | Sempre enviar `SIZE`+`GAP` em todo job; anotar valores originais antes. |

## Pré-requisitos para algum dia reconsiderar firmware

1. Placa fotografada e chips identificados (MCU, flash, BLE).
2. Acesso SWD/UART confirmado e dump integral salvo fora do repositório.
3. Restauração do dump testada com sucesso.
4. Formato/assinatura da imagem entendido.
5. Autorização escrita do proprietário aceitando perda do aparelho.
