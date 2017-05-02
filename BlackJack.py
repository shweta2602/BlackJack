'''
 BlackJack Game for single payer and dealer
 @createdby: Shweta Bhangre
'''

import random
# This class creates a deck of cards
class DeckOfCards(object):
    deck = []
    def __init__(self):
        self.createdeck()

    # creates a deck of cards and shuffle the cards
    def createdeck(self):
        del self.deck[:]
        for self.suit in ['Spades','Clubs','Hearts','Diamonds']:
            for self.value in ['Ace',2,3,4,5,6,7,8,9,10,'Jack','Queen','King']:
                 self.deck.append((self.suit,self.value))
        random.shuffle(self.deck)

    # this method picks a card and removes it from deck
    def card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    # returns the card value- 10 for jack,king and queen and 1 for ace. (value of ace may change to 11 later)
    def card_value(self, acard):
        (suit,value) = acard
        if value == 'Jack' or value =='Queen' or value =='King':
            return int(10);

        elif value == 'Ace':
            return int(1);

        else:
            return int(value)

# lets the player bet, see the cards, double the bet and make a choice for hit draw and surrender.
class PlayersHand(object):
    pflag = False
    dflag = False
    def __init__(self):
        self.f = DeckOfCards()


    #draws 2 cards for player and dealer but shows only one card of dealer and changes the value of ace accordingly
    def play(self):
        self.dealer = [self.f.card(),self.f.card()]
        self.player = [self.f.card(), self.f.card()]

        print 'Player Cards: ', str(self.player).strip('[]')
        print "Dealer Cards: ", str(self.dealer[0]).strip('[]')
        dealer_total = self.f.card_value(self.dealer[0])
        player_total = self.f.card_value(self.player[0]) + self.f.card_value(self.player[1])

        if self.player[0][1] == 'Ace' and self.f.card_value(self.player[1]) in xrange(2,11):
            player_total += 10
            self.pflag = True

        if self.player[1][1] == 'Ace' and self.f.card_value(self.player[0]) in xrange(1,11) :
            player_total += 10
            self.pflag = True

        if self.dealer[0][1] == 'Ace' and self.f.card_value(self.dealer[1]) in xrange(2,11):
            dealer_total += 10
            self.dflag = True

        if self.dealer[1][1] == 'Ace' and self.f.card_value(self.dealer[0]) in xrange(1,11) :
            dealer_total += 10
            self.dflag = True

        print "Player total: ",player_total
        #print "Dealer total: ",dealer_total

        scores = [player_total,dealer_total]
        return scores

    #if player chooses to draw more cards, this method draws card for player and calculates the new total
    def player_move(self,totals):

        draw_card = self.f.card()
        self.player.append(draw_card)
        totals[0] += self.f.card_value(self.player[-1])
        if draw_card[1] == 'Ace' and totals[0]+10 <= 21  :
            totals[0] += 10
            self.pflag = True
        elif any(sublist[1] == 'Ace' for sublist in self.player) and totals[0] > 21 and self.pflag == True:
            totals[0] -= 10
            self.pflag = False
        print 'Player Cards: ', str(self.player).strip('[]') ,'Total: ',totals[0]

    #when player hits, this method allows dealer to draw cards and calculate new total
    def dealer_move(self,totals,players_bet):
        while True:
            dealer_choice = None
            if totals[0] == totals[1] and totals[1] < 21 :
                dealer_choice = random.randint(0,1)
                print 'Dealer choice : ',dealer_choice
                if dealer_choice == 1:
                    print '\nTotals are Equal but Dealer does not wish to draw a card!'
                    print 'Nobody Wins!! '
                    break
                elif dealer_choice == 0:
                    print '\nTotals are equal but Dealer wants to draw a card!!'

            if totals[1] < 17 or totals[0] > totals[1] or dealer_choice == 0:
                draw_card = self.f.card()
                self.dealer.append(draw_card)
                totals[1] += self.f.card_value(self.dealer[-1])
                if draw_card[1] == 'Ace' and totals[1] + 10 <= 21:
                    totals[1] += 10
                    self.dflag = True
                elif any(sublist[1] == 'Ace' for sublist in self.dealer) and totals[1] > 21 and self.dflag == True:
                    totals[1] -= 10
                    self.dflag = False
                print "Dealer Cards: ", str(self.dealer).strip('[]'), 'Total: ', totals[1]

            if totals[1] <= totals[0]:
                continue
            elif totals[0] < totals[1] <= 21:
                print '\nYou just got Busted!!! Dealer Wins'
                print 'You loose : $', players_bet
                break
            elif totals[1] > totals[0] or totals[1] > 21 :
                print '\nYou WIN !!!!'
                print 'You get : $', players_bet*2
                break


while True:

    player_bet = int(raw_input('Enter your betting amount: '))

    blackjack = PlayersHand()
    scores = blackjack.play()

    while True:

        if scores[0] > 21 :
            print '\nYou just got Busted!!! Dealer Wins'
            print 'You loose : $',player_bet
            break
        elif scores[0] == 21 :
            print '\nYou WIN !!!!'
            print 'You get : $',player_bet *2
            break
        else:
            ch = raw_input('Double the bet ? (y/n): ')
            if ch.startswith('y'):
                player_bet += player_bet
                print 'New Bet : $', player_bet
            elif ch.startswith('n'):
                pass
            else:
                continue
            choice = raw_input("Player enter your choice (hit/draw/surreneder):  ")
            if choice.startswith('d'):
                print '\nPlayers chooses to draw a card '
                blackjack.player_move(scores)

            elif choice.startswith('h'):
                blackjack.dealer_move(scores,player_bet)
                break
            elif choice.startswith('s'):
                print '\nYou Surrendered!!! Dealer Wins'
                print 'You loose : $', player_bet
                break


    ch = raw_input('Do you want to play again (yes/no): ')
    if ch.startswith('n'):
        break
    print '\n--------------------New game---------------------------'''