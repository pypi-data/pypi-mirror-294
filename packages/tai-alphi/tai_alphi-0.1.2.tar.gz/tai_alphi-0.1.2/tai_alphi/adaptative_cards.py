import datetime


class CardTemplate:
    success_icon_url = "https://img.icons8.com/emoji/48/000000/check-mark-emoji.png"
    failed_icon_url = "https://img.icons8.com/emoji/48/000000/cross-mark-emoji.png"

    def __init__(
        self,
        failed: bool,
        proyecto="",
        pipeline="",
        logs="",
        notify_to=[],
        date=datetime.date,
        time=datetime.time,
    ) -> None:
        
        self.proyecto = proyecto
        self.pipeline = pipeline
        self.date = date.strftime("%a %d de %B, %Y")
        self.time = time.strftime("%H.%M")
        self.logs = logs
        self.notify_to = notify_to
        self.status = {
            "url": self.failed_icon_url if failed else self.success_icon_url,
            "text": "**ERROR**" if failed else "**SUCCESS**",
            "color": "Attention" if failed else "Good",
        }

        self.card1 = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.3",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"**{self.proyecto}**",
                                "wrap": True,
                                "separator": True,
                                "id": "title",
                                "size": "extraLarge",
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": "**Pipeline**",
                                        "value": self.pipeline},
                                    {"title": "**Fecha**", "value": self.date},
                                    {"title": "**Hora**", "value": self.time},
                                ],
                                "id": "description",
                                "separator": True,
                            },
                            {
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "width": "150px",
                                        "items": [
                                            {
                                                "type": "ColumnSet",
                                                "columns": [
                                                    {
                                                        "type": "Column",
                                                        "width": "35px",
                                                        "items": [
                                                            {
                                                                "type": "Image",
                                                                "url": self.status[
                                                                    "url"
                                                                ],
                                                                "width": "25px",
                                                                "height": "25px",
                                                                "id": "icon",
                                                                "horizontalAlignment": "Center",
                                                            }
                                                        ],
                                                    },
                                                    {
                                                        "type": "Column",
                                                        "width": "70px",
                                                        "items": [
                                                            {
                                                                "type": "TextBlock",
                                                                "text": self.status[
                                                                    "text"
                                                                ],
                                                                "color": self.status[
                                                                    "color"
                                                                ],
                                                                "wrap": True,
                                                                "id": "status",
                                                                "horizontalAlignment": "Center",
                                                            }
                                                        ],
                                                        "verticalContentAlignment": "Center",
                                                    },
                                                ],
                                            }
                                        ],
                                        "verticalContentAlignment": "Center",
                                    },
                                    {
                                        "type": "Column",
                                        "width": "stretch",
                                        "items": [
                                            {
                                                "type": "ActionSet",
                                                "actions": [
                                                    {
                                                        "type": "Action.ToggleVisibility",
                                                        "title": "Logs",
                                                        "id": "logs_btn",
                                                        "targetElements": ["logs"],
                                                    }
                                                ],
                                                "id": "action_set",
                                            }
                                        ],
                                    },
                                ],
                            },
                            {
                                "type": "TextBlock",
                                "text": self.logs,
                                "wrap": True,
                                "id": "logs",
                                "isVisible": False,
                            },
                        ],
                    },
                }
            ],
        }
        self.card2 = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.3",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"**{self.proyecto}**",
                                "wrap": True,
                                "separator": True,
                                "id": "title",
                                "size": "extraLarge",
                            },
                            {
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "width": "250px",
                                        "items": [
                                            {
                                                "type": "FactSet",
                                                "facts": [
                                                    {
                                                        "title": "**Pipeline**",
                                                        "value": self.pipeline,
                                                    },
                                                    {
                                                        "title": "**Fecha**",
                                                        "value": self.date,
                                                    },
                                                    {
                                                        "title": "**Hora**",
                                                        "value": self.time,
                                                    },
                                                ],
                                                "id": "description",
                                            }
                                        ],
                                    },
                                    {
                                        "type": "Column",
                                        "width": "46px",
                                        "items": [
                                            {
                                                "type": "Image",
                                                "url": self.status["url"],
                                                "width": "25px",
                                                "height": "25px",
                                                "id": "icon",
                                                "horizontalAlignment": "Center",
                                            }
                                        ],
                                        "verticalContentAlignment": "Center",
                                        "spacing": "None",
                                    },
                                    {
                                        "type": "Column",
                                        "width": "67px",
                                        "items": [
                                            {
                                                "type": "TextBlock",
                                                "text": self.status["text"],
                                                "color": self.status["color"],
                                                "wrap": True,
                                                "id": "status",
                                                "horizontalAlignment": "Center",
                                            }
                                        ],
                                        "verticalContentAlignment": "Center",
                                        "spacing": "None",
                                    },
                                ],
                                "separator": True,
                            },
                            {
                                "type": "ActionSet",
                                "actions": [
                                    {
                                        "type": "Action.ToggleVisibility",
                                        "title": "Logs",
                                        "id": "logs_btn",
                                        "targetElements": ["logs"],
                                    }
                                ],
                                "id": "action_set",
                            },
                            {
                                "type": "TextBlock",
                                "text": self.logs,
                                "wrap": True,
                                "id": "logs",
                                "isVisible": False,
                            },
                        ],
                    },
                }
            ],
        }
        self.card3 = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "body": [
                            {
                                "type": "TextBlock",
                                "size": "Medium",
                                "weight": "Bolder",
                                "text": "Sample Adaptive Card with User Mention"
                            },
                            {
                                "type": "TextBlock",
                                "text": "Hi <at>Juan Abia</at>"
                            }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.0",
                        "msteams": {
                            "entities": [
                                {
                                    "type": "mention",
                                    "text": "<at>Juan Abia</at>",
                                    "mentioned": {
                                        "id": "jabia@triplealpha.in",
                                        "name": "Juan Abia"
                                    }
                                }
                            ]
                        }
                    }
                }]
        }

    def _add_mentions(self, card):
        card["attachments"][0]["content"]["msteams"] = {"entities": []}
        text_mentions = "**Revisión necesaria**: "
        for email in self.notify_to:
            if "@triplealpha.in" not in email:
                continue
            name = email.split("@")[0]
            text_mentions += f" <at>{name}</at>,"
            info = {
                "type": "mention",
                        "text": f"<at>{name}</at>",
                        "mentioned": {
                            "id": email,
                            "name": name
                        }
            }

            card["attachments"][0]["content"]["msteams"]["entities"].append(
                info)
        card["attachments"][0]["content"]["body"].insert(2, {
            "type": "TextBlock",
            "text": text_mentions[:-1],
            "size": "Large"
        })

    def get_card(self, card_type: str):
        card = getattr(self, card_type)
        if self.notify_to:
            self._add_mentions(card)
        return card