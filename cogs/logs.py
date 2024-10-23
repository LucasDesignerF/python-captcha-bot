import nextcord
from nextcord.ext import commands
from nextcord import Embed
from mysql_db import get_db_connection

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando para configurar os canais de logs de entrada e saída
    @nextcord.slash_command(name="configurar_logs", description="Configura os canais de logs para entradas e saídas de membros.")
    async def configurar_logs(self, interaction: nextcord.Interaction, canal_entrada: nextcord.TextChannel, canal_saida: nextcord.TextChannel):
        guild_id = interaction.guild.id
        channel_join_id = canal_entrada.id
        channel_leave_id = canal_saida.id

        # Conectar ao banco de dados e salvar os canais de logs
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar se os canais de logs já estão configurados
        cursor.execute("SELECT * FROM logs_canais WHERE server_id = %s", (guild_id,))
        result = cursor.fetchone()

        if result:
            # Atualizar os canais de logs existentes
            cursor.execute("""
                UPDATE logs_canais 
                SET log_channel_join_id = %s, log_channel_leave_id = %s 
                WHERE server_id = %s
            """, (channel_join_id, channel_leave_id, guild_id))
        else:
            # Inserir novos canais de logs
            cursor.execute("""
                INSERT INTO logs_canais (server_id, log_channel_join_id, log_channel_leave_id) 
                VALUES (%s, %s, %s)
            """, (guild_id, channel_join_id, channel_leave_id))

        connection.commit()
        cursor.close()
        connection.close()

        await interaction.response.send_message(f"Os canais {canal_entrada.mention} (entrada) e {canal_saida.mention} (saída) foram configurados para logs de membros.")

    # Comando para configurar as cores e as imagens de fundo das embeds de log
    @nextcord.slash_command(name="configurar_logs_cores", description="Configura as cores das embeds de log e as URLs das imagens de fundo.")
    async def configurar_logs_cores(self, interaction: nextcord.Interaction, cor_entrada: str, cor_saida: str, url_imagem_entrada: str, url_imagem_saida: str):
        guild_id = interaction.guild.id
        
        # Conectar ao banco de dados e salvar as configurações
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar se as configurações já existem
        cursor.execute("SELECT * FROM logs_canais WHERE server_id = %s", (guild_id,))
        result = cursor.fetchone()

        if result:
            # Atualizar as cores e as URLs das imagens de fundo
            cursor.execute("""
                UPDATE logs_canais 
                SET log_color_join = %s, log_color_leave = %s, log_background_image_join = %s, log_background_image_leave = %s 
                WHERE server_id = %s
            """, (cor_entrada, cor_saida, url_imagem_entrada, url_imagem_saida, guild_id))
        else:
            await interaction.response.send_message("Os canais de logs não estão configurados. Configure os canais primeiro usando /configurar_logs.")
            return

        connection.commit()
        cursor.close()
        connection.close()

        await interaction.response.send_message(f"As cores das embeds foram configuradas: Entrada - {cor_entrada}, Saída - {cor_saida}, URL da imagem de fundo de entrada - {url_imagem_entrada}, URL da imagem de fundo de saída - {url_imagem_saida}.")

    # Evento de quando um membro entra no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Buscar o canal de logs de entrada no banco de dados
        cursor.execute("SELECT log_channel_join_id, log_color_join, log_background_image_join FROM logs_canais WHERE server_id = %s", (guild.id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result and result['log_channel_join_id']:
            channel_id = int(result['log_channel_join_id'])
            channel = guild.get_channel(channel_id)

            if channel:
                embed = Embed(title="Novo Membro!", description=f"{member.name} entrou no servidor.", color=int(result['log_color_join'], 16))
                embed.add_field(name="Membro:", value=f"{member.mention}", inline=True)
                embed.add_field(name="ID:", value=f"{member.id}", inline=True)
                embed.add_field(name="Contagem de Membros:", value=f"{guild.member_count}", inline=True)
                embed.set_thumbnail(url=member.avatar.url)

                # Adicionar a imagem de fundo, se houver
                if result['log_background_image_join']:
                    embed.set_image(url=result['log_background_image_join'])

                await channel.send(embed=embed)

    # Evento de quando um membro sai do servidor
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Buscar o canal de logs de saída no banco de dados
        cursor.execute("SELECT log_channel_leave_id, log_color_leave, log_background_image_leave FROM logs_canais WHERE server_id = %s", (guild.id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result and result['log_channel_leave_id']:
            channel_id = int(result['log_channel_leave_id'])
            channel = guild.get_channel(channel_id)

            if channel:
                embed = Embed(title="Membro Saiu", description=f"{member.name} saiu do servidor.", color=int(result['log_color_leave'], 16))
                embed.add_field(name="Membro:", value=f"{member.mention}", inline=True)
                embed.add_field(name="Contagem de Membros:", value=f"{guild.member_count}", inline=True)
                embed.set_thumbnail(url=member.avatar.url)

                # Adicionar a imagem de fundo, se houver
                if result['log_background_image_leave']:
                    embed.set_image(url=result['log_background_image_leave'])

                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))
