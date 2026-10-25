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
- **Menu principal**: use o mouse ou as setas / W / S + ENTER. Opções: Jogar, Configurações (tela cheia e volume da música), Como jogar e Sair. Pressione **B** para abrir a árvore de melhorias, **T** para desbloquear torres ou **R** para o ranking. Nas árvores, selecione nós com mouse ou números e confirme com ENTER; **B/T** alterna entre elas.
- **Dificuldade**: depois de escolher Jogar, selecione Fácil, Normal ou Difícil com as setas e ENTER, ou clique em uma opção.
- **Herói**: após escolher a dificuldade, selecione um dos seis fazendeiros. Cada campanha permite um herói; pressione **G** durante a partida para ativar seu poder (aponte o cursor para o mapa nas habilidades de área).
- **Durante o jogo**: clique no botão **ONDAS: MANUAL/AUTO** no painel inferior para alternar entre iniciar cada onda com **ESPAÇO** ou avançar automaticamente assim que todos os monstros forem derrotados. O modo escolhido fica salvo no perfil. **ESC** pausa a partida. No menu de pausa, escolha continuar, abrir configurações ou voltar ao menu principal; sair da campanha pede confirmação. **F11** alterna tela cheia em qualquer tela.
- **Trilha sonora**: o tema toca na tela inicial, no menu e na seleção de dificuldade. Cada dificuldade tem sua própria música; a trilha de chefão assume enquanto um chefão estiver vivo e depois a música da dificuldade retorna. Ajuste o volume em Configurações arrastando o controle ou usando as setas esquerda/direita; a alteração é aplicada imediatamente.

## Controles
- **Clique em uma torre no painel inferior** para escolhê-la; clique no mapa para posicioná-la.
- **1 a 6**: selecionar uma das torres disponíveis (Q / W / E também selecionam Espantalho, Gárgula e Lápide).
- **Clique em uma torre colocada**: selecionar para ver alcance e nível.
- **U**: melhorar a torre selecionada.
- **V** ou botão **VENDER**: vender a torre selecionada e receber 70% do custo original do tipo de torre (o custo de melhorias não é reembolsado).
- **Espaço**: iniciar a próxima onda.
- **F**: usar o pulso lunar (habilidade especial com recarga).
- **G**: ativar o poder do herói escolhido (cada poder tem recarga própria).
- **T**: consultar as habilidades equipadas durante a partida.
- **ESC**: fechar o painel de habilidades ou abrir/fechar o menu de pausa.
- **ENTER** após a vitória: abrir a seleção de iniciais. Use **← / →** para selecionar uma posição, **↑ / ↓** para mudar a letra, ou digite letras; pressione **ENTER** para gravar as três iniciais no placar.
- Depois de registrar as iniciais, **ENTER** reinicia a partida, **R** abre o placar e **ESC** volta ao menu.

