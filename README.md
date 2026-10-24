# HARVEST DEFENSE — jogo de defesa em Pygame

Tower defense de fazenda e Halloween. Proteja o celeiro em uma campanha de ondas de monstros: fantasmas, gosmas, zumbis e abóboras malditas.

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
- **Menu principal**: use o mouse ou as setas / W / S + ENTER. Opções: Jogar, Configurações (tela cheia), Como jogar e Sair. Pressione **B** para abrir a loja de habilidades ou **R** para o ranking. ESC volta à tela inicial.
- **Dificuldade**: depois de escolher Jogar, selecione Fácil, Normal ou Difícil com as setas e ENTER, ou clique em uma opção.
- **Durante o jogo**: ESC volta ao menu. **F11** alterna tela cheia em qualquer tela.

## Controles
- **Clique em uma torre no painel inferior** para escolhê-la; clique no mapa para posicioná-la.
- **1 a 6**: selecionar uma das torres disponíveis (Q / W / E também selecionam Espantalho, Gárgula e Lápide).
- **Clique em uma torre colocada**: selecionar para ver alcance e nível.
- **U**: melhorar a torre selecionada.
- **Espaço**: iniciar a próxima onda.
- **F**: usar o pulso lunar (habilidade especial com recarga).
- **T**: consultar as habilidades equipadas durante a partida.
- **ESC**: fechar o painel de habilidades ou voltar ao menu.
- **ENTER**: reiniciar após vitória ou derrota.
- **R** após uma vitória: consultar o ranking.

## Mecânicas incluídas
- Campanha com 6 ondas no Fácil, 9 no Médio e 12 no Difícil. As seis primeiras ondas mantêm a mesma sequência nas três dificuldades; as ondas 7 a 9 ampliam a campanha do Médio e também aparecem no Difícil, que acrescenta as ondas 10 a 12.
- A dificuldade ajusta vida e velocidade dos inimigos, dano ao celeiro e multiplicador de pontuação. A densidade, a resistência e a velocidade dos inimigos aumentam gradualmente nas ondas adicionais.
- Inimigos com atributos e aparência próprios: **Zumbis** lentos e resistentes; **Esqueletos** básicos que avançam em bandos; **Fantasmas** que ignoram os bloqueios da Lápide; **Morcegos**, **Aranhas** e **Traças** rápidos, frágeis e agrupados; **Vampiros** que regeneram vida; **Múmias** e **Frankenstein** com muita vida e armadura. Novos tipos entram na composição das ondas conforme a campanha avança.
- Seis torres balanceadas: **Espantalho** (dano equilibrado), **Gárgula** (golpes pesados), **Lápide** (invoca aliados que enfrentam e atrasam inimigos), **Milho** (rajada veloz), **Corvo** (longo alcance e dano alto) e **Abóbora** (explosão em área).
- **Duas moedas:** abóboras são ganhas e gastas durante a partida para comprar e melhorar torres; cérebros são ganhos ao derrotar chefões e gastos fora da partida na loja de habilidades.
- **Recompensa de cérebros:** cada chefão derrotado concede 3 cérebros, sem depender da integridade do celeiro. Chefões que chegam ao celeiro não concedem a recompensa. Os cérebros são persistentes entre sessões.
- **Economia de abóboras:** as recompensas por inimigo foram reduzidas pela metade e o bônus ao concluir cada onda foi diminuído para manter as compras e melhorias mais equilibradas ao longo da campanha.
- A loja (**B** no menu) oferece Mira de Precisão (+10% dano), Rajada Rápida (+8% velocidade de ataque), Defesa Preparada (+100 abóboras iniciais), Celeiro Reforçado (-10% dano ao celeiro), Recompensa da Colheita (+15% abóboras por inimigo), Foco Lunar (pulso recarrega 20% mais rápido e causa +20% dano) e Runas Gélidas (inimigos avançam 15% mais devagar). Cada habilidade é desbloqueada permanentemente; equipe até três antes de iniciar uma campanha.
- Chefões aparecem a cada três ondas: Esqueleto Cbum explode e invoca quatro esqueletos ao morrer; Lorde Vampiro recupera vida perto das tropas aliadas; Rei Fantasma fica intangível após permanecer com pouca vida, e lentidões atrasam a transformação; Rei do Pop fortalece a velocidade dos inimigos próximos e invoca quatro zumbis ao chegar à metade da vida.
- Pulso lunar especial, recarga, barras de vida, partículas e efeitos de impacto.
- O celeiro tem integridade; monstros que chegam ao final a reduzem.
- O score só é calculado e incluído no ranking após vencer todas as ondas da dificuldade escolhida. A integridade do celeiro vale até 5.000 pontos; tempo, melhorias de torres, habilidades equipadas e abóboras restantes completam a pontuação, que recebe um multiplicador conforme a dificuldade.
- O ranking mantém as 10 melhores vitórias de cada dificuldade neste computador. Ele é salvo em `~/.harvest-defense/leaderboard.json`; moedas e habilidades ficam em `~/.harvest-defense/profile.json`. Esses dados são locais e não são enviados a um servidor.

## Arquivos
- `main.py` — o jogo.
- `assets/tela_inicial.png` — arte da tela inicial (1100×720, sem texto; o texto que pisca é desenhado pelo código).
- `assets/menu_principal.png` — arte do menu (1100×720). Os botões fazem parte da imagem; a seleção em verde é desenhada pelo código.

## Observações
- Se `assets/tela_inicial.png` ou `assets/menu_principal.png` não forem encontradas, o jogo mostra telas de reserva em texto.
- Torres, monstros, estrada e celeiro são desenhados com formas do próprio Pygame; só a tela inicial usa imagem.
- O som não está implementado nesta versão.
