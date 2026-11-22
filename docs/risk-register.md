# Registro de riscos

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| R1 | *Brick* por flash de firmware incompatível | alta se tentado | perda do aparelho | Fora de escopo. Denylist bloqueia `1F A0 BE 66 88` (BOOT). |
| R2 | Comando desconhecido grava config persistente | média | calibração perdida/comportamento estranho | Allowlist por perfil, apenas bytes vistos em captura do app oficial. |
| R3 | Reset de fábrica acidental | baixa | perda de calibração | Denylist `1F 50 BE`. |
| R4 | Vazamento de MAC/serial em repositório público | média | privacidade | `.gitignore` em `captures/`; anonimizar fixtures; revisão antes de commit. |
| R5 | Confundir variantes (PT260 50 mm vs GS-PT260 58 mm ESC/POS) | alta | driver errado | Perfis separados; identificação por GATT + resposta de modelo antes de imprimir. |
| R6 | Sobreaquecimento da cabeça por densidade máxima contínua | baixa | desgaste | Limitar densidade padrão a valor médio; pausas entre jobs longos. |
| R7 | Mídia transparente incompatível com sensor (limite físico) | alta | feature impossível | Testes de `media-tests.md`; alternativa: mídia com marca preta. |
| R8 | Expor impressora/agente local à internet | média | abuso remoto | Agente só em `localhost`/LAN, token, sem porta aberta no roteador. |
| R9 | Licença restritiva do SDK Marklife | — | jurídico | Não copiar código; implementar a partir de capturas próprias (clean-room). |

## Pré-requisitos para algum dia reconsiderar firmware

1. Placa fotografada e chips identificados (MCU, flash, BLE).
2. Acesso SWD/UART confirmado e dump integral salvo fora do repositório.
3. Restauração do dump testada com sucesso.
4. Formato/assinatura da imagem entendido.
5. Autorização escrita do proprietário aceitando perda do aparelho.
