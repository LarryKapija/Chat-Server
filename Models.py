#groups
#room_name string
#owner string 
#invitations {}
#requests {}
class Groups():
    def __init__(self,room_name,owner, requests):
        self.room_name = room_name
        self.owner = owner
        self.invitations = {}
        self.requests = {}