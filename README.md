# BYTE DEFENSE — jogo de defesa em Pygame

Protótipo inicial de tower defense com tema de segurança digital. O objetivo é proteger o núcleo (PC) de cinco ondas de malwares.

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

## Controles
- **Clique em uma torre no painel inferior** para escolhê-la; clique no mapa para construí-la.
- **Q / W / E**: selecionar Sentinela, Firewall ou Sandbox.
- **Clique em uma torre colocada**: selecionar para ver alcance e nível.
- **U**: melhorar a torre selecionada.
- **Espaço**: iniciar a próxima onda.
- **F**: usar o pulso de firewall (habilidade especial com recarga).
- **T**: abrir a árvore de habilidades.
- **1 / 2 / 3** na árvore: desbloquear um caminho.
- **ESC**: fechar a árvore ou sair.
- **ENTER**: reiniciar após vitória ou derrota.

## Mecânicas incluídas
- Cinco fases com quantidade, resistência e velocidade dos malwares crescentes.
- Três tipos de torres com alcances, danos e cadências diferentes.
- Moeda em bytes: conversão binária de 1024 B = 1 KB, 1024 KB = 1 MB e assim por diante.
- Bônus por eliminar malwares e por concluir ondas.
- Árvore de habilidades com três caminhos: dano, recompensa e velocidade de ataque.
- Pulso especial de firewall, recarga, barras de vida, partículas e efeitos de impacto.
- Núcleo com integridade; malwares que chegam ao final reduzem a integridade.

## Observações
- O jogo desenha gráficos com formas do próprio Pygame e não precisa de imagens, fontes ou sons externos.
- O som não está implementado nesta versão; isso mantém o projeto independente de arquivos de áudio. Ele pode ser adicionado posteriormente.
- Os jogos citados servem apenas como inspiração geral. Este protótipo usa nome, código, elementos visuais e mecânicas próprias.
