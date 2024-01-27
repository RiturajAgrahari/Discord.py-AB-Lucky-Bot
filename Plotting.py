import matplotlib.pyplot as plt
import numpy as np
import discord
from database import select_query
from discord.ui import View

# async def show_graph(client, user, interaction, offset:int=0):
#     button1 = button2 = False
#     sn = await select_query(column='sn', table='record')
#     length = len(sn)
#
#     if offset < 10:
#         button2 = True
#     if offset > length - 10:
#         button1 = True
#
#     graph = await plot_graph(offset)
#
#     class MyView(View):
#         def __init__(self):
#             super().__init__(timeout=10)
#             self.response = None
#             self.click_count = 0
#
#         @discord.ui.button(label='Previous 10 days', style=discord.ButtonStyle.blurple, disabled=button1)
#         async def past_record(self, interaction: discord.Interaction, button:discord.ui.Button):
#             await show_graph(client, None, interaction, offset=offset + 10)
#
#         @discord.ui.button(label='Following 10 days', style=discord.ButtonStyle.blurple, disabled=button2)
#         async def next_record(self, interaction: discord.Interaction, button:discord.ui.Button):
#             await show_graph(client, None, interaction, offset=offset - 10)
#
#         @discord.ui.button(label='D', style=discord.ButtonStyle.red, disabled=False)
#         async def next_record(self, interaction: discord.Interaction, button:discord.ui.Button):
#             await interaction.message.delete()
#
#     view = MyView()
#     if user:
#         # view.response = await user.send(file=graph, view=view)
#         view.response = await interaction.response.send_message(attachments=[graph], view=view, )
#     else:
#         view.response = await interaction.response.edit_message(attachments=[graph], view=view, )
#
#


async def show_graph(offset:int=0):
    labels = []  # x-axis label
    uses = []  # graph data (bar length)

    record = await select_query(column='*', table='record', order_by_column='sn', ascending=False, limit=10, offset=int(offset))
    print(record)
    for i in range(0, len(record)):
        labels.append(str(record[i][1]))  # list of x-axis label
        uses.append(int(record[i][2]))  # list of graph data (bar length)

    xpoints = np.array(labels)  # array of x-axis label
    ypoints = np.array(uses)  # array of graph data (bar length)

    fig = plt.figure(facecolor="#313338")  # background color outside the graph border
    '''
    ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])
    0.1 --> left position 
    0.2 --> top position 
    0.8 --> graph width
    0.8 --> graph height
    '''
    ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])


    ax.set_xlabel('Date ')  # x-axis global label
    ax.set_ylabel('Number of Uses ')  # y-axis global label

    ax.xaxis.label.set_color('white')  # x-axis global label color
    ax.yaxis.label.set_color('white')  # y-axis global label color

    ax.tick_params(axis='x', colors='white')  # x-axis local label color
    ax.tick_params(axis='y', colors='white')  # y-axis local label color

    ax.spines['left'].set_color('white')  # graph left border color
    ax.spines['top'].set_color('white')  # graph top border color
    ax.spines['bottom'].set_color('white')  # graph bottom border color
    ax.spines['right'].set_color('white')  # graph right border color

    ax.bar(xpoints, ypoints, width=0.8)  # width of the vertical bar
    ax.set_facecolor("#313338")  # background color inside the graph border

    plt.xticks(rotation=45)  # rotation on x-axis label

    filename = "test.png"
    plt.savefig(filename)
    image = discord.File(filename)

    plt.close()

    return image

