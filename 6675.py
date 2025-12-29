### Imports ###
from core.helpers import *
from core.constants import *
from core.condition import Condition
from models.set import AchievementSet
from models.achievement import Achievement

### Define Addresses ###

gameState = byte(0x0d4110)
#0x02 - Logos
#0x03 - Logos but rolled over from the main menu
#0x04 - Intro Cutscene
#0x05 - Win
#0x06 - Menus
#0x07 - In Game

hz = byte(0x0e1412)
#0x05 - 50hz
#0x06 - 60hz

loadingScreen = byte(0x0d4420)
#0x00 - No
#0x01 - Yes

raceOutcome = Condition(tbyte(0x03e378) >> dword(0x00)).with_flag(remember) # Pointer
raceData = (tbyte(0x1181a8) >> (tbyte(0x02A0)))

modeAddress = byte(0x0e3746)
demoAddress = byte(0x0e407c)

### Functions ###

demoCheck = (demoAddress == 0x00)
championship = (modeAddress == 0x00)
miniChampionship = (modeAddress == 0x01)
arcadeRace = (modeAddress == 0x02)

raceState = (raceData >> byte(0x38))
#0x00 - Loading
#0x01 - When set, resets race 
#0x02 - Flyover
#0x03 - Countdown
#0x04 - Racing
#0x05 - Win/Lose
#0x06 - Race result

playerWin = Condition((raceData >> dword(0xa0)) == recall())
raceIndicator = byte(0x0e3152)
def raceName(race: int):
    match race:
        case 0x00:
            return "Rally Race 1"
        case 0x01:
            return "Rally Race 2"
        case 0x02:
            return "Cow Day"
        case 0x03:
            return "Valentine's Day"
        case 0x04:
            return "Spring Cleaning"
        case 0x05:
            return "Read a Book Day"
        case 0x06:
            return "Easter Egg Hunt"
        case 0x07:
            return "Pink Lemonade Race"
        case 0x08:
            return "Memorial Day"
        case 0x09:
            return "Independence Day"
        case 0x0a:
            return "Halloween Rally"
        case 0x0b:
            return "Thanksgiving"
        case 0x0c:
            return "Christmas Day"
        case 0x0d:
            return "Millenium New Year's Eve"
        case 0x0e:
            return "Ass Battle"
        case 0x0f:
            return "Random"
        case _:
            return "Unknown"

def achievementTitle(id: str):
    match id:
        case "1_champ":
            return "Gentlemen, Start Your Profanity"
        case "2_champ":
            return "Trophy Transporter"
        case "3_champ":
            return "Moo?"
        case "4_champ":
            return "Be My Big Gay Al-Entine"
        case "5_champ":
            return "Give Me Back My Undies!"
        case "6_champ":
            return "Reading Is for Nerds"
        case "7_champ":
            return "Jesus, Take the Wheel"
        case "8_champ":
            return "When Life Gives You Lemons, Ram into Someone"
        case "9_champ":
            return "You're Breakin' My Balls Here, Officer!"
        case "10_champ":
            return "This Is America, Bro"
        case "11_champ":
            return "I'm Not Fat, I'm Big-Boned!"
        case "12_champ":
            return "That Turkey's Pissed Off!"
        case "13_champ":
            return "Howdy-Ho!"
        case "14_champ":
            return "We're Gonna Have to Blame Canada"

        # Mini Championship
        case "1_mini":
            return "Still Think the Rides Are Rigged?"
        case "2_mini":
            return "Big City Dreams"
        case "3_mini":
            return "This Place Hasn't Got Shit on Tegridy Farms"
        case "4_mini":
            return "Big Gay Al's Big Gay Mini Championship"
        case "5_mini":
            return "You Kids Better Wash Your Hands"
        case "6_mini":
            return "Go, Woodland Critter, Go!"
        case "7_mini":
            return "We're Huntin' for First Place!"
        case "8_mini":
            return "We Survived, Dude!"

        # Beat My Times
        case "1_dev":
            return "Now This Is Rigged"
        case "2_dev":
            return "City-Wide Fame If You Beat This"
        case "3_dev":
            return "Farming Dev Points from This Set"
        case "4_dev":
            return "Big Gay Al's Big Gay Dev Time"
        case "5_dev":
            return "This Track Has a Special Place in Hell for It"
        case "6_dev":
            return "Many Forest Fires Were Started While Boosting to Get This Time"
        case "7_dev":
            return "The Peak of Kart Racing"
        case "8_dev":
            return "I Hate Fireballs."

        # Character Unlocks
        case "pip":
            return "Lunchy Munchies, Hmmm?"
        case "mr_garrison":
            return "I Said HOW WOULD YOU LIKE TO SUCK MY BALLS, Mr Garrison"
        case "bebe":
            return "Did You SEE These Shoes, Wendy!?"
        case "shelly":
            return "Shut Up, Turd! I'm Playing RetroAchievements"
        case "tweek":
            return "Oh Man, This Is Way Too Much Pressure!"
        case "mr_mackey":
            return "Drugs Are Bad, Mkay?"
        case "cartman_cop":
            return "Respect Mah Authoritah!"
        case "skuzzlebutt":
            return "I Am Skuzzlebutt! Lord of the Mountains!"
        case "mrs_broflovski":
            return "Weeeeeell Kyle's Mom's a Bitch, She's a Big Fat Bitch"
        case "ms_cartman":
            return "Mom, More Cheesy Poofs, Less Talking!"
        case "big_gay_al":
            return "I'm Super! Thanks for Asking!"
        case "ike":
            return "Don't Kick the Baby!"
        case "visitor":
            return "Moo!"
        case "ned":
            return "I Don't Think Eight Year Old Kids Drink Beer, Mmm"
        case "mephesto":
            return "Oh My God, He Only Has One Ass! He's of No Use to Me..."
        case "death":
            return "You Killed Kenny! You Bastard!"
        case "grandpa":
            return "Pull the Trigger, You Little Pussy!"
        case "marvin":
            return "No Starvin' Marvin, That's My Pot Pie!"
        case "jesus":
            return "Happy Birthday to Me, Happy Birthday to Me..."
        case "terrance_phillip":
            return "But We're Not Gay Phillip... We're Not?"
        case "damien":
            return "Rectus... Dominus... Cheesy Poofs..."
        case "satan":
            return "I Have Had ENOUGH of You!"
        case "extra_skins":
            return "SCOTLAND FOREVER!"
        case "cheat_sheet":
            return "If You Cheat and Succeed, You're Savvy"

        # Credits
        case "1_cred":
            return "Hey, a Quarter!"
        case "2_cred":
            return "Hey, Another Quarter!"
        case "3_cred":
            return "This Quarter Stinks..."
        case "4_cred":
            return "A Penny for My Valentine"
        case "5_cred":
            return "I Found This in My Laundry"
        case "6_cred":
            return "I Read a Book and It Said to Search Toll Bridges for Quarters"
        case "7_cred":
            return "Usually It's Candy in the Easter Eggs"
        case "8_cred":
            return "I Said a Lime, Not a Dime"
        case "9_cred":
            return "Laser-Cut Quarter"
        case "10_cred":
            return "You Have the Right to Press Pennies"
        case "11_cred":
            return "What a Treat!"
        case "12_cred":
            return "Hey! That Turkey Gobbled My Change!"
        case "13_cred":
            return "Last Christmas, I Gave You My Coins"
        case "14_cred":
            return "I Saw the Millennium Change and All I Got Was This Lousy Quarter"

        # Challenges
        case "1_challenge":
            return "Home Sweet Home"
        case "2_challenge":
            return "That There's Some Good Hunting"
        case "3_challenge":
            return "Sewer-Based Anal Probe"
        case "4_challenge":
            return "Sir, Step out of the Car Please"
        case "5_challenge":
            return "Chicken, Gravy, and Freedom!"
        case "6_challenge":
            return "What Would Jesus Do?"
        case "7_challenge":
            return "Mom Said It's MY Turn with the Laser"
        case "8_challenge":
            return "Volcanic Trophy Giving Ceremony"
        case "9_challenge":
            return "Pine Fresh Undies"
        case "10_challenge":
            return "Lemonade! Fresh Lemonade!"
        case "11_challenge":
            return "In Memorium of Doing Super"
        case "12_challenge":
            return "Christmas in the Hills"
        case "13_challenge":
             return "Super Complicated Sewer Stuff"
        case "14_challenge":
            return "Magical Mystery Tour"

        # Extras
        case _:
            return f"Missing Name"

