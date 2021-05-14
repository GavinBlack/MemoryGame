# Pizza Panic
# Player must catch falling pizzas before they hit the ground

from livewires import games, color
import random, time, pygame

games.init(screen_width = 640, screen_height = 480, fps = 60)

class SmallSprite(games.Sprite):
        #Initialize class variables
        image = games.load_image("smallSprite.png")

        def __init__(self):
                super(SmallSprite, self).__init__(image = SmallSprite.image, x = games.mouse.x,y = games.mouse.y)

        def update(self):
                self.x = games.mouse.x
                self.y = games.mouse.y 

class Card(games.Sprite):
        #Load in images, create class variables
        blocker_image = games.load_image("blocker.png")
        bird_image = games.load_image("bird.png")
        elephant_image = games.load_image("elephant.png")
        spider_image = games.load_image("spider.png")
        grape_image = games.load_image("grapes.png")
        peach_image = games.load_image("peach.png")
        pears_image = games.load_image("pears.png")
        cardsShowing = 0
        time = 0
        clickedCards = []
        clickable = True
        
        def __init__(self,world,x,y,whichImage = 1):
                super(Card,self).__init__(image = Card.blocker_image, x=x,y=y)

                #create instance variables for future use
                self.world = world
                self.whichImage = whichImage

        def update(self):
                """if no more than 2 cards are showing,
                   and the left mouse button is clicked,
                   figure out what image it is, replace
                   the back of the card with the image
                """
                if Card.clickable:
                        for sprite in self.overlapping_sprites:
                                for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                if event.button == 1:
                                                        if self.whichImage == 1:
                                                                self.image = Card.bird_image
                                                        elif self.whichImage == 2:
                                                                self.image = Card.elephant_image
                                                        elif self.whichImage == 3:
                                                                self.image = Card.spider_image
                                                        elif self.whichImage == 4:
                                                                self.image = Card.grape_image
                                                        elif self.whichImage == 5:
                                                                self.image = Card.peach_image
                                                        elif self.whichImage == 6:
                                                                self.image = Card.pears_image

                                                        Card.cardsShowing += 1
                                                        Card.clickedCards.append(self)
                """
                 if two cards are showing, make it so the
                 user can't click anymore cards. Calculate
                 time that the user sees both cards before
                 either destroying them, or putting them
                 back to the back of the card image.
                """
                if Card.cardsShowing == 2:
                        Card.clickable = False
                        Card.time += 1
                        if Card.time == games.screen.fps * 8:
                                for card in Card.clickedCards:
                                        if Card.clickedCards[0].whichImage == Card.clickedCards[1].whichImage:
                                                card.destroy()
                                                self.world.score.value += 5
                                                self.world.totalCards -= 1
                                                
                                                if self.world.totalCards == 0:
                                                        self.nextLevel()
                                        else:
                                                Card.clickedCards[0].image = Card.blocker_image
                                                Card.clickedCards[1].image = Card.blocker_image

                                Card.time = 0
                                Card.clickedCards = []
                                Card.cardsShowing = 0
                                Card.clickable = True

        def nextLevel(self):
                Card.time = 0
                Card.clickedCards = []
                Card.cardsShowing = 0
                Card.clickable = True
                
                if self.world.level == 0:
                        self.world.level += 2

                """
                TAKE LEVEL MESSAGE OUT OF FUNCTION

                """
                        
                level_message = games.Message(value = "Level " + str(self.world.level),
                                size = 40,
                                color = color.yellow,
                                x = games.screen.width/2,
                                y = games.screen.width/10,
                                lifetime = 2 * games.screen.fps,
                                is_collideable = False)
                games.screen.add(level_message)

                if World.level < World.max_rows:
                        World.rows += 1

                world = World()
                World.totalCards = World.rows * World.cols
                World.level += 1
                World.cards = []
                world.createBoard()

class World(object):
        #Initialize class variables
        cards = []
        rows = 1
        cols = 6
        totalCards = rows * cols
        level = 0
        max_rows = 5

        score = games.Text(value = 0,
                                size = 30,
                                color = color.green,
                                top = 5,
                                right = games.screen.width - 10,
                                is_collideable = False)
        games.screen.add(score)

        """
         fill up the card array based on the total
         amount of cards, shuffle it, reassign it
         to the class variable named cards
        """
        def fillCardArray(self):
                print("WORLD LEVEL",World.level)
                if World.level == 0:
                        for i in range(1,World.totalCards//2+1):
                                World.cards.append(i)
                                World.cards.append(i)
                        random.shuffle(World.cards)
                else:
                        print("more than 1")
                        for i in range(World.rows):
                                tempList = []
                                for j in range(1,World.cols+1):
                                        tempList.append(j)
                 
                                        if j % World.cols == 0:
                                                random.shuffle(tempList)
                                                World.cards.append(tempList)
                print(World.cards)                                
                        
        """
         create and add the cards to the screen
         in the correct format
        """
        def createBoard(self):
                x = 65
                y = 40
                card = None

                self.fillCardArray()
                
                if World.level == 0:
                        for i in range(World.totalCards):
                                if World.cards[i] == 1:
                                        card = Card(world = self, x = x+i*95, y = 45,whichImage = 1)
                                elif World.cards[i] == 2:
                                        card = Card(world = self, x = x+i*95, y = 45, whichImage = 2)
                                elif World.cards[i] == 3:
                                        card = Card(world = self, x = x+i*95, y = 45, whichImage = 3)
                                games.screen.add(card)
                else:
                        for i in range(World.rows):
                                #tempList = []
                                for j in range(World.cols):
                                        if World.cards[i][j] == 1:
                                                card = Card(world = self, x=x+j*95,y=y+i*95)
                                                games.screen.add(card)
                                        elif World.cards[i][j] == 2:
                                                card = Card(world = self, x=x+j*95,y=y+i*95,whichImage=2)
                                                games.screen.add(card)
                                        elif World.cards[i][j] == 3:
                                                card = Card(world = self, x=x+j*95,y=y+i*95,whichImage=3)
                                                games.screen.add(card)
                                        elif World.cards[i][j] == 4:
                                                card = Card(world = self, x=x+j*95,y=y+i*95,whichImage=4)
                                                games.screen.add(card)
                                        elif World.cards[i][j] == 5:
                                                card = Card(world = self, x=x+j*95,y=y+i*95,whichImage=5)
                                                games.screen.add(card)
                                        elif World.cards[i][j] == 6:
                                                card = Card(world = self, x=x+j*95,y=y+i*95,whichImage=6)
                                                games.screen.add(card)
                                        
def main():
	""" Play the game. """
	background_image = games.load_image("background.jpg", transparent = False)
	games.screen.background = background_image

	games.mouse.is_visible = True

	world = World()
	world.createBoard()

	smallCursor = SmallSprite()
	games.screen.add(smallCursor)
	
	#games.screen.event_grab = True
	games.screen.mainloop()

# start it up!
main()
