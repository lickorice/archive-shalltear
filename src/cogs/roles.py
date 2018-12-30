import discord, json, datetime, math
from conf import *
from discord.ext import commands
from data import db_roles
from utils import msg_utils
from objects.role import Assignable

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

stored_messages = {}

# Start of program logic:

class Roles:
    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def on_reaction_remove(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    @commands.command(aliases=['ta'])
    @commands.guild_only()
    async def toggleassignable(self, ctx, *role_name):
        """Sets self-assignable roles. (Manage Roles)"""
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send(MSG_INSUF_PERMS)
            return

        role_name = ' '.join(role_name)
        if role_name == '':
            await ctx.send(MSG_INVALID_CMD)
            return

        try:
            target_role = [role for role in ctx.guild.roles if role.name == role_name][0]
        except IndexError:
            await ctx.send(MSG_ROLE_DNE)
            return

        if target_role > ctx.guild.get_member(self.bot.user.id).top_role:
            await ctx.send(MSG_ROLE_TOGGLE_3.format(target_role.name))
            return

        _role = Assignable(target_role.id, ctx.guild.id)
        result = _role.toggle_assignable()

        if result:
            await ctx.send(MSG_ROLE_TOGGLE_1.format(target_role.name))
            return
        else:
            await ctx.send(MSG_ROLE_TOGGLE_2.format(target_role.name))
            return

    @commands.command()
    @commands.guild_only()
    async def iam(self, ctx, *role_name):
        """Gives you a self-assignable role."""

        role_name = ' '.join(role_name)
        if role_name == '':
            await ctx.send(MSG_INVALID_CMD)
            return

        try:
            target_role = [role for role in ctx.guild.roles if role.name == role_name][0]
        except IndexError:
            await ctx.send(MSG_ROLE_DNE)
            return
        
        _role = Assignable(target_role.id, ctx.guild.id)
        if not _role.hash:
            await ctx.send(MSG_ROLE_NOT_ASSIGNABLE.format(ctx.author.id))
            return
        await ctx.send(MSG_ROLE_ASSIGNED.format(ctx.author.display_name, target_role.name))
        await ctx.author.add_roles(target_role, reason="Self-assignable role")

    @commands.command()
    @commands.guild_only()
    async def iamnot(self, ctx, *role_name):
        """Removes a self-assignable role."""

        role_name = ' '.join(role_name)
        if role_name == '':
            await ctx.send(MSG_INVALID_CMD)
            return

        try:
            target_role = [role for role in ctx.guild.roles if role.name == role_name][0]
        except IndexError:
            await ctx.send(MSG_ROLE_DNE)
            return
        
        _role = Assignable(target_role.id, ctx.guild.id)
        if not _role.hash:
            await ctx.send(MSG_ROLE_NOT_ASSIGNABLE.format(ctx.author.id))
            return
        await ctx.send(MSG_ROLE_UNASSIGNED.format(ctx.author.display_name, target_role.name))
        await ctx.author.remove_roles(target_role, reason="Self-assignable role")

    @commands.command(aliases=['lsa'])
    @commands.guild_only()
    async def listassignables(self, ctx):
        """Lists self-assignables."""
        db = db_roles.RoleHelper()
        db.connect()
        guild_roles = db.get_all_roles(ctx.guild.id)
        db.close()

        if len(guild_roles) == 0:
            await ctx.send(MSG_ROLE_NONE)
            return

        guild_roles = [ctx.guild.get_role(role["role_id"]) for role in guild_roles]
        guild_roles = sorted(guild_roles, key=lambda x: x.name)

        # generate the embed
        max_pages = math.ceil(len(guild_roles) / 10)
        p = msg_utils.PaginatedEmbed([], guild_roles, 0, "lsa", max_pages)
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)
        
        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)


def setup(bot):
    bot.add_cog(Roles(bot))