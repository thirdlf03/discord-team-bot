import discord
import random
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
token = 'your_discord_bot_token'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')    
    
@bot.command(name='create')
async def create_team(ctx):
    global team_1, team_2, t1_name, t2_name
    #チームを事前に登録 コマンドで登録できるようにしたい
    team_1 = []
    team_2 = []
    t1_name = []
    t2_name = []
    
    #参加しているvcのメンバー取得
    lobby_channel = ctx.author.voice.channel
    lobby_members = lobby_channel.members

    
    n = len(lobby_members) - len(team_1) - len(team_2)
    half = int(n / 2)

    #メンバーのidとニックネームの取得
    member_ids = [member.id for member in lobby_members]
    nicks = [member.nick for member in lobby_members]

    #事前登録メンバーを削除
    for i in range(len(team_1)):
        if team_1[i] in member_ids:
            member_ids.remove(team_1[i])
            nicks.remove(t1_name[i])

    for i in range(len(team_2)):
        if team_2[i] in member_ids:
            member_ids.remove(team_2[i])
            nicks.remove(t2_name[i])
    
    r = random.sample(range(0, n, 1), n)

    #チーム決め
    if n % 2 == 0:
        for i in range(half):
            team_1.append(member_ids[r[i]])
            t1_name.append(nicks[r[i]])
            team_2.append(member_ids[r[i + half]])
            t2_name.append(nicks[r[i + half]])
    else:
        for i in range(half):
            if n == 1:
                team_1.append(member_ids[r[i]])
                t1_name.append(nicks[r[i]])
                break;
            else:
                team_1.append(member_ids[r[i]])
                t1_name.append(nicks[r[i]])
                team_2.append(member_ids[r[i + half]])
                t2_name.append(nicks[r[i + half]])
        team_1.append(member_ids[r[-1]])
        t1_name.append(nicks[r[-1]])

    await ctx.send(f'チーム1は {t1_name}')
    await ctx.send(f'チーム2は {t2_name}')

@bot.command(name='check')
async def check(ctx):
    await ctx.send(f'チーム1は {t1_name}')
    await ctx.send(f'チーム2は {t2_name}')

@bot.command(name='start')
async def move_to_team1(ctx):

    #移動させたいチャンネルの登録
    team1_channel_id = 'your_vc_id'
    team1_channel = bot.get_channel(team1_channel_id)

    team2_channel_id = 'your_vc2_id'
    team2_channel = bot.get_channel(team2_channel_id)

    #参加しているvcのメンバー取得
    lobby_channel = ctx.author.voice.channel
    lobby_members = lobby_channel.members

    #vcチャンネルの取得
    team1_channel = bot.get_channel(team1_channel_id)
    team2_channel = bot.get_channel(team2_channel_id)

    #移動
    for member in lobby_members:
        if member.id in team_1:
            await member.move_to(team1_channel)
        elif member.id in team_2:
            await member.move_to(team2_channel)

# ボットのトークンを設定
bot.run(token)
