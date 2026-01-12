### Imports ###
from typing import List
from pathlib import Path
import pycheevos.core.helpers as helpers
from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement

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

raceOutcome = remember(tbyte(0x03e378) >> dword(0x00))
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

character = byte(0x0e3415)
#-1 if not in Championship Mode after Mystery (Bebe becomes 0x0b, Shelly becomes 0x0c, etc)
#0x00 - Stan
#0x01 - Kyle
#0x02 - Cartman
#0x03 - Kenny
#0x04 - Wendy
#0x05 - Chef
#0x06 - Officer Barbrady
#0x07 - Uncle Jimbo
#0x08 - Random
#0x09 - Pip
#0x0a - Mr. Garrison
#0x0b - Mystery
#0x0c - Bebe
#0x0d - Shelly
#0x0e - Tweek
#0x0f - Mr. Mackey
#0x10 - Cartman Cop
#0x11 - Skuzzlebutt
#0x12 - Mrs. Broflovski
#0x13 - Ms. Cartman
#0x14 - Big Gay Al
#0x15 - Ike
#0x16 - Visitor
#0x17 - Ned
#0x18 - Mephesto
#0x19 - Death
#0x1a - Grandpa
#0x1b - Marvin
#0x1c - Jesus
#0x1d - Terrance & Phillip
#0x1e - Damien
#0x1f - Satan
#0x20 - Wimpy Stan
#0x21 - Kyle Vampire
#0x22 - Kenny Football
#0x23 - Cartman Homie
#0x24 - Chef Braveheart

playerWin = (raceData >> dword(0xa0)) == recall() 
playerFinish = (raceData >> dword(0xa0)) != 0x00

resetToCountdown = (raceState == 0x03).with_hits(1)

unlockTimers = (raceData >> float32(0xb0))

rallyDays2Checkpoint = (raceData >> byte(0x94))

raceIndicator = byte(0x0e3152)
trackIndicator = byte(0x0e3151)
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

def trackName(track: int, forDesc: bool = False):
    if forDesc:
        match track:
            case 0x00:
                return "in the City"
            case 0x01:
                return "in the Forest"
            case 0x02:
                return "at Big Gay Al's"
            case 0x03:
                return "in the Volcano"
            case 0x04:
                return "on the Mountain"
            case 0x05:
                return "on the Farm"
            case 0x06:
                return "in the Sewer"
            case 0x07:
                return "at the Carnival"
            case 0x08:
                return "Gridiron"
            case 0x09:
                return "Random"
            case _:
                return "Unknown"
    else:
        match track:
            case 0x00:
                return "City"
            case 0x01:
                return "Forest"
            case 0x02:
                return "Big Gay Al's"
            case 0x03:
                return "Volcano"
            case 0x04:
                return "Mountain"
            case 0x05:
                return "Farm"
            case 0x06:
                return "Sewer"
            case 0x07:
                return "Carnival"
            case 0x08:
                return "Gridiron"
            case 0x09:
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
            return "Volcanic Trophy Giving Ceremony"
        case "8_challenge":
            return "Pine Fresh Undies"
        case "9_challenge":
            return "Lemonade! Fresh Lemonade!"
        case "10_challenge":
            return "In Memorium of Doing Super"
        case "11_challenge":
            return "Christmas in the Hills"
        case "12_challenge":
             return "Super Complicated Sewer Stuff"
        case "13_challenge":
            return "Mom Said It's MY Turn with the Laser"
        case "14_challenge":
            return "Magical Mystery Tour"

        # Extras
        case "intro":
            return "Come on Down to South Park!"
        case _:
            return f"Missing Name"

def commonChampionshipLogic(race: int):
    return [
        demoCheck, 
        championship, 
        raceIndicator == race
        ]

def commonMiniChampionshipLogic(track: int):
    return [
        demoCheck, 
        miniChampionship, 
        trackIndicator == track
        ]

def commonArcadeLogic(race: int, track: int):
    return [
        demoCheck, 
        arcadeRace, 
        raceIndicator == race,
        trackIndicator == track
        ]

