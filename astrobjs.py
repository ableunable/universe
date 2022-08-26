import random

from namer import star_namer, planet_namer
from settings import *

class StarType:
    def __init__(self, name, color, temperature, life=False, chance=(0,40)):
        self.name = name #Ime vrste // string
        self.color = color #Boja zvijezde // tuple(R,G,B)
        self.temperature = temperature #Temp. planeta u °C // tuple(od, do)
        self.life = life #Dal planete mogu imati zivot // True False
        self.chance = chance

#ovdje dodavaj vrste zvijezda
star_types = [
    StarType("Gentle", GENTLE, (10,40), life=True),
    StarType("Yellow Dwarf", YELLOW, (-224, 465), life=True), #bazirana na Suncu
    StarType("Superheated", SUPERHEATED, (150, 450)), #pakao
    StarType("Frozen", FROZEN, (-300, -100)),
    StarType("Radioactive", RADIOACTIVE, (30,70), life=True),
    StarType("Acid", ACID, (-120, 120), chance=(0,80)),
    StarType("Black Hole", BHOLE, (-273, -200), chance=(0,250)),
    StarType("White Hole", WHITE, (69, 420), chance=(0,1000), life=True)
]

class Planet:
    def __init__(self, startemp, starlife, stardist, planets):
        self.startempmin, self.startempmax = startemp
        self.startemprange = self.startempmax - self.startempmin
        self.starlife = starlife
        self.stardist = stardist + 1

        if self.stardist == 1:
            self.percentmin = 100
        else:
            self.percentmin = 100-((self.stardist-1)*(100/planets))
        if self.stardist == planets:
            self.percentmax = 0
        else:
            self.percentmax = 100-(self.stardist*(100/planets))

        self.tempmin = (self.startemprange * self.percentmin)//100
        self.tempmax = (self.startemprange * self.percentmax)//100

        self.name = planet_namer()
        self.radius = random.randint(5,12)
        self.t = random.randint(0,360) #pocetna lokacija oko zvijezde
        self.reversedRotation = random.randint(0,150)==1

        print(self.name,self.tempmin,self.tempmax)

        self.moons = self.moongen()
        if not self.moons:
            self.ring = random.randint(0,10) == 1
        else:
            self.ring = 0

        #zbog zaledjenih zvijezda
        if self.tempmin < self.tempmax:
            self.temperature = random.randint(self.tempmin, self.tempmax)+\
                self.startempmin
        else:
            self.temperature = random.randint(self.tempmax, self.tempmin)+\
                self.startempmin

        self.gasses = 0
        self.minerals = 0
        self.resources = 0
        self.water = 0
        self.life = 0
        self.hasWater = 0

        if self.radius >= 10: 
            self.gas_giant = random.randint(0,5) == 1
        else:
            self.gas_giant = 0

        if not self.gas_giant:
            if self.temperature > -50 and self.temperature < 100:
                self.hasWater = random.randint(0,50) == 1
            if self.temperature > 0 and self.hasWater and self.starlife:
                self.life = random.randint(0,10) == 1
            self.gasses = random.random()
            self.minerals = random.random()
            self.resources = random.random()
            if self.hasWater: self.water = random.random()
        else:
            self.gasses = 1.0
            self.minerals = 0.0
            self.resources = 0.0
            self.water = 0.0

        final = 1 / (self.gasses + self.minerals + self.resources + self.water)
        self.gasses *= final * 100
        self.minerals *= final * 100
        self.resources *= final * 100
        self.water *= final * 100
        self.population = 0
        #Ovaj dio sluzi da izracuna procenat %

        self.color = self.colorize()
        
    def colorize(self):
        if self.water and not self.life:
            if self.temperature > 0:
                return BLUE
            else:
                return FROZEN
        elif self.life:
            return GREEN
        elif self.gas_giant:
            return GAS
        else:
            return BROWN

    def moongen(self):
        nMoons = random.randint(-5, 3)
        moons = []
        for _ in range(nMoons):
            t = random.randint(0,360) #pocetna lokacija oko planete
            reversedRotation = random.randint(0,20)==1
            moons.append([t, reversedRotation])

        return moons

class Star:
    def __init__(self, x, y, generateSystem=True):
        seed = (x & 0xFFFF) << 16 | (y & 0xFFFF)
        random.seed(seed)
        self.type = random.choice(star_types)
        self.starExists = random.randint(*self.type.chance) == 1
        if not self.starExists:
                return

        self.color = self.type.color
        self.radius = random.randint(5, 22)

        #Ako mi treba samo da prikaze zvijezdu ne mora onda
        #generisati sve planete i detalje o njoj
        #nego samo izgled
        if not generateSystem: 
            return

        self.name = star_namer()
        self.planets = []
        if self.type.name == "Black Hole":
            if not random.randint(0,10):
                self.planet_max = 1
            else:
                self.planet_max = 0
        else:
            self.planet_max = 6
        n_planets = random.randint(0, self.planet_max)
        for i in range(n_planets):
            p = Planet(self.type.temperature, self.type.life, i, n_planets)
            self.planets.append(p)
