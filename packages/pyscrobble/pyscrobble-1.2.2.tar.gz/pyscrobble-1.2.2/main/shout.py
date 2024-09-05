class Shout:
    def __init__(self, body, author, date, image):
        self.body = body
        self.author = author
        self.date = date
        self.image = image

    def __repr__(self):
        return f"Shout(body={self.body}, author={self.author}, date={self.date})"