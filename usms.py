import discord, requests, asyncio, json, os, roapipy
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
client.remove_command('help')
os.chdir("./usms")
tree = client.tree

pointsdir = "points.json"
infracsdir = "infractions.json"
applieddir = "applied.json"

def employee(interaction):
    return 935402244059316274 in [el.id for el in interaction.user.roles]

def usmicplus(interaction):
    return 935672777900441671 in [el.id for el in interaction.user.roles]

def adminstaffanddisciplineaction(interaction):
    return any(role_id in [935401876634099753, 982858358899998772] for role_id in [role.id for role in interaction.user.roles])

def adminstaff(interaction):
    return 935401876634099753 in [el.id for el in interaction.user.roles]

def hihicom(interaction):
    return any(role_id in [999499978231787590, 935402084017262612, 935402172252844123] for role_id in [role.id for role in interaction.user.roles])

def bigdaddyboys(interaction):
    return interaction.user.id in [255125932447236096, 494575907554590720]

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the U.S. Marshals Service"))
    print(f'USMS Automation now online with {round(client.latency * 1000)}ms ping.')

points = app_commands.Group(name="points", description="All things points related")
tree.add_command(points)

@points.command(name="check", description="Check a users' points")
async def check(interaction : discord.Interaction, user : discord.Member) -> None:
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(user.id) in data:
            totalpoints = data[str(user.id)]
        else:
            data[str(user.id)] = 0
            totalpoints = 0
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    embed = discord.Embed(
        title="Points",
        colour=0x0D45E6,
        description=""
    )
    embed.add_field(name=f"{user.name}#{user.discriminator}", value=f"{totalpoints}")
    await interaction.response.send_message(embed=embed)

@points.command(name="top", description="Check the top 10 users in terms of points")
async def top(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Top",
        colour=0x0D45E6,
        description=""
    )
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        ordered = dict(reversed(list(sorted(data.items(), key=lambda item: item[1]))))
    for el, foo in list(ordered.items())[:10]:
        person = client.get_user(int(el))
        if person != None:
            embed.add_field(name=f"{person.name}#{person.discriminator}", value=str(foo))
    await interaction.response.send_message(embed=embed)

@points.command(name="add", description="Add points to a user")
@app_commands.check(usmicplus)
async def add(interaction : discord.Interaction, user : discord.Member, amount : int):
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        new = 0
        if str(user.id) in data:
            data[str(user.id)] = data[str(user.id)] + amount
        else:
            data[str(user.id)] = amount
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
        new = data[str(user.id)]
    embed = discord.Embed(
        title="Add",
        colour=0x0D45E6,
        description=f"{user.mention}"
    )
    embed.add_field(name="Now", value=f"{new}")
    embed.add_field(name="Before", value=f"{new-amount}")
    await interaction.response.send_message(embed=embed)
    await user.send(f"{interaction.user.mention} has given you {amount} point(s)")

@add.error
async def adderror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@points.command(name="remove", description="Remove points from a user")
@app_commands.check(usmicplus)
async def remove(interaction : discord.Interaction, user : discord.Member, amount : int):
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        under0 = False
        if str(user.id) in data:
            if data[str(user.id)] - amount >= 0:
                data[str(user.id)] = data[str(user.id)] - amount
            else:
                under0 = True
        else:
            data[str(user.id)] = 0
            under0 = True
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
        new = data[str(user.id)]
    if under0 == True:
        await interaction.response.send_message("That user cannot have below 0 points")
    else:
        embed = discord.Embed(
            title="Remove",
            colour=0x0D45E6,
            description=f"{user.mention}"
        )
        embed.add_field(name="Now", value=f"{new}")
        embed.add_field(name="Before", value=f"{new+amount}")
        await interaction.response.send_message(embed=embed)
        await user.send(f"{interaction.user.mention} has removed {amount} point(s) from you")

@remove.error
async def removeerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@points.command(name="reset", description="Reset a users' points")
@app_commands.check(usmicplus)
async def reset(interaction : discord.Interaction, user : discord.Member):
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(user.id) in data:
            data[str(user.id)] = 0
        else:
            data[str(user.id)] = 0
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    embed = discord.Embed(
        title=f"Reset {user.name}#{user.discriminator}",
        colour=0x0D45E6,
        description="Done."
    )
    await interaction.response.send_message(embed=embed)
    await user.send(f"{interaction.user.mention} has reset your points")