def unlocks(race: int, con: int, conditionAddress: int, shouldMeasure: bool = False):
    address = (raceData >> byte(conditionAddress))
    logic = [
        (address.delta() == con - 1),
        raceState == 0x04
    ]
    if shouldMeasure:
        logic.insert(0, measured_if(demoCheck))
        logic.insert(1, measured_if(championship))
        logic.insert(2, measured_if(raceIndicator == race))
        logic.insert(4, measured(address == con))
    else:
        logic.insert(0, demoCheck)
        logic.insert(1, championship)
        logic.insert(2, (raceIndicator == race))
        logic.insert(4, (address == con))
    return logic

playerCheckpoint = (raceData >> byte(0xa4))
playerLap = (raceData >> byte(0xb4))

ai1Checkpoint = (raceData >> byte(0xd0))
ai1Lap = (raceData >> byte(0xe0))
ai2Checkpoint = (raceData >> byte(0xfc))
ai2Lap = (raceData >> byte(0x10c))
ai3Checkpoint = (raceData >> byte(0x128))
ai3Lap = (raceData >> byte(0x138))
ai4Checkpoint = (raceData >> byte(0x154))
ai4Lap = (raceData >> byte(0x164))
ai5Checkpoint = (raceData >> byte(0x180))
ai5Lap = (raceData >> byte(0x190))

def waitingOnWin():
    return [
        (raceState.delta() == 0x04),
        trigger(raceState == 0x05)
    ]

credits = byte(0x0e3251)
creditIncrease = [
    add_source(credits.delta()),
    add_source(value(0x01)),
    trigger(value(0x00) == credits) 
]
### Initialize Set ###
mySet = AchievementSet(game_id=6675, title="South Park Rally")
### Achievements ###

# Championship
order = 1
for race in range(0x00, 0x0e):
    championshipAchievementLogic = [
        commonChampionshipLogic(race),
        raceOutcome,
        playerWin,
        waitingOnWin()
    ]

    champAchievement = Achievement(achievementTitle(f"{order}_champ"), f"Win the {raceName(race)} race in Championship mode", 1)
    champAchievement.add_core(championshipAchievementLogic)
    mySet.add_achievement(champAchievement)
    order += 1 

# Mini Championship
# Carnival, City Farm, BGA, Sewers, Forest, Mountain, Volcano
raceOrder = [0x07, 0x00, 0x05, 0x02, 0x06, 0x01, 0x04, 0x03]
order = 1
for race in raceOrder:
    miniChampionshipAchievementLogic = [
        commonMiniChampionshipLogic(race),
        raceOutcome,
        playerWin,
        waitingOnWin(),
    ]

    miniChampAchievement = Achievement(achievementTitle(f"{order}_mini"), f"Win the race {trackName(race, True)} in Mini Championship mode", 1)
    miniChampAchievement.add_core(miniChampionshipAchievementLogic)
    mySet.add_achievement(miniChampAchievement)
    order += 1

# Mini Championship - Beat my Time
# Carnival, City Farm, BGA, Sewers, Forest, Mountain, Volcano
miniChampRaceOrder = [0x07, 0x00, 0x05, 0x02, 0x06, 0x01, 0x04, 0x03]
timesToBeat = [126.71, 168.57, 82.07, 113.07, 218.18, 113.07, 157.47, 135.60]
timesToBeatDesc = ["2:06.72", "2:48.58", "1:22.08", "1:53.08", "3:38.19", "2:15.61", "2:37.48", "1:53.08"]
order = 1
raceTime = (raceData >> float32(0x3c))
for race in miniChampRaceOrder:
    timeTrialAchievementLogic = [
        commonMiniChampionshipLogic(race),
        raceOutcome,
        playerWin,
        resetToCountdown,
        waitingOnWin(),
        reset_if(raceTime > timesToBeat[raceOrder.index(race)])
    ]
    timeTrialAchievement = Achievement(achievementTitle(f"{order}_dev"), f"Beat PS2Hagrid's time of {timesToBeatDesc[miniChampRaceOrder.index(race)]} {trackName(race, True)} in Mini Championship mode", 1)
    timeTrialAchievement.add_core(timeTrialAchievementLogic)
    mySet.add_achievement(timeTrialAchievement)
    order += 1

# Unlocks

