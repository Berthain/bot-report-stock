import json
import asyncio
import pymsteams
from config.variables import *


def generate_adaptive_card(id_stock, name_stock, price):
    card = {"type": "AdaptiveCard",
            "version": "1.4",
            "body": [{ "type": "TextBlock",
                        "text": "Id_projeto: {}".format(id_stock),
                        "wrap": True },
                    {
                        "type": "TextBlock",
                        "text": "Desc_projeto: {}".format(name_stock),
                        "wrap": True },
                    {
                        "type": "TextBlock",
                        "text": "Status: {}".format(price),
                        "wrap": True }],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"}
    return card


# Iterar pelas linhas do DataFrame
def send_msg_teams(df):
    cards = []
    for index, row in df.iterrows():
        id_projeto   = row["id_stock"]
        desc_projeto = row["name_stock"]
        status       = row["price"]    
        
        # Adicionar informações ao card
        card = generate_adaptive_card(id_projeto, desc_projeto, status)
        cards.append(card)

        # Converter os cards adaptativos em JSON
        cards_json = json.dumps(cards)


def send_cards():
    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(WBC)

    # Add text to the message.
    myTeamsMessage.text("First send")

    # send the message.
    myTeamsMessage.send()