@reset.error
async def reseterror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@points.command(name="resetall", description="Reset all users' points")
@app_commands.check(hihicom)
async def resetall(interaction : discord.Interaction):
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        for el in data:
            data[el] = 0
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    embed = discord.Embed(
        title="Reset All",
        colour=0x0D45E6,
        description="Done."
    )
    await interaction.response.send_message(embed=embed)

@resetall.error
async def resetallerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

log = app_commands.Group(name="log", description="All things logging related")
tree.add_command(log)

@log.command(name="patrol", description="Log your patrol")
@app_commands.check(employee)
async def patrol(interaction : discord.Interaction, totalminutes : int, screenshotstart : str, screenshotend : str):
    channel = client.get_channel(1013524748233355407)
    embed = discord.Embed(
        title="Patrol Log",
        colour=0x0D45E6,
        description=f"**Logger:**{interaction.user.mention}\n**Total:**{totalminutes}\n**Screenshot Start:**{screenshotstart}\n**Screenshot End:**{screenshotend}"
    )
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@patrol.error
async def patrolerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@log.command(name="event", description="Log your event")
@app_commands.check(usmicplus)
async def event(interaction : discord.Interaction, eventtype : str, totalminutes : int, screenshot : str, attendees : str):
    channel = client.get_channel(1013526324725428375)
    embed = discord.Embed(
        title="Event Log",
        colour=0x0D45E6,
        description=f"**Logger:**{interaction.user.mention}\n**Total Time:**{totalminutes}\n**Event Type:**{eventtype}\n**Screenshot:**{screenshot}\n**Attendees:**\n"
    )
    attendeeslist = attendees.split(" ")
    for el in attendeeslist:
        embed.description = f"{embed.description}{el}\n"
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@event.error
async def eventerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@log.command(name="inactive", description="Request inactivity")
@app_commands.check(employee)
async def inactive(interaction : discord.Interaction, start : str, end : str, reason : str):
    channel = client.get_channel(1013526352261042326)
    embed = discord.Embed(
        title="Inactivity Request",
        colour=0x0D45E6,
        description=f"**Inactive:**{interaction.user.mention}\n**Start:**{start}\n**End:**{end}\n**Reason:**{reason}"
    )
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@inactive.error
async def inactiveerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@log.command(name="resign", description="Request resignation")
@app_commands.check(employee)
async def resign(interaction : discord.Interaction, reason : str):
    channel = client.get_channel(1013526368551702530)
    embed = discord.Embed(
        title="Resignation Request",
        colour=0x0D45E6,
        description=f"**Resignee:**{interaction.user.mention}\n**Reason:**{reason}"
    )
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@resign.error
async def resignerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

infractions = app_commands.Group(name="infractions", description="All things infraction related")
tree.add_command(infractions)

@infractions.command(name="add", description="Warn a user")
@app_commands.check(usmicplus)
async def add(interaction : discord.Interaction, user : discord.Member, *, reason : str):
    with open(infracsdir, "r+") as f:
        data = json.load(f)
        if str(user.id) in data:
            data[str(user.id)].append(reason)
        else:
            data[str(user.id)] = [
                reason
            ]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    embed = discord.Embed(
        title="Warn",
        colour=0x0D45E6,
        description=f"{user.mention} has been warned for:```\n{reason}\n```"
    )
    await interaction.response.send_message(embed=embed)
    await user.send(f"{interaction.user.mention} has warned you for:\n{reason}")
    await client.get_channel(1013782999122321488).send(embed=discord.Embed(title="Warn", colour=0x0D45E6, description=f"{interaction.user.mention} has warned {user.mention} for:```\n{reason}\n```"))

@add.error
async def adderror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@infractions.command(name="clear", description="Clear a users' infractions")
@app_commands.check(usmicplus)
async def clear(interaction : discord.Interaction, user : discord.Member):
    with open(infracsdir, "r+") as f:
        data = json.load(f)
        if str(user.id) in data:
            data[str(user.id)] = []
        else:
            data[str(user.id)] = []
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    embed = discord.Embed(
        title=f"Clear Infractions {user.name}#{user.discriminator}",
        colour=0x0D45E6,
        description="Done."
    )
    await interaction.response.send_message(embed=embed)
    await user.send(f"{interaction.user.mention} has cleared your warns")
    await client.get_channel(1013782999122321488).send(embed=discord.Embed(title="Clear Infractions", colour=0x0D45E6, description=f"{interaction.user.mention} has cleared {user.mention}'s infractions"))

