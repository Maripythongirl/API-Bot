import discord
import random
import pyttsx3
import asyncio
import os
import requests
from urllib.parse import quote_plus
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
voz_escolhida = 0


class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()

        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'

        self.add_item(discord.ui.Button(label="Pesquisar no Google 🔎", url=url))
# -------- Funções --------

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

def gen_emoji():
    emoji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emoji)

def flip_coin():
    flip = random.randint(0, 1)
    if flip == 0:
        return "cara"
    else:
        return "coroa"

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


# -------- Eventos --------

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')
    print('---------------------------------------')

# evento que detecta edição de mensagem
@bot.event
async def on_message_edit(before, after):
    msg = f'**{before.author}** editou a mensagem:\n{before.content} -> {after.content}'
    await before.channel.send(msg)


# -------- Comandos --------

# -------- Comandos de boas-vindas e clima --------

@bot.command()
async def start(ctx):
    await ctx.send(
        "Oi Oi! Seja bem-vindo(a) ao servidor! "
        "💖 Sinta-se à vontade e divirta-se! 💖"
    )

###-----------------------------------------------------###
def obter_clima(cidade):
    url = "https://wttr.in/" + cidade + "?format=j1"

    resposta = requests.get(url, timeout=10)

    if resposta.status_code != 200:
        return None

    dados = resposta.json()
    clima = dados["current_condition"][0]

    descricao = clima["weatherDesc"][0]["value"]
    temperatura = clima["temp_C"]
    sensacao = clima["FeelsLikeC"]
    umidade = clima["humidity"]
    vento = clima["windspeedKmph"]

    mensagem = (
        "Previsão do tempo para " + cidade + ". "
        "Condição: " + descricao + ". "
        "Temperatura: " + temperatura + " graus Celsius. "
        "Sensação térmica: " + sensacao + " graus. "
        "Umidade do ar: " + umidade + " por cento. "
        "Velocidade do vento: " + vento + " quilômetros por hora."
    )

    return mensagem


def falar(texto):
    motor = pyttsx3.init()

    vozes = motor.getProperty("voices")

    if len(vozes) > voz_escolhida:
        motor.setProperty("voice", vozes[voz_escolhida].id)

    motor.setProperty("rate", 150)
    motor.say(texto)
    motor.runAndWait()
    motor.stop()



@bot.command()
async def weather(ctx, *, cidade: str):
    await ctx.send("🌦️ Consultando o clima de " + cidade + "...")

    try:
        mensagem = await asyncio.to_thread(obter_clima, cidade)

        if mensagem is None:
            await ctx.send("Não consegui consultar o clima dessa cidade.")
            return

        await ctx.send("🌤️ " + mensagem)

        # Lê a previsão sem bloquear o bot
        await asyncio.to_thread(falar, mensagem)

    except requests.RequestException:
        await ctx.send("Não consegui conectar à API do clima. Tente novamente!")

    except (KeyError, IndexError, ValueError):
        await ctx.send("Não consegui interpretar a previsão do tempo.")



@bot.command()
async def raca(ctx, *, nome):
    url = "https://dogapi.dog/api/v2/breeds"
    params = {"page[size]": 1000}

    resposta = requests.get(url, params=params)
    dados = resposta.json()

    for item in dados["data"]:
        raca = item["attributes"]

        if nome.lower() == raca["name"].lower():
            embed = discord.Embed(
                title="🐶 " + raca["name"],
                description=raca["description"],
                color=discord.Color.pink()
            )

            vida = raca["life"]

            embed.add_field(
                name="💗 Expectativa de vida",
                value=str(vida["min"]) + " a "
                + str(vida["max"]) + " anos",
                inline=False
            )

            altura = raca["male_height"]

            embed.add_field(
                name="📏 Altura",
                value=str(altura["min"]) + " a "
                + str(altura["max"]) + " cm",
                inline=False
            )

            foto = (
                "https://dogapi.dog/api/v2/breeds/"
                + item["id"] + "/image"
            )

            embed.set_image(url=foto)

            await ctx.send(embed=embed)

            motor = pyttsx3.init()
            motor.setProperty("rate", 120)

            texto = (
                raca["name"] + ". "
                + raca["description"] + ". "
                + "Expectativa de vida: "
                + str(vida["min"]) + " a "
                + str(vida["max"]) + " anos. "
                + "Altura: "
                + str(altura["min"]) + " a "
                + str(altura["max"]) + " centímetros."
            )

            motor.say(texto)
            motor.runAndWait()
            motor.stop()
            return

    await ctx.send("Não encontrei essa raça! 🐾")