## Mecânicas incluídas
- Campanha com 6 ondas no Fácil, 9 no Médio e 12 no Difícil. As seis primeiras ondas mantêm a mesma sequência nas três dificuldades; as ondas 7 a 9 ampliam a campanha do Médio e também aparecem no Difícil, que acrescenta as ondas 10 a 12.
- **Um mapa por dificuldade:** o mapa é escolhido pela dificuldade e vale para a campanha inteira (não muda de onda para onda). **Fácil** usa `assets/backgrounds/fase_1.png` (os monstros saem pelo portão central inferior e seguem a estrada até o portal no canto superior direito); **Médio** usa `assets/backgrounds/fase_2.png` (entram pela esquerda e seguem até a saída à direita); **Difícil** usa `assets/backgrounds/fase_3.png` (entram pelo portão INÍCIO e seguem até o portão FIM). As rotas dos inimigos seguem a estrada ilustrada em cada arte, e as torres não podem ser colocadas sobre ela. A arte mantém sua proporção original, com laterais suavizadas para preencher a área panorâmica.
- A dificuldade também define o mapa e ajusta vida e velocidade dos inimigos, dano ao celeiro e multiplicador de pontuação. A densidade, a resistência e a velocidade dos inimigos aumentam gradualmente nas ondas adicionais.
- Inimigos com atributos e aparência próprios: **Zumbis** lentos e resistentes; **Esqueletos** básicos que avançam em bandos; **Fantasmas** que ignoram os bloqueios da Lápide; **Morcegos**, **Aranhas** e **Traças** rápidos, frágeis e agrupados; **Vampiros** que regeneram vida; **Múmias** e **Frankenstein** com muita vida e armadura. Novos tipos entram na composição das ondas conforme a campanha avança.
- Seis torres balanceadas: **Espantalho** (dano equilibrado), **Gárgula** (golpes pesados), **Lápide** (invoca aliados que enfrentam e atrasam inimigos), **Milho** (rajada veloz), **Corvo** (longo alcance e dano alto) e **Abóbora** (explosão em área). Cada torre pode chegar ao nível 5; os níveis 2 a 4 melhoram dano, cadência e alcance gradualmente. O nível 5 é um salto de poder (3,2× o dano base, cadência mais rápida, alcance ampliado e explosões maiores para a Abóbora) e custa 4,25× o custo inicial da torre.
- **Melhorias de torre**: use **U** com uma torre selecionada. O custo aumenta a cada nível; o salto do nível 4 para o 5 é o mais caro. Torres no nível 5 não podem receber novas melhorias.
- **Heróis com poderes ativos:** escolha um antes de cada campanha. Cada herói tem seu retrato e cor na tela de seleção; o retrato do escolhido aparece sem painel junto à base durante a partida, e seu nome também fica no HUD. **Devair da Lentidão** desacelera inimigos numa área; **Monica** aumenta temporariamente o dano das torres; **Coan, o Frenesi** acelera os ataques; **Chico Bento** gera abóboras; **Carlos** envenena inimigos numa área; **Alessandre** causa dano instantâneo em área. Pressione **G** para ativar o poder, respeitando a recarga exibida na interface. Para Devair, Carlos e Alessandre, a posição do cursor define a área atingida.
- Ao ativar um poder de herói, uma onda percorre o mapa na cor correspondente: Devair da Lentidão em dourado, Monica em vermelho, Coan em azul, Chico Bento em verde, Carlos em violeta e Alessandre em amarelo-claro. O pulso lunar também percorre o mapa com anéis dourados e raios de luz.
- **Duas moedas:** abóboras são ganhas e gastas durante a partida para comprar e melhorar torres; cérebros são ganhos ao derrotar chefões e gastos fora da partida na loja de habilidades.
- **Recompensa de cérebros:** cada chefão derrotado concede 3 cérebros, sem depender da integridade do celeiro. Chefões que chegam ao celeiro não concedem a recompensa. Os cérebros são persistentes entre sessões.
- **Desbloqueio de torres:** Espantalho já vem disponível. Na árvore **T** do menu, cada torre custa 2 cérebros: Gárgula abre o caminho para Lápide e Milho; ambas são necessárias para liberar Corvo; Corvo libera Abóbora. Torres desbloqueadas ficam disponíveis permanentemente nas partidas. A árvore também pode ser aberta a partir da de melhorias com **T**.
- **Economia de abóboras:** as recompensas por inimigo foram reduzidas pela metade e o bônus ao concluir cada onda foi diminuído para manter as compras e melhorias mais equilibradas ao longo da campanha.
- A loja (**B** no menu) usa a imagem `assets/backgrounds/arvore_habilidades.png` como fundo da árvore. Selecione um dos sete nós para ver descrição, custo e estado; use **1-7** e **ENTER**, ou clique no nó e no botão de ação. Oferece Mira de Precisão (+10% dano), Rajada Rápida (+8% velocidade de ataque), Defesa Preparada (+100 abóboras iniciais), Celeiro Reforçado (-10% dano ao celeiro), Recompensa da Colheita (+15% abóboras por inimigo), Foco Lunar (pulso recarrega 20% mais rápido e causa +20% dano) e Runas Gélidas (inimigos avançam 15% mais devagar). Cada habilidade é desbloqueada permanentemente; equipe até três antes de iniciar uma campanha.
- Chefões aparecem a cada três ondas com sprites próprios, sempre desenhados em primeiro plano no mapa: Esqueleto Cbum (`assets/enemies/1.png`) explode e invoca quatro esqueletos ao morrer; Lorde Vampiro (`assets/enemies/2.png`) recupera vida perto das tropas aliadas; Rei Fantasma (`assets/enemies/3.png`) fica intangível após permanecer com pouca vida, e lentidões atrasam a transformação; Rei do Pop (`assets/enemies/4.png`) fortalece a velocidade dos inimigos próximos e invoca quatro zumbis ao chegar à metade da vida.
- Pulso lunar especial, recarga, barras de vida, partículas e efeitos de impacto.
- O celeiro tem integridade; monstros que chegam ao final a reduzem.
- O score só é calculado e incluído no ranking após vencer todas as ondas da dificuldade escolhida. A integridade do celeiro vale até 5.000 pontos; tempo, melhorias de torres, habilidades equipadas e abóboras restantes completam a pontuação, que recebe um multiplicador conforme a dificuldade.
- O placar local exibe as 10 maiores pontuações em estilo arcade. Após vencer, pressione **ENTER**, escolha três iniciais e confirme com **ENTER** para registrar o score. Os dados ficam em arquivos JSON na pasta `docs/` ao lado do jogo: `scores.json` contém os scores; `profile.json` guarda moedas, habilidades, torres desbloqueadas e modo de ondas. Para zerar os scores, feche o jogo e apague `docs/scores.json`, sem afetar o perfil. Dados antigos em `placar/` ou `~/.harvest-defense/` são movidos automaticamente para essa pasta. Esses dados são locais e não são enviados a um servidor.
- As músicas ficam em `assets/soundtrack/`: `The_Organist_s_Final_Act_Tema.mp3` (título e menus), `Behind_The_Barricade_Fase_Fácil.mp3` (Fácil), `Weight_of_the_Headstone_Fase_Média.mp3` (Médio), `Teeth_Of_The_Caldera_Fase_Dificil.mp3` (Difícil) e `Iron_Verdict_Chegada do chefe.mp3` (chefões).