@clear.error
async def clearerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@infractions.command(name="clearall", description="Clear all users' infractions")
@app_commands.check(hihicom)
async def clearall(interaction : discord.Interaction):
    with open(infracsdir, "r+") as f:
        data = json.load(f)
        for el in data:
            data[el] = []
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    embed = discord.Embed(
        title="Clear All Infractions",
        colour=0x0D45E6,
        description="Done."
    )
    await interaction.response.send_message(embed=embed)
    await client.get_channel(1013782999122321488).send(embed=discord.Embed(title="Clear All Infractions", colour=0x0D45E6, description=f"{interaction.user.mention} has cleared everyone's infractions"))

@clearall.error
async def clearallerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@infractions.command(name="check", description="Check a users' infractions")
async def check(interaction : discord.Interaction, user : discord.Member):
    embed = discord.Embed(
        title="Infractions",
        colour=0x0D45E6,
        description=f"{user.mention}"
    )
    with open(infracsdir, "r+") as f:
        data = json.load(f)
        infracstr = ""
        totalinfracs = 0
        if str(user.id) in data:
            if len(data[str(user.id)]) > 0:
                for el in data[str(user.id)]:
                    totalinfracs += 1
                    infracstr = f"{infracstr}\n{el}"
            else:
                totalinfracs = 0
                infracstr = "\nN/A"
        else:
            totalinfracs = 0
            infracstr = "\nN/A"
    embed.description = f"{embed.description} - {totalinfracs}"
    embed.description = f"{embed.description}\n```{infracstr}\n```"
    await interaction.response.send_message(embed=embed)

punish = app_commands.Group(name="punish", description="All things punishment related")
tree.add_command(punish)

@punish.command(name="suspend", description="Suspend a user")
@app_commands.check(usmicplus)
async def suspend(interaction : discord.Interaction, who : discord.Member, reason : str):
    channel = client.get_channel(1013782999122321488)
    embed = discord.Embed(
        title="Suspend",
        colour=0x0D45E6,
        description=f"{interaction.user.mention} has suspended {who.mention} for:```\n{reason}\n```"
    )
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@suspend.error
async def suspenderror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@punish.command(name="term", description="Terminate a user")
@app_commands.check(adminstaffanddisciplineaction)
async def term(interaction : discord.Interaction, who : discord.Member, reason : str):
    channel = client.get_channel(1013782999122321488)
    for el in who.roles:
        if el.id in [990715934085886013, 935402244059316274, 1001673816784777307, 953436023214444564, 982858358899998772, 960379184989999176, 953435623333720064, 935681273664532480, 935677292204670996, 935671548784820225, 935671492727951390, 935671444585717801, 935671366231941170, 935671336846647377, 935672777900441671, 935671103995670548, 935401806190747740, 953441520772608020, 935401876634099753]:
            try:
                await who.remove_roles(el)
            except:
                pass
    embed = discord.Embed(
        title="Termination",
        colour=0x0D45E6,
        description=f"{interaction.user.mention} has terminated {who.mention} for:```\n{reason}\n```"
    )
    await channel.send(embed=embed)
    await interaction.response.send_message("Sent for review")

@term.error
async def termerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

msg = app_commands.Group(name="msg", description="All things message related")
tree.add_command(msg)