# Garrison
def garrisonUnlock():
    garrisonUnlockLogic = [
        commonChampionshipLogic(0x01),
        raceOutcome,
        trigger(playerWin),
        resetToCountdown
    ]

    for checkpoint in range(0x00, 0x03):
        bit_func = getattr(helpers, f"bit{checkpoint}")

        droveOverCheckpoint = (raceData >> bit_func(0xc0))
        garrisonUnlockLogic.append(and_next(droveOverCheckpoint == 0x00))
        garrisonUnlockLogic.append(reset_if(rallyDays2Checkpoint.delta() > 0x00))

    garrisonUnlockLogic.append(and_next(raceState != 0x04))
    garrisonUnlockLogic.append(reset_if((raceData >> byte(0x0c)) != 0x0f))
    garrisonUnlockLogic.append(reset_if((raceData >> byte(0x0c)) == 0x0f))
    garrisonUnlockLogic.append((raceState.delta() == 0x04))
    garrisonUnlockLogic.append(trigger(raceState == 0x05))


    garrisonAchievement = Achievement(achievementTitle("mr_garrison"), "Unlock Mr. Garrison by being the only player to pass over each checkpoint with the trophy in Rally Days #2", 2)
    garrisonAchievement.add_core(garrisonUnlockLogic)
    mySet.add_achievement(garrisonAchievement)

# Pip
def pipUnlock():
    pipUnlockLogic = [
        commonChampionshipLogic(0x01),
        raceOutcome,
        trigger(playerWin),
        resetToCountdown
    ]

    for checkpoint in range(0x00, 0x03):
        print(checkpoint)
        bit_func = getattr(helpers, f"bit{checkpoint}")
        droveOverCheckpoint = (raceData >> bit_func(0xc0))

        if checkpoint == 0x00:
            pipUnlockLogic.append(and_next(droveOverCheckpoint == 0x00))
            pipUnlockLogic.append(reset_if(rallyDays2Checkpoint.delta() > 0x00))
        else:
            pipUnlockLogic.append(reset_if(droveOverCheckpoint == 0x01))



    pipUnlockLogic.append(and_next(raceState != 0x04))
    pipUnlockLogic.append(reset_if((raceData >> byte(0x0c)) != 0x09))
    pipUnlockLogic.append(reset_if((raceData >> byte(0x0c)) == 0x09))
    pipUnlockLogic.append((raceState.delta() == 0x04))
    pipUnlockLogic.append(trigger(raceState == 0x05))


    pipAchievement = Achievement(achievementTitle("pip"), "Unlock Pip by passing over only Checkpoints 1 and 4 with the trophy in Rally Days #2", 2)
    pipAchievement.add_core(pipUnlockLogic)
    mySet.add_achievement(pipAchievement)  

# Bebe
def bebeUnlock():
    bebeUnlockLogic = [
        commonChampionshipLogic(0x02),
        raceOutcome,
        playerWin,
        reset_if(unlockTimers.delta() < 120.0),
        resetToCountdown,
        waitingOnWin()
    ]

    bebeAchievement = Achievement(achievementTitle("bebe"), "Unlock Bebe by losing without touching the cure in Cow Days", 2)
    bebeAchievement.add_core(bebeUnlockLogic)
    mySet.add_achievement(bebeAchievement)
    
# Extra Skins
def extraSkinsUnlock():
    extraSkinsLogic = unlocks(0x03, 0x03, 0xc8, True)
    extraSkinsAchievement = Achievement(achievementTitle("extra_skins"), "Unlock the extra skins for The Boys and Chef by collecting all 3 Golden Cows in the Valentine's Day race", 2)
    extraSkinsAchievement.add_core(extraSkinsLogic)
    mySet.add_achievement(extraSkinsAchievement)
    
# Tweek
def tweekUnlock():
    tweekUnlockLogic = unlocks(0x04, 0x05, 0xc8, True)
    tweekAchievement = Achievement(achievementTitle("tweek"), "Unlock Tweek by using 5 caffeine boosts from the blue power up boxes in the Spring Cleaning race", 2)
    tweekAchievement.add_core(tweekUnlockLogic)
    mySet.add_achievement(tweekAchievement)

