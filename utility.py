SUITS = ['♠', '♥', '♣', '♦']
class utility:
    def comp_rank(self,first_card:str,sec_card:str):
        if first_card[1] == first_card[1]:
            return 'EQ'
        elif first_card[1] > sec_card[1]:
            return 'FIRST'
        else:
            return 'SEC'
    def comp_rank_with_suit(self,first_card:str,sec_card:str):
        if first_card[1] == first_card[1]:
            if self.SUITS(first_card) < self.SUITS(sec_card):
                return 'FIRST'
            else:
                return 'SEC'
        elif first_card[1] > sec_card[1]:
            return 'FIRST'
        else:
            return 'SEC'
    def SUITS(self,suit):
        for i in range(len(SUITS)):
            if suit == SUITS[i]:
                return i
