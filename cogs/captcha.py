import nextcord
from nextcord.ext import commands
from captcha.image import ImageCaptcha
import random
import io

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_name = None  # Variável para armazenar o nome do cargo

    @nextcord.slash_command(name="configurar_cargo", description="Configura o cargo que será dado ao membro verificado.")
    async def configurar_cargo(self, interaction: nextcord.Interaction, role: nextcord.Role):
        self.role_name = role.name
        await interaction.response.send_message(f"O cargo {role.mention} foi configurado para membros verificados.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.role_name is None:
            await member.send("O cargo de verificação não está configurado. Por favor, informe o administrador do servidor.")
            return

        attempts = 3  # Número de tentativas
        image_captcha = ImageCaptcha()

        # Gerar um código CAPTCHA aleatório
        captcha_code = str(random.randint(1000, 9999))
        image = image_captcha.generate_image(captcha_code)
        
        # Salvar a imagem em um buffer
        buffer = io.BytesIO()
        image.save(buffer, 'PNG')
        buffer.seek(0)

        # Enviar a imagem CAPTCHA para o membro
        await member.send("Por favor, responda com o código CAPTCHA abaixo:")
        await member.send(file=nextcord.File(fp=buffer, filename='captcha.png'))

        while attempts > 0:
            def check(m):
                return m.author == member and m.content == captcha_code

            try:
                response = await self.bot.wait_for('message', check=check, timeout=120)
                if response:
                    role = nextcord.utils.get(member.guild.roles, name=self.role_name)
                    await member.add_roles(role)
                    await member.send("Verificação bem-sucedida! Bem-vindo ao servidor.")
                    return  # Sai da função após a verificação bem-sucedida
            except:
                pass  # Ignora o erro se o timeout acontecer

            attempts -= 1
            await member.send(f"CAPTCHA incorreto. Você ainda tem {attempts} tentativa(s).")

        await member.send("Você não passou no CAPTCHA. Por favor, tente novamente mais tarde.")

def setup(bot):
    bot.add_cog(Captcha(bot))