def cartmanCopUnlock():
    cartmanCopLogic = unlocks(0x05, 0x05, 0xc0, True)
    cartmanCopAchievement = Achievement(achievementTitle("cartman_cop"), "Unlock Cartman Cop by hitting Chicken Lover's bus 5 times with Salty Balls in the Read a Book Day race", 2)
    cartmanCopAchievement.add_core(cartmanCopLogic)
    mySet.add_achievement(cartmanCopAchievement)

def skuzzlebuttUnlock():
    skuzzlebuttLogic = unlocks(0x06, 0x01, 0xc8)
    skuzzlebuttAchievement = Achievement(achievementTitle("skuzzlebutt"), "Unlock Skuzzlebutt by collecting the Golden Cow during the Easter race", 2)
    skuzzlebuttAchievement.add_core(skuzzlebuttLogic)
    mySet.add_achievement(skuzzlebuttAchievement)

def mrsBrovlofskiUnlock():
    mrsBrovlofskiLogic = unlocks(0x06, 0x01, 0xcc)
    mrsBrovlofskiAchievement = Achievement(achievementTitle("mrs_broflovski"), "Unlock Mrs. Broflovski by collecting the Pie during the Easter Race", 2)
    mrsBrovlofskiAchievement.add_core(mrsBrovlofskiLogic)
    mySet.add_achievement(mrsBrovlofskiAchievement)

def msCartmanUnlock():
    msCartmanLogic = [
        commonChampionshipLogic(0x07),
        raceOutcome,
        playerWin,
        resetToCountdown,
        trigger(playerCheckpoint == 0x04),
        reset_if(ai1Checkpoint != 0x00),
        reset_if(ai2Checkpoint != 0x00),
        reset_if(ai3Checkpoint != 0x00),
        reset_if(ai4Checkpoint != 0x00),
        reset_if(ai5Checkpoint != 0x00),
        waitingOnWin()
    ]
    msCartmanAchievement = Achievement(achievementTitle("ms_cartman"), "Unlock Ms. Cartman by being the only player to deliver lemonade during the Pink Lemonade race", 2)
    msCartmanAchievement.add_core(msCartmanLogic)
    mySet.add_achievement(msCartmanAchievement)

def ikeUnlock():
    ikeLogic = unlocks(0x08, 0x01, 0xc8)
    ikeAchievement = Achievement(achievementTitle("ike"), "Unlock Ike by collecting the Golden Cow on the plane wing during the Memorial Day race", 2)
    ikeAchievement.add_core(ikeLogic)
    mySet.add_achievement(ikeAchievement)

def visitorUnlock():
    visitorLogic = unlocks(0x08, 0x01, 0xcc, True)
    visitorAchievement = Achievement(achievementTitle("visitor"), "Unlock Visitor by collecting both Pies during the Memorial Day race", 2)
    visitorAchievement.add_core(visitorLogic)
    mySet.add_achievement(visitorAchievement)

def nedUnlock():
    nedLogic = [
        measured_if(demoCheck),
        measured_if(championship),
        measured_if(raceIndicator == 0x09),
        raceOutcome,
        playerWin,
        measured(raceData >> byte(0xc8) >= 0x0c),
        waitingOnWin()
    ]
    nedAchievement = Achievement(achievementTitle("ned"), "Unlock Ned by winning after using 12 Caffeine Boosts or Terrance Boosts during the Independence Day race", 2)
    nedAchievement.add_core(nedLogic)
    mySet.add_achievement(nedAchievement)

def deathUnlock():
    unlockCondition = (raceData >> byte(0xc8))
    deathLogic = [
        commonChampionshipLogic(0x0a),
        raceOutcome,
        playerWin,
        unlockCondition == 0x00,
        waitingOnWin()
    ]
    deathAchievement = Achievement(achievementTitle("death"), "Unlock Death by winning while only delivering 4 Candies at once during the Halloween race", 2)
    deathAchievement.add_core(deathLogic)
    mySet.add_achievement(deathAchievement)

def marvinUnlock():
    marvinLogic = [
        commonChampionshipLogic(0x0b),
        playerFinish,
        reset_if(playerCheckpoint != 0x00),
        resetToCountdown,
        waitingOnWin()
    ]
    marvinAchievement = Achievement(achievementTitle("marvin"), "Unlock Marvin by losing without collecting any turkeys during the Thanksgiving race", 2)
    marvinAchievement.add_core(marvinLogic)
    mySet.add_achievement(marvinAchievement)

