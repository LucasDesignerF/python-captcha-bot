
# Discord Bot com Logs, CAPTCHA e Sistema de Ativação

Este é um bot de Discord criado utilizando o `nextcord`, com funcionalidades avançadas como:
- Logs de entrada e saída de membros.
- Verificação por CAPTCHA para novos membros.
- Sistema de ativação baseado em chave de licença para servidores.
- Integração com um banco de dados MySQL.

## Funcionalidades Principais
1. **Logs de entrada e saída de membros**: Configura canais para armazenar logs detalhados de novos membros que entram ou saem do servidor.
2. **CAPTCHA para novos membros**: Um sistema de verificação com CAPTCHA para garantir que apenas membros válidos tenham acesso ao servidor.
3. **Ativação do bot**: Sistema de ativação com chave de licença para servidores.

## Tecnologias Utilizadas
- **nextcord**: API para interações com Discord.
- **MySQL**: Banco de dados para armazenar logs e dados de ativação.
- **dotenv**: Gerenciamento de variáveis de ambiente.
- **captcha**: Geração de imagens CAPTCHA para verificação de usuários.

## Instalação

### Pré-requisitos
- Python 3.8+
- Uma conta no Discord e um servidor onde o bot será adicionado.
- Variáveis de ambiente configuradas no arquivo `.env` com as seguintes chaves:

\`\`\`plaintext
DISCORD_TOKEN=seu_token_do_discord
DB_HOST=endereco_do_banco_de_dados
DB_USER=usuario_do_banco_de_dados
DB_PASSWORD=senha_do_banco_de_dados
DB_NAME=nome_do_banco_de_dados
\`\`\`

### Passos para Instalação
1. **Clonar o repositório**:
   \`\`\`bash
   git clone https://github.com/LucasDesignerF/python-captcha-bot
   cd python-captcha-bot
   \`\`\`

2. **Criar e ativar um ambiente virtual**:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   \`\`\`

3. **Instalar as dependências**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Configurar o banco de dados**:
   Execute os seguintes comandos SQL para configurar a tabela de logs e servidores no MySQL:

   \`\`\`sql
   CREATE TABLE logs_canais (
       server_id BIGINT PRIMARY KEY,
       log_channel_join_id BIGINT,
       log_channel_leave_id BIGINT,
       log_color_join VARCHAR(7),
       log_color_leave VARCHAR(7),
       log_background_image_join TEXT,
       log_background_image_leave TEXT
   );

   CREATE TABLE servidores (
       server_id BIGINT PRIMARY KEY,
       activation_key VARCHAR(255)
   );
   \`\`\`

5. **Configurar o arquivo `.env`**:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

   \`\`\`plaintext
   DISCORD_TOKEN=seu_token_do_discord
   DB_HOST=localhost
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=nome_do_banco
   \`\`\`

6. **Rodar o bot**:
   Inicie o bot com o seguinte comando:
   \`\`\`bash
   python bot.py
   \`\`\`

## Estrutura do Projeto

\`\`\`plaintext
.
├── bot.py               # Arquivo principal do bot
├── cogs                 # Diretório contendo os Cogs (módulos) do bot
│   ├── logs.py          # Cog responsável pelos logs de entrada e saída de membros
│   ├── captcha.py       # Cog responsável pela verificação por CAPTCHA
│   └── activation.py    # Cog responsável pela ativação do bot via chave de licença
├── mysql_db.py          # Script para conectar ao banco de dados MySQL
├── .env                 # Arquivo de variáveis de ambiente (não versionado)
├── requirements.txt     # Arquivo com as dependências do projeto
└── README.md            # Documentação do projeto
\`\`\`

## Comandos Slash

- \`/configurar_logs\`: Configura os canais de logs para entradas e saídas de membros.
- \`/configurar_logs_cores\`: Configura as cores e imagens de fundo das embeds de log.
- \`/configurar_cargo\`: Configura o cargo que será dado ao membro após a verificação CAPTCHA.
- \`/ativar\`: Ativa o bot no servidor com uma chave de ativação.

## Contribuindo

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias e correções. Toda contribuição é bem-vinda!

## Licença

Este projeto está sob a licença MIT. Veja o arquivo \`LICENSE\` para mais detalhes.
