from service.ticket_service.ticket_menu import TicketMenu 
import discord

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketMenu())
