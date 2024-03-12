import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

logs_channel_id = 1216891464022228992
owner_id = 660038868057325569

@bot.event
async def on_ready():
    print("Bot Is Ready!")

@bot.command()
async def role(ctx, role_name: str, name1: str, name2: str):
    role_channel = bot.get_channel(1126191952015138927)

    if ctx.channel != role_channel:
        await ctx.send("מצטער הפקודה הזאת יכולה להיעשות אך ורק בחדר (<#1126191952015138927>)")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        return

    await ctx.message.add_reaction('✅')

    def check(payload):
        allowed_roles = ["Command", "High Command"]
        user = ctx.guild.get_member(payload.user_id)
        return payload.message_id == ctx.message.id and str(payload.emoji) == "✅" and any(role.name in allowed_roles for role in user.roles)

    payload = await bot.wait_for("raw_reaction_add", check=check)

    try:
        await ctx.author.edit(nick=f"{name1} | {name2}")
    except discord.Forbidden:
        pass

    try:
        await ctx.author.add_roles(role)
    except discord.Forbidden:
        pass

    await ctx.message.delete()

    accepted_member = ctx.guild.get_member(payload.user_id)

    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        member_roles = ", ".join([r.name for r in ctx.author.roles])

        embed = discord.Embed(title="עדכון רולים", color=0x000000)  
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר שעודכן", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="מפקד אשר אישר את הבקשה", value=f"{accepted_member.mention}", inline=False)
        embed.add_field(name="דרגה עדכנית", value=role_name, inline=False)
        embed.add_field(name="שם ותג חדש", value=f"{name1} | {name2}", inline=False)
        embed.add_field(name="כל הרולים של השוטר", value=member_roles, inline=False)

        await logs_channel.send(embed=embed)

@bot.command()
async def Rerole(ctx, member: discord.Member, role_name: str):
    if ctx.channel.id != 1216852660234485871:
        await ctx.message.delete()
        return

    allowed_roles = ["Command", "High Command"]
    if not any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.message.delete()
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        return

    if role not in member.roles:
        return

    
    try:
        await member.remove_roles(role)
    except discord.Forbidden:
        return

 
    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        embed = discord.Embed(title="מחיקת רול על ידי מפקד", color=0xFF0000) 
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר", value=member.mention, inline=False)
        embed.add_field(name="הרול שירד", value=role_name, inline=False)
        await logs_channel.send(embed=embed)

   
    await ctx.message.delete()

@bot.command()
async def Arole(ctx, member: discord.Member, role_name: str):
  
    if ctx.channel.id != 1216852660234485871:
        await ctx.message.delete()
        return

  
    allowed_roles = ["Command", "High Command"]
    if not any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.message.delete()
        return

   
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        return

   
    try:
        await member.add_roles(role)
    except discord.Forbidden:
        return

   
    if role_name in ["Officer", "Sr.Officer", "Corporal"]:
        lspd_role = discord.utils.get(ctx.guild.roles, name="L.S.P.D")
        if lspd_role:
            try:
                await member.add_roles(lspd_role)
            except discord.Forbidden:
                pass

  
    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        embed = discord.Embed(title="הוספת רול על ידי מפקד", color=0x00FF00) 
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר", value=member.mention, inline=False)
        embed.add_field(name="רול שנוסף", value=role_name, inline=False)
        await logs_channel.send(embed=embed)

    await ctx.message.delete()

@bot.command()
async def Ntag(ctx, member: discord.Member, new_name: str):
  
    if ctx.channel.id != 1216852660234485871:
        await ctx.message.delete()
        return

  
    allowed_roles = ["Command", "High Command"]
    if not any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.message.delete()
        return

    
    current_nick = member.display_name.split(" | ")

    current_nick[0] = new_name

   
    new_nick = " | ".join(current_nick)

   
    try:
        await member.edit(nick=new_nick)
    except discord.Forbidden:
        return

   
    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        embed = discord.Embed(title="תג חדש", color=0x0000FF) 
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר", value=member.mention, inline=False)
        embed.add_field(name="התג", value=new_nick, inline=False)
        await logs_channel.send(embed=embed)

 
    await ctx.message.delete()

@bot.command()
async def Rescop(ctx, member: discord.Member):
   
    if ctx.channel.id != 1216852660234485871:
        await ctx.message.delete()
        return

   
    allowed_roles = ["High Command"]
    if not any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.message.delete()
        return

    try:
        await member.edit(roles=[], reason="Role reset by command")
    except discord.Forbidden:
        return

   
    try:
        await member.edit(nick=None, reason="Nickname reset by command")
    except discord.Forbidden:
        return

    
    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        embed = discord.Embed(title="איפוס רולים ותג על ידי מפקד", color=0xFFA500)  
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר", value=member.mention, inline=False)
        embed.add_field(name="הרולים שהוסרו", value="כל הרולים", inline=False)
        await logs_channel.send(embed=embed)

  
    await ctx.message.delete()

@bot.command()
async def Njob(ctx, member: discord.Member, role_name: str, name1: str, name2: str):
    
    if ctx.channel.id != 1216852660234485871:
        await ctx.message.delete()
        return

  
    allowed_roles = ["Command", "High Command"]
    if not any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.message.delete()
        return

   
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.message.delete()
        return

 
    try:
        await member.edit(nick=f"{name1} | {name2}")
    except discord.Forbidden:
        pass

 
    try:
        await member.add_roles(role)
    except discord.Forbidden:
        pass

    logs_channel = bot.get_channel(logs_channel_id)
    if logs_channel:
        embed = discord.Embed(title="שינוי תפקיד ותג על ידי מפקד", color=0x00FFFF)
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="שוטר", value=member.mention, inline=False)
        embed.add_field(name="תפקיד חדש", value=role_name, inline=False)
        embed.add_field(name="שם חדש", value=f"{name1} | {name2}", inline=False)
        await logs_channel.send(embed=embed)

    await ctx.message.delete()


@bot.command()
async def CommandList(ctx):
    if ctx.author.id != owner_id:
        return

    command_list = [
        ("!role (שם-הרול) (תג) (שם IC)", "אחרי אישור מפקד מוסיף את הרול המבוקש ומשנה את השם והתג(חשוב לכתוב את שם הרול במדויק)"),
        ("!Rerole (@שוטר) (שם-הרול)", "מוריד את הרול המבוקש מהשוטר המבוקש"),
        ("!Arole (@שוטר) (שם-הרול)", "מוסיף את הרול המבוקש לשוטר"),
        ("!Ntag (@שוטר) (תג חדש)", "משנה את התג לשוטר המבוקש"),
        ("!Rescop (@שוטר)", "מאפס את השם והרולים של השוטר(רק פיקוד גבוה)"),
        ("!Njob (@שוטר) (שם-הרול) (תג) (שם IC)", "מאפשר להוסיף רול + תג + שם IC"),
    ]

    embed = discord.Embed(title="Bot Command List", color=0x008000)
    embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)

    for command, description in command_list:
        embed.add_field(name=command, value=description, inline=False)

    await ctx.send(embed=embed)

with open("token.txt") as file:
    token = file.read()

bot.run(token)