## Arquivos
- `main.py` — o jogo.
- `assets/backgrounds/tela_inicial.png` — arte da tela inicial (1100×720, sem texto; o texto que pisca é desenhado pelo código).
- `assets/backgrounds/menu_principal.png` — arte do menu (1100×720). Os botões fazem parte da imagem; a seleção em verde é desenhada pelo código.
- `assets/backgrounds/arvore_habilidades.png` — arte de fundo da árvore de habilidades.
- `assets/backgrounds/fase_1.png`, `fase_2.png` e `fase_3.png` — mapas de Fácil, Médio e Difícil. Os waypoints de cada rota ficam em `MAP_SCENES` no `main.py`, em pixels da imagem original; se trocar a arte, refaça os pontos de `path`/`core` e o `source_size`.

## Observações
- Se as artes de `assets/backgrounds/` não forem encontradas, o jogo mostra telas de reserva em texto ou registra o erro no terminal.
- Os mapas e as telas de início, menu e habilidades usam as imagens em `assets/backgrounds/`; torres, monstros e efeitos são desenhados com formas do próprio Pygame.
- A janela pode ser redimensionada e a tela cheia preenche a resolução do monitor sem barras; os cliques são convertidos para a área lógica do jogo.
- A reprodução usa o mixer do Pygame; se a inicialização de áudio ou o carregamento de uma faixa falhar, o erro é informado no terminal.
