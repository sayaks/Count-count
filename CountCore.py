import discord
import os

import ConsoleBox

def main():

    try:
        token = os.environ['COUNT_DISCORD_TOKEN']
    except KeyError:
        print('You must set the environment variable `COUNT_DISCORD_TOKEN` to your bot token.')
        quit()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    client = discord.Client()

    @client.event
    async def on_ready():
        await client.change_presence(game=discord.Game(name='=help', type=1), afk=False)
        srvrs = 0
        chnnl = 0
        for PrivateChannel in client.private_channels:
            chnnl += 1
        for server in client.servers:
            srvrs += 1

        box = ConsoleBox.Box()
        box.add_field('Logged in as:')\
            .add_field(client.user.name)\
            .add_empty()\
            .add_field('Bot ID:')\
            .add_field(client.user.id)\
            .add_empty()\
            .add_field('Servers:')\
            .add_field(str(srvrs))\
            .add_empty()\
            .add_field('Private Channels:')\
            .add_field(str(chnnl))
        print(box.generate_box())

    @client.event
    async def on_message(message):
        if message.content.startswith('=fetch1'):
            calc = await client.send_message(message.channel, 'You can Count on Count Count to Count your messages!')
            counter = 0
            async for msg in client.logs_from(message.channel, limit=500000):
                if msg.author == message.author:
                    counter += 1
            await client.send_message(message.channel, message.author.mention + 'Counting done, final amount: `{}`'.format(str(counter)))
            return

        if message.content.startswith('=fetch2'):
            calc = await client.send_message(message.channel, 'You can Count on Count Count to Count your messages!')
            counter = 0
            async for msg in client.logs_from(message.channel, limit=500000):
                if msg.author == message.author:
                    counter += 1
                if counter % 1000 == 0:
                    await client.edit_message(calc, "{} has {} messages in #{}".format(message.author, str(counter), message.channel))
            await client.send_message(message.channel, message.author.mention + 'Counting done, final amount: `{}`'.format(str(counter)))
            return

        if message.content.startswith('=fetch'):
            fetch_target = message.mentions[0] if message.mentions else message.author
            dp_name = str(fetch_target)[:-5]
            embed = discord.Embed(title="I'm busy counting~", color=0x9975b9)
            calc = await client.send_message(message.channel, embed=embed)
            counter = 0
            Ctotal = 0
            async for msg in client.logs_from(message.channel, limit=500000):
                Ctotal += 1
                if msg.author == fetch_target:
                    counter += 1
                sum = Ctotal / 100
                sum2 = counter / sum
                sum3 = round(sum2, 2)
                if  (Ctotal % 5000 == 0):
                    embed2 = discord.Embed(title="I'm busy counting~", color=0xff0000)
                    embed2.set_author(name=dp_name, icon_url=fetch_target.avatar_url)
                    embed2.add_field(name="Total messages counted:", value="{} messages so far".format(Ctotal), inline=False)
                    embed2.add_field(name="Messages of {}:".format(dp_name), value="{} messages".format(counter), inline=False)
                    embed2.add_field(name="Your message participation percentage:", value="{}%".format(sum3), inline=False)
                    embed2.set_footer(text="counting done soonTM")
                    await client.edit_message(calc, embed=embed2)
            embed3 = discord.Embed(title="I'm done counting!", color=0x00ff00)
            embed3.set_author(name=dp_name, icon_url=fetch_target.avatar_url)
            embed3.add_field(name="Total messages counted:", value="{} messages".format(Ctotal), inline=False)
            embed3.add_field(name="Messages of {}:".format(dp_name), value="{} messages".format(counter), inline=False)
            embed3.add_field(name="Your message participation percentage:", value="{}%".format(sum3), inline=False)
            embed3.set_footer(text="counting done!")
            await client.delete_message(calc)
            await client.send_message(message.channel, embed=embed3)
            await client.send_message(message.channel, message.author.mention)
            return

        if message.content.startswith('=log'):
            counter = 0
            async for msg in client.logs_from(message.channel, limit=200):
                if msg.author == client.user:
                    counter += 1
                await client.send_message(message.channel, counter)
                return

        if message.content.startswith('=count'):
            with open(os.path.join(dir_path, "iteration.txt"), "r") as text_file:
                data=text_file.read()
            count = int(data)
            count += 1
            text_file.close()
            with open(os.path.join(dir_path, "iteration.txt"), "w") as text_file:
                text_file.write(str(count))
            text_file.close()
            await client.send_message(message.channel, str(count))
            return

        if message.content.startswith('=help'):
            dp_name = str(message.author)[:-5]
            embed = discord.Embed(title="The commands so far:", color=0x9975b9)
            embed.set_author(name=dp_name, icon_url=message.author.avatar_url)
            embed.add_field(name="=fetch", value="Fetches all your messages in this channel, and shows some statistics", inline=True)
            embed.add_field(name="=count", value="Globally count with people from other servers! \n_increases the count everytime someone runs \"=count\"_", inline=True)
            #embed.add_field(name="=fetch1 (depricated)", value="This command looks through the entire channel history and shows you your total messages send (faster)", inline=True)
            #embed.add_field(name="=fetch2 (depricated)", value="Same as the above, although this time the bot will update it's progress (slower)", inline=True)
            embed.add_field(name="=help", value="Shows this message, wasn't that helpful? :^)",     inline=True)
            embed.set_footer(text="soonTM")
            await client.send_message(message.channel, embed=embed)
            return

    client.run(token)


def logout():
    discord.Client.logout()


if __name__ == '__main__':
    main()
