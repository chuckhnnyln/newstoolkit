#!/usr/bin/env python3 

import random

if __name__ == '__main__':
    Nouns = ["Actor","Advertisement","Afternoon","Airport","Ambulance","Animal","Answer","Apple","Army","Balloon","Banana","Battery","Beach","Beard","Bed","Boy","Branch","Breakfast","Brother","Camera","Candle","Car","Caravan","Carpet","Cartoon","Church","Crayon","Crowd","Daughter","Death","Diamond","Dinner","Disease","Doctor","Dog","Dream","Dress","Egg","Eggplant","Elephant","Energy","Engine","Evening","Eye","Family","Fish","Flag","Flower","Football","Forest","Fountain","Furniture","Garage","Garden","Gas","Ghost","Girl","Glass","Gold","Grass","Guitar","Hair","Hamburger","Helicopter","Helmet","Holiday","Honey","Horse","Hospital","House","Hydrogen","Ice","Insect","Insurance","Iron","Island","Jackal","Jelly","Jewellery","Juice","Kangaroo","King","Kitchen","Kite","Knife","Lamp","Lawyer","Leather","Library","Lighter","Lion","Lizard","Lock","Lunch","Machine","Magazine","Magician","Market","Match","Microphone","Monkey","Morning","Motorcycle","Nail","Napkin","Needle","Nest","Night","Notebook","Ocean","Oil","Orange","Oxygen","Oyster","Painting","Parrot","Pencil","Piano","Pillow","Pizza","Planet","Plastic","Potato","Queen","Quill","Rain","Rainbow","Raincoat","Refrigerator","Restaurant","River","Rocket","Room","Rose","Sandwich","School","Scooter","Shampoo","Shoe","Soccer","Spoon","Stone","Sugar","Sweden","Teacher","Telephone","Television","Tent","Tomato","Toothbrush","Traffic","Train","Truck","Umbrella","Van","Vase","Vegetable","Vulture","Wall","Whale","Window","Wire","Xylophone","Yacht","Yak","Zebra","Zoo"]
    
    Adjectives = ["adorable","adventurous","aggressive","agreeable","alert","alive","amused","angry","annoyed","annoying","anxious","arrogant","ashamed","attractive","average","awful","bad","beautiful","better","bewildered","black","bloody","blue","blushing","bored","brainy","brave","breakable","bright","busy","calm","careful","cautious","charming","cheerful","clean","clear","clever","cloudy","clumsy","colorful","combative","comfortable","concerned","condemned","confused","cooperative","courageous","crazy","creepy","crowded","cruel","curious","cute","dangerous","dark","dead","defeated","defiant","delightful","depressed","determined","different","difficult","disgusted","distinct","disturbed","dizzy","doubtful","drab","dull","eager","easy","elated","elegant","embarrassed","enchanting","encouraging","energetic","enthusiastic","envious","evil","excited","expensive","exuberant","fair","faithful","famous","fancy","fantastic","fierce","filthy","fine","foolish","fragile","frail","frantic","friendly","frightened","funny","gentle","gifted","glamorous","gleaming","glorious","good","gorgeous","graceful","grieving","grotesque","grumpy","handsome","happy","healthy","helpful","helpless","hilarious","homeless","homely","horrible","hungry","hurt","ill","important","impossible","inexpensive","innocent","inquisitive","itchy","jealous","jittery","jolly","joyous","kind","lazy","light","lively","lonely","long","lovely","lucky","magnificent","misty","modern","motionless","muddy","mushy","mysterious","nasty","naughty","nervous","nice","nutty","obedient","obnoxious","odd","open","outrageous","outstanding","panicky","perfect","plain","pleasant","poised","poor","powerful","precious","prickly","proud","putrid","puzzled","quaint","real","relieved","repulsive","rich","scary","selfish","shiny","shy","silly","sleepy","smiling","smoggy","sore","sparkling","splendid","spotless","stormy","strange","stupid","successful","super","talented","tame","tasty","tender","tense","terrible","thankful","thoughtful","thoughtless","tired","tough","troubled","ugliest","ugly","uninterested","unsightly","unusual","upset","uptight","vast","victorious","vivacious","wandering","weary","wicked","wild","witty","worried","worrisome","wrong","zany","zealous"]
    
    Trys = 25
    WordLength = 5
    NounCount = len(Nouns)
    AdjCount = len(Adjectives)

    for Option in range(Trys):
        while True:
            RandomAdjIndex = random.randrange(0, AdjCount)
            RandomAdj = Adjectives[RandomAdjIndex].capitalize()
            if len(RandomAdj) <= WordLength:
                break

        while True:
            RandomNounIndex = random.randrange(0, NounCount)
            RandomNoun = Nouns[RandomNounIndex]
            if len(RandomNoun) <= WordLength:
                break
        print(f'{RandomAdj}{RandomNoun}')