# goodluck :3, you will prolly want to check out the `on_message` first, as that is where the event handler for new messages is. it is located at line 26. - zyla

import discord
from discord.ext import commands
import aiohttp
import io

# define intents and set up the bot with all intents and a command prefix
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='~', intents=intents)

# define special user ids for admin like permissions
special_user_id1 = 661690191781691414
special_user_id2 = 788706178665283605

def is_admin_or_special_user(ctx):
    """check if the user is an administrator or a special user"""
    return ctx.author.guild_permissions.administrator or ctx.author.id in (special_user_id1, special_user_id2)

@bot.event
async def on_ready():
    """event handler for when the bot is ready"""
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    """event handler for new messages(what youre prolly gonna do the most in)"""
    if message.author.id in (special_user_id1, special_user_id2):
        if 'W?' in message.content:
            await message.channel.send('yes master')
        elif '<@1252510254382583888>' in message.content.lower() and 'good girl' in message.content.lower():
            await message.channel.send('thank you master')
        elif '<@1252510254382583888>' in message.content.lower():
            await message.channel.send('yes master?')

    await bot.process_commands(message)

async def update_channel_names(guild):
    """update names of text channels to maintain a sorted order"""
    sorted_channels = sorted(guild.text_channels, key=lambda c: c.position)
    for index, channel in enumerate(sorted_channels):
        new_name = f'{channel.name.rstrip("0123456789")}{index + 1}'
        await channel.edit(name=new_name)

async def update_voice_channel_names(guild):
    """update names of voice channels to maintain a sorted order"""
    sorted_channels = sorted(guild.voice_channels, key=lambda c: c.position)
    for index, channel in enumerate(sorted_channels):
        new_name = f'{channel.name.rstrip("0123456789")}{index + 1}'
        await channel.edit(name=new_name)

@bot.command()
@commands.check(is_admin_or_special_user)
async def kick(ctx, member: discord.Member, *, reason=None):
    """kicks a member from the server(nottested)"""
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} for reason: {reason}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def ban(ctx, member: discord.Member, *, reason=None):
    """bans a member from the server(nottested)"""
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for reason: {reason}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def unban(ctx, *, member_name):
    """unban a member by their name(nottested)"""
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
    await ctx.send(f'{member_name} not found in the ban list')

