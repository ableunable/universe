import random
prvi=["Ku","Ste","Ser","Gri","Di","Ni","Pa","Bo","A","Je","Ta","Gav","Mi","Sla",
    "Sne","Snje","Di","Du","Da","Bor","Bran","Zdrav","Ra","Lje","Vu","Bo","Voj",
    "Ja","Ran","Nov","Su","Sve","Svje","Zvje","Zve","Sve","Dmi","Slav","Mir",
    "Rat","Rad","Boj","Stra","Ne","Ve","Sun","Ma","Ta","Fej","Ju","Je","I",
    "Vla"]
sred=["go","ri","mi","tri","ko","li","sta","si","li","sa","ve","tja","lo","ri",
    "dja","za","ja","brav","bor","doj","po","sa","go","sla","dran","za","tla",
    "zda","mir","ni","lja","boj","hi","ci","ri","ja","hu","a","dzu","tu","re",
    "mi","ho","di","mir","sti"]
zadn=["fan","gej","je","na","vle","jo","ja","ta","lo","mir","ca","djan","ven",
    "ka","va","ljub","slav","ko","tar","sa","nja","bor","ja","din","lah","suf",
    "da","sus","dolf","sta","sto"]

aei = "aeiouy"
bcd = "bcdfghjklmnpqrstvwxz"

def star_namer():
        middle=''
        for _ in range(random.randrange(0,3)):
                middle=''.join([middle, random.choice(sred)])
        first = random.choice(prvi)
        last = random.choice(zadn)
        return first+middle+last

def planet_namer():
    output = ""
    for i in range(random.randint(3,9)):
        if i % 2:
            output += aei[random.randint(0, 5)]
        else:
            output += bcd[random.randint(0, 19)]

    return output.capitalize()

if __name__ == "__main__":
    print(star_namer())
    print(planet_namer())