credits = byte(0x0e3251)
creditIncrease = [
    Condition(credits.delta()).with_flag(add_source),
    Condition(0x01).with_flag(add_source),
    Condition(0x00 == credits).with_flag(trigger) 
]
### Initialize Set ###
mySet = AchievementSet(game_id=6675, title="South Park Rally")
achID = 0


### Achievements ###

# Championship
order = 1
for race in range(0x00, 0x0e):
    championshipAchievementLogic = [
        demoCheck,
        championship,
        raceIndicator == race,
        raceOutcome,
        playerWin,
        Condition(raceState.delta() == 0x04),
        raceState == 0x05,
    ]

    champAchievement = Achievement(achievementTitle(f"{order}_champ"), f"Win the {raceName(race)} race in Championship mode", 1, achID)
    champAchievement.add_core(championshipAchievementLogic)
    mySet.add_achievement(champAchievement)
    achID += 1
    order += 1




# Unlocks


# Credit Achievements
order = 1
for race in range(0x00, 0x0e):
    creditAchievementLogic = [
        demoCheck,
        championship,
        raceIndicator == race,
        raceState == 0x04,
        creditIncrease,
    ]

    credAchievement = Achievement(achievementTitle(f"{order}_cred"), f"Collect the Extra Credit during the {raceName(race)} race in Championship mode", 1, achID)
    credAchievement.add_core(creditAchievementLogic)

    mySet.add_achievement(credAchievement)
    achID += 1
    order += 1
    





### Achievements ###

intro = Achievement("Come on Up to South Park!", "Watch the whole South Park intro", 5, achID)
introCore = [
    (gameState.delta() == 0x02).with_flag(or_next),
    (gameState.delta() == 0x03).with_flag(reset_if),
    (gameState == 0x06)
]

introAlt1 = [
    (hz == 0x05).with_flag(and_next),
    (loadingScreen == 0x00).with_flag(and_next),
    (gameState.delta() == 0x04).with_hits(1420)
]

introAlt2 = [
    (hz == 0x06).with_flag(and_next),
    (loadingScreen == 0x00).with_flag(and_next),
    (gameState.delta() == 0x04).with_hits(1700),
]


intro.add_core(introCore)
intro.add_alt(introAlt1)
intro.add_alt(introAlt2)

intro.add_alt(creditIncrease)

mySet.add_achievement(intro)

mySet.save()