def damienUnlock():
    damienLogic = [
        commonChampionshipLogic(0x0d),
        raceOutcome,
        playerWin,
        reset_if(raceData >> byte(0xc4) != 0x00),
        resetToCountdown,
        waitingOnWin()
    ]
    damienAchievement = Achievement(achievementTitle("damien"), "Unlock Damien by winning without letting another player pick up the key during the Millenium New Years Eve race", 2)
    damienAchievement.add_core(damienLogic)
    mySet.add_achievement(damienAchievement)

def tapUnlock():
    tapLogic = unlocks(0x0c, 0x04, 0xc8, True)
    tapAchievement = Achievement(achievementTitle("terrance_phillip"), "Unlock Terrance & Phillip by collecting all 4 Golden Cows during the Christmas race", 2)
    tapAchievement.add_core(tapLogic)
    mySet.add_achievement(tapAchievement)


# Character Unlocks

garrisonUnlock()
pipUnlock()
bebeUnlock()
extraSkinsUnlock()
tweekUnlock()
cartmanCopUnlock()
skuzzlebuttUnlock()
mrsBrovlofskiUnlock()
msCartmanUnlock()
ikeUnlock()
visitorUnlock()
nedUnlock()
deathUnlock()
marvinUnlock()
damienUnlock()
tapUnlock()



# Credit Achievements
order = 1
for race in range(0x00, 0x0e):
    creditAchievementLogic = [
        commonChampionshipLogic(race),
        raceState == 0x04,
        creditIncrease,
    ]

    credAchievement = Achievement(achievementTitle(f"{order}_cred"), f"Collect the Extra Credit during the {raceName(race)} race in Championship mode", 1)
    credAchievement.add_core(creditAchievementLogic)

    mySet.add_achievement(credAchievement)
    order += 1

# Race as X in Y on Z race

# Race as X in Y track (any race)


def challengeChar(char: List[int], offset: bool = False):
    if offset:
        for index, c in enumerate(char):
            if c >= 0x0c:
                c = c - 1
            if index + 1 == len(char):
                return(character == c)
            else:
                return(or_next(character == c))
    else:
        for index, c in enumerate(char):
            if index + 1== len(char):
                return(character == c)
            else:
                return(or_next(character == c))


trackToRaces = [
    [], # City
    [], # Forest
    [0x03, 0x07], # Big Gay Al's
    [], # Volcano
    [0x06, 0x09], # Mountain
    [], # Farm
    [0x04], # Sewer
    [], # Carnival
]

def convertTracksToRaces(track: int):
    for index, race in enumerate(trackToRaces[track]):
        if index + 1== len(trackToRaces[track]):
            return(raceIndicator == race)
        else:
            return(or_next(raceIndicator == race))

def challengeCore():
    return [
        demoCheck,
        modeAddress < 3
    ]

def charOnTrack(char: List[int], track: int):

    # Alt 1
    alt1Logic = [
        raceOutcome,
        playerWin,
        modeAddress != 2, # not arcade
        challengeChar(char),
        convertTracksToRaces(track),
        trackIndicator == track,
        waitingOnWin()
    ]
    
    # Alt 2
    alt2Logic = [
        raceOutcome,
        playerWin,
        modeAddress == 2,
        challengeChar(char),
        trackIndicator == track,
        waitingOnWin()
    ]

    return [challengeCore(), alt1Logic, alt2Logic]

# BGA on BGA
bgaBGA = Achievement(achievementTitle("1_challenge"), "Win any race at Big Gay Al's as Big Gay Al", 2)
bgaLogic = charOnTrack([0x14], 0x02)

bgaBGA.add_core(bgaLogic[0])
bgaBGA.add_alt(bgaLogic[1])
bgaBGA.add_alt(bgaLogic[2])
mySet.add_achievement(bgaBGA)

# Visitor in Sewers
visitorSewers = Achievement(achievementTitle("2_challenge"), "Win any race in the Sewer as Visitor", 2)
visitorLogic = charOnTrack([0x16], 0x06)