@bot.command()
@commands.check(is_admin_or_special_user)
async def nickname(ctx, member: discord.Member, *, new_nickname: str):
    """changes a members nickname"""
    try:
        await member.edit(nick=new_nickname)
        await ctx.send(f'{member.mention} changed to {new_nickname}')
    except discord.Forbidden:
        await ctx.send(f'No permissions to change {member.mention}\'s nickname')
    except discord.HTTPException as e:
        await ctx.send(f'Failed to change nickname: {e}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def servname(ctx, *, new_name: str):
    """changeer the server name"""
    try:
        await ctx.guild.edit(name=new_name)
        await ctx.send(f'Server name changed to {new_name}')
    except discord.Forbidden:
        await ctx.send(f'No permissions to change the server name')
    except discord.HTTPException as e:
        await ctx.send(f'Failed to change server name: {e}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def servicon(ctx, link2image: str):
    """changes the server icon"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link2image) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_bytes = io.BytesIO(image_data)
                    await ctx.guild.edit(icon=image_bytes.read())
                    await ctx.send('Server icon changed successfully')
                else:
                    await ctx.send('Failed to download the image')
    except discord.Forbidden:
        await ctx.send('No permissions to change the server icon')
    except discord.HTTPException as e:
        await ctx.send(f'Failed to change server icon: {e}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def createrole(ctx, permissions: str, *, role_name: str):
    """create a new role with specified perms"""
    try:
        perm_dict = {perm: True for perm in permissions.split(',')}
        perms = discord.Permissions(**perm_dict)
        role = await ctx.guild.create_role(name=role_name, permissions=perms)
        await ctx.send(f'Role `{role_name}` created successfully')
    except discord.Forbidden:
        await ctx.send('No permissions to create roles')
    except discord.HTTPException as e:
        await ctx.send(f'Failed to create role: {e}')

@bot.command()
@commands.check(is_admin_or_special_user)
async def role(ctx, member: discord.Member, *, role_name: str):
    """adds a role to a member"""
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'Role `{role_name}` added to {member.mention}')
    else:
        await ctx.send(f'Role `{role_name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def rerole(ctx, member: discord.Member, *, role_name: str):
    """removes a role from a member"""
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        await ctx.send(f'Role `{role_name}` removed from {member.mention}')
    else:
        await ctx.send(f'Role `{role_name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def createchannel(ctx, *, name: str):
    """creates a new text channel"""
    await ctx.guild.create_text_channel(name)
    await update_channel_names(ctx.guild)
    await ctx.send(f'Channel `{name}` created successfully')

@bot.command()
@commands.check(is_admin_or_special_user)
async def deletechannel(ctx, *, name: str):
    """deletes an existing text channel"""
    channel = discord.utils.get(ctx.guild.channels, name=name)
    if channel:
        await channel.delete()
        await update_channel_names(ctx.guild)
        await ctx.send(f'Channel `{name}` deleted successfully')
    else:
        await ctx.send(f'Channel `{name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def addcategory(ctx, *, name: str):
    """creates a new category"""
    await ctx.guild.create_category(name)
    await ctx.send(f'Category `{name}` created successfully')

@bot.command()
@commands.check(is_admin_or_special_user)
async def removecategory(ctx, *, name: str):
    """deletes an existing category"""
    category = discord.utils.get(ctx.guild.categories, name=name)
    if category:
        await category.delete()
        await ctx.send(f'Category `{name}` deleted successfully')
    else:
        await ctx.send(f'Category `{name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def movechannel(ctx, name: str, position: int):
    """moves a channel to a new position"""
    channel = discord.utils.get(ctx.guild.channels, name=name)
    if channel:
        await channel.edit(position=position-1)
        await ctx.send(f'Channel `{name}` moved to position {position}')
    else:
        await ctx.send(f'Channel `{name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def placechannel(ctx, name: str, categoryname: str, position: int):
    """places a channel in a specific category and position"""
    channel = discord.utils.get(ctx.guild.channels, name=name)
    category = discord.utils.get(ctx.guild.categories, name=categoryname)
    if channel and category:
        await channel.edit(category=category, position=position-1)
        if isinstance(channel, discord.TextChannel):
            await update_channel_names(ctx.guild)
        elif isinstance(channel, discord.VoiceChannel):
            await update_voice_channel_names(ctx.guild)
        await ctx.send(f'Channel `{name}` placed in category `{categoryname}` at position {position}')
    else:
        await ctx.send(f'Channel or category not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def createvoicechannel(ctx, *, name: str):
    """creates a new voice channel"""
    await ctx.guild.create_voice_channel(name)
    await update_voice_channel_names(ctx.guild)
    await ctx.send(f'Voice channel `{name}` created successfully')

@bot.command()
@commands.check(is_admin_or_special_user)
async def deletevoicechannel(ctx, *, name: str):
    """deletes an existing voice channel"""
    channel = discord.utils.get(ctx.guild.voice_channels, name=name)
    if channel:
        await channel.delete()
        await update_voice_channel_names(ctx.guild)
        await ctx.send(f'Voice channel `{name}` deleted successfully')
    else:
        await ctx.send(f'Voice channel `{name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def movevoicechannel(ctx, name: str, position: int):
    """moves a voice channel to a new position"""
    channel = discord.utils.get(ctx.guild.voice_channels, name=name)
    if channel:
        await channel.edit(position=position-1)
        await update_voice_channel_names(ctx.guild)
        await ctx.send(f'Voice channel `{name}` moved to position {position}')
    else:
        await ctx.send(f'Voice channel `{name}` not found')

@bot.command()
@commands.check(is_admin_or_special_user)
async def cmds(ctx):
    """lists all available commands"""
    commands_list = '''
    (Ping the bot to make sure it's active)
    ~kick <member> <reason>
    ~ban <member> <reason>
    ~unban <member_name>
    ~nickname <member> <new_nickname>
    ~servname <new_name>
    ~servicon <link2image>
    ~createrole <permissions> <role_name>
    ~role <member> <role_name>
    ~rerole <member> <role_name>
    ~createchannel <name>
    ~deletechannel <name>
    ~addcategory <name>
    ~removecategory <name>
    ~movechannel <name> <position>
    ~placechannel <name> <categoryname> <position>
    ~createvoicechannel <name>
    ~deletevoicechannel <name>
    ~movevoicechannel <name> <position>
    '''
    await ctx.send(f'Available commands: ```{commands_list}```')

# run the bot with your token
bot.run('<token>')