@bot.command()
async def fato(ctx):
        url = "https://uselessfacts.jsph.pl/random.json"

        resposta = requests.get(url)

        if resposta.status_code == 200:
            fato_aleatorio = resposta.json()["text"]
            await ctx.send(fato_aleatorio)
            await asyncio.to_thread(falar, fato_aleatorio)

        else:
            await ctx.send("Não foi possível buscar um fato agora!")
            return

        
@bot.command()
async def voz(ctx, escolha):
    global voz_escolhida

    if escolha.lower() == "masculina":
        voz_escolhida = 0
        await ctx.send("Voz masculina selecionada! 🔊")

    elif escolha.lower() == "feminina":
        voz_escolhida = 1
        await ctx.send("Voz feminina selecionada! 🎀")

    else:
        await ctx.send("Use !voz masculina ou !voz feminina")
    
  

@bot.command()
async def heroi(ctx):
    url = "https://myheroacademia-api.onrender.com/characters"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        categoria = random.choice(["students", "heroes", "villains"])
        personagem = random.choice(dados[categoria])

        nome = personagem["name"]
        individualidade = personagem.get("quirk", "Não informada")

        await ctx.send("💚 Personagem: " + nome +
                       "\n⚡ Individualidade: " + individualidade)

        await asyncio.to_thread(falar, nome + ". Individualidade: " + individualidade)
    else:
        await ctx.send("Não consegui buscar os personagens!")

    



@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! Eu sou um bot {bot.user}!')


@bot.command()
async def heh(ctx, count_heh: int = 5):
    await ctx.send("he" * count_heh)


@bot.command()
async def senha(ctx):
    await ctx.send(gen_pass(10))


@bot.command()
async def emoji(ctx):
    await ctx.send(gen_emoji())


@bot.command()
async def moeda(ctx):
    await ctx.send(flip_coin())


@bot.command()
async def entrada(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} entrou {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def google(ctx, *, pesquisa: str):
    await ctx.send(f'Resultado da busca para: `{pesquisa}`', view=Google(pesquisa))

@bot.command()
async def editme(ctx):
    msg = await ctx.send('10')
    await asyncio.sleep(3.0)
    await msg.edit(content='40')

@bot.command()
async def meme(ctx):
    memes = os.listdir("images")
    aleatorio = random.choice(memes)
    await ctx.send(file = discord.File(f"images/{aleatorio}"))


@bot.command('duck')
async def duck(ctx):
    #Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url
    image_url = get_duck_image_url()
    await ctx.send(image_url)


#specialbrother
@bot.command()
async def brother(ctx):
    await ctx.send("Paulo ou Rodrigo?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        resposta = await bot.wait_for('message', timeout=15.0, check=check)

        escolha = resposta.content.lower()

        if escolha == "paulo":
            await ctx.send("Homenagem ao Paulo 💙")
            await ctx.send(file=discord.File("brothers/paulo.mp4"))

        elif escolha == "rodrigo":
            await ctx.send("Homenagem ao Rodrigo 💙")
            await ctx.send(file=discord.File("brothers/ze.mp4"))

        else:
            await ctx.send("Escolha inválida 😅 Digite 'Paulo' ou 'Rodrigo'.")

    except asyncio.TimeoutError:
        await ctx.send("Você demorou para responder 😢")


@bot.command()
async def papai(ctx):

    await ctx.send(
        "💙 Papai...\n"
        "Essa é uma pequena homenagem para alguém tão importante.\n"
        "Obrigada por todas as experiências e memórias que vivemos juntos!\n"
        "Que Deus te abençoe muitooooo.\n"
        "Te amo muitooo, mesmo você sendo enjoado XD.\n"
        "Xoxo,\n"
        "Mari bebê"
    )

    await ctx.send("🎬 Agora um vídeo fofo com a NOSSA música! nhenhenhenhenhe🎬")
    await ctx.send(file=discord.File("papai/papai.mp4"))




bot.run("")
