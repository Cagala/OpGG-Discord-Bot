class EmbedList():

    def __init__(self) -> None:
        self.embedPages = []

    def add_embeds(self, *embedList):
        for embed in embedList:
            self.embedPages.append(embed)