visitorSewers.add_core(visitorLogic[0])
visitorSewers.add_alt(visitorLogic[1])
visitorSewers.add_alt(visitorLogic[2])
mySet.add_achievement(visitorSewers)

# Ned or Jimbo in Mountain
nedJimboMountain = Achievement(achievementTitle("3_challenge"), "Win any race in the Mountain as either Jimbo or Ned", 2)
nedJimboLogic = charOnTrack([0x07, 0x17], 0x04)

nedJimboMountain.add_core(nedJimboLogic[0])
nedJimboMountain.add_alt(nedJimboLogic[1])
nedJimboMountain.add_alt(nedJimboLogic[2])
mySet.add_achievement(nedJimboMountain)

def charInRace(char: List[int], race: int):
    coreLogic = [
        challengeCore(),
        modeAddress != 0x01
    ]

    logic = []
    for x in [0x00, 0x02]:
        logic.append([
            raceOutcome,
            playerWin,
            modeAddress == x,
            challengeChar(char, True if x == 0x02 else False),
            raceIndicator == race,
            waitingOnWin()
        ])
    return [coreLogic, logic[0], logic[1]]

def raceOnTrack(race: int, track: int):
    return [
        raceOutcome,
        playerWin,
        modeAddress == 0x02,
        raceIndicator == race,
        trackIndicator == track,
        waitingOnWin()
    ]

cartmanReadABook = Achievement(achievementTitle("4_challenge"), "Win the Read a Book Day race as Cartman Cop", 2)
cartmanReadABookLogic = charInRace([0x10], 0x05)
cartmanReadABook.add_core(cartmanReadABookLogic[0])
cartmanReadABook.add_alt(cartmanReadABookLogic[1])
cartmanReadABook.add_alt(cartmanReadABookLogic[2])
mySet.add_achievement(cartmanReadABook)

bhChefThanksgiving = Achievement(achievementTitle("5_challenge"), "Win the Thanksgiving race as Braveheart Chef", 2)
bhChefThanksgivingLogic = charInRace([0x24], 0x0b)
bhChefThanksgiving.add_core(bhChefThanksgivingLogic[0])
bhChefThanksgiving.add_alt(bhChefThanksgivingLogic[1])
bhChefThanksgiving.add_alt(bhChefThanksgivingLogic[2])
mySet.add_achievement(bhChefThanksgiving)

milleniumJesus = Achievement(achievementTitle("6_challenge"), "Win the Millenium New Year's Eve Race as Jesus", 2)
milleniumJesusLogic = charInRace([0x1c], 0x0d)
milleniumJesus.add_core(milleniumJesusLogic[0])
milleniumJesus.add_alt(milleniumJesusLogic[1])
milleniumJesus.add_alt(milleniumJesusLogic[2])
mySet.add_achievement(milleniumJesus)

rd2Volcano = Achievement(achievementTitle("7_challenge"), "Win the Rally Days #2 race at the Volcano", 2)
rd2VolcanoLogic = raceOnTrack(0x01, 0x03)
rd2Volcano.add_core(rd2VolcanoLogic)
mySet.add_achievement(rd2Volcano)

springCleaningForest = Achievement(achievementTitle("8_challenge"), "Win the Spring Cleaning race in the Forest", 2)
springCleaningForestLogic = raceOnTrack(0x04, 0x01)
springCleaningForest.add_core(springCleaningForestLogic)
mySet.add_achievement(springCleaningForest)

pinkLemonadeCarnival = Achievement(achievementTitle("9_challenge"), "Win the Pink Lemonade race at the Carnival", 2)
pinkLemonadeCarnivalLogic = raceOnTrack(0x07, 0x07)
pinkLemonadeCarnival.add_core(pinkLemonadeCarnivalLogic)
mySet.add_achievement(pinkLemonadeCarnival)

memorialBGA = Achievement(achievementTitle("10_challenge"), "Win the Memorial Day race at Big Gay Al's", 2)
memorialBGALogic = raceOnTrack(0x08, 0x02)
memorialBGA.add_core(memorialBGALogic)
mySet.add_achievement(memorialBGA)