@msg.command(name="raw", description="Send a message")
@app_commands.check(hihicom)
async def raw(interaction : discord.Interaction, channel : discord.TextChannel, message : str):
    await channel.send(message)
    embed = discord.Embed(
        title=f"Message to #{channel.name}",
        colour=0x0D45E6,
        description=f"Message with body:```\n{message}\n```has been sent to {channel.mention} by {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@raw.error
async def rawerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@msg.command(name="user", description="Message a person")
@app_commands.check(hihicom)
async def user(interaction : discord.Interaction, who : discord.Member, message : str):
    await channel.send(message)
    embed = discord.Embed(
        title=f"Message to @{who.name}#{who.discriminator}",
        colour=0x0D45E6,
        description=f"Message with body:```\n{message}\n```has been sent to {who.mention} by {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@user.error
async def usererror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

@msg.command(name="embed", description="Create an embed")
@app_commands.check(hihicom)
async def embed(interaction : discord.Interaction, channel : discord.TextChannel, title : str, body : str):
    embed = discord.Embed(
        title=title,
        colour=0x0D45E6,
        description=body
    )
    await channel.send(embed=embed)
    embed = discord.Embed(
        title=f"Embed to #{channel.name}",
        colour=0x0D45E6,
        description=f"Embed with title `{title}` and description:```\n{body}\n```has been sent to {channel.mention} by {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@embed.error
async def embederror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("You have insufficient permissions for running this command")
    else:
        raise error

roclient = roapipy.Client("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_F37BD6ED52B6BD4E2AC738E915E994CDA62D75E7B0EBAC94703E6A18B5F461BE8044C86D892157BA955EFC6C139C6C403276FEA665609741F8CC8AB83A807D801A7EBF827A4BDCA613303C60041F6B4AB5865E598DD68BB3D74DDD284CE2E7DAA1C5387689C2DF884715EAE5D3AB55CAC8A09574932FBA8CBF812218EFA090C25F82629D306DCC024A10655616FC3980F1A2B6D33773CA49DC80495973AFECCE1046291C19225A26A9AED6123145B17A86247B6930B429B0B47378314EA8CE8AE493561AB06D6EA7E32C291021FF8DE619EE86F729B12A1CA060440C5AA060CC3D7073FCBCFA4E300A0DDE52F660EBD5D8C54F061DB23C0B924112572714006139A2444DD9BBCF82B80849CC6452D5EBA77A26D46A91036571F475550880C34EE9875097BB558F91933FFA4D43119B8B652014AFC2002C00835A632B5CA449B277121EB97368ECCD23951374C5BC9BD85149C8D8CDBC8777A2E61CDB1FB4DB2AE7DC642AB12E4EEFDE52C006E6CFCE721630871B")

group = app_commands.Group(name="group", description="All things group related")
tree.add_command(group)

@group.command(name="rank", description="Rank a user")
@app_commands.check(bigdaddyboys)
@app_commands.choices(rank = [
    Choice(name="Suspended", value="Suspended"),
    Choice(name="Protectee", value="Protectee"),
    Choice(name="Detention Enforcement Officer", value="Detention Enforcement Officer"),
    Choice(name="Deputy Marshal", value="Deputy Marshal"),
    Choice(name="Senior Deputy Marshal", value="Senior Deputy Marshal"),
    Choice(name="Supervisory Deputy Marshal", value="Supervisory Deputy Marshal"),
    Choice(name="Special Deputy Marshal", value="Special Deputy Marshal"),
    Choice(name="U.S. Marshal", value="U.S. Marshal"),
    Choice(name="U.S. Marshal in Charge", value="U.S. Marshal in Charge"),
    Choice(name="Chief U.S. Marshal", value="Chief U.S. Marshal"),
    Choice(name="Unit Commander", value="Unit Commander"),
    Choice(name="Administrative Staff", value="Administrative Staff"),
    Choice(name="Chief of Staff", value="Chief of Staff")
])
async def rank(interaction : discord.Interaction, who : str, rank : Choice[str]):
    rank = rank.value
    channel = client.get_channel(1014963624017662122)

    url = f"https://api.roblox.com/users/get-by-username"
    data = {
        "username": who
    }
    el = requests.get(url, data=data)
    el = json.loads(el.content)
    userid = el["Id"]
    el = roclient.User.Info(userid)

    roclient.Group.Rank(977773, userid, rank)


    embed = discord.Embed(
        title="Rank",
        colour=0x0D45E6,
        description=f"{interaction.user.mention} has ranked `{who}` to `{rank}`"
    )
    embed.set_thumbnail(url=el["avatar"])
    await interaction.response.send_message(embed=embed)
    await channel.send(embed=embed)

@rank.error
async def rankerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Nuh-uh buddy not today.")
    else:
        raise error

@group.command(name="exile", description="Exile a user")
@app_commands.check(bigdaddyboys)
async def exile(interaction : discord.Interaction, who : str):
    channel = client.get_channel(1014963624017662122)
    url = f"https://api.roblox.com/users/get-by-username"
    data = {
        "username": who
    }
    el = requests.get(url, data=data)
    el = json.loads(el.content)

    userid = el["Id"]
    el = roclient.User.Info(userid)

    roclient.Group.Exile(977773, userid)

    embed = discord.Embed(
        title="Exile",
        colour=0x0D45E6,
        description=f"{interaction.user.mention} has exiled `{who}`"
    )
    embed.set_thumbnail(url=el["avatar"])
    await interaction.response.send_message(embed=embed)
    await channel.send(embed=embed)

@exile.error
async def exile(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Nuh-uh buddy not today.")
    else:
        raise error

@group.command(name="accept", description="Accept a user")
@app_commands.check(bigdaddyboys)
async def accept(interaction : discord.Interaction, who : str):
    channel = client.get_channel(1014963624017662122)
    url = f"https://api.roblox.com/users/get-by-username"
    data = {
        "username": who
    }
    el = requests.get(url, data=data)
    el = json.loads(el.content)
    userid = el["Id"]
    el = roclient.User.Info(userid)

    roclient.User.Info(userid)
    roclient.Group.Accept(977773, userid)

    embed = discord.Embed(
        title="Accept",
        colour=0x0D45E6,
        description=f"{interaction.user.mention} has accepted `{who}`"
    )
    embed.set_thumbnail(url=el["avatar"])
    await interaction.response.send_message(embed=embed)
    await channel.send(embed=embed)

@accept.error
async def accept(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Nuh-uh buddy not today.")
    else:
        raise error

application = app_commands.Group(name="application", description="All things application related")
tree.add_command(application)

class Confirm(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Confirmed")
        self.value = True
        self.stop()
    
    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Denied")
        self.value = False
        self.stop()

@tree.command(name="apply", description="Apply to become a U.S. Marshal")
async def apply(interaction : discord.Interaction):
    if interaction.guild is None:
        canapply = True
        with open(applieddir, "r+") as f:
            data = json.load(f)
            if interaction.user.id in data["data"]:
                canapply = False
        if canapply == True:
            await interaction.response.send_message("Loading USMS Application System...")
            await interaction.edit_original_response(content=None, embed=discord.Embed(title="Success!", colour=0x0D45E6, description="Welcome to the USMS Application System,\nThis process should be synonymous to any other application you've taken on google forms or typeform.\nTo begin, please send your **Roblox** username.").set_footer(text="This prompt will timeout in 60 seconds."))
            def check(msg):
                return msg.author.id == interaction.user.id
            username = await client.wait_for("message", timeout=60, check=check)
            usercheck = requests.get(f"https://api.roblox.com/users/get-by-username", params={"username": username.content})
            usercheckresponse = json.loads(usercheck.text)
            if "success" in usercheckresponse:
                await username.reply("Hm, seems like that username doesn't exist on Roblox.\nApplication cancelled.")
            else:
                roname = usercheckresponse["Username"]
                roid = usercheckresponse["Id"]
                await username.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="What are some of your strengths/weaknesses").set_footer(text="This prompt will expire in 3 minutes."))
                strengthsweaknesses = await client.wait_for("message", timeout=180, check=check)
                await strengthsweaknesses.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="What is the responsibility of the United States Marshal Service").set_footer(text="This prompt will expire in 3 minutes."))
                responsibilities = await client.wait_for("message", timeout=180, check=check)
                await responsibilities.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="What interests you about the United States Marshal Service").set_footer(text="This prompt will expire in 3 minutes."))
                interest = await client.wait_for("message", timeout=180, check=check)
                await interest.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="Be honest, how active would you consider yourself (1-10)").set_footer(text="This prompt will expire in 60 seconds."))
                activity = await client.wait_for("message", timeout=60, check=check)
                await activity.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="Why should your application standout from other applications").set_footer(text="This prompt will expire in 5 minutes."))
                standout = await client.wait_for("message", timeout=300, check=check)
                await standout.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="How will the United States Marshal Service benefit by hiring you").set_footer(text="This prompt will expire in 5 minutes."))
                benefit = await client.wait_for("message", timeout=300, check=check)
                msg1 = await benefit.reply(embed=discord.Embed(title="Success!", colour=0x0D45E6, description="Ensure that your roblox inventory is set to __**public**__ as your application will instantly be denied if it is not."))
                view1 = Confirm(timeout=30)
                appagree = await msg1.reply(embed=discord.Embed(title="Agreement", colour=0x0D45E6, description="Do you agree that we may decline your application for any reason").set_footer(text="This prompt will expire in 30 seconds."), view=view1)
                await view1.wait()
                if view1.value is None:
                    await appagree.reply("Timed out.")
                elif view1.value:
                    view2 = Confirm(timeout=30)
                    policyagree = await appagree.reply(embed=discord.Embed(title="Agreement", colour=0x0D45E6, description="Do you agree to abide by all USMS [Policy](https://docs.google.com/document/d/13Dcstg5oUcvtlws6Gm12_sZDT0NUluntFmO18QjrbzQ/edit?usp=sharing) while employed within the USMS").set_footer(text="This prompt will expire in 30 seconds."), view=view2)
                    await view2.wait()
                    if view2.value is None:
                        await policyagree.reply("Timed out.")
                    elif view2.value:
                        embed = discord.Embed(
                            title="Success!",
                            colour=0x0D45E6,
                            description="Your application is complete!\nDoes everything look right?"
                        )
                        embed.add_field(name="Roblox", value=f"{roname} | {roid}")
                        embed.add_field(name="Discord", value=f"{interaction.user.name}#{interaction.user.discriminator} | {interaction.user.id}")
                        embed.add_field(name="Strengths/Weaknesses", value=strengthsweaknesses.content)
                        embed.add_field(name="Responsibilities", value=responsibilities.content)
                        embed.add_field(name="Interest", value=interest.content)
                        embed.add_field(name="Activity", value=activity.content)
                        embed.add_field(name="Standout", value=standout.content)
                        embed.add_field(name="Benefit", value=benefit.content)
                        embed.add_field(name="Application Agreement", value="Agree")
                        embed.add_field(name="Policy Agreement", value="Agree")
                        embed.set_footer(text="This prompt will expire in 60 seconds.")
                        view3 = Confirm(timeout=60)
                        allcorrect = await policyagree.reply(embed=embed, view=view3)
                        await view3.wait()
                        if view3.value is None:
                            await allcorrect.reply("Timed out.")
                        elif view3.value:
                            embed.title = f"{roname} Application"
                            embed.description = ""
                            embed.remove_footer()
                            appschannel = client.get_channel(1016740755072630855)
                            await appschannel.send(content=interaction.user.mention, embed=embed)
                            await allcorrect.reply("Your application has been sent for review!")
                            with open(applieddir, "r+") as f:
                                data = json.load(f)
                                data["data"].append(interaction.user.id)
                                f.seek(0)
                                f.truncate()
                                json.dump(data, f, indent=4)
                        else:
                            await allcorrect.reply("Cancelling...")
                    else:
                        await policyagree.reply("Cancelling...")
                else:
                    await appagree.reply("Cancelling...")
        else:
            await interaction.response.send_message("Uh-oh, seems like you've already submitted an application")
    else:
        await interaction.response.send_message("You can only apply in dms")

