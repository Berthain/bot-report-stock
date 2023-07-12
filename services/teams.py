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
    
    myTeamsMessage.color(CYAN_COLOR)
    myTeamsMessage.title("Resume of stock prices")
    
    # Add text to the message.
    myTeamsMessage.text("MCD information")

    myTeamsMessage.addLinkButton("Mc Donald's stock", "https://finance.yahoo.com/quote/MCD?p=MCD&ncid=yahooproperties_peoplealso_km0o32z3jzm")

    # send the message.
    myTeamsMessage.send()


def async_card():
    loop = asyncio.get_event_loop()

    # the async_connectorcard object is used instead of the normal one.
    myTeamsMessage = pymsteams.async_connectorcard(WBC)

    # all formatting for the message should be the same
    myTeamsMessage.text("Async send")

    # to send the message, pass to the event loop
    loop.run_until_complete(myTeamsMessage.send())


def test_send_potential_action():
    """
        This sends a message with a potential action
    """
    #os.getenv("MS_TEAMS_WEBHOOK")
    myTeamsMessage = pymsteams.connectorcard(WBC)
    myTeamsMessage.text("This message should have four potential actions.")
    myTeamsMessage.title("Action Message Title")

    myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
    myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment",False)
    myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction2 = pymsteams.potentialaction(_name = "Get Users")
    myTeamsPotentialAction2.addInput("DateInput","dueDate","Enter due date")
    myTeamsPotentialAction2.addAction("HttpPost","save","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
    myTeamsPotentialAction3.choices.addChoices("In progress","0")
    myTeamsPotentialAction3.choices.addChoices("Active","1")
    myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select a status",False)
    myTeamsPotentialAction3.addAction("HttpPost","Save","https://jsonplaceholder.typicode.com/posts")

    myTeamsPotentialAction4 = pymsteams.potentialaction(_name = "Download pymsteams")
    myTeamsPotentialAction4.addOpenURI("Links", [
                                                    {
                                                        "os": "default",
                                                        "uri": "https://pypi.org/project/pymsteams/",
                                                    },
                                                ])

    myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction4)
    myTeamsMessage.summary("Message Summary")

    myTeamsMessage.send()
    assert isinstance(myTeamsMessage.last_http_response.status_code, int)
