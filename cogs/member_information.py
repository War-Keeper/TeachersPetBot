import discord
from discord.ext import commands

# ---------------------------------------------------------------------------------------
# Contains Instructor only commands for getting member information
# ---------------------------------------------------------------------------------------
class Helper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------------------------------
    #    Function: get_member_information(self, ctx, *, member_name: str = None)
    #    Description: Instructor command for getting information about member
    #                 based on member_username
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - member_name: username of the member
    # ----------------------------------------------------------------------------------------------
    @commands.command(name="whois", help="This command is used to get information about the member")
    @commands.has_role("Instructor")
    async def get_member_information(self, ctx, *, member_name: str = None):
        msg = ctx.message.content
        await ctx.message.delete()
        if ctx.channel.name == "instructor-commands": # check for channel
            if member_name is None: # Error handling for None member_name
                embed = discord.Embed(
                    description="!whois command should be used in following way:"
                    + "\n\n`!whois member_username`",
                    color=discord.colour.Color.red(),
                )
                await ctx.author.send(embed=embed)
                return
            member = ctx.guild.get_member_named(member_name)
            if member:
                roles = [role for role in member.roles]
                embed = discord.Embed(
                    colour=discord.Colour.orange(),
                    timestamp=ctx.message.created_at,
                    title=str(member),
                )
                # embed information about member
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Display Name:", value=member.display_name)
                embed.add_field(name="ID:", value=member.id)
                embed.add_field(
                    name="Created Account On:",
                    value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                )
                if member.joined_at is not None:
                    embed.add_field(
                        name="Joined Server On:",
                        value=(
                            member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
                        ),
                    )
                embed.add_field(
                    name="Roles:", value="".join([role.mention for role in roles[1:]])
                )
                embed.add_field(name="Highest Role:", value=member.top_role.mention)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description="!whois could not find member with username\n\n`{member_name}`",
                    color=discord.colour.Color.red(),
                )
                await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(
                description="`!whois` can only be used in the `instructor-commands` channel."
                + "\n\nYou entered the following command:\n\n`"
                + msg
                + "`",
                color=discord.colour.Color.red(),
            )
            await ctx.author.send(embed=embed)

# add the file to the bot's cog system
# --------------------------------------
def setup(bot):
    bot.add_cog(Helper(bot))
