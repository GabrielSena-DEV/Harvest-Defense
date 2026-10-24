# HARVEST DEFENSE — jogo de defesa em Pygame

Tower defense de fazenda e Halloween. O objetivo é proteger o celeiro de cinco ondas de monstros: fantasmas, gosmas, zumbis e abóboras malditas.

## Requisitos
- Python 3.10 ou superior
- Visual Studio Code (ou outro editor)
- Pygame

## Como executar
1. Extraia a pasta `ByteDefense`.
2. Abra a pasta no Visual Studio Code.
3. Abra o terminal integrado (`Terminal > Novo Terminal`).
4. (Opcional, recomendado) crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
   No Windows, ative-o com:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
5. Instale a dependência:
   ```bash
   python -m pip install -r requirements.txt
   ```
6. Execute:
   ```bash
   python main.py
   ```

## Telas
- **Tela inicial**: aperte qualquer tecla ou clique para ir ao menu (ESC sai).
- **Menu principal**: use o mouse ou as setas / W / S + ENTER. Opções: Jogar, Configurações (tela cheia), Como jogar e Sair. Pressione **R** para abrir o ranking. ESC volta à tela inicial.
- **Dificuldade**: depois de escolher Jogar, selecione Fácil, Normal ou Difícil com as setas e ENTER, ou clique em uma opção.
- **Durante o jogo**: ESC volta ao menu. **F11** alterna tela cheia em qualquer tela.

## Controles
- **Clique em uma torre no painel inferior** para escolhê-la; clique no mapa para posicioná-la.
- **1 a 6**: selecionar uma das torres disponíveis (Q / W / E também selecionam Espantalho, Gárgula e Lápide).
- **Clique em uma torre colocada**: selecionar para ver alcance e nível.
- **U**: melhorar a torre selecionada.
- **Espaço**: iniciar a próxima onda.
- **F**: usar o pulso lunar (habilidade especial com recarga).
- **T**: abrir a árvore de habilidades.
- **1 / 2 / 3** na árvore: desbloquear um caminho.
- **ESC**: fechar a árvore ou voltar ao menu.
- **ENTER**: reiniciar após vitória ou derrota.
- **R** após uma vitória: consultar o ranking.

## Mecânicas incluídas
- Cinco fases com quantidade, resistência e velocidade dos monstros crescentes.
- Seis torres balanceadas: **Espantalho** (dano equilibrado), **Gárgula** (golpes pesados), **Lápide** (invoca aliados que enfrentam e atrasam inimigos), **Milho** (rajada veloz), **Corvo** (longo alcance e dano alto) e **Abóbora** (explosão em área).
- Moeda em abóboras, com bônus por eliminar monstros e por concluir ondas.
- Árvore de habilidades com três caminhos: Amuleto Sombrio (dano), Colheita Farta (recompensa) e Ritmo de Batalha (velocidade de ataque).
- Pulso lunar especial, recarga, barras de vida, partículas e efeitos de impacto.
- O celeiro tem integridade; monstros que chegam ao final a reduzem.
- O score só é calculado e incluído no ranking após vencer as cinco ondas. A integridade do celeiro vale até 5.000 pontos; tempo, melhorias de torres, talentos e abóboras restantes completam a pontuação, que recebe um multiplicador conforme a dificuldade.
- O ranking mantém as 10 melhores vitórias de cada dificuldade neste computador. Ele é salvo em `~/.harvest-defense/leaderboard.json` e não é enviado a um servidor.

## Arquivos
- `main.py` — o jogo.
- `assets/tela_inicial.png` — arte da tela inicial (1100×720, sem texto; o texto que pisca é desenhado pelo código).
- `assets/menu_principal.png` — arte do menu (1100×720). Os botões fazem parte da imagem; a seleção em verde é desenhada pelo código.

## Observações
- Se `assets/tela_inicial.png` ou `assets/menu_principal.png` não forem encontradas, o jogo mostra telas de reserva em texto.
- Torres, monstros, estrada e celeiro são desenhados com formas do próprio Pygame; só a tela inicial usa imagem.
- O som não está implementado nesta versão.