@application.command(name="accept", description="Accept a user's application")
@app_commands.check(usmicplus)
async def appaccept(interaction : discord.Interaction, who : discord.Member):
    with open(applieddir, "r+") as f:
        data = json.load(f)
        if who.id in data["data"]:
            data["data"].remove(who.id)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            msg = await interaction.response.send_message("Application status has been reset")
            try:
                await who.send("Your USMS Application has been accepted.")
                await msg.reply("User has been informed.")
            except:
                await msg.reply("Couldn't message the user.")
        else:
            await interaction.response.send_message("That user hasn't applied")

@appaccept.error
async def appaccepterror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Yeah no you cant do that.")
    else:
        raise error

@application.command(name="deny", description="Deny a user's application")
@app_commands.check(usmicplus)
async def appdeny(interaction : discord.Interaction, who : discord.Member):
    with open(applieddir, "r+") as f:
        data = json.load(f)
        if who.id in data["data"]:
            data["data"].remove(who.id)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            msg = await interaction.response.send_message("Application status has been reset")
            try:
                await who.send("Your USMS Application has been denied.")
                await msg.reply("User has been informed.")
            except:
                await msg.reply("Couldn't message the user.")
        else:
            await interaction.response.send_message("That user hasn't applied")

@appdeny.error
async def appdenyerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Yeah no you cant do that.")
    else:
        raise error

@application.command(name="appreset", description="Reset a user's application status")
@app_commands.check(usmicplus)
async def appreset(interaction : discord.Interaction, who : discord.Member):
    with open(applieddir, "r+") as f:
        data = json.load(f)
        if who.id in data["data"]:
            data["data"].remove(who.id)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            await interaction.response.send_message("Application status has been reset")
        else:
            await interaction.response.send_message("That user hasn't applied")

@appreset.error
async def appreseterror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message("Yeah no you cant do that.")
    else:
        raise error

@client.command()
@commands.check(lambda ctx : ctx.author.id in [301014178703998987, 255125932447236096])
async def connect(ctx):
    await tree.sync()

client.run('MTAxMjc3Mjc5MDU2MDExMjc0MA.G0iUfr.FVSkWqq90RaR4MLG_oPBw9NoidiF_FB3TULHr8')