christmasMountain = Achievement(achievementTitle("11_challenge"), "Win the Christmas Day race on the Mountain", 2)
christmasMountainLogic = raceOnTrack(0x0c, 0x04)
christmasMountain.add_core(christmasMountainLogic)
mySet.add_achievement(christmasMountain)

complexSewerRace = Achievement(achievementTitle("12_challenge"), "With the Random Checkpoints and Pick Ups options enabled as well as 5 random CPUs, win the Rally Days #2 race in the Sewer on Arcade mode with the map turned off before the countdown finishes and kept off for the entire race", 5)
complexSewerRaceLogic = [
    demoCheck,
    modeAddress == 0x02,
    byte(0x0e376a) == 0x01, # Random Checkpoints On
    byte(0x0e3fde) == 0x01, # Pick Ups On
    byte(0x0e352a) == 0x04, # 5 CPUs
    byte(0x0e42fe) == 0x03, # HUD Off
    trackIndicator == 0x06,
    raceIndicator == 0x01,
    raceOutcome,
    playerWin,
    resetToCountdown,
    trigger(raceState.delta() == 0x04),
    trigger(raceState == 0x05),
    and_next(raceState == 0x04),
    reset_if(byte(0x0e42fe) != 0x03) # HUD Off
]
complexSewerRace.add_core(complexSewerRaceLogic)
mySet.add_achievement(complexSewerRace)

memorialDayLaser = Achievement(achievementTitle("13_challenge"), "Win the Memorial Day race while being the only player to pass over all 4 checkpoints with the laser", 2)
memorialDayLaserLogic = [
    demoCheck,
    modeAddress < 3,
    modeAddress != 0x01,
    raceOutcome,
    playerWin,
    raceIndicator == 0x08,
    resetToCountdown,
    reset_if(ai1Checkpoint > 0x00),
    reset_if(ai2Checkpoint > 0x00),
    reset_if(ai3Checkpoint > 0x00),
    reset_if(ai4Checkpoint > 0x00),
    reset_if(ai5Checkpoint > 0x00),
    waitingOnWin(),
]

memorialDayLaser.add_core(memorialDayLaserLogic)
mySet.add_achievement(memorialDayLaser)

charUnlock1 = byte(0x0d9eb8)
charUnlock2 = byte(0x0d9eb9)
charUnlock3 = byte(0x0d9eba)
charUnlock4 = byte(0x0d9ebb)

magicalMysteryTour = Achievement(achievementTitle("14_challenge"), "Win the Championship without restarting after Rally Days #1 while playing as the Mystery character after unlocking every character. The icon will appear in the bottom right if you have everyone when you load into the race.", 50)
magicalMysteryTourLogic = [
    demoCheck,
    reset_if(gameState == 0x06),
    (raceIndicator == 0x00).with_hits(1),
    trigger(raceIndicator == 0x0d),
    championship,
    character == 0x0b,
    reset_if(credits < credits.delta()),
    raceOutcome,
    and_next(loadingScreen == 0x00),
    and_next(raceData >> dword(0xa0) != 0x00), # race in progress
    reset_if(raceData >> dword(0xa0) != recall()),
    trigger(raceState.delta() == 0x04),
    trigger(raceState == 0x05),
    reset_if(charUnlock1 + charUnlock2 + charUnlock3 + charUnlock4 < 0x2b7)
]

magicalMysteryTour.add_core(magicalMysteryTourLogic)
mySet.add_achievement(magicalMysteryTour)

# Intro - likely UWC but was a good pointer test
intro = Achievement(achievementTitle("intro"), "Watch the whole South Park intro", 0)
introCore = [
    or_next(gameState.delta() == 0x02),
    reset_if(gameState.delta() == 0x03),
    (gameState == 0x06)
]

def introAlts(currentHz: int):
    return [
        and_next(hz == currentHz),
        and_next(loadingScreen == 0x00),
        (gameState.delta() == 0x04).with_hits(1420 if currentHz == 0x05 else 1700)
    ]

intro.add_core(introCore)
intro.add_alt(introAlts(0x05))
intro.add_alt(introAlts(0x06))
mySet.add_achievement(intro)

laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")

if laptopPath.exists():
    mySet.save(laptopPath)
elif pcPath.exists():
    mySet.save(pcPath)
else:
    mySet.save()