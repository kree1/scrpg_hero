#! python3.7

import math
import os
import random
import string
import tkinter
import tkSimpleDialog
from tkinter import *
from tkinter import messagebox

random.seed()

global categories_plural, categories_singular, pronouns, step_names
categories_plural = ["Qualities",
                     "Powers",
                     "Powers/Qualities"]
categories_singular = ["Quality",
                       "Power",
                       "Power/Quality"]
pronouns = [["she", "her", "her"],
            ["he", "him", "his"],
            ["they", "them", "their"]]
step_names = ["",
              "Background",
              "Power Source",
              "Archetype",
              "Personality",
              "Red Abilities",
              "Retcon",
              "Health"]

global p_athletic, p_elemental, p_hallmark, p_intellectual, p_materials, p_mobility, p_psychic
global p_self_control, p_technological, p_unlisted, p_categories, p_collection
p_athletic = ["Agility",
              "Speed",
              "Strength",
              "Vitality"]
p_elemental = ["Cold",
               "Cosmic",
               "Electricity",
               "Fire",
               "Infernal",
               "Nuclear",
               "Radiant",
               "Sonic",
               "Weather"]
p_hallmark = ["Signature Vehicle",
              "Signature Weaponry"]
p_intellectual = ["Awareness",
                  "Deduction",
                  "Intuition",
                  "Lightning Calculator",
                  "Presence"]
p_materials = ["Metal",
               "Plants",
               "Stone",
               "Toxic",
               "Transmutation"]
p_mobility = ["Flight",
              "Leaping",
              "Momentum",
              "Swimming",
              "Swinging",
              "Teleportation",
              "Wall-Crawling"]
p_psychic = ["Animal Control",
             "Illusions",
             "Postcognition",
             "Precognition",
             "Remote Viewing",
             "Suggestion",
             "Telekinesis",
             "Telepathy"]
p_self_control = ["Absorption",
                  "Density Control",
                  "Duplication",
                  "Elasticity",
                  "Intangibility",
                  "Invisibility",
                  "Part Detachment",
                  "Shapeshifting",
                  "Size-Changing"]
p_technological = ["Gadgets",
                   "Inventions",
                   "Power Suit",
                   "Robotics"]
p_unlisted = ["Invented Power"]
p_categories = ["Athletic",
                "Elemental/Energy",
                "Hallmark",
                "Intellectual",
                "Materials",
                "Mobility",
                "Psychic",
                "Self Control",
                "Technological",
                "Unlisted"]
p_collection = [p_athletic,
                p_elemental,
                p_hallmark,
                p_intellectual,
                p_materials,
                p_mobility,
                p_psychic,
                p_self_control,
                p_technological,
                p_unlisted]

global q_information, q_mental, q_physical, q_social, q_special, q_categories, q_collection
q_information = ["Criminal Underworld Info",
                 "Deep Space Knowledge",
                 "History",
                 "Magical Lore",
                 "Medicine",
                 "Otherworldly Mythos",
                 "Science",
                 "Technology"]
q_mental = ["Alertness",
            "Conviction",
            "Creativity",
            "Investigation",
            "Self-Discipline"]
q_physical = ["Acrobatics",
              "Close Combat",
              "Finesse",
              "Fitness",
              "Ranged Combat",
              "Stealth"]
q_social = ["Banter",
            "Imposing",
            "Insight",
            "Leadership",
            "Persuasion"]
q_special = ["Roleplaying Quality"]
q_categories = ["Information",
                "Mental",
                "Physical",
                "Social",
                "Special"]
q_collection = [q_information, q_mental, q_physical, q_social, q_special]

global mixed_collection, mixed_categories
mixed_collection = [q_collection, p_collection]
mixed_categories = [q_categories, p_categories]

global legal_dice
legal_dice = [4, 6, 8, 10, 12]

def printlong(text, width, prefix=""):
    # Prints the string [text] with line breaks inserted to prevent any line showing more than
    #  [width] characters, and with [prefix] inserted at the start of each line.
    if len(text) <= width:
        print(prefix + text)
    elif " " not in text[0:width]:
        print(prefix + text)
    elif width <= 0:
        print(prefix + text)
    else:
        sec_start = 0
        sec_end = text.rfind(" ", sec_start, sec_start + width)
        while sec_start < len(text):
            if sec_end == -1:
                print(prefix + text[sec_start:])
                sec_start = len(text)
            else:
                print(prefix + text[sec_start:sec_end+1])
                sec_start = sec_end + 1
                if sec_start + width >= len(text):
                    sec_end = len(text)
                else:
                    sec_end = text.rfind(" ", sec_start, sec_start + width)

def split_text(text, width=100, prefix=""):
    # Returns the string [text] with line breaks inserted to prevent any line showing more than
    #  [width] characters, and with [prefix] inserted at the start of each line.
##    print("### split_text: len(text)=" + str(len(text)))
    if "\n" in text:
        # If text already contains multiple lines, consider each one separately
        sections = text.split("\n")
        lines = split_text(sections[0], width, prefix)
        for s in sections[1:]:
            lines += "\n" + split_text(s, width, prefix)
        return lines
    elif len(text) < width or " " not in text[0:width] or width <= 0:
        # If text is less that width characters long,
        # or if the first [width] characters contain no spaces,
        # or if width <= 0,
        #  return text with prefix and no changes
        return prefix + text
    else:
        if prefix == "":
            # No prefix specified? Check to see if text starts with whitespace
            while text[0] == " ":
                prefix += text[0]
                text = text[1:]
        lines = prefix + text
        sec_start = 0
        sec_end = lines.rfind(" ", sec_start + len(prefix), sec_start + len(prefix) + width)
        while sec_start < len(text):
##            print(lines)
##            print("### split_text: sec_end=" + str(sec_end) + " ('" + lines[sec_end] + "')")
            if sec_end in range(len(text)):
                # Insert a line break and the prefix after sec_end
                pre_break = lines[0:sec_end]
                post_break = lines[sec_end+1:]
                lines = pre_break + "\n" + prefix + post_break
                # Move sec_start to the character after the new prefix
                sec_start = sec_end + len(prefix) + 1
                # Move sec_end to either the last space between sec_start and sec_start + width, or
                #  to the end of the string
                if sec_start + width >= len(text):
                    sec_end = len(text)
                else:
                    sec_end = lines.rfind(" ", sec_start, sec_start + len(prefix) + width)
            else:
                sec_start = len(text)
##        print(text)
##        print(lines)
        return lines

def dice_combo(die_sizes, results=[]):
    # Converts a list of die sizes (e.g., [6, 6, 10]) to a phrase describing the set of dice
    #  (e.g. "2d6 + 1d10")
    # Ignores any die whose corresponding entry in results is nonzero.
    if results == []:
        results = [0 for i in range(len(die_sizes))]
    dice_by_size = [0 for i in range(4)]
    for i in range(4):
        size = 12 - 2*i
        dice_by_size[i] = len([j for j in range(len(die_sizes)) \
                               if die_sizes[j]==size and results[j]==0])
    dice_text = ""
    for i in [j for j in range(4) if dice_by_size[j] != 0]:
        if dice_text == "":
            dice_text = str(dice_by_size[i]) + "d" + str(12-2*i)
        else:
            dice_text += " + " + str(dice_by_size[i]) + "d" + str(12-2*i)
    return dice_text

global invalid_message
invalid_message = "Please choose a listed letter option."

def choose_letter(entry_options,
                  blank_choice,
                  prompt="",
                  repeat_message=invalid_message,
                  inputs=[]):
    # Keeps asking the user for a text entry (first with prompt, then with repeat_message)
    #   until they provide one that matches one of entry_options (ignoring case).
    # inputs: a list of text inputs to use automatically instead of prompting the user.
    # Returns [their choice, any remaining inputs]
    if len(inputs) > 0:
        print("### choose_letter: inputs=" + str(inputs))
    entry_choice = blank_choice
    if len(inputs) > 0:
        if len(prompt) > 0:
            print(prompt)
        print("> " + inputs[0])
        entry_choice = inputs.pop(0)[0].upper()
    elif entry_options == "YN":
        # If there are no inputs and the choices are Y and N, we can use a simple dialog to
        #   ask the question instead of a text entry
        title = "Hero Creation"
        msg_prompt = prompt.replace(" (y/n)","")
        if messagebox.askyesno(title, msg_prompt):
            entry_choice = "Y"
        else:
            entry_choice = "N"
    else:
        if len(prompt) > 0:
            entry_choice = input(prompt + "\n")[0].upper()
        else:
            entry_choice = input()[0].upper()
    while entry_choice not in entry_options:
        if len(inputs) > 0:
            print(repeat_message)
            print("> " + inputs[0])
            entry_choice = inputs.pop(0)[0].upper()
        else:
            entry_choice = input(repeat_message + "\n")[0].upper()
    return [entry_choice, inputs]

def Power(indices):
    return p_collection[indices[0]][indices[1]]

def Powers(pairs):
    return [p_collection[entry[0]][entry[1]] for entry in pairs]

def Quality(indices):
    return q_collection[indices[0]][indices[1]]

def Qualities(pairs):
    return [q_collection[entry[0]][entry[1]] for entry in pairs]

def MixedPQ(triplet):
    return mixed_collection[triplet[0]][triplet[1]][triplet[2]]

def MixedPQs(triplets):
    return [mixed_collection[entry[0]][entry[1]][entry[2]] for entry in triplets]

def Category(index1, index2):
    return [[index1, index2, x] for x in range(len(mixed_collection[index1][index2]))]

def AllCategories(t=2, custom=False):
    roster = []
    types = [0,1]
    if t == 0:
        types = [0]
    elif t == 1:
        types = [1]
    for i in types:
        max_category = len(mixed_collection[i])
        if not custom:
            max_category -= 1
        for j in range(max_category):
            roster += Category(i,j)
    return roster

def DieCategory(triplets):
    any_powers = sum([1 for x in triplets if x[0]==1])
    any_qualities = sum([1 for x in triplets if x[0]==0])
    if any_powers > 0 and any_qualities > 0:
        return 2
    elif any_powers > 0:
        return 1
    else:
        return 0

def ValidPQs(triplets):
    # Returns the members of triplets which refer to existing powers/qualities
    valid_triplets = []
    for t in triplets:
        if t[0] in range(len(mixed_collection)):
            if t[1] in range(len(mixed_collection[t[0]])):
                if t[2] in range(len(mixed_collection[t[0]][t[1]])):
                    valid_triplets.append(t)
    return valid_triplets

# Class representing a die assigned to a power or quality
class PQDie:
    def __init__(self, ispower, category, index, diesize, flavorname="", stepnum=0):
        self.ispower = ispower
        self.category = category
        self.index = index
        self.diesize = diesize
        if self.ispower:
            self.name = p_collection[self.category][self.index]
        else:
            self.name = q_collection[self.category][self.index]
        if flavorname == "":
            self.flavorname = self.name
        else:
            self.flavorname = flavorname
        self.step = max([0,stepnum])
        self.steps_modified = []
        self.prev_version = None
    def __str__(self):
        summary = self.flavorname
        if self.name in ["Invented Power",
                         "Signature Vehicle",
                         "Signature Weaponry",
                         "Roleplaying Quality"]:
            summary = self.flavorname + "*"
        elif self.flavorname != self.name:
            summary = self.flavorname + " (" + self.name + ")"
        summary += " [" + str(self.diesize) + "]"
        return summary
    def __eq__(self, other):
        if isinstance(other, PQDie):
            match = self.ispower == other.ispower and \
                    self.category == other.category and \
                    self.index == other.index and \
                    self.diesize == other.diesize and \
                    self.flavorname == other.flavorname and \
                    self.step == other.step and \
                    self.steps_modified == other.steps_modified and \
                    self.prev_version == other.prev_version
            return match
        else:
            return False
    def CategoryName(self):
        if self.ispower:
            return p_categories[self.category]
        else:
            return q_categories[self.category]
    def triplet(self):
        return [self.ispower, self.category, self.index]
    def copy(self):
        mirror = PQDie(self.ispower,
                       self.category,
                       self.index,
                       self.diesize,
                       self.flavorname,
                       stepnum=self.step)
        mirror.steps_modified = [x for x in self.steps_modified]
        if self.prev_version:
            mirror.prev_version = self.prev_version.copy()
        return mirror
    def SetPrevious(self, stepnum):
        # Used in preparation for editing the PQDie's attributes during character creation
        # Creates a copy of the PQDie with its current attributes and saves it in self.prev_version, then adds the specified step number to the list of steps when this die was modified.
        self.prev_version = self.copy()
        self.steps_modified.append(stepnum)
    def RetrievePrior(self, stepnum):
        # Returns a copy of the PQDie as it existed prior to the specified step of character creation.
        if stepnum < 1:
            print("Error! " + str(stepnum) + " is too small to be a valid step index.")
            return self
        ancestor = self.copy()
        while len(ancestor.steps_modified) > 0:
            if max(ancestor.steps_modified) >= stepnum:
                ancestor = ancestor.prev_version
            else:
                return ancestor
        return ancestor

global r_destiny, r_energy, r_exorcism, r_fauna, r_flora, r_future, r_immortality, r_inner_demon
global r_magic, r_sea, r_space, r_time_traveler, r_undead, rc_esoteric
r_destiny = ["Destiny",
             "Signs and portents lead you towards an inevitable place in your life. You can " + \
             "always gain some measure of direction when needed.",
             "What omen of dire fortune did you just witness?",
             "What heinous prophecy just came true?",
             "Overcome in a situation directly connected to your destiny. Use your Max die. " + \
             "You and each of your allies gain a hero point."]
r_energy = ["[Energy/Element]",
            "You have an affinity for or a love of [energy/element]. You can interact with " + \
            "that energy/element with ease.",
            "What other energy/element is currently causing your powers to go on the fritz?",
            "What source of energy is currently dampening all your powers?",
            "Overcome a challenge involving [energy/element]. Use your Max die. You and each " + \
            "of your allies gain a hero point."]
r_exorcism = ["Exorcism",
              "You can detect the subtle hints of influences from other realms in an event.",
              "What is (literally or figuratively) coming back to haunt you?",
              "What has been allowed to enter this world?",
              "Overcome entities or elements from another dimension. Use your Max die. You " + \
              "and each of your allies gain a hero point."]
r_fauna = ["Fauna",
           "Your innate animalistic nature allows you to identify any type of non-sentient " + \
           "animal life and determine its origin in broad terms, such as Earth, alien, etc..",
           "How did your primal nature get the better of you?",
           "What is the only way the animal within can be restrained?",
           "Overcome with the aid of local fauna. Use your Max die. You and each of your " + \
           "allies gain a hero point."]
r_flora = ["Flora",
           "You can identify any type of plant life and determine its origin in broad terms, " + \
           "such as Earth, alien, etc.",
           "What grows out of your control?",
           "How is nature reclaiming something important?",
           "Overcome with the aid of local flora. Use your Max die. You and each of your " + \
           "allies gain a hero point."]
r_future = ["the Future",
            "You have visions or knowledge of things yet to come.",
            "What unintended ripple did your actionx have?",
            "What ripple effect now threatens the future as you know it?",
            "Overcome using your knowledge of possible futures. Use your Max die. You and " + \
            "each of your allies gain a hero point."]
r_immortality = ["Immortality",
                 "You do not age and will not be affected by mundane ailments.",
                 "You take the long view of things. How does that cause you to be too slow?",
                 "What important attachment must you shed?",
                 "Overcome a situation involving your physical condition. Use your Max die. " + \
                 "You and each of your allies gain a hero point."]
r_inner_demon = ["the Inner Demon",
                 "You have a darkness within you that you strive to keep suppressed. You can " + \
                 "reach out to your dark side to connect with similar forces.",
                 "What sinister act comes from tapping into your dark side?",
                 "What havoc does your dark side inflict as you allow it to take control?",
                 "Tap into your dark psyche to Overcome a problem. Use your Max die. You and " + \
                 "each of your allies gain a hero point."]
r_magic = ["Magic",
           "You are attuned to an otherworldly force, and can feel the mystic energies of the " + \
           "area.",
           "What weird curse is now following you around?",
           "What mystical backlash has changed your life?",
           "Overcome against a mystical force. Use your Max die. You and each of your allies " + \
           "gain a hero point."]
r_sea = ["the Sea",
         "You can speak to aquatic creatures and breathe underwater.",
         "What challenge does the surface world pose for you?",
         "What disaster is incoming as the sea comes calling?",
         "Overcome a situation while underwater. Use your Max die. You and each of your " + \
         "allies gain a hero point."]
r_space = ["Space",
           "You can survive in the vacuum of space without additional equipment.",
           "Who can hear you scream?",
           "What caused you to drift off into the unknown?",
           "Overcome while in space (or conditions similar to space). Use your Max die. You " + \
           "and each of your allies gain a hero point."]
r_time_traveler = ["the Time Traveler",
                   "You are far from your own time and are often unsure how to act in this " + \
                   "time. You have an innate sense for when time is not quite right in the " + \
                   "era you're in.",
                   "What detail of this era did you not previously know about?",
                   "What effects are happening as you discorporate in time?",
                   "Overcome a problem using knowledge from your home era. Use your Max die. " + \
                   "You and each of your allies gain a hero point."]
r_undead = ["the Undead",
            "You are \"living-challenged.\" You can still be hurt and damaged, but you can " + \
            "ignore many of the afflictions that bother the living.",
            "How did your undead nature unnerve those around you?",
            "How are you risking your connection to the living world with what happened?",
            "Overcome a situation where your undead nature comes in handy. Use your Max die. " + \
            "You and each of your allies gain a hero point."]
rc_esoteric = [r_destiny,
               r_energy,
               r_exorcism,
               r_fauna,
               r_flora,
               r_future,
               r_immortality,
               r_inner_demon,
               r_magic,
               r_sea,
               r_space,
               r_time_traveler,
               r_undead]

global r_clockwork, r_gearhead, r_history, r_indestructible, r_lab, r_mastery, r_mentor
global r_powerless, r_science, r_speed, r_stealth, r_strength, r_tactician, r_whispers, rc_expertise
r_clockwork = ["Clockwork",
               "You are good at understanding how pieces operate in tandem and can identify " + \
               "flaws in ordered systems.",
               "What tool just broke?",
               "What faraway location are your tools now occupying?",
               "Overcome a complex problem with a simple tool. Use your Max die. You and each " + \
               "of your allies gain a hero point."]
r_gearhead = ["the Gearhead",
              "You always know the general state of repair or function of an item of " + \
              "technology, whether it's a simple toaster or an alien orbital defense system.",
              "What mechanical device just shorted out?",
              "What machine just went terribly off the rails?",
              "Overcome a technological challenge. Use your Max die. You and each of your " + \
              "allies gain a hero point."]
r_history = ["History",
             "You have many contacts and references in the archaeological, historical, and " + \
             "anthropological fields.",
             "How did your old-timeyness cause an issue?",
             "What ancient force is now making itself known in the present?",
             "Overcome a situation involving archaeology, history, or puzzle-solving. Use " + \
             "your Max die. You and each of your allies gain a hero point."]
r_indestructible = ["the Indestructible",
                    "You ignore damage from unpowered close-combat weapons and attacks, such " + \
                    "as clubs and non-powered fists, or basic ranged attacks, such as slings " + \
                    "and arrows.",
                    "What goes wrong with your defenses?",
                    "Who gets hurt other than you as a result of you not being able to take " + \
                    "damage?",
                    "Overcome in a situation where you charge headlong into danger. Use your " + \
                    "Max die. You and each of your allies gain a hero point."]
r_lab = ["the Lab",
         "You have nearly unlimited access to a dedicated research area, and are at home there.",
         "What did you make a detour to observe and sample for later experiments?",
         "Something's gone very wrong at the lab; what was it?",
         "Overcome while in a familiar workspace or when you have ample research time. Use " + \
         "your Max die. You and each of your allies gain a hero point."]
r_mastery = ["Mastery",
             "You have thoroughly studied your own powers and are proud of your mastery of " + \
             "them. You understand a good deal about the metaphysics of your powers.",
             "How did your powers fail you in the moment?",
             "What side effects are you suffering from your powers?",
             "Overcome in a situation that uses your powers in a new way. Use your Max die. " + \
             "You and each of your allies gain a hero point."]
r_mentor = ["the Mentor",
            "It is important to you to share your knowledge and experience with " + \
            "less-weathered heroes. Everyone grants you some measure of respect for your wisdom.",
            "Which whippersnapper just showed you up?",
            "What has just proven that you're too behind the times?",
            "Overcome a challenge that someone else younger already tried and failed. Use " + \
            "your Max die. You and each of your allies gain a hero point."]
r_powerless = ["the Powerless",
               "You value training and hard work over enhanced abilities. You understand how " + \
               "to get things done without powers and how to exploit flaws in powered " + \
               "individuals.",
               "What temporary injury did you just suffer?",
               "What more serious injury did you just suffer?",
               "Use your knowledge of the limitations of super powers in an Overcome action. " + \
               "Use your Max die. You and each of your allies gain a hero point."]
r_science = ["Science",
             "You are up to date on and understand most modern scientific theories and " + \
             "research and can quote from them during conversations.",
             "What were the surprising effects of leveraging that scientific principle in " + \
             "this situation?",
             "Oh heck! What just blew up?",
             "Overcome while applying specific scientific principles. Use your Max die. You " + \
             "and each of your allies gain a hero point."]
r_speed = ["Speed",
           "You're fast, and you don't like to waste time. You like to be on your way as " + \
           "quickly as possible.",
           "What physical drawbacks do you suffer from going too fast?",
           "What critical detail did you speed by earlier that is now coming back to haunt you?",
           "When you successfully Overcome, you may end up anywhere in the current " + \
           "environment. You and each of your allies gain a hero point."]
r_stealth = ["Stealth",
             "You always know the most efficient method to enter or leave a location.",
             "What evidence of your presence did you just leave behind?",
             "What just happened that identified you as an obvious threat?",
             "Overcome to infiltrate somewhere or avoid detection. Use your Max die. You and " + \
             "each of your allies gain a hero point."]
r_strength = ["Strength",
              "You are very strong, so you must be careful to not crush delicate things. You " + \
              "do not need to roll to perform mundane acts of great strength.",
              "What just broke?",
              "Who just broke?",
              "Overcome using brute force. Use your Max die. You and each of your allies gain " + \
              "a hero point."]
r_tactician = ["the Tactician",
               "You are constantly assessing the situation, making plans and backup plans, " + \
               "and then reassessing the situation.",
               "What one variable did your plan not account for?",
               "What major threat is revealed that invalidates all your plans?",
               "Overcome when you can flashback to how you prepared for this exact situation. " + \
               "Use your Max die. You and each of your allies gain a hero point."]
r_whispers = ["Whispers",
              "You hear a voice in your head that no one else hears. That voice tells you " + \
              "things, which might be true or false, but the voice certainly seems to know a lot.",
              "How did the voice in your head just distract you?",
              "What is the voice demanding of you now?",
              "Overcome against a challenge that involves information you have no real way of " + \
              "knowing. Use your Max die. You and each of your allies gain a hero point."]
rc_expertise = [r_clockwork,
                r_gearhead,
                r_history,
                r_indestructible,
                r_lab,
                r_mastery,
                r_mentor,
                r_powerless,
                r_science,
                r_speed,
                r_stealth,
                r_strength,
                r_tactician,
                r_whispers]

global r_chaos, r_compassion, r_defender, r_dependence, r_equality, r_great_power, r_hero, r_honor
global r_justice, r_liberty, r_order, r_self_preservation, r_zealot, rc_ideals
r_chaos = ["Chaos",
           "You are an unpredictable free spirit. Even towering intellects can't predict what " + \
           "you will do next.",
           "How did you fall in line in order to get something done?",
           "What has caused you to become predictable and stale?",
           "Overcome a situation in a way that is truly unpredictable. Use your Max die. You " + \
           "and each of your allies gain a hero point."]
r_compassion = ["Compassion",
                "You are an empathetic person. You feel the suffering of others around you.",
                "What overwhelming injustice causes you extra pain?",
                "How will you handle disconnecting from humanity?",
                "Overcome to connect with an individual on a personal level. Use your Max " + \
                "die. You and each of your allies gain a hero point."]
r_defender = ["the Defender",
              "You will put yourself in harm's way to defend another without a second thought.",
              "How do your actions put you in more danger than before?",
              "What great sacrifice did you just make to succeed?",
              "Overcome a situation that requires you to hold the line. Use your Max die, OR " + \
              "use your Mid die and Defend with your Min die. You and each of your allies " + \
              "gain a hero point."]
r_dependence = ["Dependence",
                "You are reliant on [something] and cannot normally function without it.",
                "How did the object of your dependence get damaged or lost?",
                "How is your dependence preventing you from functioning as a hero?",
                "Overcome in a situation that the object of your dependence was made for. Use " + \
                "your Max die. You and each of your allies gain a hero point."]
r_equality = ["Equality",
              "You have a keen sense of social status and can spot any situation where people " + \
              "are treated unfairly.",
              "Who is in danger that you just spotted?",
              "What will you sacrifice to protect the downtrodden?",
              "Overcome to protect the rights of the underprivileged. Use your Max die. You " + \
              "and each of your allies gain a hero point."]
r_great_power = ["Great Power",
                 "Your powers are so strong they can even scare you sometimes, but you work " + \
                 "hard to control them. You can wield those powers to intimidate others.",
                 "How do you restrain yourself from unleashing your full power?",
                 "What major damage do you inflict in the process of saving the day?",
                 "Overcome a situation using one of your highest rated Powers. Use your Max " + \
                 "die. You and each of your allies gain a hero point."]
r_hero = ["the Hero",
          "Because of your abilities, you have a calling to protect others.",
          "Your immediate need to help someone else causes you to drop the ball in your " + \
          "personal life. What was it?",
          "You're given an ultimatum between your life as a hero and something else you " + \
          "value. What do you give up?",
          "Overcome in a situation in which innocent people are in immediate danger. Use your " + \
          "Max die. You and each of your allies gain a hero point."]
r_honor = ["Honor",
           "You are governed by a strict code of conduct. Even under coercion, you will not " + \
           "compromise your ideals.",
           "Your honor has been challenged. How will you answer?",
           "Will you choose your honor, or your life?",
           "Overcome a situation to maintain your code of honor. Use your Max die. You and " + \
           "each of your allies gain a hero point."]
r_justice = ["Justice",
             "You are always aware of acts of injustice in your environment and those who " + \
             "have committed them.",
             "How are you taking extra time to show yourself as a shining example of justice?",
             "How do you unnerve your allies in the single-minded pursuit of justice?",
             "Overcome to stop an act of injustice in progress. Use your Max die. You and " + \
             "each of your allies gain a hero point."]
r_liberty = ["Liberty",
             "You believe strongly in freedom and always side with the oppressed. You can " + \
             "never truly be mentally restrained.",
             "How do you become temporarily trapped?",
             "How have you become a prisoner yourself?",
             "Overcome in a situation where you are restricted or bound. Use your Max die. " + \
             "You and each of your allies gain a hero point."]
r_order = ["Order",
           "You believe in organization and concordance. You always keep your head in the " + \
           "face of chaos.",
           "What element of disorder causes your plan to fall apart?",
           "How is your ordered existence ruined by chaos?",
           "Overcome a challenge where you can organize other people. Use your Max die. You " + \
           "and each of your allies gain a hero point."]
r_self_preservation = ["Self-Preservation",
                       "You value your own safety more than most others in your line of work. " + \
                       "You will never be caught fully unaware in a situation where your life " + \
                       "is at stake.",
                       "Who suffers because of your hesitation?",
                       "Are you willing to lay down your life to save others?",
                       "Overcome to get yourself out of immediate danger. Use your Max die. " + \
                       "You and each of your allies gain a hero point."]
r_zealot = ["the Zealot",
            "Your will is indomitable, and your beliefs govern your actions.",
            "Who suffered more because of your zealous persecution?",
            "What has your faith called on you to do that no one else will understand?",
            "Overcome a situation that tests your faith. Use your Max die. You and each of " + \
            "your allies gain a hero point."]
rc_ideals = [r_chaos,
             r_compassion,
             r_defender,
             r_dependence,
             r_equality,
             r_great_power,
             r_hero,
             r_honor,
             r_justice,
             r_liberty,
             r_order,
             r_self_preservation,
             r_zealot]

global r_ambition, r_amnesia, r_detachment, r_discovery, r_levity, r_loner, r_nomad, r_peace
global r_rage, r_savagery, r_split, r_spotless_mind, rc_identity
r_ambition = ["Ambition",
              "There's something that you want, and you strive toward achieving your goals, " + \
              "no matter the cost. You see paths to victory that no one else will.",
              "How is the pursuit of your goals getting in the way of being a hero in this " + \
              "situation?",
              "What did you just pass up or miss that could've helped you achieve your " + \
              "biggest goal at last?",
              "Overcome in a situation where someone else has given you a bonus from a Boost. " + \
              "Use your Max die. You and each of your allies gain a hero point."]
r_amnesia = ["Amnesia",
             "Your past is lost to you or otherwise obscured. Others have immense difficulty " + \
             "in keeping track of you.",
             "You have a flash of your former life that momentarily distracted you- what was it?",
             "A shocking detail of your past changes the current situation- how does it " + \
             "affect the scene?",
             "Overcome in a situation where a completely fresh perspective is useful. Use " + \
             "your Max die. You and each of your allies gain a hero point."]
r_detachment = ["Detachment",
                "You are detached from emotional situations and always keep your cool.",
                "Which hero or supporting character have you just alienated with your distant " + \
                "behavior?",
                "How have you withdrawn from the current situation to cope?",
                "Overcome a challenge related to duress or fear. Use your Max die. You and " + \
                "each of your allies gain a hero point."]
r_discovery = ["Discovery",
               "You are eager to learn new things at any cost. You can rattle off data about " + \
               "newly discovered concepts and ideas.",
               "What new discovery causes you to reconsider what you are doing?",
               "What new discovery must you keep hidden at all costs?",
               "When you're at the forefront in making a discovery or invention and take an " + \
               "Overcome action to further your knowledge, use your Max die. You and each of " + \
               "your allies gain a hero point."]
r_levity = ["Levity",
            "You keep your positive outlook even when all hope is lost. Your spirit is nearly " + \
            "impossible to break.",
            "Who did you offend by making light at the wrong time?",
            "What has occurred to finally break your good spirits?",
            "Overcome a dire situation where your jokes prevent demoralization. Use your Max " + \
            "die. You and each of your allies gain a hero point."]
r_loner = ["the Loner",
           "You're the best at what you do, as long as no one else sees you do it. You can " + \
           "always find your own path.",
           "Now that you're separated from your team, how will you get back?",
           "How do you alienate the rest of your team with your loner tendencies?",
           "Overcome when doing something different from the rest of your team. Use your Max " + \
           "die. You and each of your allies gain a hero point."]
r_nomad = ["the Nomad",
           "You are far away from home, but you're used to living on the road. You know how " + \
           "to get by on the run.",
           "What problem does your lack of attachments cause?",
           "How have you become lost from your new home?",
           "Overcome a situation where you can apply lessons from the road. Use your Max die. " + \
           "You and each of your allies gain a hero point."]
r_peace = ["Peace",
           "You believe that the ultimate goal of your mission is peace, and that violence is " + \
           "usually not the answer. While not necessarily a pacifist, you can almost always " + \
           "come up with a non-violent solution to problems.",
           "What causes you to lose your calm?",
           "What major issue do you create with your team when you refuse to engage in violence?",
           "Overcome a situation with serenity instead of violence. Use your Max die. You and " + \
           "each of your allies gain a hero point."]
r_rage = ["Rage",
          "They don't like you when you're angry. Your fury is intimidating to many.",
          "What did your anger just mess up?",
          "Who have you thoroughly alienated with your outbursts?",
          "Overcome a situation where you can channel your rage for good. Use your Max die. " + \
          "You and each of your allies gain a hero point."]
r_savagery = ["Savagery",
              "Your wild instincts stay with you and guide your actions. You can survive in " + \
              "the wild and resist the trappings of civilization.",
              "Who did you harm with your rampage?",
              "What major act of collateral damage are you responsible for?",
              "Overcome a situation that taps into your primal nature. Use your Max die. You " + \
              "and each of your allies gain a hero point."]
r_split = ["the Split",
           "You have two (or more) entirely separate facets to your personality. As a result, " + \
           "you can look at a situation from many different angles.",
           "What perspective ended up being the wrong one for this situation?",
           "What inner conflict has completely thrown you off?",
           "Overcome a situation that benefits from having a completely new outlook. Use your " + \
           "Max die. You and each of your allies gain a hero point."]
r_spotless_mind = ["the Spotless Mind",
                   "You have a state of blissful ignorance. Grudges, entanglements, and " + \
                   "commitments slide right off you.",
                   "What slid off you previously that could have been useful right now?",
                   "What major thing did you forget, and why did forgetting it make your " + \
                   "situation much worse?",
                   "Overcome a situation where being free of the past is useful. Use your Max " + \
                   "die. You and each of your allies gain a hero point."]
rc_identity = [r_ambition,
               r_amnesia,
               r_detachment,
               r_discovery,
               r_levity,
               r_loner,
               r_nomad,
               r_peace,
               r_rage,
               r_savagery,
               r_split,
               r_spotless_mind]

global r_business, r_debtor, r_detective, r_double_agent, r_everyman, r_family, r_mask, r_sidekick
global r_team, r_underworld, r_veteran, r_youth, rc_responsibility
r_business = ["Business",
              "You are an entrepreneur- running a business is an important part of your life " + \
              "and your identity. You have a base of operations that you can rely on for support.",
              "You're always looking at the bigger picture. How does that cause friction in " + \
              "the moment with your team?",
              "Your business interests are in danger. Where are your priorities, truly?",
              "Overcome in a situation related to the field of your business or knowing " + \
              "locals. Use your Max die. You and each of your allies gain a hero point."]
r_debtor = ["the Debtor",
            "You owe someone or something more than you can ever repay. You know plenty of " + \
            "folks willing to give out favors, but it'll cost you later.",
            "What potential source of wealth looks mighty tempting right now?",
            "Who has come to collect?",
            "Overcome in a situation related to repaying a debt. Use your Max die. You and " + \
            "each of your allies gain a hero point."]
r_detective = ["the Detective",
               "You can always tell when an important piece of information is being left out " + \
               "or obscured, though you might not know exactly what it is.",
               "What important clue did you miss?",
               "What major secret was just revealed that you would rather had stayed hidden?",
               "Overcome to learn hidden information. Use your Max die. You and each of your " + \
               "allies gain a hero point."]
r_double_agent = ["the Double Agent",
                  "You are loyal to more than one organization, possibly working at cross " + \
                  "purposes. You always cover your tracks.",
                  "What were you just forced to do that seemed strange to your current allies?",
                  "Will you shatter your trust with your current allies or forfeit what your " + \
                  "other allegiance offers?",
                  "Overcome in a situation where you can draw upon resources from your other " + \
                  "organization. Use your Max die. You and each of your allies gain a hero point."]
r_everyman = ["the Everyman",
              "You are just a normal person who has had power thrust upon them or are " + \
              "otherwise in over your head. You don't have the same sense of lofty purpose as " + \
              "other heroes. When needed, you can make yourself just another face in the crowd.",
              "Which hero did you make look good at the expense of yourself?",
              "How are you utterly and totally out of your league?",
              "Overcome when using a bonus made by another hero. Use your Max die. You and " + \
              "each of your allies gain a hero point."]
r_family = ["Family",
            "Your family is an important part of your life. You have relatives in a wide " + \
            "range of fields that you can call upon.",
            "Which member of your family just compromised your mission?",
            "What do you have to give up in your heroic life for the sake of your family?",
            "Overcome in a situation where you have been given advice from a family member. " + \
            "Use your Max die. You and each of your allies gain a hero point."]
r_mask = ["the Mask",
          "It is vitally important that you hide your true identity. You have a career that " + \
          "allows you to slip between identities when necessary.",
          "What clue about your real identity did you leave behind?",
          "Who from your civilian life is now in imminent danger?",
          "Overcome using knowledge from your civilian life. Use your Max die. You and each " + \
          "of your allies gain a hero point."]
r_sidekick = ["the Sidekick",
              "You always seem to be where the trouble is; you're never too far away when a " + \
              "crisis strikes the group you sidekick for.",
              "Which hero has to rescue you from your current predicament?",
              "What serious lesson that you ignored is now getting you into big trouble?",
              "Overcome a challenge that has already flummoxed a more senior teammate. Use " + \
              "your Max die. You and each of your allies gain a hero point."]
r_team = ["the Team",
          "Your heroic team takes up a significant portion of your life and you have an " + \
          "official position in that team. Civilian authorities will recognize your status in " + \
          "the team.",
          "What embarrassment did you just cause as a representative of your team?",
          "What major sanctions will you suffer as a result of your actions?",
          "Overcome by using your status as an official representative. Use your Max die. You " + \
          "and each of your allies gain a hero point."]
r_underworld = ["the Underworld",
                "You have a variety of contacts from the criminal underworld and organized crime.",
                "What shady detail causes others to distrust you?",
                "Are you guilty of what you're being arrested for?",
                "Overcome a problem related to your knowledge of the criminal underworld or " + \
                "using one of your contacts. Use your Max die. You and each of your allies " + \
                "gain a hero point."]
r_veteran = ["the Veteran",
             "You remain clear-headed under intense combat situations.",
             "What affected you emotionally about the current conflict?",
             "How are you withdrawing from the current conflict?",
             "Overcome a tactical challenge using knowledge of a previous conflict. Use your " + \
             "Max die. You and each of your allies gain a hero point."]
r_youth = ["Youth",
           "You have an innocent and cheerful outlook on most things, based on your upbeat " + \
           "personality and general lack of experience. You can slip into many situations " + \
           "that adults would have trouble with.",
           "Who has been put out by your overconfidence?",
           "What person that you would hate to let down is now very disappointed in you?",
           "Overcome a situation where your age or size is an asset. Use your Max die. You " + \
           "and each of your allies gain a hero point."]
rc_responsibility = [r_business,
                     r_debtor,
                     r_detective,
                     r_double_agent,
                     r_everyman,
                     r_family,
                     r_mask,
                     r_sidekick,
                     r_team,
                     r_underworld,
                     r_veteran,
                     r_youth]

global rc_master, rc_names
rc_master = [rc_esoteric, rc_expertise, rc_ideals, rc_identity, rc_responsibility]
rc_names = ["Esoteric", "Expertise", "Ideals", "Identity", "Responsibility"]

# Class representing a Principle
class Principle:
    def __init__(self,
                 category,
                 index,
                 title="",
                 roleplaying="",
                 minor="",
                 major="",
                 green="",
                 stepnum=0):
        self.category = category
        self.index = index
        self.step = max([0, stepnum])
        self.steps_modified = []
        ref = ["[undefined]"] * 5
        self.has_ref = False
        self.is_template = False
        if self.category in range(len(rc_master)):
            r_cat = rc_master[self.category]
            if self.index in range(len(r_cat)):
                ref = rc_master[self.category][self.index]
                self.has_ref = True
                self.is_template = True
        if not title:
            title = ref[0]
        elif title.startswith("Principle of "):
            title = title[13:]
        self.title = title
        if not roleplaying:
            roleplaying = ref[1]
        self.during_roleplaying = roleplaying
        if not minor:
            minor = ref[2]
        self.minor_twist = minor
        if not major:
            major = ref[3]
        self.major_twist = major
        if not green:
            green = ref[4]
        self.green_ability = green
        if self.is_template and (self.title != ref[0] or self.during_roleplaying != ref[1] or \
                                 self.minor_twist != ref[2] or self.major_twist != ref[3] or \
                                 self.green_ability != ref[4]):
            self.is_template = False
        if self.title != ref[0] and self.during_roleplaying != ref[1] and \
           self.minor_twist != ref[2] and self.major_twist != ref[3] and \
           self.green_ability != ref[4]:
            self.has_ref = False
    def __str__(self):
        summary = "Principle of " + self.title
        if self.has_ref and not self.is_template:
            summary += "*"
        return summary
    def display(self,
                prefix="",
                width=100,
                green=True):
        indent = "    "
        printlong("Principle of " + self.title,
                  width=width-len(prefix),
                  prefix=prefix)
        printlong(self.during_roleplaying,
                  width=width-len(prefix+indent),
                  prefix=prefix+indent)
        printlong("Minor Twist: " + self.minor_twist,
                  width=width-len(prefix+indent+indent),
                  prefix=prefix+indent+indent)
        printlong("Major Twist: " + self.major_twist,
                  width=width-len(prefix+indent+indent),
                  prefix=prefix+indent+indent)
        if green:
            printlong("Green Ability: " + self.green_ability,
                      width-len(prefix+indent),
                      prefix=prefix+indent)
    def details(self,
                prefix="",
                width=100,
                green=True,
                breaks=2):
        indent = "    "
        text = split_text("Principle of " + self.title,
                          width=width-len(prefix),
                          prefix=prefix)
        text += "\n" * breaks + split_text(self.during_roleplaying,
                                           width=width-len(prefix+indent),
                                           prefix=prefix+indent)
        text += "\n" * breaks + split_text("Minor Twist: " + self.minor_twist,
                                           width=width-len(prefix+indent+indent),
                                           prefix=prefix+indent+indent)
        text += "\n" * breaks + split_text("Major Twist: " + self.major_twist,
                                           width=width-len(prefix+indent+indent),
                                           prefix=prefix+indent+indent)
        if green:
            text += "\n" * breaks + split_text("Green Ability: " + self.green_ability,
                                               width=width-len(prefix+indent+indent),
                                               prefix=prefix+indent+indent)
        return text

global hp_bounds
hp_bounds = [[17, 13, 6],
             [18, 14, 7],
             [19, 14, 7],
             [20, 15, 7],
             [21, 16, 8],
             [22, 17, 8],
             [23, 18, 8],
             [24, 18, 9],
             [25, 19, 9],
             [26, 20, 9],
             [27, 20, 10],
             [28, 21, 10],
             [29, 22, 10],
             [30, 22, 11],
             [31, 23, 11],
             [32, 24, 11],
             [33, 25, 12],
             [34, 25, 12],
             [35, 26, 12],
             [36, 27, 13],
             [37, 28, 13],
             [38, 28, 13],
             [39, 29, 14],
             [40, 29, 14]]

global bg_upper_class, bg_dynasty, bg_struggling, bg_adventurer, bg_unremarkable
global bg_law_enforcement, bg_academic, bg_tragic, bg_performer, bg_military, bg_retired
global bg_criminal, bg_medical, bg_anachronistic, bg_exile, bg_former_villain, bg_interstellar
global bg_blank_slate, bg_otherworldly, bg_created, bg_collection, bg_width
bg_upper_class = ["Upper Class",
                  "You were born in the upper echelons of society. Likely you're also pretty " + \
                  "darn rich.",
                  [10, 8],
                  [],
                  [[0, 2, 3], [0, 3, 4]] + Category(0,1),
                  4,
                  [10, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Fitness, Persuasion, any Mental
# Principle category: Responsibility
# Power Source dice:  1d10 + 2d8
bg_blank_slate = ["Blank Slate",
                  "You remember nothing. Were you brainwashed? Maybe you were just created? " + \
                  "One way or another, you have no history. You start now. Your future is " + \
                  "what you make of it.",
                  [10, 8],
                  [],
                  Category(0,1) + Category(0,2),
                  3,
                  [10, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    any Mental, any Physical
# Principle category: Identity
# Power Source dice:  1d10 + 2d8
bg_struggling = ["Struggling",
                 "You've been down and out. Perhaps you've recovered a bit, but you also " + \
                 "might still be stuck in a terrible situation. Low on resources and luck, " + \
                 "you did your best, but it often just wasn't good enough.",
                 [8, 6, 6],
                 [],
                 [[0, 3, 0], [0, 0, 0]] + Category(0,2),
                 4,
                 [8, 8, 6]]
# Quality dice:       1d8 + 2d6
# Required Qualities: none
# Quality options:    Banter, Criminal Underworld Info, any Physical
# Principle category: Responsibility
# Power Source dice:  2d8 + 1d6
bg_adventurer = ["Adventurer",
                 "In your past, you have sought excitement and adventure at every turn. Even " + \
                 "before you were a hero, you were a thrill seeker.",
                 [10, 8],
                 [],
                 [[0, 0, 2], [0, 3, 3]] + Category(0,2),
                 1,
                 [8, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    History, Leadership, any Physical
# Principle category: Expertise
# Power Source dice:  3d8
bg_unremarkable = ["Unremarkable",
                   "You were just a regular person, leading a normal life, until something " + \
                   "came along and changed your life in a major way. You came from a " + \
                   "commonplace background, but now you're a hero.",
                   [10, 8],
                   [],
                   [[0, 2, 1]] + Category(0,1) + Category(0,3),
                   3,
                   [10, 8, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Close Combat, any Mental, any Social
# Principle category: Identity
# Power Source dice:  1d10 + 1d8 + 1d6
bg_law_enforcement = ["Law Enforcement",
                      "You're a member of law enforcement, such as a beat cop, detective, or " + \
                      "perhaps a lawyer or judge. You made a career of the law at one point. " + \
                      "Perhaps you still do.",
                      [10, 8],
                      [],
                      [[0, 2, 1], [0, 0, 0], [0, 2, 4]] + Category(0,1) + Category(0,3),
                      4,
                      [10, 8, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Close Combat, Criminal Underworld Info, Ranged Combat, any Mental, any Social
# Principle category: Responsibility
# Power Source dice:  1d10 + 1d8 + 1d6
bg_academic = ["Academic",
               "You work or study in a field of knowledge. You could be a school teacher, " + \
               "professor, researcher, or clergy member. The pursuit of knowledge is very " + \
               "important to you, and possibly what led you to become a hero.",
               [12, 8],
               [],
               [[0, 3, 3], [0, 1, 4]] + Category(0,0),
               1,
               [10, 8]]
# Quality dice:       1d12 + 1d8
# Required Qualities: none
# Quality options:    Leadership, Self-Discipline, any Information
# Principle category: Expertise
# Power Source dice:  1d10 + 1d8
bg_tragic = ["Tragic",
             "Your history is eclipsed by a major negative event that shaped the rest of your " + \
             "life. You struggle to overcome the memory of the tragic event, be it the loss " + \
             "of a loved one or something that happened to you directly. Either way, the " + \
             "tragedy both fuels and haunts you.",
             [10, 8],
             [],
             [[0, 3, 0], [0, 2, 1], [0, 3, 1]] + Category(0,1),
             2,
             [10, 10, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Banter, Close Combat, Imposing, any Mental
# Principle category: Ideals
# Power Source dice:  2d10 + 1d6
bg_performer = ["Performer",
                "You were born for the stage. How you present yourself to the world is " + \
                "important to you, whether in or out of the limelight.",
                [10, 8],
                [],
                [[0, 2, 0], [0, 1, 2], [0, 2, 2]] + Category(0,3),
                4,
                [10, 8, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Acrobatics, Creativity, Finesse, any Social
# Principle category: Responsibility
# Power Source dice:  1d10 + 1d8 + 1d6
bg_military = ["Military",
               "You have some sort of combat training, possibly as part of an organized armed " + \
               "forces. You might have even had combat experience before you became a hero.",
               [10, 8],
               [],
               [[0, 3, 3], [0, 1, 4]] + Category(0,2),
               2,
               [10, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Leadership, Self-Discipline, any Physical
# Principle category: Ideals
# Power Source dice:  1d10 + 2d8
bg_retired = ["Retired",
              "You used to wear the cape and cowl, but hung them up long ago. Now, something " + \
              "has changed, making you feel compelled to once again take up the fight for " + \
              "what is right. You never thought you would be here again.",
              [10, 10],
              [],
              Category(0,0) + Category(0,3),
              3,
              [12, 6, 6]]
# Quality dice:       2d10
# Required Qualities: none
# Quality options:    any Information, any Social
# Principle category: Identity
# Power Source dice:  1d12 + 2d6
bg_criminal = ["Criminal",
               "You spent too much time on the wrong side of the law. But something changed " + \
               "for you. Now you've turned over a new leaf, using your powers and abilities " + \
               "to be the best hero you can.",
               [10, 8],
               [],
               [[0, 0, 0], [0, 3, 1]] + Category(0,2),
               1,
               [8, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Criminal Underworld Info, Imposing, any Physical
# Principle category: Expertise
# Power Source dice:  3d8
bg_medical = ["Medical",
              "You were in the business of healing, as a doctor or nurse or maybe even a " + \
              "veterinarian. Given your medical background, you have a lot of experience with " + \
              "treating injuries and diseases.",
              [10, 8, 6],
              [[0, 0, 4]],
              [[0, 2, 2], [0, 0, 6], [0, 0, 7]] + Category(0,1),
              1,
              [10, 8, 8]]
# Quality dice:       1d10 + 1d8 + 1d6
# Required Qualities: Medicine
# Quality options:    Finesse, Science, Technology, any Mental
# Principle category: Expertise
# Power Source dice:  1d10 + 2d8
bg_anachronistic = ["Anachronistic",
                    "One way or another, you aren't quite in your time. You could be a " + \
                    "stranded time traveler, or just a person who fits more with the ideals " + \
                    "and customs of a time long before or after the one in which you " + \
                    "currently reside. Either way, though this time is not your own, you " + \
                    "still fight to protect it.",
                    [10, 8],
                    [],
                    [[0, 0, 2], [0, 0, 3], [0, 0, 7]] + Category(0,2),
                    0,
                    [10, 8, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    History, Magical Lore, Technology, any Physical
# Principle category: Esoteric
# Power Source dice:  1d10 + 1d8 + 1d6
bg_exile = ["Exile",
            "You're far from your home, one way or another. You may have left of your own " + \
            "accord, but it's equally likely that you were sent away from whatever place you " + \
            "came from. Either way, you're making your own way in the land where you now live.",
            [10, 8],
            [],
            [[0, 1, 1], [0, 3, 2]] + Category(0,0),
            2,
            [8, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Conviction, Insight, any Information
# Principle category: Ideals
# Power Source dice:  3d8
bg_former_villain = ["Former Villain",
                     "You used to be a foe to the heroes, but you've changed your stripes. " + \
                     "You may have realized the evil of your former ways, or your motivation " + \
                     "might have changed to ally you with those you once fought. Either way, " + \
                     "you are now a hero, though many other heroes are hesitant to trust you.",
                     [10, 8],
                     [],
                     [[0, 1, 1]] + Category(0,0) + Category(0,3),
                     1,
                     [10, 8, 8]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Conviction, any Information, any Social
# Principle category: Expertise
# Power Source dice:  1d10 + 2d8
bg_interstellar = ["Interstellar",
                   "You come from beyond the stars! As a newcomer to planet Earth, you may be " + \
                   "unaware of the strange customs here, but you can still communicate with " + \
                   "Earthlings, one way or another. You might be an alien, or a human from a " + \
                   "civilization lost in space long ago, or something else entirely.",
                   [12, 6],
                   [],
                   Category(0,0) + Category(0,1),
                   0,
                   [10, 8, 6]]
# Quality dice:       1d12 + 1d6
# Required Qualities: none
# Quality options:    any Information, any Mental
# Principle category: Esoteric
# Power Source dice:  1d10 + 1d8 + 1d6
bg_dynasty = ["Dynasty",
              "You come from a line of heroes. It could be that your parents and their " + \
              "parents and their parents have all been heroes. Maybe you're adopted into a " + \
              "hero family. Regardless of how you came to be a part of this dynasty, heroism " + \
              "is part of your life.",
              [10, 10],
              [],
              [[0, 2, 1], [0, 2, 3], [0, 0, 2]] + Category(0,3),
              2,
              [8, 8, 6]]
# Quality dice:       2d10
# Required Qualities: none
# Quality options:    Close Combat, Fitness, History, any Social
# Principle category: Ideals
# Power Source dice:  2d8 + 1d6
bg_otherworldly = ["Otherworldly",
                   "You have at least a little of the uncanny in you. You could be a fully " + \
                   "supernatural creature or perhaps the spawn of one and a human.",
                   [10, 8],
                   [],
                   [[0, 0, 3], [0, 0, 5]] + Category(0,1),
                   0,
                   [10, 6, 6]]
# Quality dice:       1d10 + 1d8
# Required Qualities: none
# Quality options:    Magical Lore, Otherworldly Mythos, any Mental
# Principle category: Esoteric
# Power Source dice:  1d10 + 2d6
bg_created = ["Created",
              "Were you built to be the hero you are today? Perhaps. But it's undeniable that " + \
              "you were created by someone or something. As a constructed being, you don't " + \
              "have the same experiences or expectations as similar organic creatures, but " + \
              "you still feel drawn to the role of hero.",
              [12, 6],
              [],
              [[0, 1, 0], [0, 0, 6], [0, 0, 7]] + Category(0,2),
              1,
              [10, 10, 6]]
# Quality dice:       1d12 + 1d6
# Required Qualities: none
# Quality options:    Alertness, Science, Technology, any Physical
# Principle category: Expertise
# Power Source dice:  2d10 + 1d6
bg_collection = [bg_upper_class,
                 bg_blank_slate,
                 bg_struggling,
                 bg_adventurer,
                 bg_unremarkable,
                 bg_law_enforcement,
                 bg_academic,
                 bg_tragic,
                 bg_performer,
                 bg_military,
                 bg_retired,
                 bg_criminal,
                 bg_medical,
                 bg_anachronistic,
                 bg_exile,
                 bg_former_villain,
                 bg_interstellar,
                 bg_dynasty,
                 bg_otherworldly,
                 bg_created]
bg_width = 100

# Options to insert into an ability's text
global basic_actions, status_zones, damage_categories
basic_actions = ["Attack", "Defend", "Boost", "Hinder", "Overcome"]
status_zones = ["Green", "Yellow", "Red", "Out"]
damage_categories = ["physical", "energy", "[physical or energy]"]

def Actions(action_ids):
    action_list = "["
    for i in range(len(action_ids)-1):
        action_list += basic_actions[action_ids[i]] + " or "
    action_list += basic_actions[action_ids[len(action_ids)-1]] + "]"
    return action_list

class Ability:
    def __init__(self,
                 name,
                 subtype,
                 main_text,
                 z_num,
                 f_name="",
                 die_names=["",""],
                 pq_reqs=[],
                 pq_opts=[],
                 pq_ids=[],
                 element_id=99,
                 actions=[99,99],
                 action_choices=[],
                 categories=[2,2],
                 damage_id=99,
                 energy=False,
                 hero_step=0):
        # name -> self.name: The rulebook-specified base name for this Ability.
        # subtype -> self.type: A for Action, I for Inherent, R for Reaction
        # main_text -> self.text: The game text of this Ability, with user-specified sections
        #  replaced with placeholders
        # z_num -> self.zone: -1 for unspecified, 0 for Green, 1 for Yellow, 2 for Red, 3 for Out
        # f_name -> self.flavorname: the user-specified custom name for this Ability
        # die_names -> self.flavordice: 2 strings containing any user-specified custom names for
        #     the Power/Quality dice used in this Ability
        #     Only kept if the relevant pq_ids are specified
        # categories -> self.required_categories: 2 ints identifying each power/quality die's
        #  category: 0 for Quality, 1 for Power, 2 for either
        # pq_reqs -> self.required_pqs: <=2 sets of triplets identifying powers and/or qualities
        #     required to add this Ability
        #     NOTE: these powers/qualities may not necessarily appear in the ability text... BUT
        #     any powers/qualities that appear in the ability text should also appear in this list,
        #     if it exists
        # pq_opts -> self.pq_options: <=2 sets of triplets identifying options from which the
        #     respective pq_ids can be chosen
        # pq_ids -> self.insert_pqs: <=2 triplets identifying powers/qualities used in the ability
        #     text
        #     NOTE: pq_ids overrules pq_opts,
        #           pq_opts overrules pq_reqs,
        #           pq_opts overrules categories
        # element_id -> self.insert_element: int identifying an element/energy (from
        #     mixed_collection[1][1]: Elemental/Energy Powers) used in the ability text
        #     99 for none, -1 for unspecified
        # actions -> self.insert_actions: <=2 ints identifying a basic action (from basic_actions)
        #     -1 for unspecified
        # action_choices -> self.action_options: <=2 lists of ints identifying basic action options
        # damage_id -> self.insert_damage: int identifying damage type:
        #     0 for physical, 1 for energy, -1 for unspecified
        # energy -> self.requires_energy: True if the ability requires the hero to have an
        #     Elemental/Energy power matching the element in the ability text; False otherwise
        # hero_step -> self.step: the number of the step of hero creation (1-7) at which this
        #     ability was added
        self.zone = -1
        self.insert_element = 99
        self.insert_pqs = []
        self.insert_damage = damage_id
        self.has_pq = False
        self.has_element = False
        self.has_actions = False
        self.has_damage = False
        self.requires_energy = energy
        self.step = max([0, hero_step])
        self.steps_modified = []
        self.prev_version = None
        self.required_categories = [2,2]
        # Validate z_num
        if -1 <= z_num <= 3:
            self.zone = z_num
        else:
            print("Error! " + str(z_num) + " is not a valid status zone")
            return
        # Validate subtype
        self.type = ""
        if subtype in "AIR":
            self.type = subtype
        else:
            print("Error! " + str(subtype) + " is not a valid ability type")
            return
        self.name = name
        self.text = main_text
        if "%p" in self.text:
            self.has_pq = True
        if "%a" in self.text:
            self.has_actions = True
        if "%e" in self.text:
            self.has_element = True
        if "%d" in self.text:
            self.has_damage = True
        self.flavorname = f_name
        if not self.flavorname:
            self.flavorname = self.name
        self.flavordice = ["", ""]
        # Validate the entries in categories
        for i in range(len(categories)):
            c = categories[i]
            if c in [0,1,2]:
                if i in range(len(self.required_categories)):
                    self.required_categories[i] = c
            else:
                print("Error! " + str(c) + " is not a valid die category")
                return
        # Validate the entries in pq_ids, add the valid ones to self.insert_pqs
        self.insert_pqs = [[], []]
        if pq_ids:
            self.has_pq = True
            for i in range(len(pq_ids)):
                triplet = pq_ids[i]
                if len(triplet) == 3:
                    if triplet[0] in range(len(mixed_collection)):
                        if triplet[1] in range(len(mixed_collection[triplet[0]])):
                            if triplet[2] in range(len(mixed_collection[triplet[0]][triplet[1]])):
                                # triplet refers to an existing power/quality
                                self.insert_pqs[i] = triplet
                                if len(die_names) >= i:
                                    if die_names[i] != "":
                                        self.flavordice[i] = die_names[i]
        # Validate the entries in pq_opts, add the valid ones to self.pq_options
        self.pq_options = [[], []]
        for i in range(len(pq_opts)):
            for triplet in pq_opts[i]:
                if triplet[0] in range(len(mixed_collection)):
                    if triplet[1] in range(len(mixed_collection[triplet[0]])):
                        if triplet[2] in range(len(mixed_collection[triplet[0]][triplet[1]])):
                            # triplet refers to an existing power/quality
                            self.pq_options[i].append(triplet)
            # After adding the specified options, make sure the known powers/qualities are also
            #  present
            if self.insert_pqs[i] not in self.pq_options[i] and \
               len(self.pq_options[i]) > 0 and len(self.insert_pqs[i]) > 0:
                print("Specified power/quality " + str(self.insert_pqs[i]) + \
                      " not in option list " + str(self.pq_options[i]) + ". Expanding options.")
                self.pq_options[i].append(self.insert_pqs[i])
        # Validate the entries in pq_reqs, add the valid ones to self.required_pqs
        self.required_pqs = [[], []]
        for i in range(len(pq_reqs)):
            for triplet in pq_reqs[i]:
                if triplet[0] in range(len(mixed_collection)):
                    if triplet[1] in range(len(mixed_collection[triplet[0]])):
                        if triplet[2] in range(len(mixed_collection[triplet[0]][triplet[1]])):
                            # triplet refers to an existing power/quality
                            self.required_pqs[i].append(triplet)
            # After adding the specified requirements, also add the known in-text options
            for triplet in self.pq_options[i]:
                if len(triplet) == 3:
                    if triplet not in self.required_pqs[i]:
                        print("Specified power/quality option " + str(triplet) + \
                              " not in requirement set " + str(self.required_pqs[i]) + \
                              ". Expanding requirement set.")
                        self.required_pqs[i].append(triplet)
                        self.required_pqs[i].append(triplet)
                    # Also make sure that required_categories is expanded to include these options
                    if self.required_categories[i] not in [2, triplet[0]]:
                        print("Specified power/quality option " + str(triplet) + \
                              " not in category " + str(self.required_categories[i]) + \
                              ". Expanding category.")
                        self.required_categories[i] = 2
        # Validate element_id: if it's valid, save it to insert_element; if it's unspecified, note
        #  that an element is required
        if element_id in range(len(mixed_collection[1][1])):
            self.has_element = True
            self.insert_element = element_id
            if self.requires_energy and [1, 1, self.insert_element] not in self.required_pqs[0]:
                print("Specified element/energy [1, 1, " + self.insert_element + \
                      "] is required as a Power but not in requirement set " + \
                      str(self.required_pqs[0]) + ". Expanding requirement set.")
                self.required_pqs[0].append([1,1,self.insert_element])
        elif element_id == -1:
            self.has_element = True
        # Validate action_choices, add the valid ones to self.action_options
        self.insert_actions = [99, 99]
        self.action_options = [[],[]]
        if action_choices != []:
            for i in range(len(action_choices)):
                subset = action_choices[i]
                v_subset = []
                for action_id in subset:
                    if action_id in range(len(basic_actions)):
                        v_subset.append(action_id)
                if len(v_subset) == 0 and len(subset) > 0:
                    print("Error! None of " + str(subset) + " are valid basic action identifiers")
                    return
                elif len(v_subset) == 1:
                    self.insert_actions[i].append(v_subset[0])
                    self.action_options[i] = self.action_options[i] + v_subset
                else:
                    self.action_options[i] = self.action_options[i] + v_subset
        elif self.has_actions:
            # has_actions is true but no action_choices were specified
            # all basic actions are valid, but only for indices that appear in the text
            for i in [0,1]:
                if ("%a" + str(i)) in self.text:
                    self.action_options[i] = [x for x in range(len(basic_actions))]
        # Validate actions, add the valid ones to self.insert_actions
        if actions:
            for i in range(len(actions)):
                if actions[i] in range(len(basic_actions)):
                    if i in range(len(self.action_options)):
                        # Valid action, valid index. Save it.
                        self.insert_actions[i] = actions[i]
                        # Check this entry in actions against the matching requirement entry
                        if actions[i] not in self.action_options[i] and actions[i] != 99:
                            print("Specified basic action " + basic_actions[actions[i]] + \
                                  " not found in option set " + Actions(self.action_options[i]) + \
                                  ". Expanding options.")
                            self.action_options[i].append(actions[i])
    def __str__(self):
        summary = self.name
        if self.flavorname:
            summary = self.flavorname
        summary += " (" + self.type + ")"
        return summary
    def display(self, prefix="", width=100):
        # Prints a list of the ability's attributes.
        pref = prefix
        indent = "    "
        firstline = ""
        if self.zone != 3:
            # Out Abilities don't get names when displayed like this.
            # The only time an Out Ability needs a name is when a Divided hero chooses between two
            #  of them.
            if self.flavorname:
                firstline = self.flavorname
            else:
                firstline = self.name
        if len(firstline) > 0:
            firstline += " "
        firstline += "[" + self.type + "]"
        if self.zone in range(len(status_zones)):
            firstline += " (" + status_zones[self.zone] + ")"
        print(pref + firstline)
        printlong(self.dispText(), width-4, prefix=pref+indent)
    def details(self, width=100, prefix=""):
        fullText = "" + prefix
        if self.zone != 3:
            if self.flavorname:
                fullText += self.flavorname
            else:
                fullText += self.name
            fullText += " "
        fullText += "[" + self.type + "]"
        if self.zone in range(len(status_zones)):
            fullText += " (" + status_zones[self.zone] + ")"
        fullText += "\n" + split_text(self.dispText(), width=width, prefix=prefix+"    ")
        return fullText
    def dispText(self):
        disptext = self.text
        if self.has_element:
            if self.insert_element in range(len(mixed_collection[1][1])):
                disptext = disptext.replace("%e", mixed_collection[1][1][self.insert_element])
            elif self.requires_energy:
                disptext = disptext.replace("%e", "[energy/element you have a related power for]")
            else:
                disptext = disptext.replace("%e", "[energy/element]")
        if self.has_damage:
            if self.insert_damage in [-1,0,1]:
                disptext = disptext.replace("%d", damage_categories[self.insert_damage])
            else:
                disptext = disptext.replace("%d", damage_categories[2])
        for i in [0,1]:
            # If we have a specified power/quality for index i, replace "%p[i]" with that
            if self.insert_pqs[i]:
                # Use the custom name for the die if there is one, otherwise use MixedPQ to get the
                #  default name
                if self.flavordice[i] != "":
                    disptext = disptext.replace("%p" + str(i), self.flavordice[i])
                else:
                    disptext = disptext.replace("%p" + str(i), MixedPQ(self.insert_pqs[i]))
            # If we have a specified basic action for index i, replace "%a[i]" with that
            # If we don't have a specified basic action, and the list of basic action options is
            #  the same as the list of all basic actions, use a placeholder for that instead of
            #  listing all five
            # If we don't have a specified basic action but we DO have a list of basic action
            #  OPTIONS, replace "%a[i]" with that instead
            if self.insert_actions[i] in range(len(basic_actions)):
                disptext = disptext.replace("%a" + str(i),
                                            basic_actions[self.insert_actions[i]])
            elif self.action_options[i] == [0,1,2,3,4]:
                disptext = disptext.replace("%a" + str(i),
                                            "[basic action " + str(i+1) + "]")
            elif self.action_options[i]:
                disptext = disptext.replace("%a" + str(i), Actions(self.action_options[i]))
        # Replace any remaining "%p" entries with the name of the relevant category enclosed in
        #  brackets.
        if "%p" in disptext:
            disptext = disptext.replace("%p0",
                                        "[" + categories_singular[self.required_categories[0]] + \
                                        "]")
            if self.required_categories[0] == self.required_categories[1]:
                disptext = disptext.replace("%p1",
                                            "[other " + \
                                            categories_singular[self.required_categories[1]] + "]")
            else:
                disptext = disptext.replace("%p1",
                                            "[" + \
                                            categories_singular[self.required_categories[1]] + "]")
        return disptext
    def copy(self):
        mirror = Ability(self.name,
                         self.type,
                         self.text,
                         self.zone,
                         f_name=self.flavorname,
                         pq_reqs=self.required_pqs,
                         pq_opts=self.pq_options,
                         pq_ids=self.insert_pqs,
                         element_id=self.insert_element,
                         actions=self.insert_actions,
                         action_choices=self.action_options,
                         categories=self.required_categories,
                         damage_id=self.insert_damage,
                         energy=self.requires_energy,
                         hero_step=self.step)
        mirror.steps_modified = [x for x in self.steps_modified]
        if self.prev_version:
            mirror.prev_version = self.prev_version.copy()
        return mirror
    def SetPrevious(self, stepnum):
        # Used in preparation for editing the Ability's characteristics during character creation.
        # Creates a copy of the Ability with its current attributes and saves it in
        #  self.prev_version, then adds the specified step number to the list of steps when this
        #  Ability was modified.
        self.prev_version = self.copy()
        self.steps_modified.append(stepnum)
    def RetrievePrior(self, stepnum):
        # Returns a copy of the Ability as it existed prior to the specified step of character
        #  creation.
        if stepnum < 1:
            print("Error! " + str(stepnum) + " is too small to be a valid step index.")
            return self
        ancestor = self.copy()
        while len(ancestor.steps_modified) > 0:
            if max(ancestor.steps_modified) >= stepnum:
                ancestor = ancestor.prev_version
            else:
                return ancestor
        return ancestor

# Power Sources...
# Accident Abilities
global a_area_alteration, a_inflict, a_reflexive_burst, a_ambush_awareness
global a_change_in_circumstance, a_immunity
# Training Abilities
global a_always_be_prepared, a_reactive_field, a_flowing_fight
# Genetic Abilities
global a_danger_sense, a_adaptive, a_area_assault, a_growth, a_rally
# Experimentation Abilities
global a_personal_upgrade, a_misdirection, a_throw_minion, a_overpower, a_unflagging
# Mystical Abilities
global a_modification_wave, a_mystic_redirection, a_sever_link
# Nature Abilities
global a_call_to_the_wild, a_predators_eye, a_wild_strength, a_natural_weapon
# Relic Abilities
global a_harvest_life_force, a_magical_shield, a_momentary_power, a_relic_drain, a_draw_power
global a_punishment
# Powered Suit Abilities
global a_energy_converter, a_explosive_attack, a_onboard_upgrade, a_damage_reduction
global a_diagnostic_subroutine
# Radiation Abilities
global a_radioactive_recharge, a_unstable_reaction, a_wither, a_charged_up, a_dangerous_lash
global a_radioactive_aura
# Tech Upgrades Abilities
global a_energy_burst, a_recharge, a_techno_absorb, a_tactical_analysis
global a_indiscriminate_fabrication, a_organi_hack
# Supernatural Abilities
global a_area_healing, a_mass_modification, a_reach_through_veil
# Artificial Being Abilities
global a_created_immunity, a_multiple_assault, a_recalculating, a_created_form, a_intentionality
# Cursed Abilities
global a_attunement, a_costly_strength, a_cursed_resolve, a_double_edged_luck, a_extremes
# Alien Abilities
global a_alien_boost, a_empower_and_repair, a_halt
# Genius Abilities
global a_a_plan_for_everything, a_expanded_mind, a_overwhelming_vision
# Cosmos Abilities
global a_cosmic_ray_absorption, a_encourage, a_mass_adjust
# Extradimensional Abilities
global a_absorb_essence, a_aura_of_pain, a_bizarre_strike, a_attune, a_extrasensory_awareness
# Unknown Abilities
global a_brainstorm, a_strange_enhancement, a_volatile_creations
# Higher Power Abilities
global a_command_power, a_dangerous_explosion, a_embolden, a_resolve, a_resilience, a_twist_reality
# The Multiverse Abilities
global a_power_from_beyond, a_respond_in_kind, a_dread_pallor, a_reality_scorned
# Archetypes...
# Speedster Abilities
global a_always_on_the_move, a_fast_fingers, a_non_stop_assault, a_blinding_strike
global a_flurry_of_fists, a_supersonic_streak, a_speedy_analysis
# Shadow Abilities
global a_sabotage, a_shadowy_figure
global a_untouchable, a_overcome_from_the_darkness, a_diversion
# Physical Powerhouse Abilities
global a_damage_resistant, a_frontline_fighting, a_galvanize, a_power_strike, a_strength_in_victory
# Marksman Abilities
global a_dual_wielder, a_load, a_precise_shot, a_spin_and_shoot, a_sniper_aim, a_called_shot
global a_exploding_ammo, a_hair_trigger_reflexes, a_ricochet
# Blaster Abilities
global a_exploit_vulnerability, a_disabling_blast, a_danger_zone, a_precise_hit, a_energy_immunity
global a_heedless_blast, a_imbue_with_element
# Close Quarters Combatant Abilities
global a_defensive_strike, a_dual_strike, a_flexible_stance, a_offensive_strike, a_precise_strike
global a_throw_minion2
# Armored Abilities
global a_armored, a_deflect, a_dual_offense, a_living_bulwark, a_repair, a_unstoppable_charge
# Flier Abilities
global a_aerial_bombardment, a_aerial_surveillance, a_barrel_roll, a_dive_and_drop, a_sonic_boom
global a_strike_and_swoop
# Elemental Manipulator Abilities
global a_backlash, a_external_combustion, a_energy_conversion, a_focused_apparatus, a_damage_spike
global a_energy_alignment, a_energy_redirection, a_live_dangerously
# Robot/Cyborg Abilities
global a_adaptive_programming, a_metal_skin, a_living_arsenal, a_self_improvement
global a_something_for_everyone
# Sorcerer Abilities
global a_banish, a_energy_jaunt, a_powerful_blast, a_subdue, a_cords_of_magic, a_field_of_energy
global a_living_bomb
# Psychic Abilities
global a_psychic_assault, a_psychic_coordination, a_psychic_insight, a_astral_projection
global a_illusionary_double, a_minion_suggestion, a_precognitive_alteration
global a_postcognitive_understanding, a_psychic_analysis, a_swarm, a_telekinetic_assault
global a_telepathic_whammy
# Transporter Abilities
global a_displacement_assault, a_hit_and_run, a_mobile_dodge, a_mobile_assist, a_run_down
# Minion-Maker Abilities
global a_make_minion, a_power_up, a_minion_formation, a_rapid_deployment, a_upgrade_minion
global a_construction_focus, a_swarm_combat, a_sacrifice
# Wild Card Abilities
global a_gimmick, a_multitask, a_surprise_results, a_unknown_results, a_break_the_4th, a_danger
global a_expect_the_unexpected, a_imitation, a_turn_the_tables
# Form-Changer Abilities
global a_change_forms, a_form_recovery, a_surprise_shift, a_clever_form, a_miniscule_form
global a_strong_form, a_tough_form, a_tricky_form, a_weird_form, a_agile_form, a_regenerating_form
global a_speedy_form, a_towering_form, a_emergency_change
# Gadgeteer Abilities
global a_analyze_probabilities, a_analyze_weakness, a_equip, a_helpful_invention
global a_helpful_analysis, a_snap_decision
# Reality Shaper Abilities
global a_negative_likelihood, a_not_quite_right, a_probability_insight, a_warp_space
global a_alternate_outcome, a_never_happened, a_retroactive_rewrite
# Divided Abilities
global a_transform, a_device_transform, a_merge, a_possess_person, a_possess_object
global a_uncontrolled_transform, a_divided_psyche, a_split_form
# Modular Abilities
global a_switch, a_quick_switch, a_emergency_switch, a_debilitator, a_improvement, a_scout
global a_analysis, a_bombardment, a_regeneration, a_skirmish, a_stalwart, a_destroyer
global a_hunter_killer, a_shield
# Out Abilities (from Personalities)
global a_out_pboost, a_out_qboost, a_out_rboost, a_out_reaction, a_out_pdefend, a_out_qdefend
global a_out_qhinder_plus, a_out_phinder, a_out_qhinder, a_out_remove, a_out_reroll
# Red Abilities...
# Athletic Red Abilities
global a_major_regeneration, a_paragon_feat, a_push_your_limits, a_reactive_strike
# Elemental/Energy Red Abilities
global a_charged_up_blast, a_eruption, a_improved_immunity, a_powerful_strike, a_purification
global a_summoned_allies
# Hallmark Red Abilities
global a_quick_exit, a_sacrificial_ram, a_ultimate_weaponry
# Intellectual Red Abilities
global a_calculated_dodge, a_give_time, a_reliable_aptitude, a_unerring_strike
# Materials Red Abilities
global a_field_of_hazards, a_impenetrable_defense, a_like_the_wind
# Mobility Red Abilities
global a_heroic_interruption, a_intercession, a_take_down, a_untouchable_movement
# Psychic Red Abilities
global a_dangerous_hinder, a_dire_control, a_final_wrath, a_impossible_knowledge
# Self Control Red Abilities
global a_change_self, a_empowerment, a_defensive_deflection, a_mutable_form, a_resurrection
# Technological Red Abilities
global a_combustion, a_full_defensive, a_unload
# Information Red Abilities
global a_critical_eye, a_discern_weakness, a_specialized_info
# Mental Red Abilities
global a_aware_response, a_canny_awareness, a_considered_planning, a_harmony
# Physical Red Abilities
global a_book_it, a_endurance_fighting, a_finishing_blow, a_reactive_defense
# Social Red Abilities
global a_heroic_sacrifice, a_inspiring_totem, a_lead_by_example, a_ultimatum
global a_width
a_area_alteration = Ability("Area Alteration",
                            "A",
                            "%a0 any number of nearby targets using %p0. Use your Max die.",
                            1,
                            action_choices=[[2, 3]],
                            categories=[1,2])
a_inflict = Ability("Inflict",
                    "A",
                    "Attack using %p0. Hinder that same target using your Min die.",
                    1,
                    categories=[1,2])
a_reflexive_burst = Ability("Reflexive Burst",
                            "R",
                            "When your personal zone changes, Attack all close enemy targets " + \
                            "by rolling your single %p0 die.",
                            1,
                            categories=[1,2])
a_ambush_awareness = Ability("Ambush Awareness",
                             "R",
                             "If you haven't yet acted in an action scene, you may Defend " + \
                             "against an Attack by rolling your single %p0 die.",
                             0,
                             categories=[1,2])
a_change_in_circumstance = Ability("Change in Circumstance",
                                   "R",
                                   "When you change your personal zones, you may Boost by " + \
                                   "rolling your single %p0 die.",
                                   0,
                                   categories=[1,2])
a_immunity = Ability("Immunity",
                     "I",
                     "You do not take damage from %e.",
                     0)
a_always_be_prepared = Ability("Always Be Prepared",
                               "A",
                               "Boost yourself using %p0. Use your Max die. That bonus is " + \
                               "persistent and exclusive. Then, Attack using your Min die. " + \
                               "You may use the bonus you just created on that Attack.",
                               1,
                               categories=[1,2])
a_reactive_field = Ability("Reactive Field",
                          "R",
                          "When you are attacked by a nearby enemy, the attacker also takes " + \
                          "an equal amount of damage.",
                          1)
a_flowing_fight = Ability("Flowing Fight",
                          "A",
                          "Attack using %p0. Use your Mid die to Attack one extra target for " + \
                          "each bonus you have. Apply a different bonus to each Attack.",
                          1,
                          categories=[1,2])
a_danger_sense = Ability("Danger Sense",
                         "R",
                         "When damaged by an environment target or a surprise Attack, Defend " + \
                         "by rolling your single %p0 die.",
                         1,
                         categories=[1,2])
a_adaptive = Ability("Adaptive",
                     "A",
                     "Boost yourself using %p0, then either remove a penalty on yourself or " + \
                     "Recover using your Min die.",
                     1,
                     categories=[1,2])
a_area_assault = Ability("Area Assault",
                         "A",
                         "Attack multiple targets using %p0, using your Min die against each.",
                         1,
                         categories=[1,2])
a_growth = Ability("Growth",
                   "A",
                   "Boost yourself using %p0. That bonus is persistent and exclusive.",
                   0,
                   categories=[0,2])
a_rally = Ability("Rally",
                  "A",
                  "Attack using %p0. Other nearby heroes in the Yellow or Red zone Recover " + \
                  "equal to your Min die.",
                  0,
                  categories=[0,2])
a_personal_upgrade = Ability("Personal Upgrade",
                             "A",
                             "Boost yourself using %p0. Use your Max die. That bonus is " + \
                             "persistent and exclusive.",
                             1,
                             categories=[1,2])
a_misdirection = Ability("Misdirection",
                         "R",
                         "When a nearby hero in the Yellow or Red zone would take damage, " + \
                         "Defend against that damage by rolling your single %p0 die, then " + \
                         "redirect any remaining damage to a nearby minion of your choice.",
                         1,
                         categories=[1,2])
a_throw_minion = Ability("Throw Minion",
                         "A",
                         "Attack a minion using %p0. The result of that minion's save Attacks " + \
                         "another target of your choice.",
                         1,
                         categories=[1,2])
a_overpower = Ability("Overpower",
                      "I",
                      "Whenever you are Boosted, increase that bonus by +1. Then, if that " + \
                      "bonus is +5 or higher, take damage equal to that bonus and remove it.",
                      0)
a_unflagging = Ability("Unflagging",
                       "I",
                       "At the start of your turn, remove a penalty on yourself.",
                       0)
a_modification_wave = Ability("Modification Wave",
                              "A",
                              "Boost or Hinder using %p0, and apply that mod against multiple " + \
                              "nearby targets.",
                              1,
                              categories=[1,2])
a_mystic_redirection = Ability("Mystic Redirection",
                               "R",
                               "When another hero in the Yellow or Red zone would take " + \
                               "damage, you may redirect it to yourself and Defend against it " + \
                               "by rolling your single %p0 die.",
                               1,
                               categories=[1,2])
a_sever_link = Ability("Sever Link",
                       "A",
                       "Overcome an environmental challenge using %p0. Use your Max die. " + \
                       "Either remove any penalty in the scene or Boost equal to your Mid die.",
                       1,
                       categories=[1,2])
a_call_to_the_wild = Ability("Call to the Wild",
                             "A",
                             "Gain a d8 minion. It takes its turn before yours, but goes away " + \
                             "at the end of the scene. You may only have one such minion at a " + \
                             "time.",
                             1)
a_predators_eye = Ability("Predator's Eye",
                          "A",
                          "Attack using %p0. Use your Max+Min dice. Then, gain a Boost using " + \
                          "your Mid die. The target of the Attack gains a Boost of the same size.",
                          1,
                          categories=[1,2])
a_wild_strength = Ability("Wild Strength",
                          "R",
                          "When you defeat a minion, roll that minion's die and Boost " + \
                          "yourself using that roll to create a bonus for your next action.",
                          1)
a_grasping_vines = Ability("Grasping Vines",
                           "A",
                           "Hinder using %p0. Use your Max die. You may split that penalty " + \
                           "across multiple nearby targets.",
                           0,
                           categories=[1,2])
a_natural_weapon = Ability("Natural Weapon",
                           "A",
                           "Attack using %p0. Use your Max die.",
                           0,
                           categories=[1,2])
a_harvest_life_force = Ability("Harvest Life Force",
                               "A",
                               "Attack using %p0. Use your Min die. Take damage equal to your " + \
                               "Mid die, and one nearby ally Recovers Health equal to your " + \
                               "Max die.",
                               1,
                               categories=[1,2])
a_magical_shield = Ability("Magical Shield",
                           "R",
                           "When another hero in the Yellow or Red zone would take damage, " + \
                           "you may Defend them by rolling your single %p0 die.",
                           1,
                           categories=[1,2])
a_momentary_power = Ability("Momentary Power",
                            "A",
                            "Boost yourself using %p0. Use your Max die. Hinder a nearby " + \
                            "opponent with your Min die.",
                            1,
                            categories=[1,2])
a_relic_drain = Ability("Relic Drain",
                        "A",
                        "Hinder using %p0. Also Recover Health equal to your Min die.",
                        1,
                        categories=[1,2])
a_draw_power = Ability("Draw Power",
                       "A",
                       "Boost yourself using %p0. That bonus is persistent and exclusive.",
                       0,
                       categories=[1,2])
a_punishment = Ability("Punishment",
                       "I",
                       "Whenever you Attack an enemy that has inflicted a penalty on you, " + \
                       "treat that penalty as if it were a bonus for the purpose of that Attack.",
                       0)
a_energy_converter = Ability("Energy Converter",
                             "R",
                             "When you take damage from %e, gain a bonus equal to that amount " + \
                             "of damage.",
                             1)
a_explosive_attack = Ability("Explosive Attack",
                             "A",
                             "Attack up to three different targets using %p0. Apply your Max " + \
                             "die to one, your Mid die to another, and your Min die to the " + \
                             "third. If you roll doubles, take a minor twist or take " + \
                             "irreducible damage equal to that die.",
                             1,
                             categories=[1,2])
a_onboard_upgrade = Ability("Onboard Upgrade",
                            "A",
                            "Boost yourself using %p0. Use your Min+Mid dice. That bonus is " + \
                            "persistent and exclusive.",
                            1,
                            categories=[1,2],
                            pq_ids=[[1,8,2]],
                            pq_reqs=[[[1,8,2]]])
a_damage_reduction = Ability("Damage Reduction",
                             "I",
                             "Reduce %d damage you take by 1 while you are in the Green zone, " + \
                             "2 while in the Yellow zone, and 3 while in the Red zone.",
                             0,
                             damage_id=-1)
a_diagnostic_subroutine = Ability("Diagnostic Subroutine",
                                  "I",
                                  "Whenever your status changes due to a change in your " + \
                                  "current Health, you may remove a penalty on yourself.",
                                  0)
a_radioactive_recharge = Ability("Radioactive Recharge",
                                 "A",
                                 "Boost yourself using %p0. Then, either remove a penalty on " + \
                                 "yourself or Recover using your Min die.",
                                 1,
                                 categories=[1,2])
a_unstable_reaction = Ability("Unstable Reaction",
                              "R",
                              "After rolling during your turn, you may take 1 irreducible " + \
                              "damage to reroll your entire dice pool.",
                              1)
a_wither = Ability("Wither",
                   "A",
                   "Attack using %p0. Hinder that target using your Max die.",
                   1,
                   categories=[1,2])
a_charged_up = Ability("Charged Up",
                       "I",
                       "Whenever you roll a 1 on one or more dice, you may reroll those dice. " + \
                       "You must accept the result of the reroll.",
                       0)
a_dangerous_lash = Ability("Dangerous Lash",
                           "A",
                           "Attack multiple targets using %p0, applying your Min die to each. " + \
                           "If you roll doubles, also attack an ally using your Mid die.",
                           0,
                           categories=[1,2])
a_radioactive_aura = Ability("Radioactive Aura",
                             "R",
                             "When a new target enters the scene close to you, you may Attack " + \
                             "it by rolling your single %p0 die.",
                             0,
                             categories=[1,2])
a_energy_burst = Ability("Energy Burst",
                         "A",
                         "Attack multiple targets using %p0, using your Min die against each.",
                         1,
                         categories=[1,2])
a_recharge = Ability("Recharge",
                     "A",
                     "Boost yourself using %p0. Then, either remove a penalty on yourself or " + \
                     "Recover using your Min die.",
                     1,
                     categories=[1,2])
a_techno_absorb = Ability("Techno-Absorb",
                          "I",
                          "If you would take damage from %e, instead reduce that damage to 0 " + \
                          "and Recover that amount of Health instead.",
                          1,
                          pq_reqs=[Category(1,1)],
                          categories=[1,2],
                          energy=True)
a_tactical_analysis = Ability("Tactical Analysis",
                              "R",
                              "When Attacked, treat the amount of damage you take as a Boost " + \
                              "action for yourself.",
                              1)
a_indiscriminate_fabrication = Ability("Indiscriminate Fabrication",
                                       "A",
                                       "Boost using %p0, assigning your Min, Mid, and Max " + \
                                       "dice to 3 different bonuses, one of which must be " + \
                                       "given to an enemy.",
                                       0,
                                       categories=[1,2])
a_organi_hack = Ability("Organi-Hack",
                        "A",
                        "Attack a target using %p0. Hinder that target with your Min die.",
                        0,
                        categories=[1,2])
a_area_healing = Ability("Area Healing",
                         "A",
                         "Boost an ally using %p0. You and nearby heroes in the Yellow and " + \
                         "Red zones Recover Health equal to your Min die.",
                         1,
                         categories=[1,2])
a_mass_modification = Ability("Mass Modification",
                              "A",
                              "Boost or Hinder using %p0, and apply that mod to multiple " + \
                              "close targets.",
                              1,
                              categories=[1,2])
a_reach_through_veil = Ability("Reach through Veil",
                               "R",
                               "When a nearby ally would take damage, Defend that ally by " + \
                               "rolling your single status die, and move them elsewhere in " + \
                               "the same scene.",
                               1)
a_created_immunity = Ability("Created Immunity",
                             "I",
                             "When you would take damage from %e, you may Recover that amount " + \
                             "of Health instead.",
                             1)
a_multiple_assault = Ability("Multiple Assault",
                             "A",
                             "Attack using %p0 against multiple targets, using your Min die " + \
                             "against each.",
                             1,
                             categories=[1,2])
a_recalculating = Ability("Recalculating...",
                          "R",
                          "After rolling during your turn, you may take 1 irreducible damage " + \
                          "to reroll your entire dice pool.",
                          1)
a_created_form = Ability("Created Form",
                         "I",
                         "Reduce physical damage to yourself by 1 while you are in the Green " + \
                         "zone, 2 while in the Yellow zone, and 3 while in the Red zone.",
                         0)
a_intentionality = Ability("Intentionality",
                           "I",
                           "Whenever you roll a 1 on one or more dice, you may reroll those " + \
                           "dice. You must accept the result of the reroll.",
                           0)
a_attunement = Ability("Attunement",
                       "I",
                       "When you would take damage from %e, you may Recover that amount of " + \
                       "Health instead.",
                       1)
a_costly_strength = Ability("Costly Strength",
                            "A",
                            "Boost all nearby allies using %p0. Use your Max+Mid dice. Hinder " + \
                            "yourself with your Min die.",
                            1,
                            categories=[1,2])
a_cursed_resolve = Ability("Cursed Resolve",
                           "A",
                           "Boost yourself using %p0. Then, either remove a penalty on " + \
                           "yourself or Recover using your Min die.",
                           1,
                           categories=[1,2])
a_double_edged_luck = Ability("Double Edged Luck",
                              "I",
                              "Whenever you roll a 1 on one or more dice, you may reroll " + \
                              "those dice. You must accept the result of the reroll.",
                              0)
a_extremes = Ability("Extremes",
                     "I",
                     "Whenever you roll a die's max value, treat that value as 1 higher. " + \
                     "Whenever you roll a 1 on a die, treat that die as if it had rolled a 0.",
                     0)
a_alien_boost = Ability("Alien Boost",
                        "A",
                        "Boost all nearby allies using %p0. Use your Max+Mid dice. Hinder " + \
                        "yourself with your Min die.",
                        1,
                        categories=[1,2])
a_empower_and_repair = Ability("Empower and Repair",
                               "A",
                               "Boost, Hinder, Defend, or Attack using %p0. You and all " + \
                               "nearby heroes in the Yellow or Red zone Recover Health equal " + \
                               "to your Min die.",
                               1,
                               categories=[1,2])
a_halt = Ability("Halt",
                 "R",
                 "When you are Attacked at close range, Defend yourself by rolling your " + \
                 "single %p0 die.",
                 1,
                 categories=[1,2])
a_a_plan_for_everything = Ability("A Plan For Everything",
                                  "R",
                                  "When you are attacked, first roll your single %p0 die. " + \
                                  "Defend yourself with that roll. Then, Boost yourself using " + \
                                  "that roll.",
                                  1)
a_expanded_mind = Ability("Expanded Mind",
                          "A",
                          "Boost yourself using %p0. Use your Max die. That bonus is " + \
                          "persistent and exclusive. Then Attack using your Min die.",
                          1,
                          categories=[1,2])
a_overwhelming_vision = Ability("Overwhelming Vision",
                                "A",
                                "Attack using %p0. Then, if the target of the Attack " + \
                                "survived, also Attack that target with your Max die. " + \
                                "Otherwise, Recover an amount of Health equal to your Min die.",
                                1,
                                categories=[1,2])
a_cosmic_ray_absorption = Ability("Cosmic Ray Absorption",
                                  "I",
                                  "If you would take damage from %e, instead reduce that " + \
                                  "damage to 0 and Recover that amount of Health instead.",
                                  1,
                                  pq_reqs=[Category(1,1)],
                                  categories=[1,2],
                                  energy=True)
a_encourage = Ability("Encourage",
                      "A",
                      "Attack using %p0. Boost all nearby heroes taking Attack or Overcome " + \
                      "actions using your Min die until your next turn.",
                      1,
                      categories=[1,2])
a_mass_adjust = Ability("Mass Adjust",
                        "A",
                        "Boost or Hinder using %p0 and apply that mod against multiple close " + \
                        "targets.",
                        1,
                        categories=[1,2])
a_absorb_essence = Ability("Absorb Essence",
                          "R",
                          "When you defeat a minion, roll that minion's die and Boost " + \
                           "yourself using that roll.",
                          1)
a_aura_of_pain = Ability("Aura of Pain",
                         "A",
                         "Attack multiple targets using %p0. Then, take irreducible damage " + \
                         "equal to the number of targets hit.",
                         1,
                         categories=[1,2])
a_bizarre_strike = Ability("Bizarre Strike",
                           "A",
                           "Attack using %p0. Use your Max die. Hinder that target with your " + \
                           "Mid die. Hinder yourself with your Min die.",
                           1,
                           categories=[1,2])
a_attune = Ability("Attune",
                   "A",
                   "Boost yourself using %p0. That bonus is persistent and exclusive. Damage " + \
                   "dealt using that bonus is all %e.",
                   0,
                   categories=[1,2])
a_extrasensory_awareness = Ability("Extrasensory Awareness",
                                   "R",
                                   "When you would take damage that would change your zone, " + \
                                   "Defend against that damage by rolling your single %p0 die.",
                                   0,
                                   categories=[0,2])
a_brainstorm = Ability("Brainstorm",
                       "A",
                       "Attack using %p0. Hit one target using your Min die, another target " + \
                       "with your Mid die, and Boost using your Max die.",
                       1,
                       categories=[1,2])
a_strange_enhancement = Ability("Strange Enhancement",
                                "A",
                                "Boost all nearby allies using %p0 using your Max+Mid dice. " + \
                                "Hinder yourself with your Min die.",
                                1,
                                categories=[1,2])
a_volatile_creations = Ability("Volatile Creations",
                               "R",
                               "When one of your bonuses, penalties, or other creation of " + \
                               "your powers is destroyed, deal a target damage equal to the " + \
                               "roll of your %p0 die.",
                               1,
                               categories=[1,2])
a_command_power = Ability("Command Power",
                          "R",
                          "When you take damage from %e, you may deal that much damage to " + \
                          "another target.",
                          1)
a_dangerous_explosion = Ability("Dangerous Explosion",
                                "A",
                                "Attack multiple targets using %p0. Use your Mid die. Hinder " + \
                                "all targets damaged by this ability with your Min die. " + \
                                "Hinder yourself with your Max die.",
                                1,
                                categories=[1,2])
a_embolden = Ability("Embolden",
                     "A",
                     "Attack using %p0, and Boost all nearby heroes taking %a0 or %a1 actions " + \
                     "using your Min die until your next turn.",
                     1,
                     categories=[1,2])
a_resolve = Ability("Resolve",
                    "A",
                    "Boost yourself using %p0, then remove a penalty on yourself or Recover " + \
                    "using your Min die.",
                    1,
                    categories=[1,2])
a_resilience = Ability("Resilience",
                       "I",
                       "At the start of your turn, remove any -1 penalties on you.",
                       0)
a_twist_reality = Ability("Twist Reality",
                          "R",
                          "After rolling during your turn, you may take 1 damage to reroll " + \
                          "your entire dice pool.",
                          0)
a_power_from_beyond = Ability("Power from Beyond",
                              "A",
                              "Boost yourself using %p0. Use your Max die. That bonus is " + \
                              "persistent and exclusive. Then, Attack using your Min die.",
                              1,
                              categories=[1,2])
a_respond_in_kind = Ability("Respond in Kind",
                            "R",
                            "When you are hit with an Attack at close range, the attacker " + \
                            "also takes damage equal to their effect die.",
                            1)
a_dread_pallor = Ability("Dread Pallor",
                         "A",
                         "Hinder multiple targets using %p0. Use your Mid die for one and " + \
                         "your Min die for the rest.",
                         1,
                         categories=[1,2])
a_reality_scorned = Ability("Reality Scorned",
                            "A",
                            "Attack using %p0. If your target survived, Hinder them using " + \
                            "your Max die.",
                            1,
                            categories=[1,2])
a_always_on_the_move = Ability("Always on the Move",
                               "A",
                               "Attack using %p0. Defend yourself using your Min die.",
                               0,
                               categories=[2,2])
a_fast_fingers = Ability("Fast Fingers",
                         "A",
                         "Boost or Hinder using %p0. Use your Max die. If you roll doubles, " + \
                         "you may also Attack using your Mid die.",
                         0,
                         categories=[1,2])
a_non_stop_assault = Ability("Non-stop Assault",
                             "A",
                             "Attack multiple targets using %p0. Use your Min die. Hinder " + \
                             "each target equal to your Mid die.",
                             0,
                             categories=[0,2])
a_blinding_strike = Ability("Blinding Strike",
                            "A",
                            "Attack multiple targets using %p0. Hinder each target equal to " + \
                            "your Min die.",
                            1,
                            categories=[0,2])
a_flurry_of_fists = Ability("Flurry of Fists",
                            "A",
                            "Attack using %p0. Use your Max die. If you roll doubles, use " + \
                            "Max+Min instead.",
                            1,
                            categories=[0,2])
a_supersonic_streak = Ability("Supersonic Streak",
                              "A",
                              "Attack multiple targets using %p0. Use your Max die against " + \
                              "one target, and your Mid die against each other target. If you " + \
                              "roll doubles, take irreducible damage equal to your Mid die.",
                              1,
                              categories=[1,2])
a_speedy_analysis = Ability("Speedy Analysis",
                            "A",
                            "Boost multiple targets using %p0. Use your Max die.",
                            1,
                            categories=[1,2])
a_sabotage = Ability("Sabotage",
                     "A",
                     "Attack using %p0. Remove one physical bonus or penalty, Hinder a target " + \
                     "using your Min die, or maneuver to a new location in your environment.",
                     0,
                     categories=[2,2])
a_shadowy_figure = Ability("Shadowy Figure",
                           "A",
                           "Attack using %p0. Defend using your Min die against all Attacks " + \
                           "until your next turn.",
                           0,
                           categories=[2,2])
a_untouchable = Ability("Untouchable",
                        "R",
                        "When you would be dealt damage, roll a d4 while in the Green zone, " + \
                        "d6 while in the Yellow zone, or d8 while in Red. Reduce the damage " + \
                        "you take by the value rolled. Attack another target with that roll.",
                        0)
a_overcome_from_the_darkness = Ability("Overcome from the Darkness",
                                       "A",
                                       "Attack or Overcome using %p0. Boost yourself using " + \
                                       "your Min die.",
                                       1,
                                       categories=[2,2])
a_diversion = Ability("Diversion",
                      "R",
                      "When you would take damage, Defend against that damage by rolling " + \
                      "your single %p0 die.",
                      1,
                      categories=[2,2])
a_damage_resistant = Ability("Damage Resistant",
                             "I",
                             "Reduce any physical or energy damage you take by 1 while you " + \
                             "are in the Green zone, 2 while in the Yellow zone, and 3 while " + \
                             "in the Red zone.",
                             -1)
a_frontline_fighting = Ability("Frontline Fighting",
                               "A",
                               "Attack using %p0. The target of that Attack must take the " + \
                               "Attack action against you as its next turn, if possible.",
                               -1,
                               categories=[2,2])
a_galvanize = Ability("Galvanize",
                      "A",
                      "Boost using %p0. Apply that bonus to all hero Attack and Overcome " + \
                      "actions until your next turn.",
                      -1,
                      categories=[2,2])
a_power_strike = Ability("Power Strike",
                         "A",
                         "Attack using %p0 and use your Max die.",
                         -1,
                         categories=[2,2])
a_strength_in_victory = Ability("Strength in Victory",
                                "R",
                                "When you eliminate a minion with an Attack using %p0, " + \
                                "Recover Health equal to your Min die.",
                                -1,
                                categories=[2,2])
a_dual_wielder = Ability("Dual Wielder",
                         "A",
                         "Attack two different targets using %p0, one target using your Mid " + \
                         "die and the other your Min die.",
                         0,
                         categories=[2,2])
a_load = Ability("Load",
                 "A",
                 "Boost using %p0 to create one bonus using your Max die and another using " + \
                 "your Mid die.",
                 0,
                 categories=[2,2])
a_precise_shot = Ability("Precise Shot",
                         "A",
                         "Attack using %p0. Ignore all penalties on this Attack, ignore any " + \
                         "Defend actions, and it cannot be affected by Reactions.",
                         0,
                         categories=[2,2])
a_spin_and_shoot = Ability("Spin & Shoot",
                           "A",
                           "Attack using %p0. Defend using your Min die.",
                           0)
a_sniper_aim = Ability("Sniper Aim",
                       "A",
                       "Boost yourself using %p0. Use your Max+Min dice. This bonus can only " + \
                       "be used against one chosen target, and is persistent & exclusive " + \
                       "against that target until it leaves the scene.",
                       0,
                       categories=[2,2])
a_called_shot = Ability("Called Shot",
                        "A",
                        "Attack using %p0. Create a Boost for another hero using your Max die.",
                        1,
                        categories=[0,2])
a_exploding_ammo = Ability("Exploding Ammo",
                           "A",
                           "Attack or Overcome using %p0 on an environmental target, using " + \
                           "your Max+Min dice. If you roll doubles, take a minor twist.",
                           1,
                           categories=[0,2])
a_hair_trigger_reflexes = Ability("Hair Trigger Reflexes",
                                  "R",
                                  "When a new target enters close range, Attack that target " + \
                                  "by rolling your single %p0 die.",
                                  1,
                                  categories=[0,2])
a_ricochet = Ability("Ricochet",
                     "A",
                     "Attack using %p0. Use your Max die. If you roll doubles, use Max+Min " + \
                     "instead.",
                     1,
                     categories=[0,2])
a_exploit_vulnerability = Ability("Exploit Vulnerability",
                                  "A",
                                  "Attack using %p0. If you Attacked or Hindered that target " + \
                                  "in your previous turn, use your Max die in this Attack.",
                                  0,
                                  categories=[1,2])
a_disabling_blast = Ability("Disabling Blast",
                            "A",
                            "Attack using %p0. Hinder using your Min die.",
                            0,
                            categories=[1,2])
a_danger_zone = Ability("Danger Zone",
                        "A",
                        "Attack multiple targets using %p0. Use your Min die against each.",
                        0,
                        categories=[1,2])
a_precise_hit = Ability("Precise Hit",
                        "A",
                        "Attack using %p0. Ignore all penalties on this Attack, ignore any " + \
                        "Defend actions, and it cannot be affected by Reactions.",
                        0,
                        categories=[1,2])
a_energy_immunity = Ability("Energy Immunity",
                            "I",
                            "If you would take damage from %e, instead reduce that damage to " + \
                            "0 and Recover that amount of Health instead.",
                            1,
                            pq_reqs=[Category(1,1)],
                            categories=[1,2],
                            energy=True)
a_heedless_blast = Ability("Heedless Blast",
                           "A",
                           "Attack multiple targets using %p0. Use your Mid die against each " + \
                           "target. Take irreducible damage equal to your Mid die.",
                           1,
                           categories=[1,2])
a_imbue_with_element = Ability("Imbue with Element",
                               "A",
                               "Attack using %p0. Use your Max die. If you choose another " + \
                               "hero to go next, Boost that hero using your Mid die.",
                               1,
                               categories=[1,2])
a_defensive_strike = Ability("Defensive Strike",
                             "A",
                             "Defend using %p0. Attack using your Min die.",
                             -1)
a_dual_strike = Ability("Dual Strike",
                        "A",
                        "Attack one target using %p0. Attack a second target using your Min die.",
                        -1)
a_flexible_stance = Ability("Flexible Stance",
                            "A",
                            "Take any two basic actions using %p0, each using your Min die.",
                            -1)
a_offensive_strike = Ability("Offensive Strike",
                             "A",
                             "Attack using %p0. Use your Max die.",
                             -1)
a_precise_strike = Ability("Precise Strike",
                           "A",
                           "Attack using %p0. Ignore all penalties on this Attack, ignore any " + \
                           "Defend actions, and it cannot be affected by Reactions.",
                           -1)
a_throw_minion2 = Ability("Throw Minion",
                          "A",
                          "Attack a minion using %p0. Whatever that minion rolls as defense " + \
                          "Attacks another target of your choice.",
                          -1,
                          categories=[1,2])
a_armored = Ability("Armored",
                    "I",
                    "Reduce any physical or energy damage you take by 1 while you are in the " + \
                    "Green zone, 2 while in the Yellow zone, and 3 while in the Red zone.",
                    0)
a_deflect = Ability("Deflect",
                    "R",
                    "When you would be dealt damage, you may deal damage to a nearby target " + \
                    "equal to the amount reduced by your Armored ability.",
                    0)
a_dual_offense = Ability("Dual Offense",
                         "A",
                         "Attack using %p0. Attack a second target with your Min die.",
                         0,
                         categories=[1,2])
a_living_bulwark = Ability("Living Bulwark",
                           "A",
                           "Attack using %p0. Defend another target with your Min die.",
                           0,
                           categories=[1,2])
a_repair = Ability("Repair",
                   "A",
                   "Attack using %p0. Recover Health equal to your Min die.",
                   0,
                   categories=[1,2])
a_unstoppable_charge = Ability("Unstoppable Charge",
                               "A",
                               "Attack using %p0. Ignore all penalties on this Attack, ignore " + \
                               "any Defend actions, and it cannot be affected by Reactions.",
                               0)
a_aerial_bombardment = Ability("Aerial Bombardment",
                               "A",
                               "Attack up to three targets using %p0. Apply your Min die to " + \
                               "each of them.",
                               -1)
a_aerial_surveillance = Ability("Aerial Surveillance",
                                "A",
                                "Boost using %p0. Apply that bonus to all hero Attack and " + \
                                "Overcome actions until your next turn.",
                                -1)
a_barrel_roll = Ability("Barrel Roll",
                        "R",
                        "When you are Attacked while flying, you may Defend yourself by " + \
                        "rolling your single %p0 die.",
                        -1)
a_dive_and_drop = Ability("Dive & Drop",
                          "A",
                          "Attack a minion using %p0. Use whatever that minion rolls for its " + \
                          "save as an Attack against another target of your choice.",
                          -1,
                          categories=[1,2])
a_sonic_boom = Ability("Sonic Boom",
                       "A",
                       "Hinder multiple targets using %p0. Apply your Min die to each of them.",
                       -1,
                       categories=[1,2])
a_strike_and_swoop = Ability("Strike & Swoop",
                             "A",
                             "Attack using %p0. Defend against all Attacks against you using " + \
                             "your Min die until your next turn.",
                             -1)
a_backlash = Ability("Backlash",
                     "A",
                     "Attack using %p0. Take damage equal to your Min die.",
                     0,
                     pq_reqs=[Category(1,1)],
                     pq_opts=[Category(1,1)],
                     categories=[1,2])
a_external_combustion = Ability("External Combustion",
                                "A",
                                "Attack up to two targets using %p0. Also take an amount of " + \
                                "damage equal to your Mid die.",
                                0,
                                pq_reqs=[Category(1,1)],
                                pq_opts=[Category(1,1)],
                                categories=[1,2])
a_energy_conversion = Ability("Energy Conversion",
                              "A",
                              "Defend using %p0. Use your Max die. Boost using your Min die.",
                              0,
                              pq_reqs=[Category(1,1)],
                              pq_opts=[Category(1,1)],
                              categories=[1,2])
a_focused_apparatus = Ability("Focused Apparatus",
                              "A",
                              "Hinder using %p0. Attack using your Min die. If you are in the " + \
                              "Red zone, you may apply that penalty to any number of nearby " + \
                              "targets.",
                              0,
                              pq_reqs=[Category(1,1)],
                              pq_opts=[Category(1,1)],
                              categories=[1,2])
a_damage_spike = Ability("Damage Spike",
                         "A",
                         "Attack using %p0. Use your Max+Min dice. Take damage equal to your " + \
                         "Mid die.",
                         1,
                         pq_reqs=[Category(1,1)],
                         pq_opts=[Category(1,1)],
                         categories=[1,2])
a_energy_alignment = Ability("Energy Alignment",
                             "I",
                             "If you would take damage from %e, reduce that damage to 0 and " + \
                             "Recover that amount of Health instead.",
                             1,
                             pq_reqs=[Category(1,1)],
                             categories=[1,2],
                             energy=True)
a_energy_redirection = Ability("Energy Redirection",
                               "I",
                               "Whenever you take damage from %e, you may also inflict that " + \
                               "much damage on another target.",
                               1,
                               pq_reqs=[Category(1,1)],
                               categories=[1,2],
                               energy=True)
a_live_dangerously = Ability("Live Dangerously",
                             "A",
                             "Attack multiple targets using %p0. Take damage equal to your " + \
                             "Max die.",
                             1,
                             pq_reqs=[Category(1,1)],
                             pq_opts=[Category(1,1)],
                             categories=[1,2])
a_adaptive_programming = Ability("Adaptive Programming",
                                 "A",
                                 "Boost yourself using %p0, and Defend with your Min die.",
                                 -1,
                                 categories=[1,2])
a_metal_skin = Ability("Metal Skin",
                       "I",
                       "Reduce the amount of physical damage taken by 1 while you are in the " + \
                       "Green zone, 2 while in the Yellow zone, and 3 while in the Red zone.",
                       -1)
a_living_arsenal = Ability("Living Arsenal",
                           "A",
                           "Attack using %p0 with a bonus equal to the number of bonuses you " + \
                           "currently have.",
                           -1,
                           categories=[1,2])
a_self_improvement = Ability("Self-Improvement",
                             "A",
                             "Boost yourself using %p0. That bonus is persistent and exclusive.",
                             -1,
                             categories=[1,2])
a_something_for_everyone = Ability("Something for Everyone",
                                   "A",
                                   "Attack using %p0. Use your Mid die to Attack one extra " + \
                                   "target for each bonus you have. Apply a different bonus " + \
                                   "to each Attack.",
                                   -1,
                                   categories=[1,2])
a_banish = Ability("Banish",
                   "A",
                   "Hinder using %p0. Use your Max die. If you roll doubles, also Attack " + \
                   "using your Mid die.",
                   0,
                   categories=[1,2])
a_energy_jaunt = Ability("Energy Jaunt",
                         "A",
                         "Attack multiple targets using %p0, applying your Min die against each.",
                         0,
                         categories=[1,2])
a_powerful_blast = Ability("Powerful Blast",
                           "A",
                           "Attack using %p0 and use your Max die.",
                           0,
                           categories=[1,2])
a_subdue = Ability("Subdue",
                   "A",
                   "Attack using %p0. Hinder the same target using your Min die.",
                   0,
                   categories=[1,2])
a_cords_of_magic = Ability("Cords of Magic",
                           "A",
                           "Destroy all bonuses and penalties on a target. Then, Hinder that " + \
                           "target using %p0, using your Max die.",
                           1,
                           categories=[1,2])
a_field_of_energy = Ability("Field of Energy",
                            "A",
                            "Attack multiple targets near each other using %p0.",
                            1,
                            categories=[1,2])
a_living_bomb = Ability("Living Bomb",
                        "A",
                        "Destroy one d6 or d8 minion. Roll that minion's die as an Attack " + \
                        "against another target.",
                        1)
a_psychic_assault = Ability("Psychic Assault",
                            "A",
                            "Attack using %p0. Hinder the target using your Min die.",
                            0,
                            pq_reqs=[Category(1,6)],
                            pq_opts=[Category(1,6)],
                            categories=[1,2])
a_psychic_coordination = Ability("Psychic Coordination",
                                 "A",
                                 "Boost using %p0. Apply that bonus to all hero Attack and " + \
                                 "Overcome actions until your next turn.",
                                 0,
                                 pq_reqs=[Category(1,6)],
                                 pq_opts=[Category(1,6)],
                                 categories=[1,2])
a_psychic_insight = Ability("Psychic Insight",
                            "R",
                            "After rolling during your turn, you may take 1 damage to reroll " + \
                            "your entire dice pool.",
                            0)
a_astral_projection = Ability("Astral Projection",
                              "A",
                              "Overcome using %p0 and use your Max+Min dice. You do not have " + \
                              "to be physically present in the area you are Overcoming.",
                              1,
                              pq_reqs=[[[1,6,4]]],
                              pq_opts=[[[1,6,4]]],
                              pq_ids=[[1,6,4]],
                              categories=[1,2])
a_illusionary_double = Ability("Illusionary Double",
                               "R",
                               "When you are Attacked, Defend by rolling your single %p0 die.",
                               1,
                               pq_reqs=[[[1,6,1]]],
                               pq_opts=[[[1,6,1]]],
                               pq_ids=[[1,6,1]],
                               categories=[1,2])
a_minion_suggestion = Ability("Minion Suggestion",
                              "A",
                              "Attack a minion using %p0. If that minion would be taken out, " + \
                              "you control its next action, and then it is removed. " + \
                              "Otherwise, Hinder it using your Min die.",
                              1,
                              pq_reqs=[[[1,6,5]]],
                              pq_opts=[[[1,6,5]]],
                              pq_ids=[[1,6,5]],
                              categories=[1,2])
a_precognitive_alteration = Ability("Precognitive Alteration",
                                    "R",
                                    "After an ally rolls dice to take an action for their " + \
                                    "turn but before using the result, Boost that ally's roll " + \
                                    "using your single %p0 die.",
                                    1,
                                    pq_reqs=[[[1,6,3]]],
                                    pq_opts=[[[1,6,3]]],
                                    pq_ids=[[1,6,3]],
                                    categories=[1,2])
a_postcognitive_understanding = Ability("Postcognitive Understanding",
                                        "R",
                                        "After an enemy rolls dice to take an action for " + \
                                        "their turn but before using the result, Hinder that " + \
                                        "enemy's roll using your single %p0 die.",
                                        1,
                                        pq_reqs=[[[1,6,2]]],
                                        pq_opts=[[[1,6,2]]],
                                        pq_ids=[[1,6,2]],
                                        categories=[1,2])
a_psychic_analysis = Ability("Psychic Analysis",
                             "A",
                             "Boost yourself using %p0. Either use your Max die, or use your " + \
                             "Mid die and make it persistent.",
                             1,
                             pq_reqs=[Category(0,1)],
                             pq_opts=[Category(0,1)],
                             categories=[0,2])
a_swarm = Ability("Swarm",
                  "A",
                  "Attack multiple targets using %p0 and use your Min die.",
                  1,
                  pq_reqs=[[[1,6,0]]],
                  pq_opts=[[[1,6,0]]],
                  pq_ids=[[1,6,0]],
                  categories=[1,2])
a_telekinetic_assault = Ability("Telekinetic Assault",
                                "A",
                                "Attack using %p0. Either Attack one target and use your Max " + \
                                "die, or two targets and use your Mid die against one and " + \
                                "your Min die against another.",
                                1,
                                pq_reqs=[[[1,6,6]]],
                                pq_opts=[[[1,6,6]]],
                                pq_ids=[[1,6,6]],
                                categories=[1,2])
a_telepathic_whammy = Ability("Telepathic Whammy",
                              "A",
                              "Attack using %p0 and use your Max die. Hinder the target with " + \
                              "a persistent penalty equal to your Min die.",
                              1,
                              pq_reqs=[[[1,6,7]]],
                              pq_opts=[[[1,6,7]]],
                              pq_ids=[[1,6,7]],
                              categories=[1,2])
a_displacement_assault = Ability("Displacement Assault",
                                 "A",
                                 "Attack using %p0. Either Hinder your target with your Min " + \
                                 "die or move them somewhere else in the scene.",
                                 -1,
                                 categories=[1,2])
a_hit_and_run = Ability("Hit & Run",
                        "A",
                        "Attack using %p0. Defend against all Attacks against you using your " + \
                        "Min die until your next turn.",
                        -1,
                        categories=[1,2])
a_mobile_dodge = Ability("Mobile Dodge",
                         "R",
                         "When you are hit with an Attack, you may take 1 irreducible damage " + \
                         "to have the attacker reroll their dice pool.",
                         -1)
a_mobile_assist = Ability("Mobile Assist",
                          "A",
                          "Boost another hero using %p0. Attack using your Min die.",
                          -1,
                          categories=[1,2])
a_run_down = Ability("Run Down",
                     "A",
                     "Attack multiple targets using %p0. Use your Min die against each.",
                     -1,
                     categories=[1,2])
a_make_minion = Ability("Make Minion",
                        "A",
                        "Create a minion using %p0. Reference the minion chart to see what " + \
                        "size of minion it is. Choose whether it can Attack, Defend, Boost, " + \
                        "Hinder, or Overcome. It acts on the start of your turn. You can only " + \
                        "use this ability in a situation conducive to how you create minions.",
                        0,
                        categories=[1,2])
a_power_up = Ability("Power Up",
                     "A",
                     "Boost another hero or one of your minions using %p0. Either use your " + \
                     "Max die, or use your Mid die and make that bonus persistent.",
                     0,
                     categories=[1,2])
a_minion_formation = Ability("Minion Formation",
                             "R",
                             "Reduce any damage you take by the number of minions you have. " + \
                             "Whenever damage is reduced this way, reduce the size of one of " + \
                             "your minions.",
                             1)
a_rapid_deployment = Ability("Rapid Deployment",
                             "A",
                             "Create a minion using %p0, using your Min die, and reference " + \
                             "the minion chart to see what size of minion it is. It acts now " + \
                             "and at the start of your turns.",
                             1,
                             categories=[1,2])
a_upgrade_minion = Ability("Upgrade Minion",
                           "A",
                           "Boost one of your minions using %p0. You may also upgrade that " + \
                           "minion to your Max die size, replacing its minion form.",
                           1,
                           categories=[1,2])
a_construction_focus = Ability("Construction Focus",
                               "A",
                               "Create two minions using %p0, one with your Max die and " + \
                               "one with your Mid die. Choose which one basic action each of " + \
                               "them can perform. They act on the start of your turn.",
                               2,
                               categories=[1,2])
a_swarm_combat = Ability("Swarm Combat",
                         "A",
                         "Attack using %p0. Use your Max die plus a bonus equal to the number " + \
                         "of minions you have.",
                         2,
                         categories=[1,2])
a_sacrifice = Ability("Sacrifice",
                      "R",
                      "When you are Attacked, redirect the Attack to one of your nearby minions.",
                      2)
a_gimmick = Ability("Gimmick",
                    "A",
                    "Boost or Hinder using %p0. Use your Max die. If you roll doubles, you " + \
                    "may also Attack using your Mid die.",
                    0,
                    categories=[1,2])
a_multitask = Ability("Multitask",
                      "A",
                      "Take any two different basic actions using %p0, each using your Min die.",
                      0)
a_surprise_results = Ability("Surprise Results",
                             "R",
                             "After rolling your dice pool for the turn, you may lose 1 " + \
                             "Health to reroll your entire pool.",
                             0)
a_unknown_results = Ability("Unknown Results",
                            "A",
                            "Take any basic action using %p0. Then roll a d6. On 1, Boost " + \
                            "with your Min die. On 2, Hinder with your Min die. On 3, Defend " + \
                            "with your Min die. On 4, lose Health equal to your Min die. On " + \
                            "5, your basic action uses your Max die. On 6, your basic action " + \
                            "uses your Min die.",
                            0,
                            categories=[1,2])
a_break_the_4th = Ability("Break the 4th",
                          "R",
                          "You may uncheck a checked off collection on your hero sheet.",
                          1)
a_danger = Ability("Danger!",
                   "A",
                   "Attack multiple targets using %p0. If you roll doubles, one nearby ally " + \
                   "is also hit with the Attack.",
                   1,
                   categories=[1,2])
a_expect_the_unexpected = Ability("Expect the Unexpected",
                                  "R",
                                  "Apply a bonus after rolling your action, instead of before.",
                                  1)
a_imitation = Ability("Imitation",
                      "A",
                      "Use a Green action ability of a nearby ally (using the same size " + \
                      "power/quality die they would use).",
                      1)
a_turn_the_tables = Ability("Turn the Tables",
                            "A",
                            "Change any bonus into a penalty of equal size or vice versa.",
                            1)
a_change_forms = Ability("Change Forms",
                         "A",
                         "Take a basic action using %p0, then switch to any available form.",
                         0,
                         pq_reqs=[Category(1,7)],
                         pq_opts=[Category(1,7)],
                         categories=[1,2])
a_form_recovery = Ability("Form Recovery",
                          "A",
                          "Attack using %p0 and Recover Health equal to your Min die. Return " + \
                          "to your base form.",
                          0,
                          pq_reqs=[Category(1,7)],
                          pq_opts=[Category(1,7)],
                          categories=[1,2])
a_surprise_shift = Ability("Surprise Shift",
                           "A",
                           "Attack using %p0 and use your Max die. Then change to any " + \
                           "available form.",
                           0,
                           pq_reqs=[Category(1,7)],
                           pq_opts=[Category(1,7)],
                           categories=[1,2])
a_clever_form = Ability("Clever Form",
                        "A",
                        "Boost or Overcome using %p0. Use your Max die.",
                        -1,
                        categories=[1,2])
a_miniscule_form = Ability("Miniscule Form",
                           "A",
                           "Defend using %p0. Use your Max die. Remove all penalties on you.",
                           -1,
                           categories=[1,2])
a_strong_form = Ability("Strong Form",
                        "A",
                        "Attack using %p0. Use your Max die.",
                        -1,
                        categories=[1,2])
a_tough_form = Ability("Tough Form",
                       "I",
                       "Reduce any physical or energy damage you take by 1 while you are in " + \
                       "the Green zone, 2 while in the Yellow zone, and 3 while in the Red zone.",
                       -1)
a_tricky_form = Ability("Tricky Form",
                        "A",
                        "Boost or Hinder using %p0. Use your Max die.",
                        -1,
                        categories=[1,2])
a_weird_form = Ability("Weird Form",
                       "R",
                       "When an opponent would Attack you in close combat while in this form, " + \
                       "you may Attack or Hinder them first by rolling your single %p0 die.",
                       -1,
                       categories=[1,2])
a_agile_form = Ability("Agile Form",
                       "A",
                       "Attack using %p0. Defend against all attacks until your next turn " + \
                       "with your Min die.",
                       -1,
                       categories=[1,2])
a_regenerating_form = Ability("Regenerating Form",
                              "A",
                              "Boost using %p0. Recover Health equal to your Min die.",
                              -1,
                              categories=[1,2])
a_speedy_form = Ability("Speedy Form",
                        "A",
                        "Hinder multiple targets using %p0.",
                        -1,
                        categories=[1,2])
a_towering_form = Ability("Towering Form",
                          "A",
                          "Attack multiple targets using %p0.",
                          -1,
                          categories=[1,2])
a_emergency_change = Ability("Emergency Change",
                             "R",
                             "When hit with an Attack, change to any form before resolving " + \
                             "the Attack. Take a minor twist.",
                             2)
a_analyze_probabilities = Ability("Analyze Probabilities",
                                  "R",
                                  "After rolling your dice pool, you may lose 1 Health to " + \
                                  "reroll your dice pool.",
                                  0)
a_analyze_weakness = Ability("Analyze Weakness",
                             "A",
                             "Hinder using %p0. Use your Max die, or use your Mid die and " + \
                             "make it persistent and exclusive.",
                             0,
                             categories=[1,2])
a_equip = Ability("Equip",
                  "A",
                  "Boost using %p0. Make one bonus for one ally using your Mid die and " + \
                  "another for another ally using your Min die.",
                  0,
                  categories=[1,2])
a_helpful_invention = Ability("Helpful Invention",
                              "A",
                              "Boost using %p0. Use your Max die, or use your Mid die and " + \
                              "make it persistent and exclusive.",
                              0,
                              categories=[1,2])
a_helpful_analysis = Ability("Helpful Analysis",
                             "R",
                             "One nearby ally may reroll their dice pool. You lose Health " + \
                             "equal to the Min die of the new roll.",
                             1)
a_snap_decision = Ability("Snap Decision",
                          "A",
                          "Boost using %p0. Use your Max+Min dice. Then Attack using your Mid " + \
                          "die with that bonus.",
                          1,
                          categories=[1,2])
a_negative_likelihood = Ability("Negative Likelihood",
                                "A",
                                "Hinder using %p0. That penalty is persistent and exclusive.",
                                0,
                                categories=[1,2])
a_not_quite_right = Ability("Not Quite Right",
                            "R",
                            "After a dice pool is rolled, adjust one die up or down one value " + \
                            "on the die.",
                            0)
a_probability_insight = Ability("Probability Insight",
                                "A",
                                "Boost using %p0. Use your Max die. If you roll doubles, you " + \
                                "may also Attack using your Mid die.",
                                0,
                                categories=[1,2])
a_warp_space = Ability("Warp Space",
                       "A",
                       "Attack using %p0. You may move the target of that Attack anywhere " + \
                       "else nearby. If the target goes next, you decide who takes the next " + \
                       "turn after that.",
                       0,
                       categories=[1,2])
a_alternate_outcome = Ability("Alternate Outcome",
                              "R",
                              "When a nearby enemy rolls their dice pool for the turn, you " + \
                              "may lose 1 Health to reroll their entire dice pool.",
                              1)
a_never_happened = Ability("Never Happened",
                           "R",
                           "When a nearby enemy would create a bonus or penalty, you may " + \
                           "remove it immediately.",
                           1)
a_retroactive_rewrite = Ability("Retroactive Rewrite",
                                "R",
                                "You may apply a bonus to a roll after rolling instead of before.",
                                1)
a_transform = Ability("Transform",
                      "A",
                      "Change from your civilian form to your heroic form, or vice versa.",
                      0)
a_device_transform = Ability("Device Transform",
                             "A",
                             "If you have access to your device, change from your civilian " + \
                             "form to your heroic form, or vice versa. After your " + \
                             "transformation, take a basic action using your Min die. If you " + \
                             "have any penalties that separate you from your device or " + \
                             "otherwise inhibit you having full access to your device, you " + \
                             "cannot use this ability.",
                             0)
a_merge = Ability("Merge",
                  "A",
                  "If you have access to a willing compatible person to enable your " + \
                  "transformation, change from your civilian form to your heroic form, or " + \
                  "vice versa. After your transformation, take a basic action using your Min " + \
                  "die. If you have any penalties that separate you from that person, you " + \
                  "cannot use this ability.",
                  0)
a_possess_person = Ability("Possess Person",
                           "A",
                           "Attack using %p0. If you incapacitate the target and change " + \
                           "forms, you may use your Min die as a bonus to your next action. " + \
                           "Alternatively, you may possess a willing target for no bonus.",
                           0,
                           categories=[1,2])
a_possess_object = Ability("Possess Object",
                           "A",
                           "Overcome using %p0. On a success, merge with an item and then use " + \
                           "your Min die to take a basic action.",
                           0,
                           categories=[0,2])
a_uncontrolled_transform = Ability("Uncontrolled Transform",
                                   "AI",
                                   "The first time you take damage or change zones in a " + \
                                   "scene, you must change from your civilian form to your " + \
                                   "heroic form. You can also transform by taking an action " + \
                                   "and taking damage equal to a roll of your current status " + \
                                   "die. After an action scene, you change back to your " + \
                                   "civilian form.",
                                   0)
a_divided_psyche = Ability("Divided Psyche",
                           "I",
                           "While you are in your civilian form, use two qualities instead of " + \
                           "a power and a quality. While in your heroic form, use two powers " + \
                           "instead of a power and a quality. (Use your status in both " + \
                           "cases.) You cannot use abilities related to a power or quality " + \
                           "you don't have access to.",
                           0)
a_split_form = Ability("Split Form",
                       "I",
                       "Choose two powers and two qualities that you always have access to in " + \
                       "either form. You must divide up the remainder of your powers and " + \
                       "qualities between your civilian and heroic forms, so they are only " + \
                       "usable within those forms. You cannot use abilities related to a power " + \
                       "or quality you don't have access to. In the next step, when you create " + \
                       "a roleplaying quality, you will have access to that in either form.",
                       0)
a_switch = Ability("Switch",
                   "A",
                   "Boost yourself using %p0. Then change modes.",
                   0)
a_quick_switch = Ability("Quick Switch",
                         "A",
                         "Destroy one bonus on you. Change modes, then take an action in the " + \
                         "new mode.",
                         1)
a_emergency_switch = Ability("Emergency Switch",
                             "R",
                             "When you are hit with an Attack, you may change to any mode. If " + \
                             "you do, take extra damage equal to the Min die or take a minor " + \
                             "twist.",
                             2)
a_debilitator = Ability("Debilitator",
                        "A",
                        "Hinder all nearby opponents using %p0. If you roll doubles, take " + \
                        "damage equal to your Max die, and then you may also Attack all " + \
                        "nearby opponents with your Min die.",
                        0,
                        categories=[1,2])
a_improvement = Ability("Improvement",
                        "A",
                        "Boost yourself using %p0. Create one bonus using your Max die and " + \
                        "one bonus using your Mid die. These bonuses are persistent and " + \
                        "exclusive.",
                        0,
                        categories=[1,2])
a_scout = Ability("Scout",
                  "A",
                  "Overcome using %p0. Defend yourself with your Max die. Then, you may end " + \
                  "up anywhere in the current scene.",
                  0,
                  categories=[1,2])
a_analysis = Ability("Analysis",
                     "A",
                     "Hinder or use one of your Principles to Overcome using %p0. Use your " + \
                     "Max+Min dice.",
                     1,
                     categories=[1,2])
a_bombardment = Ability("Bombardment",
                        "A",
                        "Defend yourself using %p0. You may Attack one target with your Max die.",
                        1,
                        categories=[1,2])
a_regeneration = Ability("Regeneration",
                         "A",
                         "Defend using %p0. Use your Max die. Recover Health equal to your " + \
                         "Min die.",
                         1,
                         categories=[1,2])
a_skirmish = Ability("Skirmish",
                     "A",
                     "Attack one target using %p0. Attack a different target with your Min " + \
                     "die. At the end of your turn, you may change modes.",
                     1,
                     categories=[1,2])
a_stalwart = Ability("Stalwart",
                     "A",
                     "Defend yourself and all nearby allies using %p0 against each Attack " + \
                     "until the beginning of your next turn.",
                     1,
                     categories=[1,2])
a_destroyer = Ability("Destroyer",
                      "I",
                      "Whenever you take a basic Attack action, either use your Max+Min dice " + \
                      "to Attack one target, or Attack two different targets, one using your " + \
                      "Max die and one using your Mid die.",
                      2)
a_hunter_killer = Ability("Hunter/Killer",
                          "A",
                          "Move to any target in this scene and Hinder that target using %p0. " + \
                          "Then, Attack that target using your Max+Min dice.",
                          2,
                          categories=[1,2])
a_shield = Ability("Shield",
                   "R",
                   "When you are attacked, you may Defend against the Attack by rolling your " + \
                   "single %p0 die. If you reduce the damage to 0 or less, you may also " + \
                   "Hinder the source of the damage with the result of the die you rolled.",
                   2,
                   categories=[1,2])
a_out_pboost = Ability("Boost with a Power",
                       "A",
                       "Boost an ally by rolling your single %p0 die.",
                       3,
                       categories=[1,2])
a_out_qboost = Ability("Boost with a Quality",
                       "A",
                       "Boost an ally by rolling your single %p0 die.",
                       3,
                       categories=[0,2])
a_out_rboost = Ability("Boost with Red status",
                       "A",
                       "Boost an ally by rolling your single Red status die.",
                       3)
a_out_reaction = Ability("Grant an ally a single die reroll",
                         "A",
                         "Choose an ally. Until your next turn, that ally may reroll one of " + \
                         "their dice by using a Reaction.",
                         3)
a_out_pdefend = Ability("Defend with a Power",
                        "A",
                        "Defend an ally by rolling your single %p0 die.",
                        3,
                        categories=[1,2])
a_out_qdefend = Ability("Defend with a Quality",
                        "A",
                        "Defend an ally by rolling your single %p0 die.",
                        3,
                        categories=[0,2])
a_out_qhinder_plus = Ability("Hinder a Minion or Lieutenant",
                             "A",
                             "Hinder a Minion or Lieutenant by rolling your single %p0 die. " + \
                             "Increase that Penalty by 1.",
                             3,
                             categories=[0,2])
a_out_phinder = Ability("Hinder with a Power",
                        "A",
                        "Hinder an enemy by rolling your single %p0 die.",
                        3,
                        categories=[1,2])
a_out_qhinder = Ability("Hinder with a Quality",
                        "A",
                        "Hinder an enemy by rolling your single %p0 die.",
                        3,
                        categories=[0,2])
a_out_remove = Ability("Remove a bonus or penalty",
                       "A",
                       "Remove a bonus or penalty of your choice.",
                       3)
a_out_reroll = Ability("Next hero may take 1 damage to reroll",
                       "I",
                       "The hero who goes directly after you may take 1 damage to reroll " + \
                       "their dice pool.",
                       3)
a_major_regeneration = Ability("Major Regeneration",
                               "A",
                               "Hinder yourself using %p0. Use your Min die. Recover health " + \
                               "equal to your Max+Mid dice.",
                               2,
                               pq_reqs=[[[1,0,3]] + Category(1,7)],
                               pq_opts=[[[1,0,3]] + Category(1,7)],
                               categories=[1,2])
a_paragon_feat = Ability("Paragon Feat",
                         "A",
                         "Overcome using %p0 in a situation that requires you to be more than " + \
                         "humanly capable, like an extreme feat of strength or speed. Use " + \
                         "your Max+Min dice. Boost all nearby allies with your Mid die.",
                         2,
                         pq_reqs=[Category(1,0)],
                         pq_opts=[Category(1,0)],
                         categories=[1,2])
a_push_your_limits = Ability("Push Your Limits",
                             "I",
                             "You have no limit on amount of Reactions you can take. Each " + \
                             "time you use a Reaction after the first one each turn, take 1 " + \
                             "irreducible damage or take a minor twist.",
                             2,
                             pq_reqs=[Category(1,0)])
a_reactive_strike = Ability("Reactive Strike",
                            "R",
                            "When you are Attacked and dealt damage, you may Attack the " + \
                            "source of that damage by rolling your single %p0 die, plus the " + \
                            "amount of damage you take.",
                            2,
                            pq_reqs=[Category(1,0)],
                            pq_opts=[Category(1,0)],
                            categories=[1,2])
a_charged_up_blast = Ability("Charged Up Blast",
                             "A",
                             "Attack using %p0 and at least one bonus. Use your Max+Mid+Min " + \
                             "dice. Destroy all of your bonuses, adding each of them to this " + \
                             "Attack first, even if they are exclusive.",
                             2,
                             pq_reqs=[[[1,2,1]] + Category(1,1)],
                             pq_opts=[[[1,2,1]] + Category(1,1)],
                             categories=[1,2])
a_eruption = Ability("Eruption",
                     "A",
                     "Attack up to three targets (one of which must be you) using %p0. Assign " + \
                     "your Min, Mid, and Max dice as you choose among those targets.",
                     2,
                     pq_reqs=[Category(1,1)],
                     pq_opts=[Category(1,1)],
                     categories=[1,2])
a_improved_immunity = Ability("Improved Immunity",
                              "I",
                              "If you would take damage from %e, ignore that damage and " + \
                              "Recover that amount instead. Use the value of the damage to " + \
                              "Boost yourself.",
                              2,
                              pq_reqs=[Category(1,1)])
a_powerful_strike = Ability("Powerful Strike",
                            "A",
                            "Attack using %p0. Use your Max+Mid dice.",
                            2,
                            pq_reqs=[Category(1,1) + Category(1,4) + Category(1,7)],
                            pq_opts=[Category(1,1) + Category(1,4) + Category(1,7)],
                            categories=[1,2])
a_purification = Ability("Purification",
                         "A",
                         "Remove all bonuses and penalties from the scene. You cannot use " + \
                         "this ability again this scene.",
                         2,
                         pq_reqs=[Category(1,1) + Category(0,1)])
a_summoned_allies = Ability("Summoned Allies",
                            "A",
                            "Use %p0 and create a number of d6 minions equal to your Mid die. " + \
                            "Choose the one same basic action that they each perform. They " + \
                            "all act at the start of your turn.",
                            2,
                            pq_reqs=[Category(1,1) + Category(1,4) + \
                                     Category(1,6) + Category(1,7)],
                            pq_opts=[Category(1,1) + Category(1,4) + \
                                     Category(1,6) + Category(1,7)],
                            categories=[1,2])
a_quick_exit = Ability("Quick Exit",
                       "A",
                       "Attack using %p0. Use your Max die. Hinder each nearby opponent with " + \
                       "your Mid die. After using this ability, you and up to 2 allies may " + \
                       "end up anywhere in the scene, even outside of the action.",
                       2,
                       pq_reqs=[[[1,2,0]]],
                       pq_opts=[[[1,2,0]]],
                       pq_ids=[[1,2,0]])
a_sacrificial_ram = Ability("Sacrificial Ram",
                            "A",
                            "Attack up to three nearby targets using %p0. Use your Max+Mid " + \
                            "dice against each of them. You cannot use your %p0 power for the " + \
                            "rest of this scene and until it is recovered/repaired.",
                            2,
                            pq_reqs=[[[1,2,0]]],
                            pq_opts=[[[1,2,0]]],
                            pq_ids=[[1,2,0]])
a_ultimate_weaponry = Ability("Ultimate Weaponry",
                              "A",
                              "Boost using %p0. Use your Max die. That bonus is persistent " + \
                              "and exclusive. Then, Attack using your Mid die plus that bonus.",
                              2,
                              pq_reqs=[Category(1,2) + Category(1,8)],
                              pq_opts=[Category(1,2) + Category(1,8)])
a_calculated_dodge = Ability("Calculated Dodge",
                             "R",
                             "You may take 1 irreducible damage to reroll the dice pool of a " + \
                             "target that is Attacking or Hindering you.",
                             2,
                             pq_reqs=[Category(1,3) + Category(1,5)])
a_give_time = Ability("Give Time",
                      "A",
                      "Boost another hero using %p0. If that hero has already acted for the " + \
                      "turn, use your Max die, and that hero loses Health equal to your Min " + \
                      "die. That hero acts next in the turn order.",
                      2,
                      pq_reqs=[Category(1,3) + Category(1,6)],
                      pq_opts=[Category(1,3) + Category(1,6)],
                      categories=[1,2])
a_reliable_aptitude = Ability("Reliable Aptitude",
                              "I",
                              "When taking any action using %p0, you may reroll your Min die " + \
                              "before determining effects.",
                              2,
                              pq_reqs=[Category(1,3) + Category(0,0)],
                              pq_opts=[Category(1,3) + Category(0,0)])
a_unerring_strike = Ability("Unerring Strike",
                            "A",
                            "Attack using %p0. Use your Max+Min dice. Ignore all penalties on " + \
                            "this attack, ignore any Defend actions, and it cannot be " + \
                            "affected by Reactions.",
                            2,
                            pq_reqs=[Category(1,3)],
                            pq_opts=[Category(1,3)],
                            categories=[1,2])
a_field_of_hazards = Ability("Field of Hazards",
                             "A",
                             "Hinder any number of targets in the scene using %p0. Use your " + \
                             "Max+Min dice. If you roll doubles, also Attack each target " + \
                             "using your Mid die.",
                             2,
                             pq_reqs=[Category(1,4)],
                             pq_opts=[Category(1,4)],
                             categories=[1,2])
a_impenetrable_defense = Ability("Impenetrable Defense",
                                 "A",
                                 "Defend using %p0 against all Attacks against you until your " + \
                                 "next turn using your Max+Mid dice.",
                                 2,
                                 pq_reqs=[Category(1,4) + Category(1,6) + Category(1,7)],
                                 pq_opts=[Category(1,4) + Category(1,6) + Category(1,7)],
                                 categories=[1,2])
a_like_the_wind = Ability("Like the Wind",
                          "R",
                          "When you are Attacked and dealt damage, you may ignore that damage " + \
                          "completely. If you do, treat the value of the damage as a Hinder " + \
                          "action against you instead.",
                          2,
                          pq_reqs=[Category(1,4)])
a_heroic_interruption = Ability("Heroic Interruption",
                                "R",
                                "When an Attack deals damage to a nearby hero in the Red " + \
                                "zone, you may take 1d6 irreducible damage to redirect that " + \
                                "Attack to a target of your choice, other than the source of " + \
                                "the Attack.",
                                2,
                                pq_reqs=[Category(1,5)])
a_intercession = Ability("Intercession",
                         "R",
                         "When multiple nearby heroes are Attacked, you may take all the " + \
                         "damage instead. If you do, roll your %p0 die + Red zone die and " + \
                         "Defend against the Attack by the total.",
                         2,
                         pq_reqs=[Category(1,5)],
                         pq_opts=[Category(1,5)],
                         categories=[1,2])
a_take_down = Ability("Take Down",
                      "A",
                      "Attack using %p0. Use your Max die. Then, Hinder that target using " + \
                      "your Mid+Min dice.",
                      2,
                      pq_reqs=[Category(1,5)],
                      pq_opts=[Category(1,5)],
                      categories=[1,2])
a_untouchable_movement = Ability("Untouchable Movement",
                                 "A",
                                 "Boost yourself using %p0. Use your Max+Min dice. Then, you " + \
                                 "may end up anywhere else in the scene, avoiding any dangers " + \
                                 "between your starting and ending locations.",
                                 2,
                                 pq_reqs=[Category(1,5)],
                                 pq_opts=[Category(1,5)],
                                 categories=[1,2])
a_dangerous_hinder = Ability("Dangerous Hinder",
                             "A",
                             "Hinder using %p0. Use your Max+Mid dice. If you roll doubles, " + \
                             "also Attack the target using your Mid+Min dice and take damage " + \
                             "equal to your Min die.",
                             2,
                             pq_reqs=[Category(1,6)],
                             pq_opts=[Category(1,6)],
                             categories=[1,2])
a_dire_control = Ability("Dire Control",
                         "A",
                         "Select a minion. That minion is now entirely under your control and " + \
                         "acts at the start of your turn. If you are incapacitated, you lose " + \
                         "control of this minion. You may also choose to release control of " + \
                         "this minion at any time. At the end of the scene, this minion is " + \
                         "defeated.",
                         2,
                         pq_reqs=[Category(1,6)])
a_final_wrath = Ability("Final Wrath",
                        "A",
                        "Attack using %p0. Use your Max+Mid+Min dice. Take a major twist.",
                        2,
                        pq_reqs=[Category(1,6) + Category(1,8) + Category(0,1)],
                        pq_opts=[Category(1,6) + Category(1,8) + Category(0,1)],
                        categories=[2,2])
a_impossible_knowledge = Ability("Impossible Knowledge",
                                 "I",
                                 "At the start of your turn, change any penalty into a bonus.",
                                 2,
                                 pq_reqs=[Category(1,6)])
a_change_self = Ability("Change Self",
                        "I",
                        "At the start of your turn, swap two of your power dice. They stay " + \
                        "swapped until changed again or the scene ends.",
                        2,
                        pq_reqs=[Category(1,7)])
a_empowerment = Ability("Empowerment",
                        "R",
                        "Whenever you are dealt damage, roll your single %p0 die to Defend " + \
                        "against the Attack and Boost yourself.",
                        2,
                        pq_reqs=[Category(1,7)],
                        pq_opts=[Category(1,7)],
                        categories=[1,2])
a_defensive_deflection = Ability("Defensive Deflection",
                                 "R",
                                 "When you would be dealt damage, you may roll your single " + \
                                 "%p0 die as a Defend against that damage and as an Attack " + \
                                 "against a nearby target other than the source of that damage.",
                                 2,
                                 pq_reqs=[Category(1,7)],
                                 pq_opts=[Category(1,7)],
                                 categories=[1,2])
a_mutable_form = Ability("Mutable Form",
                         "A",
                         "Choose three basic actions. Use %p0 in your pool and take one " + \
                         "action with your Max die, a different action with your Mid die, and " + \
                         "a third action with your Min die.",
                         2,
                         pq_reqs=[Category(1,7)],
                         pq_opts=[Category(1,7)],
                         categories=[1,2])
a_resurrection = Ability("Resurrection",
                         "I",
                         "Once per issue, if you would go to 0 Health, roll %p0 + %p1 + Red " + \
                         "zone die. Your Health becomes that number.",
                         2,
                         pq_reqs=[Category(1,7), Category(0,1) + Category(0,2)],
                         pq_opts=[Category(1,7), Category(0,1) + Category(0,2)],
                         categories=[1,0])
a_combustion = Ability("Combustion",
                       "A",
                       "Attack multiple nearby targets using %p0. Use your Max+Mid dice. Take " + \
                       "irreducible damage equal to your Min die.",
                       2,
                       pq_reqs=[Category(1,8)],
                       pq_opts=[Category(1,8)],
                       categories=[1,2])
a_full_defensive = Ability("Full Defensive",
                           "A",
                           "Hinder yourself by rolling your single %p0 die. You are immune to " + \
                           "damage until the start of your next turn. You cannot use this " + \
                           "ability again this scene.",
                           2,
                           pq_reqs=[Category(1,8)],
                           pq_opts=[Category(1,8)],
                           categories=[1,2])
a_unload = Ability("Unload",
                   "A",
                   "Attack multiple targets using %p0, using your Max+Min dice. If you roll " + \
                   "doubles, take a minor twist or damage equal to your Mid die.",
                   2,
                   pq_reqs=[Category(1,8)],
                   pq_opts=[Category(1,8)],
                   categories=[1,2])
a_critical_eye = Ability("Critical Eye",
                         "A",
                         "Select a target. Boost using %p0. Use your Max+Mid+Min dice. That " + \
                         "bonus must be used against that target before the end of your next " + \
                         "turn, or it is wasted.",
                         2,
                         pq_reqs=[Category(0,0)],
                         pq_opts=[Category(0,0)],
                         categories=[0,2])
a_discern_weakness = Ability("Discern Weakness",
                             "A",
                             "Remove a bonus on a target. Hinder that target using %p0. Use " + \
                             "your Max die, and that penalty is persistent and exclusive.",
                             2,
                             pq_reqs=[Category(0,0)],
                             pq_opts=[Category(0,0)],
                             categories=[0,2])
a_specialized_info = Ability("Specialized Info",
                             "A",
                             "Overcome using %p0. Use your Max+Min dice.",
                             2,
                             pq_reqs=[Category(0,0)],
                             pq_opts=[Category(0,0)],
                             categories=[0,2])
a_aware_response = Ability("Aware Response",
                           "R",
                           "After an opponent Attacks or Hinders you or a nearby ally, Attack " + \
                           "the opponent by rolling your single %p0 die.",
                           2,
                           pq_reqs=[Category(0,1)],
                           pq_opts=[Category(0,1)],
                           categories=[0,2])
a_canny_awareness = Ability("Canny Awareness",
                            "A",
                            "Overcome using %p0. Use your Max+Min dice. Hinder all nearby " + \
                            "opponents with your Mid die.",
                            2,
                            pq_reqs=[Category(0,1)],
                            pq_opts=[Category(0,1)],
                            categories=[0,2])
a_considered_planning = Ability("Considered Planning",
                                "A",
                                "Boost using %p0 and use your Max die. Defend against all " + \
                                "Attacks against you using your Mid die until your next turn. " + \
                                "Note your Min die- as a Reaction, until your next turn, you " + \
                                "may Hinder an attacker using that die.",
                                2,
                                pq_reqs=[Category(0,1)],
                                pq_opts=[Category(0,1)],
                                categories=[0,2])
a_harmony = Ability("Harmony",
                    "I",
                    "As long as you have at least one bonus created from %p0, treat your %p1 " + \
                    "die as one size higher (max d12).",
                    2,
                    pq_reqs=[Category(0,1)],
                    pq_opts=[Category(0,1)],
                    categories=[0,1])
a_book_it = Ability("Book It",
                    "A",
                    "Hinder any number of close targets using %p0. Use your Max die. End your " + \
                    "turn elsewhere in the scene.",
                    2,
                    pq_reqs=[Category(0,2)],
                    pq_opts=[Category(0,2)],
                    categories=[0,2])
a_endurance_fighting = Ability("Endurance Fighting",
                               "I",
                               "Whenever you Attack a target with an action, also Hinder that " + \
                               "target with your Min die.",
                               2,
                               pq_reqs=[Category(0,2)])
a_finishing_blow = Ability("Finishing Blow",
                           "A",
                           "Attack using %p0. Use your Max die. Remove any number of " + \
                           "penalties from the target. Add your Min die to the Attack each " + \
                           "time you remove a penalty.",
                           2,
                           pq_reqs=[Category(0,2)],
                           pq_opts=[Category(0,2)],
                           categories=[0,2])
a_reactive_defense = Ability("Reactive Defense",
                             "R",
                             "When an opponent Attacks, you may become the target of that " + \
                             "Attack and Defend by rolling your single %p0 die.",
                             2,
                             pq_reqs=[Category(0,2)],
                             pq_opts=[Category(0,2)],
                             categories=[0,2])
a_heroic_sacrifice = Ability("Heroic Sacrifice",
                             "R",
                             "When an opponent Attacks, you may become the target of the " + \
                             "Attack and Defend by rolling your single Red zone die.",
                             2,
                             pq_reqs=[Category(0,3)])
a_inspiring_totem = Ability("Inspiring Totem",
                            "I",
                            "When you use an ability action, you may also perform any one " + \
                            "basic action using your Mid die on the same roll.",
                            2,
                            pq_reqs=[Category(0,3)])
a_lead_by_example = Ability("Lead by Example",
                            "A",
                            "Take a basic action using %p0. Use your Max die. All other " + \
                            "heroes who take the same basic action on their turn against the " + \
                            "same target receive a Boost from your Mid+Min dice.",
                            2,
                            pq_reqs=[Category(0,3)],
                            pq_opts=[Category(0,3)],
                            categories=[0,2])
a_ultimatum = Ability("Ultimatum",
                      "A",
                      "Hinder using %p0. Use your Max+Min dice. Boost yourself or an ally " + \
                      "with your Mid die.",
                      2,
                      pq_reqs=[Category(0,3)],
                      pq_opts=[Category(0,3)],
                      categories=[0,2])
a_width = 100

global ra_athletic, ra_elemental, ra_hallmark, ra_intellectual, ra_materials, ra_mobility
global ra_psychic, ra_self_control, ra_technological, ra_information, ra_mental, ra_physical
global ra_social, ra_collection, ra_minion_maker
ra_athletic = [a_major_regeneration, a_paragon_feat, a_push_your_limits, a_reactive_strike]
ra_elemental = [a_charged_up_blast, a_eruption, a_improved_immunity, a_powerful_strike,
                a_purification, a_summoned_allies]
ra_hallmark = [a_charged_up_blast, a_quick_exit, a_sacrificial_ram, a_ultimate_weaponry]
ra_intellectual = [a_calculated_dodge, a_give_time, a_reliable_aptitude, a_unerring_strike]
ra_materials = [a_field_of_hazards, a_impenetrable_defense, a_like_the_wind, a_powerful_strike,
                a_summoned_allies]
ra_mobility = [a_calculated_dodge, a_heroic_interruption, a_intercession, a_take_down,
               a_untouchable_movement]
ra_psychic = [a_dangerous_hinder, a_dire_control, a_final_wrath, a_give_time, a_impenetrable_defense,
              a_impossible_knowledge, a_summoned_allies]
ra_self_control = [a_change_self, a_empowerment, a_impenetrable_defense, a_major_regeneration,
                   a_defensive_deflection, a_mutable_form, a_powerful_strike, a_resurrection, a_summoned_allies]
ra_technological = [a_combustion, a_final_wrath, a_full_defensive, a_ultimate_weaponry, a_unload]
ra_information = [a_critical_eye, a_discern_weakness, a_reliable_aptitude, a_specialized_info]
ra_mental = [a_aware_response, a_canny_awareness, a_considered_planning, a_final_wrath, a_harmony,
             a_purification]
ra_physical = [a_book_it, a_endurance_fighting, a_finishing_blow, a_reactive_defense]
ra_social = [a_heroic_sacrifice, a_inspiring_totem, a_lead_by_example, a_ultimatum]
ra_collection = [[ra_information, ra_mental, ra_physical, ra_social],
                 [ra_athletic, ra_elemental, ra_hallmark, ra_intellectual, ra_materials, ra_mobility, ra_psychic, ra_self_control, ra_technological]]
ra_minion_maker = [a_construction_focus, a_swarm_combat, a_sacrifice]

global ps_accident, ps_training, ps_genetic, ps_experimentation, ps_mystical, ps_nature, ps_relic
global ps_powered_suit, ps_radiation, ps_tech_upgrades, ps_supernatural, ps_artificial_being
global ps_cursed, ps_alien, ps_genius, ps_cosmos, ps_extradimensional, ps_unknown, ps_higher_power
global ps_the_multiverse, ps_collection, ps_width, ps_special
ps_accident = ["Accident",
               "An external source caused you to manifest powers, or perhaps the cure for an " + \
               "accident caused it.",
               [],
               Category(1,0) + Category(1,1) + Category(1,3) + Category(1,4) + Category(1,6) + \
               Category(1,7),
               2,
               [a_area_alteration, a_inflict, a_reflexive_burst],
               1,
               [a_ambush_awareness, a_change_in_circumstance, a_immunity],
               0,
               [12,6]]
# Required Powers:        none
# Optional Powers:        any Athletic, any Elemental/Energy, any Intellectual, any Materials,
#                         any Psychic, any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Area Alteration, Inflict, Reflexive Burst
# Green Ability Qty:      1
# Green Ability Options:  Ambush Awareness, Change in Circumstance, Immunity
# Bonus:                  none
# Archetype Dice:         1d12 + 1d6
ps_training = ["Training",
               "The source of your powers is the result of your hard work, dedication, and " + \
               "long hours.",
               [],
               [[1,8,0]] + Category(1,2) + Category(1,0) + Category(1,3),
               2,
               [a_always_be_prepared, a_reactive_field, a_flowing_fight],
               0,
               [],
               1,
               [10,8,8]]
# Required Powers:        none
# Optional Powers:        Gadgets, any Hallmark, any Athletic, any Intellectual
# Yellow Ability Qty:     2
# Yellow Ability Options: Always Be Prepared, Reactive Field, Flowing Fight
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d8 Quality from Archetype
# Archetype Dice:         1d10 + 2d8
ps_genetic = ["Genetic",
              "Mutations in your DNA have caused you to develop unusual abilities.",
              [],
              [[1,0,0], [1,5,0], [1,2,1], [1,0,2], [1,0,3]] + Category(1,3) + Category(1,6),
              2,
              [a_danger_sense, a_adaptive, a_area_assault],
              1,
              [a_growth, a_rally],
              0,
              [10,8,8]]
# Required Powers:        none
# Optional Powers:        Agility, Flight, Signature Weaponry, Strength, Vitality,
#                         any Intellectual, any Psychic
# Yellow Ability Qty:     2
# Yellow Ability Options: Danger Sense, Adaptive, Area Assault
# Green Ability Qty:      1
# Green Ability Options:  Growth, Rally
# Bonus:                  none
# Archetype Dice:         1d10 + 2d8
ps_experimentation = ["Experimentation",
                      "Your powers were created in a lab and had some unexpected side effects.",
                      [],
                      [[1,2,1]] + Category(1,0) + Category(1,1) + Category(1,3) + Category(1,5) + \
                      Category(1,7),
                      2,
                      [a_personal_upgrade, a_misdirection, a_throw_minion],
                      1,
                      [a_overpower, a_unflagging],
                      0,
                      [8,8,8]]
# Required Powers:        none
# Optional Powers:        Signature Weaponry, any Athletic, any Elemental/Energy, any Intellectual,
#                         any Mobility, any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Personal Upgrade, Misdirection, Throw Minion
# Green Ability Qty:      1
# Green Ability Options:  Overpower, Unflagging
# Bonus:                  none
# Archetype Dice:         3d8
ps_mystical = ["Mystical",
               "Your magical training or alteration by magic gives you your powers.",
               [],
               [[1,3,0], [1,5,0], [1,3,4], [1,2,1], [1,5,5]] + Category(1,1) + Category(1,4) + \
               Category(1,6) + Category(1,7),
               2,
               [a_modification_wave, a_mystic_redirection, a_sever_link],
               0,
               [],
               2,
               [10,8,8]]
# Required Powers:        none
# Optional Powers:        Awareness, Flight, Presence, Signature Weaponry, Teleportation,
#                         any Elemental/Energy, any Materials, any Psychic, any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Modification Wave, Mystic Redirection, Sever Link
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d10 Information Quality
# Archetype Dice:         1d10 + 2d8
ps_nature = ["Nature",
             "The power of nature flows through you.",
             [],
             [[1,6,0], [1,1,0], [1,1,2], [1,1,3], [1,5,0], [1,5,1], [1,7,7], [1,5,3], [1,5,4],
              [1,5,6], [1,1,8]] + Category(1,0) + Category(1,4),
             2,
             [a_call_to_the_wild, a_predators_eye, a_wild_strength],
             1,
             [a_grasping_vines, a_natural_weapon],
             0,
             [10,8,8]]
# Required Powers:        none
# Optional Powers:        Animal Control, Cold, Electricity, Fire, Flight, Leaping, Shapeshifting,
#                         Swimming, Swinging, Wall-Crawling, Weather, any Athletic, any Materials
# Yellow Ability Qty:     2
# Yellow Ability Options: Call to the Wild, Predator's Eye, Wild Strength
# Green Ability Qty:      1
# Green Ability Options:  Grasping Vines, Natural Weapon
# Bonus:                  none
# Archetype Dice:         1d10 + 2d8
ps_relic = ["Relic",
            "An object (or collection of objects) of mystic significance either grants you " + \
            "powers or altered you to give you powers.",
            [],
            [[1,3,0], [1,3,2]] + Category(1,2) + Category(1,1) + Category(1,4) + Category(1,5) + \
            Category(1,6) + Category(1,7),
            2,
            [a_harvest_life_force, a_magical_shield, a_momentary_power, a_relic_drain],
            1,
            [a_draw_power, a_punishment],
            0,
            [10,10,6]]
# Required Powers:        none
# Optional Powers:        Awareness, Intuition, any Hallmark, any Elemental/Energy, any Materials,
#                         any Mobility, any Psychic, any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Harvest Life Force, Magical Shield, Momentary Power, Relic Drain
# Green Ability Qty:      1
# Green Ability Options:  Draw Power, Punishment
# Bonus:                  none
# Archetype Dice:         2d10 + 1d6
ps_powered_suit = ["Powered Suit",
                   "An engineered suit provides you with your powers, and may even be " + \
                   "important to keeping you alive.",
                   [[1,8,2]],
                   [[1,3,0], [1,1,0], [1,7,3], [1,1,2], [1,1,3], [1,3,3], [1,1,5], [1,7,6]] + \
                   Category(1,2) + Category(1,0) + Category(1,5),
                   2,
                   [a_energy_converter, a_explosive_attack, a_onboard_upgrade],
                   1,
                   [a_damage_reduction, a_diagnostic_subroutine],
                   0,
                   [10,6,6]]
# Required Powers:        Power Suit
# Optional Powers:        Awareness, Cold, Elasticity, Electricity, Fire, Lightning Calculator,
#                         Nuclear, Part Detachment, any Hallmark, any Athletic, any Mobility
# Yellow Ability Qty:     2
# Yellow Ability Options: Energy Converter, Explosive Attack, Onboard Upgrade
# Green Ability Qty:      1
# Green Ability Options:  Damage Reduction, Diagnostic Subroutine
# Bonus:                  none
# Archetype Dice:         1d10 + 2d6
ps_radiation = ["Radiation",
                "Exposure to radiation has charged your system and given you new abilities.",
                [],
                [[1,1,5]] + Category(1,2) + Category(1,0) + Category(1,7) + Category(1,8),
                2,
                [a_radioactive_recharge, a_unstable_reaction, a_wither],
                1,
                [a_charged_up, a_dangerous_lash, a_radioactive_aura],
                0,
                [10,8,6]]
# Required Powers:        none
# Optional Powers:        Nuclear, any Hallmark, any Athletic, any Self Control, any Technological
# Yellow Ability Qty:     2
# Yellow Ability Options: Radioactive Recharge, Unstable Reaction, Wither
# Green Ability Qty:      1
# Green Ability Options:  Charged Up, Dangerous Lash, Radioactive Aura
# Bonus:                  none
# Archetype Dice:         1d10 + 1d8 + 1d6
ps_tech_upgrades = ["Tech Upgrades",
                    "You have technological upgrades and implants that give you your powers.",
                    [],
                    Category(1,2) + Category(1,0) + Category(1,1) + Category(1,3) + \
                    Category(1,5) + Category(1,8),
                    2,
                    [a_energy_burst, a_recharge, a_techno_absorb, a_tactical_analysis],
                    1,
                    [a_indiscriminate_fabrication, a_organi_hack],
                    0,
                    [10,8,8]]
# Required Powers:        none
# Optional Powers:        any Hallmark, any Athletic, any Elemental/Energy, any Intellectual,
#                         any Mobility, any Technological
# Yellow Ability Qty:     2
# Yellow Ability Options: Energy Burst, Recharge, Techno-Absorb, Tactical Analysis
# Green Ability Qty:      1
# Green Ability Options:  Indiscriminate Fabrication, Organi-Hack
# Bonus:                  none
# Archetype Dice:         1d10 + 2d8
ps_supernatural = ["Supernatural",
                   "In some way, you have pierced the veil of life and reality and brought " + \
                   "back power.",
                   [],
                   [[1,3,0], [1,1,0], [1,1,2], [1,1,3], [1,1,4], [1,4,1], [1,3,4], [1,1,6],
                    [1,0,2], [1,4,4], [1,0,3], [1,1,8]] + Category(1,5) + Category(1,6) + \
                   Category(1,7),
                   2,
                   [a_area_healing, a_mass_modification, a_personal_upgrade, a_reach_through_veil],
                   0,
                   [],
                   3,
                   [10,10,6]]
# Required Powers:        none
# Optional Powers:        Awareness, Cold, Electricity, Fire, Infernal, Plants, Presence, Radiant,
#                         Strength, Transmutation, Vitality, Weather, any Mobility, any Psychic,
#                         any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Area Healing, Mass Modification, Personal Upgrade, Reach through Veil
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d10 Power not on the above list
# Archetype Dice:         2d10 + 1d6
ps_artificial_being = ["Artificial Being",
                       "You were created, not born, and your abilities simply stem from your " + \
                       "makeup.",
                       [],
                       [[1,8,1], [1,8,3]] + Category(1,2) + Category(1,0) + Category(1,1) + \
                       Category(1,3) + Category(1,5) + Category(1,7),
                       2,
                       [a_created_immunity, a_multiple_assault, a_recalculating],
                       1,
                       [a_created_form, a_intentionality],
                       0,
                       [10,8,8]]
# Required Powers:        none
# Optional Powers:        Inventions, Robotics, any Hallmark, any Athletic, any Elemental/Energy,
#                         any Intellectual, any Mobility, any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Created Immunity, Multiple Assault, Recalculating...
# Green Ability Qty:      1
# Green Ability Options:  Created Form, Intentionality
# Bonus:                  none
# Archetype Dice:         1d10 + 2d8
ps_cursed = ["Cursed",
             "A supernatural curse has been inflicted upon you and/or your family line, " + \
             "granting both boons and banes.",
             [],
             [[1,2,1]] + Category(1,0) + Category(1,1) + Category(1,4) + Category(1,7),
             2,
             [a_attunement, a_costly_strength, a_cursed_resolve],
             1,
             [a_double_edged_luck, a_extremes],
             0,
             [12,6]]
# Required Powers:        none
# Optional Powers:        Signature Weaponry, any Athletic, any Elemental/Energy, any Materials,
#                         any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Attunement, Costly Strength, Cursed Resolve
# Green Ability Qty:      1
# Green Ability Options:  Double Edged Luck, Extremes
# Bonus:                  none
# Archetype Dice:         1d12 + 1d6
ps_alien = ["Alien",
            "You are not from Earth, though your powers might not be all that unusual where " + \
            "you come from. Or you've been granted abilities by an extraterrestrial source.",
            [],
            Category(1,2) + Category(1,0) + Category(1,1) + Category(1,3) + Category(1,5) + \
            Category(1,6) + Category(1,8),
            2,
            [a_alien_boost, a_empower_and_repair, a_halt],
            0,
            [],
            4,
            [8,8,8]]
# Required Powers:        none
# Optional Powers:        any Hallmark, any Athletic, any Elemental/Energy, any Intellectual,
#                         any Mobility, any Psychic, any Technological
# Yellow Ability Qty:     2
# Yellow Ability Options: Alien Boost, Empower and Repair, Halt
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  Upgrade a d6 Power/Quality to d8; if you can't, gain a bonus d6 Power
#                         from the above list
# Archetype Dice:         3d8
ps_genius = ["Genius",
             "The source of your powers is your brilliant mind. You have put your staggering " + \
             "intellect to the task of fighting crime.",
             [],
             [[1,8,1], [1,8,3]] + Category(1,2) + Category(1,3),
             2,
             [a_a_plan_for_everything, a_expanded_mind, a_overwhelming_vision],
             0,
             [],
             5,
             [10,6,6]]
# Required Powers:        none
# Optional Powers:        Inventions, Robotics, any Hallmark, any Intellectual
# Yellow Ability Qty:     2
# Yellow Ability Options: A Plan for Everything, Expanded Mind, Overwhelming Vision
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d10 Information or Mental Quality
# Archetype Dice:         1d10 + 2d6
ps_cosmos = ["Cosmos",
             "Exposure to forces from beyond the stars have changed you.",
             [],
             [[1,1,1], [1,3,2]] + Category(1,2) + Category(1,5) + Category(1,6) + Category(1,7) + \
             Category(1,8),
             2,
             [a_cosmic_ray_absorption, a_encourage, a_mass_adjust],
             0,
             [],
             6,
             [10,8,8]]
# Required Powers:        none
# Optional Powers:        Cosmic, Intuition, any Hallmark, any Mobility, any Psychic,
#                         any Self Control, any Technological
# Yellow Ability Qty:     2
# Yellow Ability Options: Cosmic Ray Absorption, Encourage, Mass Adjust
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  Downgrade a d8+ Power one size and upgrade a d10- Power one size
# Archetype Dice:         1d10 + 2d8
ps_extradimensional = ["Extradimensional",
                       "Exposure to side dimensions like the Realm of Discord has left its " + \
                       "mark on you.",
                       [],
                       [[1,1,1], [1,7,2], [1,1,4], [1,7,4], [1,7,5], [1,1,6], [1,4,4], [1,5,5]] + \
                       Category(1,2) + Category(1,3) + Category(1,6),
                       2,
                       [a_absorb_essence, a_aura_of_pain, a_bizarre_strike],
                       1,
                       [a_attune, a_extrasensory_awareness],
                       0,
                       [12,6]]
# Required Powers:        none
# Optional Powers:        Cosmic, Duplication, Infernal, Intangibility, Invisibility, Radiant,
#                         Transmutation, Teleportation, any Hallmark, any Intellectual,
#                         any Psychic
# Yellow Ability Qty:     2
# Yellow Ability Options: Absorb Essence, Aura of Pain, Bizarre Strike
# Green Ability Qty:      1
# Green Ability Options:  Attune, Extrasensory Awareness
# Bonus:                  none
# Archetype Dice:         1d12 + 1d6
ps_unknown = ["Unknown",
              "You don't know the source of your powers: they either just manifested one day, " + \
              "or hint at a bigger mystery.",
              [],
              Category(1,1) + Category(1,3) + Category(1,4) + Category(1,7) + Category(1,8),
              2,
              [a_brainstorm, a_strange_enhancement, a_volatile_creations],
              0,
              [],
              7,
              [10,8,6]]
# Required Powers:        none
# Optional Powers:        any Elemental/Energy, any Intellectual, any Materials, any Self Control,
#                         any Technological
# Yellow Ability Qty:     2
# Yellow Ability Options: Brainstorm, Strange Enhancement, Volatile Creations
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d8 Social Quality
# Archetype Dice:         1d10 + 1d8 + 1d6
ps_higher_power = ["Higher Power",
                   "You have been chosen by a higher force to carry out their work and have " + \
                   "been given powers to make it happen; or you are a being from another " + \
                   "realm, incarnated into a physical body, and your powers are a reflection " + \
                   "of your true form.",
                   [],
                   Category(1,0) + Category(1,1) + Category(1,4) + Category(1,6) + Category(1,7),
                   2,
                   [a_command_power, a_dangerous_explosion, a_embolden, a_resolve],
                   1,
                   [a_resilience, a_twist_reality],
                   0,
                   [10,8,8]]
# Required Powers:        none
# Optional Powers:        any Athletic, any Elemental/Energy, any Materials, any Psychic,
#                         any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Command Power, Dangerous Explosion, Embolden, Resolve
# Green Ability Qty:      1
# Green Ability Options:  Resilience, Twist Reality
# Bonus:                  none
# Archetype Dice:         1d10 + 2d8
ps_the_multiverse = ["The Multiverse",
                     "Your origin comes from traveling or being flung through the infinitely " + \
                     "branching realms of time and space. Without the Multiverse itself, you " + \
                     "would not have the powers you do now.",
                     [],
                     [[1,3,0], [1,1,1], [1,3,2], [1,0,1], [1,5,5]] + Category(1,6) + Category(1,7),
                     2,
                     [a_power_from_beyond, a_respond_in_kind, a_dread_pallor, a_reality_scorned],
                     0,
                     [],
                     8,
                     [10,8,6]]
# Required Powers:        none
# Optional Powers:        Awareness, Cosmic, Intuition, Speed, Teleportation, any Psychic,
#                         any Self Control
# Yellow Ability Qty:     2
# Yellow Ability Options: Power from Beyond, Respond in Kind, Dread Pallor, Reality Scorned
# Green Ability Qty:      0
# Green Ability Options:  none
# Bonus:                  d6 Power from any category
# Archetype Dice:         1d10 + 1d8 + 1d6
ps_collection = [ps_accident,
                 ps_training,
                 ps_genetic,
                 ps_experimentation,
                 ps_mystical,
                 ps_nature,
                 ps_relic,
                 ps_powered_suit,
                 ps_radiation,
                 ps_tech_upgrades,
                 ps_supernatural,
                 ps_artificial_being,
                 ps_cursed,
                 ps_alien,
                 ps_genius,
                 ps_cosmos,
                 ps_extradimensional,
                 ps_unknown,
                 ps_higher_power,
                 ps_the_multiverse]
ps_width = 100
ps_special = ["",
              "Bonus d8 Quality from Archetype",
              "Bonus d10 Information Quality",
              "Bonus d10 Power that ISN'T listed above",
              "Upgrade a d6 Power or Quality to d8; if you can't, gain a bonus d6 Power " + \
              "listed above.",
              "Bonus d10 Information or Mental Quality",
              "Downgrade a Power by 1 die size and upgrade another Power by 1 die size.",
              "Bonus d8 Social Quality",
              "Bonus d6 Power from ANY category"]

global arc_speedster, arc_shadow, arc_physical_powerhouse, arc_marksman, arc_blaster
global arc_close_quarters_combatant, arc_armored, arc_flier, arc_elemental_manipulator
global arc_robot_cyborg, arc_sorceror, arc_psychic, arc_transporter, arc_minion_maker
global arc_wild_card, arc_form_changer, arc_gadgeteer, arc_reality_shaper, arc_divided
global arc_modular, arc_collection, arc_special, arc_width
arc_speedster = ["Speedster",
                 "Sorrygottagobeintwelveplacesatonce...",
                 [[1,0,1]],
                 2,
                 2,
                 [[1,0,0], [1,7,4], [1,3,3], [1,0,3]] + Category(1,5),
                 Category(0,1) + Category(0,2),
                 [],
                 2,
                 1,
                 [a_always_on_the_move, a_fast_fingers, a_non_stop_assault],
                 [a_blinding_strike, a_flurry_of_fists, a_supersonic_streak, a_speedy_analysis],
                 [],
                 False,
                 -1,
                 99,
                 0,
                 True,
                 1,
                 0]
# Primary Power/Quality:  Speed
# If already present:     Skip or swap out
# Secondary Power Qty:    1 or more
# Secondary Powers:       Agility, Intangibility, Lightning Calculator, Vitality, any Mobility
# Tertiary PQs:           any Mental, any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Always on the Move, Fast Fingers, Non-Stop Assault
# Yellow Ability Options: Blinding Strike, Flurry of Fists, Supersonic Streak, Speedy Analysis
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  all
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  Yes
# Principle Category:     Expertise
# Archetype Bonus:        none
arc_shadow = ["Shadow",
              "You operate in the shadows via subtlety and guile.",
              [[0,2,5]],
              2,
              0,
              [],
              [[1,7,4], [1,7,5], [1,2,1]] + Category(1,0) + [[0,2,m] for m in range(5)],
              [],
              2,
              1,
              [a_sabotage, a_shadowy_figure, a_untouchable],
              [a_overcome_from_the_darkness, a_diversion],
              [],
              False,
              -1,
              99,
              0,
              True,
              1,
              0]
# Primary Power/Quality:  Stealth
# If already present:     Skip or swap out
# Secondary Power Qty:    0
# Secondary Powers:       none
# Tertiary PQs:           Intangibility, Invisibility, Signature Weaponry, any Athletic, 
#                         any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Sabotage, Shadowy Figure, Untouchable
# Yellow Ability Options: Overcome from the Darkness, Diversion
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  Yes
# Principle Category:     Expertise
# Archetype Bonus:        none
arc_physical_powerhouse = ["Physical Powerhouse",
                           "You are the brute squad.",
                           [[1,0,2]],
                           2,
                           1,
                           [[1,7,1], [1,5,1], [1,2,1], [1,7,8]] + Category(1,0),
                           Category(0,2) + Category(0,3),
                           [],
                           2,
                           1,
                           [],
                           [],
                           [a_damage_resistant, a_frontline_fighting, a_galvanize, a_power_strike,
                            a_strength_in_victory],
                           False,
                           -1,
                           99,
                           0,
                           True,
                           1,
                           0]
# Primary Power/Quality:  Strength
# If already present:     Skip or swap out
# Secondary Power Qty:    1
# Secondary Powers:       Density Control, Leaping, Signature Weaponry, Size-Changing, any Athletic
# Tertiary PQs:           any Physical, any Social
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    Damage Resistant, Frontline Fighting, Galvanize, Power Strike, 
#                         Strength in Victory
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  Yes
# Principle Category:     Expertise
# Archetype Bonus:        none
arc_marksman = ["Marksman",
                "Whether it's guns, a bow and arrow, or something else, you know your aim is true.",
                [[1,2,1]],
                2,
                2,
                [[1,2,0], [1,5,4]] + Category(1,0) + Category(1,3) + Category(1,8),
                Category(0,0) + Category(0,1) + Category(0,2),
                [],
                2,
                2,
                [a_dual_wielder, a_load, a_precise_shot, a_sniper_aim, a_spin_and_shoot],
                [a_called_shot, a_exploding_ammo, a_hair_trigger_reflexes, a_ricochet],
                [],
                True,
                0,
                0,
                99,
                False,
                4,
                0]
# Primary Power/Quality:  Signature Weaponry
# If already present:     Skip or swap out
# Secondary Power Qty:    1 or more
# Secondary Powers:       Signature Vehicle, Swinging, any Athletic, any Intellectual, 
#                         any Technological
# Tertiary PQs:           any Information, any Mental, any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     2
# Green Ability Options:  Dual Wielder, Load, Precise Shot, Sniper Aim, Spin & Shoot
# Yellow Ability Options: Called Shot, Exploding Ammo, Hair Trigger Reflexes, Ricochet
# G/Y Ability Options:    none
# Primary PQ Required:    Yes
# G Category Required:    Quality
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: All
# Green Dice- Arc only?:  no
# Principle Category:     Responsibility
# Archetype Bonus:        none
arc_blaster = ["Blaster",
               "No need to mess around- the best way to use energy is to throw it at the bad guy.",
               Category(1,1),
               1,
               1,
               [[1,2,1]] + Category(1,1) + Category(1,5) + Category(1,8),
               Category(0,1) + Category(0,2),
               [],
               2,
               2,
               [a_exploit_vulnerability, a_disabling_blast, a_danger_zone, a_precise_hit],
               [a_energy_immunity, a_heedless_blast, a_imbue_with_element],
               [],
               False,
               -1,
               99,
               99,
               True,
               0,
               0]
# Primary Power/Quality:  any Elemental/Energy
# If already present:     Skip or choose another
# Secondary Power Qty:    1
# Secondary Powers:       Signature Vehicle, any Elemental/Energy, any Mobility, any Technological
# Tertiary PQs:           any Mental, any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     2
# Green Ability Options:  Exploit Vulnerability, Disabling Blast, Danger Zone, Precise Hit
# Yellow Ability Options: Energy Immunity, Heedless Blast, Imbue with Element
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  all
# Min Unique Yellow Dice: all
# Green Dice- Arc only?:  Yes
# Principle Category:     Esoteric
# Archetype Bonus:        none
arc_close_quarters_combatant = ["Close Quarters Combatant",
                                "You prefer to fight up close and personal.",
                                [[0,2,1]],
                                2,
                                2,
                                [[1,2,1]] + Category(1,0) + Category(1,5) + Category(1,8),
                                Category(0,2) + Category(0,3),
                                [],
                                3,
                                1,
                                [],
                                [],
                                [a_defensive_strike, a_dual_strike, a_flexible_stance,
                                 a_offensive_strike, a_precise_strike, a_throw_minion2],
                                True,
                                1,
                                0,
                                0,
                                False,
                                4,
                                0]
# Primary Power/Quality:  Close Combat
# If already present:     Skip or swap out
# Secondary Power Qty:    1 or more
# Secondary Powers:       Signature Weaponry, any Athletic, any Mobility, any Technological
# Tertiary PQs:           any Physical, any Social
# Mandatory Abilities:    none
# Green Ability Qty:      3
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    Defensive Strike, Dual Strike, Flexible Stance, Offensive Strike, 
#                         Precise Strike, Throw Minion (v2)
# Primary PQ Required:    Yes
# G Category Required:    Power
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Responsibility
# Archetype Bonus:        none
arc_armored = ["Armored",
               "You are an indomitable and unstoppable force.",
               [],
               0,
               2,
               Category(1,2) + Category(1,0) + Category(1,3) + Category(1,4) + Category(1,5) + \
               Category(1,8),
               Category(0,2) + Category(0,3),
               [a_armored],
               3,
               0,
               [a_deflect, a_dual_offense, a_living_bulwark, a_repair, a_unstoppable_charge],
               [],
               [],
               False,
               -1,
               2,
               0,
               False,
               1,
               1]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Hallmark, any Athletic, any Intellectual, any Materials, 
#                         any Mobility, any Technological
# Tertiary PQs:           any Physical, any Social
# Mandatory Abilities:    Armored
# Green Ability Qty:      3
# Yellow Ability Qty:     0
# Green Ability Options:  Deflect, Dual Offense, Living Bulwark, Repair, Unstoppable Charge
# Yellow Ability Options: none
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  2
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Expertise
# Archetype Bonus:        may use a Materials or Technological Power for Health
arc_flier = ["Flier",
             "The best way to support your team is from the air.",
             [[1,5,0], [1,2,0]],
             2,
             2,
             Category(1,2) + Category(1,0) + Category(1,5) + Category(1,8),
             Category(0,0) + Category(0,2),
             [],
             2,
             1,
             [],
             [],
             [a_aerial_bombardment, a_aerial_surveillance, a_barrel_roll, a_dive_and_drop,
              a_sonic_boom, a_strike_and_swoop],
             True,
             -1,
             0,
             0,
             False,
             2,
             0]
# Primary Power/Quality:  Flight or Signature Vehicle
# If already present:     Skip or swap out
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Hallmark, any Athletic, any Mobility, any Technological
# Tertiary PQs:           any Information, any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    Aerial Bombardment, Aerial Surveillance, Barrel Roll, Dive & Drop, 
#                         Sonic Boom, Strike & Swoop
# Primary PQ Required:    Yes
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Ideals
# Archetype Bonus:        none
arc_elemental_manipulator = ["Elemental Manipulator",
                             "Energies are yours to command and flow, sometimes through your " + \
                             "own body.",
                             Category(1,1),
                             2,
                             1,
                             [[1,7,0], [1,5,0], [1,5,1], [1,5,3], [1,4,4]] + Category(1,2) + \
                             Category(1,1),
                             [[0,0,3], [0,0,6]] + Category(0,1) + Category(0,2),
                             [],
                             2,
                             1,
                             [a_backlash, a_external_combustion, a_energy_conversion,
                              a_focused_apparatus],
                             [a_damage_spike, a_energy_alignment, a_energy_redirection,
                              a_live_dangerously],
                             [],
                             False,
                             -1,
                             0,
                             0,
                             False,
                             0,
                             0]
# Primary Power/Quality:  any Elemental/Energy
# If already present:     Skip or swap out
# Secondary Power Qty:    1
# Secondary Powers:       Absorption, Flight, Leaping, Swimming, Transmutation, any Hallmark, 
#                         any Elemental/Energy
# Tertiary PQs:           Magical Lore, Science, any Mental, any Physical
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Backlash, External Combustion, Energy Conversion, Focused Apparatus
# Yellow Ability Options: Damage Spike, Energy Alignment, Energy Redirection, Live Dangerously
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Esoteric
# Archetype Bonus:        none
arc_robot_cyborg = ["Robot/Cyborg",
                    "Your machine nature gives you adaptability and firepower.",
                    [],
                    0,
                    2,
                    Category(1,2) + Category(1,0) + Category(1,3) + Category(1,5) + \
                    Category(1,7) + Category(1,8),
                    Category(0,0) + Category(0,1),
                    [],
                    2,
                    1,
                    [],
                    [],
                    [a_adaptive_programming, a_living_arsenal, a_metal_skin, a_self_improvement,
                     a_something_for_everyone],
                    False,
                    -1,
                    99,
                    0,
                    False,
                    1,
                    2]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Hallmark, any Athletic, any Intellectual, any Mobility, 
#                         any Self-Control, any Technological
# Tertiary PQs:           any Information, any Mental
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    Adaptive Programming, Living Arsenal, Metal Skin, Self-Improvement, 
#                         Something for Everyone
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Expertise
# Archetype Bonus:        d10 Technological Power; you may use a Technological Power for Health
arc_sorceror = ["Sorcerer",
                "You command an arsenal of spells and mystical forces.",
                [],
                0,
                2,
                Category(1,1) + Category(1,4) + Category(1,5) + Category(1,6) + Category(1,7),
                Category(0,0) + Category(0,1),
                [],
                2,
                1,
                [a_banish, a_energy_jaunt, a_powerful_blast, a_subdue],
                [a_cords_of_magic, a_field_of_energy, a_living_bomb],
                [],
                False,
                -1,
                99,
                0,
                False,
                0,
                0]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Elemental/Energy, any Materials, any Mobility, any Psychic, 
#                         any Self-Control
# Tertiary PQs:           any Information, any Mental
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Banish, Energy Jaunt, Powerful Blast, Subdue
# Yellow Ability Options: Cords of Magic, Field of Energy, Living Bomb
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Esoteric
# Archetype Bonus:        none
arc_psychic = ["Psychic",
               "Mysterious mental abilities give you the ability to manifest a variety of " + \
               "powers with but a thought.",
               Category(1,6),
               0,
               2,
               Category(1,3) + Category(1,4) + Category(1,6) + Category(1,7),
               Category(0,1),
               [],
               2,
               2,
               [a_psychic_assault, a_psychic_coordination, a_psychic_insight],
               [a_astral_projection, a_illusionary_double, a_minion_suggestion,
                a_precognitive_alteration, a_postcognitive_understanding, a_psychic_analysis,
                a_swarm, a_telekinetic_assault, a_telepathic_whammy],
               [],
               False,
               -1,
               0,
               0,
               False,
               0,
               0]
# Primary Power/Quality:  any Psychic
# If already present:     none
# Secondary Power Qty:    1 or more(*)
# Secondary Powers:       any Intellectual, any Materials, any Psychic, any Self-Control(*)
# Tertiary PQs:           any Mental
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     2
# Green Ability Options:  Psychic Assault, Psychic Coordination, Psychic Insight
# Yellow Ability Options: Astral Projection, Illusionary Double, Minion Suggestion,
#                         Precognitive Alteration, Postcognitive Understanding, Psychic Analysis,
#                         Swarm, Telekinetic Assault, Telepathic Whammy
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Esoteric
# Archetype Bonus:        none
arc_transporter = ["Transporter",
                   "You know how to get exactly where you need to be, when you need to be there.",
                   [[1,2,0]] + Category(1,5),
                   2,
                   2,
                   [[1,2,0]] + Category(1,0) + Category(1,5) + Category(1,6) + Category(1,8),
                   Category(0,2) + Category(0,3),
                   [],
                   2,
                   1,
                   [],
                   [],
                   [a_displacement_assault, a_hit_and_run, a_mobile_dodge, a_mobile_assist,
                    a_run_down],
                   False,
                   -1,
                   99,
                   0,
                   False,
                   1,
                   0]
# Primary Power/Quality:  Signature Vehicle or any Mobility
# If already present:     Skip or swap out
# Secondary Power Qty:    1 or more
# Secondary Powers:       Signature Vehicle, any Athletic, any Mobility, any Psychic, 
#                         any Technological
# Tertiary PQs:           any Physical, any Social
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    Displacement Assault, Hit & Run, Mobile Dodge, Mobile Assist, Run Down
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Expertise
# Archetype Bonus:        none
arc_minion_maker = ["Minion-Maker",
                    "Who needs friends when you can just make them?",
                    [],
                    0,
                    2,
                    [[1,7,2], [1,8,1], [1,7,6], [1,8,3]] + Category(1,1) + Category(1,4),
                    Category(0,0) + Category(0,1),
                    [a_make_minion, a_power_up],
                    0,
                    1,
                    [],
                    [a_minion_formation, a_rapid_deployment, a_upgrade_minion],
                    [],
                    False,
                    -1,
                    99,
                    0,
                    False,
                    1,
                    0]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       Duplication, Inventions, Part Detachment, Robotics, any Elemental/Energy,
#                         any Materials
# Tertiary PQs:           any Information, any Mental
# Mandatory Abilities:    Make Minion, Power Up
# Green Ability Qty:      0
# Yellow Ability Qty:     1
# Green Ability Options:  none
# Yellow Ability Options: Minion Formation, Rapid Deployment, Upgrade Minion
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Expertise
# Archetype Bonus:        none (AddArchetype recognizes that Minion-Maker creates Minion Forms,
#                         AddRedAbility recognizes that Minion-Maker gets special Red options)
arc_wild_card = ["Wild Card",
                 "No one knows what you will do next- not the bad guys, not your allies, " + \
                 "sometimes not even you.",
                 [],
                 0,
                 2,
                 Category(1,2) + Category(1,0) + Category(1,3) + Category(1,5) + Category(1,7),
                 Category(0,2) + Category(0,3),
                 [],
                 2,
                 1,
                 [a_gimmick, a_multitask, a_surprise_results, a_unknown_results],
                 [a_break_the_4th, a_danger, a_expect_the_unexpected, a_imitation,
                  a_turn_the_tables],
                 [],
                 False,
                 -1,
                 99,
                 0,
                 False,
                 2,
                 0]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Hallmark, any Athletic, any Intellectual, any Mobility, 
#                         any Self Control
# Tertiary PQs:           any Physical, any Social
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Gimmick, Multitask, Surprise Results, Unknown Results
# Yellow Ability Options: Break the 4th, Danger!, Expect the Unexpected, Imitation, Turn the Tables
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Ideals
# Archetype Bonus:        none
arc_form_changer = ["Form-Changer",
                    "You can shift yourself between a few different forms.",
                    Category(1,7),
                    1,
                    2,
                    Category(1,0) + Category(1,5) + Category(1,7) + Category(1,8),
                    Category(0,0) + Category(0,2),
                    [a_change_forms, a_emergency_change],
                    1,
                    0,
                    [a_form_recovery, a_surprise_shift],
                    [],
                    [],
                    False,
                    -1,
                    0,
                    0,
                    False,
                    0,
                    3]
# Primary Power/Quality:  any Self-Control
# If already present:     Skip or choose another
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Athletic, any Mobility, any Self-Control, any Technological
# Tertiary PQs:           any Information, any Physical
# Mandatory Abilities:    Change Forms, Emergency Change
# Green Ability Qty:      1
# Yellow Ability Qty:     0
# Green Ability Options:  Form Recovery, Surprise Shift
# Yellow Ability Options: none
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Esoteric
# Archetype Bonus:        Create Forms
arc_gadgeteer = ["Gadgeteer",
                 "Any problem can be solved through sufficient brainpower.",
                 Category(1,3),
                 0,
                 2,
                 Category(1,2) + Category(1,3) + Category(1,5) + Category(1,6) + Category(1,8),
                 Category(0,0) + Category(0,1),
                 [],
                 2,
                 1,
                 [a_analyze_probabilities, a_analyze_weakness, a_equip, a_helpful_invention],
                 [a_helpful_analysis, a_snap_decision, a_turn_the_tables],
                 [],
                 False,
                 -1,
                 99,
                 0,
                 False,
                 3,
                 0]
# Primary Power/Quality:  any Intellectual
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       any Hallmark, any Intellectual, any Mobility, any Psychic, 
#                         any Technological
# Tertiary PQs:           any Information, any Mental
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Analyze Probabilities, Analyze Weakness, Equip, Helpful Invention
# Yellow Ability Options: Helpful Analysis, Snap Decision, Turn the Tables
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Identity
# Archetype Bonus:        none
arc_reality_shaper = ["Reality Shaper",
                      "God may not play dice with the universe, but you do.",
                      [],
                      0,
                      2,
                      [[1,7,1], [1,7,4], [1,7,5], [1,0,1], [1,5,5], [1,4,4]] + Category(1,3) + \
                      Category(1,6) + Category(1,8),
                      Category(0,0) + Category(0,1),
                      [],
                      2,
                      1,
                      [a_negative_likelihood, a_not_quite_right, a_probability_insight,
                       a_warp_space],
                      [a_alternate_outcome, a_helpful_analysis, a_never_happened,
                       a_retroactive_rewrite],
                      [],
                      False,
                      -1,
                      99,
                      0,
                      False,
                      1,
                      0]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    1 or more
# Secondary Powers:       Density Control, Intangibility, Invisibility, Speed, Teleportation, 
#                         Transmutation, any Intellectual, any Psychic, any Technological
# Tertiary PQs:           any Information, any Mental
# Mandatory Abilities:    none
# Green Ability Qty:      2
# Yellow Ability Qty:     1
# Green Ability Options:  Negative Likelihood, Not Quite Right, Probability Insight, Warp Space
# Yellow Ability Options: Alternate Outcome, Helpful Analysis, Never Happened, Retroactive Rewrite
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  All
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Expertise
# Archetype Bonus:        none
arc_divided = ["Divided",
               "You have two very different forms, such as an unpowered civilian form and a " + \
               "powered heroic form.",
               [],
               0,
               0,
               [],
               [],
               [],
               0,
               0,
               [],
               [],
               [],
               False,
               -1,
               0,
               0,
               False,
               4,
               4]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    0
# Secondary Powers:       none
# Tertiary PQs:           none
# Mandatory Abilities:    none
# Green Ability Qty:      0
# Yellow Ability Qty:     0
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     Responsibility
# Archetype Bonus:        Divided- gains PQs and Abilities from another Archetype, then chooses 
#                         transition type and build option
arc_modular = ["Modular",
               "You have multiple forms (configurations, fighting styles, etc.) that each " + \
               "give their own advantages and disadvantages.",
               [],
               0,
               0,
               [],
               [],
               [a_switch, a_quick_switch, a_emergency_switch],
               0,
               0,
               [],
               [],
               [],
               False,
               -1,
               0,
               0,
               False,
               -1,
               5]
# Primary Power/Quality:  none
# If already present:     none
# Secondary Power Qty:    none
# Secondary Powers:       none
# Tertiary PQs:           none
# Mandatory Abilities:    Switch, Quick Switch, Emergency Switch
# Green Ability Qty:      0
# Yellow Ability Qty:     0
# Green Ability Options:  none
# Yellow Ability Options: none
# G/Y Ability Options:    none
# Primary PQ Required:    no
# G Category Required:    none
# Min Unique Green Dice:  none
# Min Unique Yellow Dice: none
# Green Dice- Arc only?:  no
# Principle Category:     none
# Archetype Bonus:        Modular- gains PQs and Principle from another Archetype, creates Modes
arc_collection = [arc_speedster,
                  arc_shadow,
                  arc_physical_powerhouse,
                  arc_marksman,
                  arc_blaster,
                  arc_close_quarters_combatant,
                  arc_armored,
                  arc_flier,
                  arc_elemental_manipulator,
                  arc_robot_cyborg,
                  arc_sorceror,
                  arc_psychic,
                  arc_transporter,
                  arc_minion_maker,
                  arc_wild_card,
                  arc_form_changer,
                  arc_gadgeteer,
                  arc_reality_shaper,
                  arc_divided,
                  arc_modular]
arc_simple = [x for x in arc_collection[0:18]]
arc_modifiers = [[], arc_divided, arc_modular]
arc_special = ["",
               "May use a Materials or Technological power for Health",
               "Bonus d10 Technological power; may use a Technological power for Health",
               "Creates 2 additional Green forms and 1 additional Yellow form with alternate " + \
               "Power lists and special Abilities",
               "Gains Powers/Qualities & Abilities from another Archetype",
               "Gains Powers/Qualities & Principle from another Archetype. In place of that " + \
               "Archetype's Abilities, creates 1 Green Mode, 2 Yellow Modes, & 1 Red Mode " + \
               "with modified Power lists and special Abilities"]
arc_width = 150

global form_abilities_green, form_abilities_yellow, fc_zones
form_abilities_green = [a_clever_form, a_miniscule_form, a_strong_form, a_tough_form, \
                        a_tricky_form, a_weird_form]
form_abilities_yellow = [a_agile_form, a_regenerating_form, a_speedy_form, a_towering_form]
fc_zones = [form_abilities_green, form_abilities_yellow]

global mt_powerless, mt_debilitator, mt_improvement, mt_scout, mt_analysis, mt_bombardment
global mt_regeneration, mt_skirmish, mt_stalwart, mt_destroyer, mt_hunter_killer, mt_shield
mt_powerless = ["Powerless Mode",
               0,
               [6, 10],
               [],
               ["use non-Principle Abilities"],
               []]
# Zone:               Green
# Power Sizes:        1d6, 1d10
# Power Mods:         none
# Prohibited Actions: use non-Principle Abilities
# Ability:            none
mt_debilitator = ["Debilitator Mode",
                 0,
                 [],
                 [0, -1, 1, 1],
                 ["Boost", "Defend", "Overcome"],
                 a_debilitator]
# Zone:               Green
# Power Sizes:        none
# Power Mods:         0, +1, -1, -1
# Prohibited Actions: Boost, Defend, Overcome
# Ability:            Debilitator
mt_improvement = ["Improvement Mode",
                 0,
                 [],
                 [0, 0, 1, 1],
                 ["Attack", "Hinder"],
                 a_improvement]
# Zone:               Green
# Power Sizes:        none
# Power Mods:         0, 0, +1, +1
# Prohibited Actions: Attack, Hinder
# Ability:            Improvement
mt_scout = ["Scout Mode",
           0,
           [],
           [0, 0, -1, 1],
           ["Attack", "Boost"],
           a_scout]
# Zone:               Green
# Power Sizes:        none
# Power Mods:         0, 0, -1, 1
# Prohibited Actions: Attack, Boost
# Ability:            Scout
mt_analysis = ["Analysis Mode",
              1,
              [],
              [0, 0, 1, 1],
              ["Attack", "Defend"],
              a_analysis]
# Zone:               Yellow
# Power Sizes:        none
# Power Mods:         0, 0, +1, +1
# Prohibited Actions: Attack, Defend
# Ability:            Analysis
mt_bombardment = ["Bombardment Mode",
                 1,
                 [12],
                 [-1, -1],
                 ["Boost", "Hinder", "Overcome"],
                 a_bombardment]
# Zone:               Yellow
# Power Sizes:        d12
# Power Mods:         -1, -1
# Prohibited Actions: Boost, Hinder, Overcome
# Ability:            Bombardment
mt_regeneration = ["Regeneration Mode",
                  1,
                  [],
                  [0, 2],
                  ["Attack", "Hinder"],
                  a_regeneration]
# Zone:               Yellow
# Power Sizes:        none
# Power Mods:         0, +2
# Prohibited Actions: Attack, Hinder
# Ability:            Regeneration
mt_skirmish = ["Skirmish Mode",
              1,
              [],
              [0, -1, 1, 1],
              ["Boost", "Defend", "Overcome"],
              a_skirmish]
# Zone:               Yellow
# Power Sizes:        none
# Power Mods:         0, -1, +1, +1
# Prohibited Actions: Boost, Defend, Overcome
# Ability:            Skirmish
mt_stalwart = ["Stalwart Mode",
              1,
              [],
              [0, -1, -1, 2],
              ["Hinder", "Overcome"],
              a_stalwart]
# Zone:               Yellow
# Power Sizes:        none
# Power Mods:         0, -1, -1, +2
# Prohibited Actions: Hinder, Overcome
# Ability:            Stalwart
mt_destroyer = ["Destroyer Mode",
               2,
               [],
               [0, 0, 1],
               ["move", "Boost"],
               a_destroyer]
# Zone:               Red
# Power Sizes:        none
# Power Mods:         0, 0, +1
# Prohibited Actions: move, Boost
# Ability:            Destroyer
mt_hunter_killer = ["Hunter/Killer Mode",
                   2,
                   [],
                   [1, 1],
                   ["Defend", "Overcome"],
                   a_hunter_killer]
# Zone:               Red
# Power Sizes:        none
# Power Mods:         +1, +1
# Prohibited Actions: Defend, Overcome
# Ability:            Hunter/Killer
mt_shield = ["Shield Mode",
            2,
            [],
            [0, 0, 1, 1],
            ["Attack"],
            a_shield]
# Zone:               Red
# Power Sizes:        none
# Power Mods:         0, 0, +1, +1
# Prohibited Actions: Attack
# Ability:            Shield

global mc_green, mc_yellow, mc_red, mc_zones
mc_green = [mt_debilitator, mt_improvement, mt_scout]
mc_yellow = [mt_analysis, mt_bombardment, mt_regeneration, mt_skirmish, mt_stalwart]
mc_red = [mt_destroyer, mt_hunter_killer, mt_shield]
mc_zones = [mc_green, mc_yellow, mc_red, [mt_powerless]]

global tr_controllable, tr_device, tr_merging_possession, tr_collection, tr_width, dv_defaults
tr_controllable = ["Controllable Transition",
                   "You change between two different forms through some method that you have " + \
                   "control over at all times. It might be yelling a magic word, or an " + \
                   "elaborate sparkly transformation sequence. The disadvantage of " + \
                   "controllable transition is that it always takes time to transform.",
                   [a_transform]]
tr_device = ["Device Transition",
             "You transform between forms via a device of some kind, possibly via cybernetic " + \
             "upgrades or a magical artifact that channels the essence of a demigod. The " + \
             "disadvantage of device transition is that you need access to the device to " + \
             "enact your transformation.",
             [a_device_transform]]
tr_merging_possession = ["Merging/Possession Transition",
                         "Your transformation isn't entirely within you and you require other " + \
                         "entities to change forms. For some, you must merge with someone " + \
                         "else/something else to achieve your full heroic potential. For " + \
                         "others, you take direct control over inanimate objects or people to " + \
                         "manifest your powers.",
                         [a_merge, a_possess_person, a_possess_object]]
tr_uncontrollable = ["Uncontrollable Transition",
                     "You transform in response to stress - whether you want to or not.",
                     [a_uncontrolled_transform]]
tr_collection = [tr_controllable, tr_device, tr_merging_possession, tr_uncontrollable]
tr_width = 100
dv_defaults = ["Civilian", "Heroic"]

global min_autonomous, min_burrowing, min_floating, min_pack, min_explosive, min_reinforced
global min_harsh, min_stealth, min_swift, min_champion, min_hive_mind, min_turret, min_collection
min_autonomous = ["Autonomous",
                  "The minion can take any of the basic actions, not just one.",
                  1]
min_burrowing = ["Burrowing",
                 "The minion can tunnel through the earth.",
                 1]
min_floating = ["Floating",
                "The minion can fly and maneuver in the air.",
                1]
min_pack = ["Pack",
            "The minion adds +1 to its Attack for each other Pack minion attacking the same " + \
            "target this round.",
            2]
min_explosive = ["Explosive",
                 "When the minion is destroyed, also remove a bonus or penalty of your choice.",
                 2]
min_reinforced = ["Reinforced",
                  "The minion adds +1 to its roll to save.",
                  2]
min_harsh = ["Harsh",
             "When the minion Hinders, the target also takes damage equal to that penalty.",
             3]
min_stealth = ["Stealth",
               "On a successful minion save, do not reduce this minion's die size.",
               3]
min_swift = ["Swift",
             "The minion rolls twice for its action and chooses the higher die.",
             3]
min_champion = ["Champion",
                "When the minion Boosts, it may apply the bonus to all actions by its creator " + \
                "and their minions until your next turn.",
                4]
min_hive_mind = ["Hive-Mind",
                 "While this minion is active, all your other minions can take the same " + \
                 "action as it does.",
                 4]
min_turret = ["Turret",
              "When the minion Attacks, it may split its die into two dice of smaller sizes.",
              4]
min_collection = [min_autonomous,
                  min_burrowing,
                  min_floating,
                  min_pack,
                  min_explosive,
                  min_reinforced,
                  min_harsh,
                  min_stealth,
                  min_swift,
                  min_champion,
                  min_hive_mind,
                  min_turret]

global pn_lone_wolf, pn_natural_leader, pn_impulsive, pn_mischievous, pn_sarcastic, pn_distant
global pn_stalwart, pn_fast_talking, pn_inquisitive, pn_alluring, pn_stoic, pn_nurturing
global pn_analytical, pn_decisive, pn_jovial, pn_cheerful, pn_naive, pn_apathetic, pn_jaded
global pn_arrogant, pn_collection, pn_special, pn_width
pn_lone_wolf = ["Lone Wolf", [8, 8, 8], a_out_qboost, 0]
pn_natural_leader = ["Natural Leader", [6, 8, 10], a_out_qboost, 0]
pn_impulsive = ["Impulsive", [6, 6, 8], a_out_reroll, 1]
pn_mischievous = ["Mischievous", [6, 8, 8], a_out_phinder, 2]
pn_sarcastic = ["Sarcastic", [8, 8, 8], a_out_qhinder, 0]
pn_distant = ["Distant", [10, 8, 6], a_out_rboost, 0]
pn_stalwart = ["Stalwart", [8, 8, 8], a_out_pdefend, 0]
pn_fast_talking = ["Fast Talking", [6, 8, 10], a_out_qhinder_plus, 0]
pn_inquisitive = ["Inquisitive", [6, 8, 10], a_out_reaction, 0]
pn_alluring = ["Alluring", [6, 8, 10], a_out_pboost, 0]
pn_stoic = ["Stoic", [6, 8, 10], a_out_qdefend, 0]
pn_nurturing = ["Nurturing", [6, 6, 12], a_out_qboost, 0]
pn_analytical = ["Analytical", [10, 8, 6], a_out_remove, 0]
pn_decisive = ["Decisive", [8, 8, 8], a_out_pboost, 0]
pn_jovial = ["Jovial", [6, 8, 10], a_out_qdefend, 0]
pn_cheerful = ["Cheerful", [10, 8, 6], a_out_pboost, 0]
pn_naive = ["Naive", [6, 6, 12], a_out_phinder, 0]
pn_apathetic = ["Apathetic", [6, 8, 10], a_out_remove, 0]
pn_jaded = ["Jaded", [10, 8, 6], a_out_remove, 0]
pn_arrogant = ["Arrogant", [10, 8, 6], a_out_phinder, 0]
pn_collection = [pn_lone_wolf,
                 pn_natural_leader,
                 pn_impulsive,
                 pn_mischievous,
                 pn_sarcastic,
                 pn_distant,
                 pn_stalwart,
                 pn_fast_talking,
                 pn_inquisitive,
                 pn_alluring,
                 pn_stoic,
                 pn_nurturing,
                 pn_analytical,
                 pn_decisive,
                 pn_jovial,
                 pn_cheerful,
                 pn_naive,
                 pn_apathetic,
                 pn_jaded,
                 pn_arrogant]
pn_special = ["",
              "Upgrade a d10 or smaller Power or Quality by one die size.",
              "May use any Power or Quality for Health"]
pn_width = 100

def DisplayBackground(index, prefix="", width=100):
    if index in range(len(bg_collection)):
        pref = prefix
        bg = bg_collection[index]
        printlong(bg[0] + ": " + bg[1], width, prefix=pref)
        print(prefix + "    Quality Dice: " + str(bg[2]))
        if len(bg[3]) > 0:
            print(prefix + "    Required Quality: " + MixedPQ(bg[3][0]))
        print(prefix + "    Optional Qualities: ")
        quality_choices = bg[4]
        col_num = 4
        columns = [0] * col_num
        for c in range(len(columns)):
            columns[c] = max([len(MixedPQ(quality_choices[i]))+2 \
                              for i in range(len(quality_choices)) if i%col_num == c])
        for i in range(len(quality_choices)):
            quality_text = MixedPQ(quality_choices[i])
            while len(quality_text) < columns[i%col_num]:
                quality_text += " "
            if i%col_num == 0:
                print(prefix + "        ", end="")
            if i%col_num == col_num-1 or i == len(quality_choices)-1:
                print(quality_text)
            else:
                print(quality_text, end="")
        print(prefix + "    " + rc_names[bg[5]] + " Principle")
        print(prefix + "    Power Source Dice: " + str(bg[6]))

def BackgroundDetails(index, width=100):
    if index in range(len(bg_collection)):
        bg = bg_collection[index]
        bgText = split_text(bg[0] + ": " + bg[1], width=width)
        bgText += "\n\n" + "Quality Dice: " + str(bg[2])
        if len(bg[3]) > 0:
            bgText += "\n\n" + "Required Quality: " + MixedPQ(bg[3][0])
        bgText += "\n\n" + "Optional Qualities: "
        quality_choices = bg[4]
        this_line = ""
        for i in range(len(quality_choices)):
            quality_text = MixedPQ(quality_choices[i])
##            if len(this_line) + len(quality_text) + 4 > width:
##                bgText += "\n  " + this_line
##                this_line = "" + quality_text
##            else:
##                this_line += quality_text
            this_line += quality_text
            if i < len(quality_choices) - 1:
                this_line += ", "
        bgText += "\n" + split_text(this_line, width=width, prefix="  ")
        bgText += "\n\n" + rc_names[bg[5]] + " Principle"
        bgText += "\n\n" + "Power Source Dice: " + str(bg[6])
        return bgText
    else:
        return "Invalid Background index: " + str(index)

def DisplayPowerSource(index, prefix="", width=100):
    if index in range(len(ps_collection)):
        pref = prefix
        indent = "    "
        powersource = ps_collection[index]
        printlong(powersource[0] + ": " + powersource[1], width, prefix=pref)
        if len(powersource[2]) > 0:
            print(prefix + indent + "Required Power: " + MixedPQ(powersource[2][0]))
        print(prefix + indent + "Optional Powers: ")
        power_choices = powersource[3]
        col_num = 4
        columns = [0] * col_num
        for c in range(len(columns)):
            columns[c] = max([len(MixedPQ(power_choices[i]))+2 \
                              for i in range(len(power_choices)) if i%col_num == c])
        for i in range(len(power_choices)):
            power_text = MixedPQ(power_choices[i])
            while len(power_text) < columns[i%col_num]:
                power_text += " "
            if i%col_num == 0:
                print(prefix + indent + indent, end="")
            if i%col_num == col_num-1 or i == len(power_choices)-1:
                print(power_text)
            else:
                print(power_text, end="")
        if powersource[4] > 0:
            if powersource[4] == 1:
                print(prefix + indent + str(powersource[4]) + " Yellow Ability from:")
            else:
                print(prefix + indent + str(powersource[4]) + " Yellow Abilities from:")
            for ability in powersource[5]:
                ability.display(prefix=pref+indent+indent, width=width-len(indent+indent))
        if powersource[6] > 0:
            if powersource[6] == 1:
                print(prefix + indent + str(powersource[6]) + " Green Ability from:")
            else:
                print(prefix + indent + str(powersource[6]) + " Green Abilities from:")
            for ability in powersource[7]:
                ability.display(prefix=pref+indent+indent, width=width-len(indent+indent))
        if powersource[8] > 0:
            print(prefix + indent + ps_special[powersource[8]])
        print(prefix + indent + "Archetype Dice: " + str(powersource[9]))

def PowerSourceDetails(index, width=100):
    if index in range(len(ps_collection)):
        psText = ""
        powersource = ps_collection[index]
        psText += split_text(powersource[0] + ": " + powersource[1], width=width)
        if len(powersource[2]) > 0:
            psText += "\n\n" + "Required Power: " + MixedPQ(powersource[2][0])
        psText += "\n\n" + "Optional Powers: "
        power_choices = powersource[3]
        this_line = ""
        for i in range(len(power_choices)):
            power_text = MixedPQ(power_choices[i])
            this_line += power_text
            if i < len(power_choices) - 1:
                this_line += ", "
        psText += "\n" + split_text(this_line, width=width, prefix="  ")
        if powersource[4] > 0:
            if powersource[4] == 1:
                psText += "\n\n" + str(powersource[4]) + " Yellow Ability from:"
            else:
                psText += "\n\n" + str(powersource[4]) + " Yellow Abilities from:"
            for ability in powersource[5]:
                psText += "\n" + ability.details(width=width)
        if powersource[6] > 0:
            if powersource[6] == 1:
                psText += "\n\n" + str(powersource[6]) + " Green Ability from:"
            else:
                psText += "\n\n" + str(powersource[6]) + " Green Abilities from:"
            for ability in powersource[7]:
                psText += "\n" + ability.details(width=width)
        if powersource[8] > 0:
            psText += "\n\n" + ps_special[powersource[8]]
        psText += "\n\n" + "Archetype Dice: " + str(powersource[9])
        return psText
    else:
        return "Invalid Power Source index: " + str(index)

def MinionFormStr(min_form):
    return min_form[0] + " (requires +" + str(min_form[2]) + " or higher): " + min_form[1]

def DisplayTransitionMethod(index, prefix="", width=100):
    indent = "    "
    transition = tr_collection[index]
    print(prefix + transition[0])
    printlong(transition[1], width-len(indent), prefix=prefix+indent)
    if len(transition[2]) > 1:
        print(prefix + indent + "Optional Green Abilities:")
    else:
        print(prefix + indent + "Required Green Ability:")
    for i in range(len(transition[2])):
        transition[2][i].display(prefix+indent+indent,width=width-len(indent+indent))

def TransitionDetails(index, width=50):
    if index in range(len(tr_collection)):
        transition = tr_collection[index]
        trText = split_text(transition[0] + ": " + transition[1], width=width)
        if len(transition[2]) > 1:
            trText += "\n" + "Optional Green Abilities:"
        else:
            trText += "\n" + "Required Green Ability:"
        for i in range(len(transition[2])):
            trText += "\n" + transition[2][i].details(width=width)
        return trText
    else:
        return "Invalid transition index: " + str(index)

def DisplayModeTemplate(zone, index, prefix="", width=100):
    indent = "    "
    mode = []
    if zone in [-1,3]:
        mode = mt_powerless
        zone = 0
    else:
        mode = mc_zones[zone][index]
    print(prefix + mode[0] + " [" + status_zones[zone] + "]:")
    for d in legal_dice:
        matching_dice = [size for size in mode[2] if size==d]
        if len(matching_dice) == 1:
            print(prefix + indent + str(len(matching_dice)) + " Power at d" + str(d))
        elif len(matching_dice) > 1:
            print(prefix + indent + str(len(matching_dice)) + " Powers at d" + str(d))
    for modifier in range(-2, 3):
        mod_text = str(modifier)
        if modifier >=0:
            mod_text = "+" + mod_text
        if abs(modifier) == 1:
            mod_text += " die size"
        else:
            mod_text += " die sizes"
        matching_mods = [m for m in mode[3] if m==modifier]
        if len(matching_mods) == 1:
            print(prefix + indent + str(len(matching_mods)) + " Power at " + mod_text)
        elif len(matching_mods) > 1:
            print(prefix + indent + str(len(matching_mods)) + " Powers at " + mod_text)
    if len(mode[4]) > 0:
        prohibited_text = mode[4][0]
        for i in range(1, len(mode[4])-1):
            prohibited_text += ", " + mode[4][i]
        if len(mode[4]) > 2:
            prohibited_text += ","
        if len(mode[4]) > 1:
            prohibited_text += " or " + mode[4][len(mode[4])-1]
        print(prefix + indent + "You cannot " + prohibited_text + " while in this mode.")
    if mode[5]:
        print(prefix + indent + "You gain access to this Ability:")
        pref = prefix
        mode[5].display(prefix=pref+indent+indent,width=width-len(indent+indent))

def ModeTemplateDetails(zone, index, width=100):
    mode = []
    if zone in [-1,3]:
        mode = mt_powerless
        zone = 0
    elif zone not in range(len(status_zones)):
        return "Invalid zone index: " + str(zone)
    elif index not in range(len(mc_zones[zone])):
        return "Invalid mode index for " + status_zones[zone] + " zone: " + str(index)
    else:
        mode = mc_zones[zone][index]
    modeText = mode[0] + " [" + status_zones[zone] + "]:"
    for d in legal_dice:
        matching_dice = [size for size in mode[2] if size==d]
        if len(matching_dice) == 1:
            modeText += "\n" + str(len(matching_dice)) + " Power at d" + str(d)
        elif len(matching_dice) > 1:
            modeText += "\n" + str(len(matching_dice)) + " Powers at d" + str(d)
    for modifier in range(-2, 3):
        mod_text = str(modifier)
        if modifier >=0:
            mod_text = "+" + mod_text
        if abs(modifier) == 1:
            mod_text += " die size"
        else:
            mod_text += " die sizes"
        matching_mods = [m for m in mode[3] if m==modifier]
        if len(matching_mods) == 1:
            modeText += "\n" + str(len(matching_mods)) + " Power at " + mod_text
        elif len(matching_mods) > 1:
            modeText += "\n" + str(len(matching_mods)) + " Powers at " + mod_text
    if len(mode[4]) > 0:
        prohibited_text = mode[4][0]
        for i in range(1, len(mode[4])-1):
            prohibited_text += ", " + mode[4][i]
        if len(mode[4]) > 2:
            prohibited_text += ","
        if len(mode[4]) > 1:
            prohibited_text += " or " + mode[4][len(mode[4])-1]
        modeText += "\n" + "You cannot " + prohibited_text + " while in this mode."
    if mode[5]:
        modeText += "\n" + "You gain access to this Ability:"
        modeText += "\n" + mode[5].details(width=width)
    return modeText
        
def DisplayArchetype(index, prefix="", width=100):
    if index in range(len(arc_collection)):
        pref = prefix
        indent = "    "
        archetype = arc_collection[index]
        printlong(archetype[0] + ": " + archetype[1], width, prefix=pref)
        if index in range(18):
            # A normal standalone archetype
            # Display the primary power(s)/quality(ies) from archetype[2]
            pcat = DieCategory(archetype[2])
            if len(archetype[2])==1:
                print(prefix + indent + "Primary " + categories_singular[pcat] + ": " + \
                      MixedPQ(archetype[2][0]))
            elif len(archetype[2])>1:
                print(prefix + indent + "Primary " + categories_plural[pcat] + " (choose 1):")
                primary_choices = archetype[2]
                col_num = 4
                columns = [0] * col_num
                for c in range(len(columns)):
                    if c in range(len(primary_choices)):
                        columns[c] = max([len(MixedPQ(primary_choices[i]))+2 \
                                          for i in range(len(primary_choices)) if i%col_num == c])
                for i in range(len(primary_choices)):
                    pq_text = MixedPQ(primary_choices[i])
                    while len(pq_text) < columns[i%col_num]:
                        pq_text += " "
                    if i%col_num == 0:
                        print(prefix + "        ", end="")
                    if i%col_num == col_num-1 or i == len(primary_choices)-1:
                        print(pq_text)
                    else:
                        print(pq_text, end="")
            if archetype[3] > 0:
                alternatives = ["", "skip it or choose another", "skip it or swap in a new die"]
                print(prefix + indent + "(If already present: " + alternatives[archetype[3]] + ")")
            # Display the secondary power(s)/quality(ies) from archetype[5]
            secondary_count = "1"
            if archetype[4] > 1:
                secondary_count = "1 or more"
            if archetype[4] > 0:
                print(prefix + indent + "Required Powers/Qualities (choose " + secondary_count + \
                      "):")
                secondary_choices = archetype[5]
                col_num = 4
                columns = [0] * col_num
                for c in range(len(columns)):
                    if c in range(len(secondary_choices)):
                        columns[c] = max([len(MixedPQ(secondary_choices[i]))+2 \
                                          for i in range(len(secondary_choices)) if i%col_num == c])
                for i in range(len(secondary_choices)):
                    pq_text = MixedPQ(secondary_choices[i])
                    while len(pq_text) < columns[i%col_num]:
                        pq_text += " "
                    if i%col_num == 0:
                        print(prefix + indent + indent, end="")
                    if i%col_num == col_num-1 or i == len(secondary_choices)-1:
                        print(pq_text)
                    else:
                        print(pq_text, end="")
            # Display the tertiary power(s)/quality(ies) from archetype[6]
            if len(archetype[6]) > 0:
                print(prefix + indent + "Optional Powers/Qualities:")
                tertiary_choices = archetype[6]
                col_num = 4
                columns = [0] * col_num
                for c in range(len(columns)):
                    columns[c] = max([len(MixedPQ(tertiary_choices[i]))+2 \
                                      for i in range(len(tertiary_choices)) if i%col_num == c])
                for i in range(len(tertiary_choices)):
                    pq_text = MixedPQ(tertiary_choices[i])
                    while len(pq_text) < columns[i%col_num]:
                        pq_text += " "
                    if i%col_num == 0:
                        print(prefix + indent + indent, end="")
                    if i%col_num == col_num-1 or i == len(tertiary_choices)-1:
                        print(pq_text)
                    else:
                        print(pq_text, end="")
            # Display the mandatory Abilities from archetype[7]
            if len(archetype[7]) > 0:
                if len(archetype[7]) == 1:
                    print(prefix + indent + "Required Ability:")
                else:
                    print(prefix + indent + "Required Abilities:")
                for ability in archetype[7]:
                    ability.display(prefix=pref+indent+indent,width=width-len(indent+indent))
            # If applicable, display the Green/Yellow Abilities from archetype[12]
            # Otherwise, display Green Abilities from archetype[10] and Yellow Abilities from
            #  archetype[11] separately
            green_text = "Green Ability"
            yellow_text = "Yellow Ability"
            if archetype[8] > 1:
                green_text = "Green Abilities"
                green_restrictions = ""
                if archetype[15] >= archetype[8]:
                    green_restrictions = "each using a different Power/Quality"
                elif archetype[15] > 0:
                    green_restrictions = "using at least " + str(archetype[15]) + \
                                         " different Powers/Qualities"
                if archetype[17]:
                    if len(green_restrictions) == 0:
                        green_restrictions = "using only Powers/Qualities from the " + \
                                             archetype[0] + " lists"
                    else:
                        green_restrictions += " from the " + \
                                              archetype[0] + " lists"
                if len(green_restrictions) > 0:
                    green_text += ", " + green_restrictions + ","
            if archetype[9] > 1:
                yellow_text = "Yellow Abilities"
                if archetype[16] >= archetype[9]:
                    yellow_text += ", each using a different Power/Quality,"
            # Prepare restrictions on Green Abilities from archetype[13] and archetype[14], if
            #  applicable
            # If Green and Yellow Abilities are separate, this is displayed after Green; otherwise,
            #  after both
            gcat = "Power/Quality"
            gtext = ""
            ptext = "the Primary " + categories_singular[pcat]
            if len(archetype[2])==1:
                ptext = MixedPQ(archetype[2][0])
            if archetype[14] >= 0:
                gcat = categories_singular[archetype[14]]
                gtext = "1 Green Ability uses " + ptext + \
                        "; another uses a " + gcat
            elif archetype[13]:
                gtext = "1 Green Ability uses " + ptext
            if len(gtext) > 0:
                gtext = "(" + gtext + ")"
            if len(archetype[12]) > 0:
                printlong(str(archetype[8]) + " " + green_text + " and " + \
                          str(archetype[9]) + " " + yellow_text + " from:",
                          prefix=prefix+indent,
                          width=width-len(indent))
                for ability in archetype[12]:
                    ability.display(prefix=pref+indent+indent,width=width-len(indent+indent))
                if len(gtext) > 0:
                    print(prefix + indent + gtext)
            else:
                if archetype[8] > 0:
                    print(prefix + indent + str(archetype[8]) + " " + green_text + " from:")
                    for ability in archetype[10]:
                        ability.display(prefix=pref+indent+indent,width=width-len(indent+indent))
                    if len(gtext) > 0:
                        print(prefix + indent + gtext)
                if archetype[9] > 0:
                    print(prefix + indent + str(archetype[9]) + " " + yellow_text + " from:")
                    for ability in archetype[11]:
                        ability.display(prefix=pref+indent+indent,width=width-len(indent+indent))
            # Display the Principle category from archetype[18]
            print(prefix + indent + rc_names[archetype[18]] + " Principle")
            # Display bonus effects, if applicable
            if archetype[19] > 0:
                printlong(arc_special[archetype[19]],prefix=pref+indent,width=width-len(indent))
        elif index == 18:
            # Divided
            # Bonus effects first- they indicate that this is a complex Archetype that needs a
            #  simple one underneath
            printlong(arc_special[archetype[19]],prefix=pref+indent,width=width-len(indent))
            # Display the Transition Types and their associated Green Abilities.
            print(prefix + indent + "Transition Types (choose 1):")
            for i in range(len(tr_collection)):
                DisplayTransitionMethod(i, prefix=pref+indent+indent, width=width-len(indent+indent))
            # Display the Build Options and the Green Ability associated with Split Form.
            build_options = [a_divided_psyche, a_split_form]
            print(prefix + indent + "Divided Nature (choose 1):")
            for i in range(len(build_options)):
                build_options[i].display(prefix=pref+indent+indent, width=width-len(indent+indent))
            # Display the Principle category from archetype[18]
            print(prefix + indent + rc_names[archetype[18]] + " Principle")
        elif index == 19:
            # Modular
            # Bonus effects first- they indicate that this is a complex Archetype that needs a
            #  simple one underneath
            printlong(arc_special[archetype[19]],prefix=pref+indent,width=width-len(indent))
            # Display the mandatory Abilities from archetype[7]
            if len(archetype[7]) > 0:
                if len(archetype[7]) == 1:
                    print(prefix + indent + "Required Ability:")
                else:
                    print(prefix + indent + "Required Abilities:")
                for ability in archetype[7]:
                    ability.display(prefix=pref+indent+indent,width=width-len(indent+indent))
            print(prefix + indent + "Optional Mode:")
            DisplayModeTemplate(3,
                                0,
                                prefix=prefix+indent+indent,
                                width=width-len(indent+indent))
            mode_counts = [1, 2, 1]
            for z in range(3):
                print(prefix + indent + status_zones[z] + " Modes (choose " + \
                      str(mode_counts[z]) + "):")
                for i in range(len(mc_zones[z])):
                    DisplayModeTemplate(z,
                                        i,
                                        prefix=prefix+indent+indent,
                                        width=width-len(indent+indent))

def ArchetypeDetails(index, width=100):
    if index in range(len(arc_collection)):
        archetype = arc_collection[index]
        arcText = ""
        arcText += split_text(archetype[0] + ": " + archetype[1], width=width)
        if index in range(18):
            # A normal standalone archetype
            # Display the primary power(s)/quality(ies) from archetype[2]
            pcat = DieCategory(archetype[2])
            if len(archetype[2])==1:
                arcText += "\n\nPrimary " + categories_singular[pcat] + ": " + \
                      MixedPQ(archetype[2][0])
            elif len(archetype[2])>1:
                arcText += "\n\nPrimary " + categories_plural[pcat] + " (choose 1):"
                primary_choices = archetype[2]
                this_line = ""
                for i in range(len(primary_choices)):
                    this_line += MixedPQ(primary_choices[i])
                    if i < len(primary_choices) - 1:
                        this_line += ", "
                arcText += "\n" + split_text(this_line, width=width, prefix="  ")
            if archetype[3] > 0:
                alternatives = ["", "skip it or choose another", "skip it or swap in a new die"]
                arcText += "\n(If already present: " + alternatives[archetype[3]] + ")"
            # Display the secondary power(s)/quality(ies) from archetype[5]
            secondary_count = "1"
            if archetype[4] > 1:
                secondary_count = "1 or more"
            if archetype[4] > 0:
                arcText += "\n\nRequired Powers/Qualities (choose " + secondary_count + "):"
                secondary_choices = archetype[5]
                this_line = ""
                for i in range(len(secondary_choices)):
                    this_line += MixedPQ(secondary_choices[i])
                    if i < len(secondary_choices) - 1:
                        this_line += ", "
                arcText += "\n" + split_text(this_line, width=width, prefix="  ")
            # Display the tertiary power(s)/quality(ies) from archetype[6]
            if len(archetype[6]) > 0:
                arcText += "\n\nOptional Powers/Qualities:"
                tertiary_choices = archetype[6]
                this_line = ""
                for i in range(len(tertiary_choices)):
                    this_line += MixedPQ(tertiary_choices[i])
                    if i < len(tertiary_choices) - 1:
                        this_line += ", "
                arcText += "\n" + split_text(this_line, width=width, prefix="  ")
            # Display the mandatory Abilities from archetype[7]
            if len(archetype[7]) > 0:
                if len(archetype[7]) == 1:
                    arcText += "\n\nRequired Ability:"
                else:
                    arcText += "\n\nRequired Abilities:"
                for ability in archetype[7]:
                    arcText += "\n" + ability.details(width=width)
            green_text = "Green Ability"
            yellow_text = "Yellow Ability"
            if archetype[8] > 1:
                green_text = "Green Abilities"
                green_restrictions = ""
                if archetype[15] >= archetype[8]:
                    green_restrictions = "each using a different Power/Quality"
                elif archetype[15] > 0:
                    green_restrictions = "using at least " + str(archetype[15]) + \
                                         " different Powers/Qualities"
                if archetype[17]:
                    if len(green_restrictions) == 0:
                        green_restrictions = "using only Powers/Qualities from the " + \
                                             archetype[0] + " lists"
                    else:
                        green_restrictions += " from the " + \
                                              archetype[0] + " lists"
                if len(green_restrictions) > 0:
                    green_text += ", " + green_restrictions + ","
            if archetype[9] > 1:
                yellow_text = "Yellow Abilities"
                if archetype[16] >= archetype[9]:
                    yellow_text += ", each using a different Power/Quality,"
            # Prepare restrictions on Green Abilities from archetype[13] and archetype[14], if
            #  applicable
            # If Green and Yellow Abilities are separate, this is displayed after Green; otherwise,
            #  after both
            gcat = "Power/Quality"
            gtext = ""
            ptext = "the Primary " + categories_singular[pcat]
            if len(archetype[2])==1:
                ptext = MixedPQ(archetype[2][0])
            if archetype[14] >= 0:
                gcat = categories_singular[archetype[14]]
                gtext = "  (1 Green Ability uses " + ptext + "; another uses a " + gcat + ")"
            elif archetype[13]:
                gtext = "  (1 Green Ability uses " + ptext + ")"
            if len(archetype[12]) > 0:
                # Green and Yellow Abilities are listed together
                # Add list of Green/Yellow Abilities from archetype[12], then add Green
                #  restrictions if present
                arcText += "\n\n" + split_text(str(archetype[8]) + " " + green_text + " and " + \
                                               str(archetype[9]) + " " + yellow_text + " from:",
                                               width=width)
                for ability in archetype[12]:
                    arcText += "\n" + ability.details(width=width)
                if len(gtext) > 0:
                    arcText += "\n" + gtext
            else:
                # Green and Yellow Abilities are listed separately
                # Add list of Green Abilities from archetype[10], then add Green restrictions if
                #  present, then add list of Yellow Abilities from archetype[11]
                if archetype[8] > 0:
                    arcText += "\n\n" + split_text(str(archetype[8]) + " " + green_text + " from:",
                                                   width=width)
                    for ability in archetype[10]:
                        arcText += "\n" + ability.details(width=width)
                    if len(gtext) > 0:
                        arcText += "\n" + gtext
                if archetype[9] > 0:
                    arcText += "\n\n" + split_text(str(archetype[9]) + " " + yellow_text + " from:",
                                                   width=width)
                    for ability in archetype[11]:
                        arcText += "\n" + ability.details(width=width)
            # Add Principle category from archetype[18]
            arcText += "\n\n" + rc_names[archetype[18]] + " Principle"
            # Add bonus effects, if applicable
            if archetype[19] > 0:
                arcText += "\n\n" + split_text(arc_special[archetype[19]], width=width)
        elif index == 18:
            # Divided
            # Bonus effects first- they indicate that this is a complex Archetype that needs a
            #  simple one underneath
            arcText += "\n\n" + split_text(arc_special[archetype[19]], width=width)
            # Display the Transition Types and their associated Green Abilities.
            arcText += "\n\n" + "Transition Types (choose 1):"
            # ...
            for i in range(len(tr_collection)):
                arcText += "\n" + TransitionDetails(i, width=width) + "\n"
            # Display the Build Options and the Green Ability associated with Split Form.
            build_options = [a_divided_psyche, a_split_form]
            arcText += "\n" + "Divided Nature (choose 1):"
            for i in range(len(build_options)):
                arcText += "\n" + build_options[i].details(width=width)
            # Display the Principle category from archetype[18]
            arcText += "\n\n" + rc_names[archetype[18]] + " Principle"
        elif index == 19:
            # Modular
            # Bonus effects first- they indicate that this is a complex Archetype that needs a
            #  simple one underneath
            arcText += "\n\n" + split_text(arc_special[archetype[19]], width=width)
            # Display the mandatory Abilities from archetype[7]
            if len(archetype[7]) > 0:
                if len(archetype[7]) == 1:
                    arcText += "\n\n" + "Required Ability:"
                else:
                    arcText += "\n\n" + "Required Abilities:"
                for ability in archetype[7]:
                    arcText += "\n" + ability.details(width=width)
##            arcText += "\n\n" + "Optional Mode:"
##            arcText += "\n" + ModeTemplateDetails(3, 0, width=width)
##            mode_counts = [1, 2, 1]
##            for z in range(3):
##                arcText += "\n\n" + status_zones[z] + " Modes (choose " + str(mode_counts[z]) + \
##                           "):"
##                for i in range(len(mc_zones[z])):
##                    arcText += "\n" + ModeTemplateDetails(z,i)
        return arcText

def DisplayPersonality(index, prefix="", width=100):
    # Display the attributes of the Personality specified by index.
    indent = "    "
    personality = pn_collection[index]
    print(prefix + personality[0])
    print(prefix + indent + "Status Dice: " + str(personality[1]))
    personality[2].display(prefix=prefix+indent, width=width-len(indent))
    if personality[3] > 0:
        print(prefix + indent + "Bonus: " + pn_special[personality[3]])

def PersonalityDetails(index, width=100):
    personality = pn_collection[index]
    pnText = "" + personality[0]
    pnText += "\n" + split_text("Status Dice: " + str(personality[1]), width=width)
    pnText += "\n" + personality[2].details(width=width)
    if personality[3] > 0:
        pnText += "\n" + split_text("Bonus: " + pn_special[personality[3]], width=width)
    return pnText

class Hero:
    def __init__(self, codename="", civ_name="", pro_index=2):
        self.hero_name = codename
        self.alias = civ_name
        self.pronoun_set = pro_index
        self.power_dice = []
        self.quality_dice = []
        self.health_zones = [0, 0, 0]
        self.status_dice = [0, 0, 0]
        self.status_step = 0
        self.status_steps_modified = []
        self.background = 99
        self.ps_dice = []
        self.power_source = 99
        self.arc_dice = []
        self.arc_bonus_quality = 0
        self.archetype = 99
        self.archetype_modifier = 99
        self.dv_tags = ["Civilian", "Heroic"]
        self.min_forms = []
        self.mf_step = 0
        self.personality = 99
        self.dv_personality = 99
        self.used_retcon = False
        self.principles = []
        self.abilities = []
        self.other_modes = []
        self.other_forms = []
        self.health_pqs = Category(1,0) + Category(0,1)
        self.health_step = 0
        self.myFrame = None
        self.myWindow = None
    def SetFrame(self, frame):
        if isinstance(frame, HeroFrame):
            self.myFrame = frame
            self.myWindow = self.myFrame.winfo_toplevel()
    def RefreshFrame(self):
        if isinstance(self.myFrame, HeroFrame):
            self.myFrame.UpdateAll(self)
    def UseGUI(self, inputs):
        return len(inputs) <= 0 and isinstance(self.myFrame, HeroFrame)
    def ChooseIndex(self,
                    print_options,
                    prompt="",
                    repeat_message=invalid_message,
                    title="Hero Creation",
                    inputs=[]):
        # Prints a prompt and a list of lettered options (print_options, indicated by A, B, C,
        #  etc.), then lets the user choose from among them
        # Keeps prompting the user (displaying repeat_message) until the first letter of their
        #  response matches one of the options
        # title: a string to display in the title bar of the SelectWindow, if there is one
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns [index of user's response, any remaining inputs]
        if len(inputs) > 0:
            print("### choose_index: inputs=" + str(inputs))
        # If we have a GUI and no text inputs, create a SelectWindow to ask the question
        # Otherwise, use the text shell
        if self.UseGUI(inputs):
            print("Using SelectWindow")
            answer = IntVar()
            question = SelectWindow(self.myWindow,
                                    prompt=prompt,
                                    options=print_options,
                                    var=answer,
                                    title=title)
            return [answer.get(), inputs]
        else:
            indent = "    "
            entry_options = string.ascii_uppercase[0:len(print_options)]
            entry_choice = ' '
            if len(prompt) > 0:
                print(prompt)
            for i in range(len(print_options)):
                print(indent + entry_options[i] + ": " + print_options[i])
            if len(inputs) > 0:
                print("> " + inputs[0])
                entry_choice = inputs.pop(0)[0].upper()
            else:
                entry_choice = input()[0].upper()
            while entry_choice not in entry_options:
                if len(inputs) > 0:
                    print(repeat_message)
                    print("> " + inputs[0])
                    entry_choice = inputs.pop(0)[0].upper()
                else:
                    entry_choice = input(repeat_message + "\n")[0].upper()
            entry_index = entry_options.find(entry_choice)
            return [entry_index, inputs]
    def EnterText(self,
                  prompt="",
                  title="Hero Creation",
                  default="",
                  inputs=[]):
        # Prints a prompt for the user to enter a line of text.
        # title: a string to display in the title bar of the EntryWindow, if there is one
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns [user's response, any remaining inputs]
        if len(inputs) > 0:
            print("### EnterText: inputs=" + str(inputs))
        entry_line = ""
        if len(inputs) > 0:
            print(prompt)
            print("> " + inputs[0])
            entry_line = inputs.pop(0)
        elif self.UseGUI(inputs):
            # If we have a GUI and no prepared inputs, create an EntryWindow to get text from the
            #  user
            print("Using EntryWindow")
            answer = StringVar(self.myFrame, default)
            question = EntryWindow(self.myWindow,
                                   prompt=prompt,
                                   var=answer,
                                   title=title)
            entry_line = answer.get()
        else:
            entry_line = input(prompt + "\n")
        return [entry_line, inputs]
    def AddPQDie(self,
                 ispower,
                 pair,
                 diesize,
                 custom_name=False,
                 flavorname="",
                 stepnum=0,
                 inputs=[]):
        # Adds a power/quality die of the specified die size, with the specified identity
        #  (ispower & pair) and custom name (flavorname)
        # custom_name: should the user be prompted to customize the name of this die?
        # stepnum: the number of the step of hero creation (1-7) at which this die is being added
        # inputs: a set of text inputs to use instead of prompting the user
        if len(inputs) > 0:
            print("### AddPQDie: inputs=" + str(inputs))
        category = pair[0]
        index = pair[1]
        if ispower:
            if pair[0] not in range(len(p_collection)):
                # Category doesn't exist. Set to [9, 0]: Created Power.
                category = 9
                index = 0
            elif pair[1] not in range(len(p_collection[pair[0]])):
                # Category exists, but index does not.
                category = 9
                index = 0
        else:
            if pair[0] not in range(len(q_collection)):
                # Category doesn't exist. Set to [4, 0]: Roleplaying Quality.
                category = 4
                index = 0
            elif pair[1] not in range(len(q_collection[pair[0]])):
                # Category exists, but index does not.
                category = 4
                index = 0
        # If the power or quality is a Hallmark or Unlisted Power or a Special Quality, and no new
        #  name is provided, prompt the user to rename it
        if ([ispower, category] in [[0,4],[1,2],[1,9]] or custom_name==True) and flavorname=="":
            entry_options = "YN"
            decision = choose_letter(entry_options,
                                     ' ',
                                     prompt="Do you want to give " + \
                                     MixedPQ([ispower, category, index]) + \
                                     " a new name? (y/n)",
                                     repeat_message="Please enter Y or N.",
                                     inputs=inputs)
            entry_choice = decision[0]
            inputs = decision[1]
            if entry_choice == 'Y':
                decision = self.EnterText("Enter a new name for " + \
                                          MixedPQ([ispower, category, index]) + ":",
                                          inputs=inputs)
                flavorname = decision[0]
                inputs = decision[1]
        new_die = PQDie(ispower,
                        category,
                        index,
                        diesize,
                        flavorname,
                        stepnum=max([0,stepnum]))
        if ispower:
            self.power_dice.append(new_die)
        else:
            self.quality_dice.append(new_die)
        # If we have a GUI, update it
        self.RefreshFrame()
    def ChoosePQDieSize(self,
                        ispower,
                        pair,
                        die_options,
                        custom_name=False,
                        flavorname="",
                        stepnum=0,
                        inputs=[]):
        # Lets the user choose from a list of dice (die_options) to assign to the specified power
        #  or quality (ispower, pair) with custom name (flavorname)
        # Returns the set of unused dice.
        # custom_name: should the user be prompted to customize the name of this die?
        # stepnum: the number of the step of hero creation (1-7) at which this die is being added
        # inputs: a set of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### ChoosePQDieSize: inputs=" + str(inputs))
        # Validate each entry in die_options:
        valid_dice = [diesize for diesize in die_options if diesize in legal_dice]
        print_name = ""
        # Determine how to refer to the power/quality in text:
        category = pair[0]
        index = pair[1]
        if ispower:
            if pair[0] not in range(len(p_collection)):
                # Category doesn't exist. Set to [9, 0]: Created Power.
                category = 9
                index = 0
            elif pair[1] not in range(len(p_collection[pair[0]])):
                # Category exists, but index does not.
                category = 9
                index = 0
        else:
            if pair[0] not in range(len(q_collection)):
                # Category doesn't exist. Set to [4, 0]: Roleplaying Quality.
                category = 4
                index = 0
            elif pair[1] not in range(len(q_collection[pair[0]])):
                # Category exists, but index does not.
                category = 4
                index = 0
        print_name = MixedPQ([ispower, category, index])
        if flavorname:
            print_name = flavorname + " (" + print_name + ")"
        print_type = categories_singular[ispower]
        if len(valid_dice) == 0:
            # No dice available? Uh oh.
            print("Error! No dice available!")
            return []
        elif len(valid_dice) == 1:
            # Only one die available? Just assign it
            print("d" + str(valid_dice[0]) + " assigned to " + print_name)
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddPQDie(ispower,
                          [category, index],
                          valid_dice[0],
                          flavorname,
                          stepnum=max([0, stepnum]),
                          inputs=pass_inputs)
            return []
        else:
            # Are all of valid_dice matching values? If so, just assign that die size.
            first = valid_dice[0]
            for sample in valid_dice:
                if not sample == first:
                    break
            else:
                print("d" + str(valid_dice[0]) + " assigned to " + print_name)
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddPQDie(ispower,
                              pair,
                              valid_dice[0],
                              flavorname,
                              stepnum=max([0, stepnum]),
                              inputs=pass_inputs)
                return valid_dice[1:]
        # Now we know there are multiple valid_dice with different values. Time to make a choice.
        decision = self.ChooseIndex([str(d) for d in valid_dice],
                                    prompt="Choose a die to assign to " + print_name + ":",
                                    inputs=inputs)
        entry_index = decision[0]
        inputs = decision[1]
        pass_inputs = []
        if len(inputs) > 0:
            if str(inputs[0]) != inputs[0]:
                pass_inputs = inputs.pop(0)
        self.AddPQDie(ispower,
                      pair,
                      valid_dice[entry_index],
                      flavorname,
                      stepnum=max([0, stepnum]),
                      inputs=pass_inputs)    
        print("d" + str(valid_dice[entry_index]) + " assigned to " + print_name)
        valid_dice.remove(valid_dice[entry_index])
        return valid_dice
    def ChoosePQ(self, triplets, die_options, custom_name=False, stepnum=0, inputs=[]):
        # Lets the user choose from a list of powers and/or qualities (triplets) to assign one of a
        #  list of dice (die_options)
        # Returns the list of unused triplets and the list of unused die sizes
        # custom_name: should the user be prompted to customize the name of this die?
        # stepnum: the number of the step of hero creation (1-7) at which this die is being added
        # inputs: a set of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### ChoosePQ: inputs=" + str(inputs))
        # Start by validating each entry in triplets:
        valid_triplets = []
        for entry in triplets:
            if entry[0] in range(len(mixed_collection)):
                # entry[0] is either 0 (a quality) or 1 (a power)
                if entry[1] in range(len(mixed_collection[entry[0]])):
                    # entry[1] is a valid index for a power/quality category
                    if entry[2] in range(len(mixed_collection[entry[0]][entry[1]])):
                        # entry[2] is a valid index for a power/quality within that category
                        if entry not in [d.triplet() for d in self.power_dice + self.quality_dice]:
                            # entry is a power/quality this hero doesn't already have
                            valid_triplets.append(entry)
        # Then validate each entry in die_options:
        valid_dice = [diesize for diesize in die_options if diesize in legal_dice]
        triplet_choice = []
        if len(valid_triplets) == 0:
            # We can't assign dice to a nonexistent power/quality
            print("Error! No power/quality options available!")
            return [[], die_options]
        elif len(valid_dice) == 0:
            # We can't assign dice that we don't have
            print("Error! No dice to assign!")
            return [triplets, []]
        elif len(valid_triplets) == 1:
            # Only one power/quality to assign to? Pass it to ChoosePQDieSize
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            return [[], self.ChoosePQDieSize(valid_triplets[0][0],
                                             valid_triplets[0][1:2],
                                             die_options,
                                             stepnum=max([0, stepnum]),
                                             inputs=pass_inputs)]
        else:
            # If none of these, the user has to make a choice...
            # Define some useful text variables:
            list_cat = DieCategory(valid_triplets)
            print_type = categories_singular[list_cat]
            print_types = categories_plural[list_cat]
            print_names = [mixed_collection[entry[0]][entry[1]][entry[2]] \
                           for entry in valid_triplets]
            print_triplets = [entry for entry in valid_triplets]
            dice_report = "You have the following " + print_type + " dice available: " + \
                          str(valid_dice)
            section_length = 25
            if len(valid_triplets) > section_length:
                sections = math.ceil(len(valid_triplets)/section_length)
                section_bounds = [print_names[s*section_length] + \
                                " through " + \
                                print_names[min(s*section_length + section_length-1,
                                                len(valid_triplets)-1)] \
                                for s in range(sections)]
                options_report = "You have a lot of " + print_type + " options..."
                choice_request = "Choose a section of the list to pick from:"
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    dispWidth = 75
                    details = ["" for i in range(sections)]
                    for i in range(sections):
                        this_section = print_names[i*section_length]
                        for j in range(1, section_length):
                            if i*section_length + j < len(valid_triplets):
                                this_section += ", " + print_names[i*section_length + j]
                        details[i] = split_text(this_section, width=dispWidth)
                    answer = IntVar()
                    question = ExpandWindow(self.myWindow,
                                            dice_report + "\n" + \
                                            options_report + "\n" + \
                                            choice_request,
                                            section_bounds,
                                            details,
                                            var=answer,
                                            title=print_type + " Selection",
                                            rwidth=dispWidth)
                    entry_index = answer.get()
                else:
                    entry_options = string.ascii_uppercase[0:sections]
                    section_list = [entry_options[s] + ": " + section_bounds[s] \
                                    for s in range(sections)]
                    col_num = 4
                    columns = [0] * col_num
                    for c in range(len(columns)):
                        if c in range(len(print_names)):
                            columns[c] = max([len(print_names[i])+2 \
                                              for i in range(len(print_names)) \
                                              if i%section_length%col_num == c])
                    for i in range(len(print_names)):
                        pq_text = print_names[i]
                        this_col = i%section_length%col_num
                        while len(pq_text) < columns[this_col]:
                            pq_text += " "
                        if i%section_length == 0:
                            # First in a section; prepend "*: "
                            print("    " + entry_options[math.floor(i/section_length)] + ": ",
                                  end="")
                        elif this_col == 0:
                            # First in a row within a section; prepend empty space
                            print("    " + "   ", end="")
                        if this_col == col_num-1:
                            # Last in a row
                            print(pq_text)
                        elif i%section_length == section_length-1:
                            # Last in a section
                            print(pq_text)
                        elif i == len(print_names)-1:
                            # Last in the list
                            print(pq_text)
                        else:
                            print(pq_text, end="")
                    decision = self.ChooseIndex(section_list,
                                                prompt=dice_report + "\n" + options_report + \
                                                "\n" + choice_request,
                                                inputs=inputs,
                                                title=print_type + " Selection")
                    entry_index = decision[0]
                    inputs = decision[1]
                entry_start = entry_index * section_length
                entry_end = min(entry_start + section_length, len(valid_triplets))
                print_names = print_names[entry_start:entry_end]
                print_triplets = print_triplets[entry_start:entry_end]
            # Now we can ask the user to choose the power/quality they want.
            decision = self.ChooseIndex(print_names,
                                        prompt=dice_report + "\n" + "Choose one of these " + \
                                        print_types + ":",
                                        inputs=inputs,
                                        title=print_type + " Selection")
            entry_index = decision[0]
            inputs = decision[1]
            triplet_choice = print_triplets[entry_index]
            # Now we have the user's choice.
            # We can have them assign a die to it using ChoosePQDieSize.
            remaining_dice = []
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            remaining_dice = self.ChoosePQDieSize(triplet_choice[0],
                                                  triplet_choice[1:],
                                                  valid_dice,
                                                  stepnum=max([0, stepnum]),
                                                  inputs=pass_inputs)
            valid_triplets.remove(triplet_choice)
            return [valid_triplets, remaining_dice]
    def AssignAllPQ(self, triplets, dice_options, stepnum=0, inputs=[]):
        # Prompts the user to assign ALL the dice in dice_options to powers and/or qualities from
        #  triplets, one at a time
        # inputs: a set of text inputs to use automatically instead of prompting the user
        # stepnum: the number of the step of hero creation (1-7) at which these dice are being added
        # No return value
        if len(inputs) > 0:
            print("### AssignAllPQ: inputs=" + str(inputs))
        remaining_triplets = [entry for entry in triplets]
        remaining_dice = [die_size for die_size in dice_options]
        while len(remaining_dice) > 0:
            # Use ChoosePQ to have the user assign one of the dice to one of the powers/qualities
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            remainders = self.ChoosePQ(remaining_triplets,
                                       remaining_dice,
                                       stepnum=max([0, stepnum]),
                                       inputs=pass_inputs)
            remaining_triplets = remainders[0]
            remaining_dice = remainders[1]
            # Repeat until there are no more dice.
    def AddPrinciple(self,
                     category,
                     index,
                     title="",
                     roleplaying="",
                     minor="",
                     major="",
                     green="",
                     stepnum=0,
                     inputs=[]):
        # Adds a fully defined Principle with the specified category, index, title, roleplaying
        #  text, minor twist, major twist, and Green Ability.
        # stepnum: the number of the step of hero creation (1-7) at which this Principle is being
        #  added
        # inputs: a set of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### AddPrinciple: inputs=" + str(inputs))
        if len(self.principles) > 1:
            # Can't have more than 2 Principles.
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user to choose.
                answer = IntVar()
                dispWidth = 100
                options = [str(x) for x in self.principles] + ["Cancel"]
                details = [x.details(width=dispWidth) for x in self.principles]
                question = ExpandWindow(self.myWindow,
                                        "Choose a Principle to replace: ",
                                        options,
                                        details,
                                        var=answer,
                                        title="Principle Selection",
                                        rwidth=dispWidth)
                entry_index = answer.get()
            else:
                print(self.hero_name + " already has 2 Principles: ")
                for ex in self.principles:
                    ex.display(prefix="    ")
                if len(inputs) > 0:
                    print("Enter A to replace the first one, B to replace the second one, or " + \
                          "anything else to cancel.")
                    print("> " + inputs[0])
                    entry_choice = inputs.pop(0)[0].upper()
                else:
                    entry_choice = input("Enter A to replace the first one, B to replace the " + \
                                         "second one, or anything else to cancel.\n").upper()
                if entry_choice in "AB":
                    entry_index = "AB".find(entry_choice)
            if entry_index in range(2):
                pri = Principle(category,
                                index,
                                title,
                                roleplaying,
                                minor,
                                major,
                                green,
                                stepnum=max([0, stepnum]))
                removed = self.principles[entry_index]
                removed_indices = [i for i in range(len(self.abilities)) \
                                   if self.abilities[i].text == removed.green_ability]
                self.principles[entry_index] = pri
                self.abilities[removed_indices[0]] = Ability("Principle of " + pri.title,
                                                             "A",
                                                             pri.green_ability,
                                                             0,
                                                             hero_step=max([0, stepnum]))
                print("Replaced " + str(removed) + " with " + str(pri) + "!")
        else:
            pri = Principle(category,
                            index,
                            title,
                            roleplaying,
                            minor,
                            major,
                            green,
                            stepnum=max([0, stepnum]))
            self.principles.append(pri)
            pri_ability = Ability("Principle of " + pri.title,
                                  "A",
                                  pri.green_ability,
                                  0,
                                  hero_step=max([0, stepnum]))
            self.abilities.append(pri_ability)
            print("Added " + str(pri) + "!")
        # If we have a GUI, update it
        if isinstance(self.myFrame, HeroFrame):
            self.myFrame.UpdateAll(self)
    def ChoosePrinciple(self, category, stepnum=0, inputs=[]):
        # Lets the user choose a Principle from the specified category and modify it if necessary
        #  before adding it to the hero.
        # stepnum: the number of the step of hero creation (1-7) at which this Principle is being
        #  added
        # inputs: a set of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### ChoosePrinciple: category=" + str(category))
            print("### ChoosePrinciple: inputs=" + str(inputs))
        if category not in range(len(rc_master)):
            print("Error! Invalid category: " + str(category))
        else:
            r_options = [Principle(category, i) for i in range(len(rc_master[category]))]
            if rc_names[category][0].upper() in "AEIOU":
                prompt = "Choose an " + rc_names[category] + " Principle."
            else:
                prompt = "Choose a " + rc_names[category] + " Principle."
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user
                answer = IntVar()
                question = ExpandWindow(self.myWindow,
                                        prompt,
                                        [x.title for x in r_options],
                                        [x.details() for x in r_options],
                                        var=answer,
                                        title="Principle Selection")
                entry_index = answer.get()
            else:
                print(prompt)
                print("The following Principles are in this category...")
                entry_options = string.ascii_uppercase[0:len(r_options)]
                for i in range(len(r_options)):
                    print("    " + entry_options[i] + ": " + r_options[i].title)
                entry_choice = ' '
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a Principle expanded, or an " + \
                              "uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a Principle " + \
                                             "expanded, or an uppercase letter to select it.\n")
                    if entry_choice.upper() in entry_options and not entry_choice in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        r_options[entry_index].display("    ", width=96)
                entry_index = entry_options.find(entry_choice)
            ri = r_options[entry_index]
            print(str(ri) + " selected!")
            entry_choice = ' '
            entry_options = "YN"
            entry_title = ri.title
            rename_prompt = "Do you want to customize " + str(ri) + "?"
            decision = choose_letter(entry_options,
                                     ' ',
                                     prompt=rename_prompt,
                                     repeat_message="Please enter Y or N.",
                                     inputs=inputs)
            entry_choice = decision[0]
            inputs = decision[1]
            if entry_choice == "N":
                print("Standard " + str(ri) + " selected.")
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddPrinciple(category,
                                  entry_index,
                                  stepnum=max([0, stepnum]),
                                  inputs=pass_inputs)
            else:
                # Copy the values in ri so they can be edited or left alone.
                entry_title = ri.title
                entry_roleplaying = ri.during_roleplaying
                entry_minor = ri.minor_twist
                entry_major = ri.major_twist
                entry_green = ri.green_ability
                if self.UseGUI(inputs):
                    # Create a PrincipleWindow to prompt the user.
                    dispWidth = 100
                    titleVar = StringVar()
                    roleplayingVar = StringVar()
                    minorVar = StringVar()
                    majorVar = StringVar()
                    greenVar = StringVar()
                    prinModifier = PrincipleWindow(self.myWindow,
                                                   ri,
                                                   titleVar,
                                                   roleplayingVar,
                                                   minorVar,
                                                   majorVar,
                                                   greenVar,
                                                   title="Customize " + str(ri),
                                                   width=dispWidth)
                    entry_title = titleVar.get()
                    entry_roleplaying = roleplayingVar.get()
                    entry_minor = minorVar.get()
                    entry_major = majorVar.get()
                    entry_green = greenVar.get()
                    # ...
                else:
                    # Ask the user what part they want to change.
                    entry_dict = dict(A="Title",
                                      B="During Roleplaying text",
                                      C="Minor Twist",
                                      D="Major Twist",
                                      E="Green Ability",
                                      F="Done (no further changes)")
                    entry_id = ' '
                    while entry_id != 'F':
                        if entry_id == ' ':
                            print("Choose a section to customize:")
                        else:
                            print("Any further changes?")
                        for i in range(len(entry_dict)):
                            # Print a list of all options that haven't been used
                            print("    " + list(entry_dict)[i] + ": " + \
                                  entry_dict[list(entry_dict)[i]])
                        decision = choose_letter(list(entry_dict), ' ', inputs=inputs)
                        entry_id = decision[0]
                        inputs = decision[1]
                        # Now the user has chosen a section to customize...
                        if entry_id == 'A':
                            print("Current title: " + entry_title)
                            if len(inputs) > 0:
                                print("Enter a new title:")
                                print("> Principle of " + inputs[0])
                                entry_title = inputs.pop(0)
                            else:
                                entry_title = input("Enter a new title:\nPrinciple of ")
                            print("New title: Principle of " + entry_title)
                        elif entry_id == 'B':
                            printlong("Current During Roleplaying text: " + entry_roleplaying, 100)
                            if len(inputs) > 0:
                                print("Enter new During Roleplaying text:")
                                print("> " + inputs[0])
                                entry_roleplaying = inputs.pop(0)
                            else:
                                entry_roleplaying = input("Enter new During Roleplaying text:\n")
                            printlong("New During Roleplaying text: " + entry_roleplaying, 100)
                        elif entry_id == 'C':
                            printlong("Current minor twist: " + entry_minor, 100)
                            if len(inputs) > 0:
                                print("Enter a new minor twist:")
                                print("> " + inputs[0])
                                entry_minor = inputs.pop(0)
                            else:
                                entry_minor = input("Enter a new minor twist:\n")
                            printlong("New minor twist: " + entry_minor, 100)
                        elif entry_id == 'D':
                            printlong("Current major twist: " + entry_major, 100)
                            if len(inputs) > 0:
                                print("Enter a new major twist:")
                                print("> " + inputs[0])
                                entry_major = inputs.pop(0)
                            else:
                                entry_major = input("Enter a new major twist:\n")
                            printlong("New major twist: " + entry_major, 100)
                        elif entry_id == 'E':
                            printlong("Current Green Ability: " + entry_green, 100)
                            if len(inputs) > 0:
                                print("Enter a new Green Ability:")
                                print("> " + inputs[0])
                                entry_green = inputs.pop(0)
                            else:
                                entry_green = input("Enter a new Green Ability:\n")
                            printlong("New Green Ability: " + entry_green, 100)
                        del entry_dict[entry_id]
                    print("OK!")
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddPrinciple(category,
                                  entry_index,
                                  entry_title,
                                  entry_roleplaying,
                                  entry_minor,
                                  entry_major,
                                  entry_green,
                                  stepnum=max([0, stepnum]),
                                  inputs=pass_inputs)
    def AddBackground(self, bg_index, inputs=[]):
        # Walks the user through adding the quality dice and Principle that they get from the
        #  Background specified by bg_index.
        # inputs: a set of text inputs to use automatically instead of prompting the user
        # Returns the set of dice they'll use in the Power Source step.
        if len(inputs) > 0:
            print("### AddBackground: inputs=" + str(inputs))
        # This is Step 1 of hero creation!
        this_step = 1
        your_bg = bg_collection[bg_index]
        # your_bg is a list of 7 objects:
        # 0: title
        # 1: description
        # 2: list of quality dice
        remaining_dice = [d for d in your_bg[2]]
        # 3: required quality triplet (if applicable)
        q_requirements = your_bg[3]
        # 4: optional quality triplets
        q_options = [triplet for triplet in your_bg[4]]
        # 5: Principle category
        r_category = your_bg[5]
        # 6: list of Power Source dice
        ps_dice = your_bg[6]
        if self.background in range(len(bg_collection)):
            # This hero already has a Background
            print("Error! " + self.hero_name + " already has the " + \
                  bg_collection[self.background][0] + " Background.")
            input()
            # Return the Power Source dice from the existing Background.
            return bg_collection[self.background][6]
        else:
            # This hero doesn't have a Background yet, so we can add this one.
            print("OK! You've chosen the " + your_bg[0] + " Background!")
            self.background = bg_index
            print("You get " + str(your_bg[2]) + " to assign to Qualities.")
            if len(q_requirements) > 0:
                # Use ChoosePQDieSize to have the user choose which of their dice goes to the
                #  required quality.
                # ChoosePQDieSize returns the list of unused dice, so update remaining_dice with
                #  that list.
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                remaining_dice = self.ChoosePQDieSize(q_requirements[0][0],
                                                      q_requirements[0][1:],
                                                      remaining_dice,
                                                      stepnum=this_step,
                                                      inputs=pass_inputs)
            # Use AssignAllPQ to have the user assign each remaining die to one of the optional
            #  qualities.
            # AssignAllPQ runs until there are no dice left, so there's no need to update
            #  remaining_dice afterward.
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AssignAllPQ(q_options, remaining_dice, stepnum=this_step, inputs=pass_inputs)
            self.RefreshFrame()
            # Use ChoosePrinciple to have the user select a Principle from the specified category.
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.ChoosePrinciple(r_category, stepnum=this_step, inputs=pass_inputs)
            print("That's all for your Background! Take " + str(ps_dice) + \
                  " to use in the Power Source step.")
            self.ps_dice = ps_dice
            self.RefreshFrame()
            return ps_dice
    def GuidedBackground(self, inputs=[]):
        # Walks the user through randomly selecting a Background as specified in the rulebook.
        # Returns the index of the Background selected.
        # inputs: a set of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### GuidedBackground: inputs=" + str(inputs))
        # The user can reroll any number of their dice once per step.
        rerolls = 1
        prev_result = 0
        while rerolls >= 0:
            die_results = []
            if prev_result < 1:
                print("Rolling 2d10 for Background...")
                die_results = [random.randint(1, 10), random.randint(1, 10)]
            else:
                print("Keeping " + str(prev_result) + \
                      " from previous roll. Rolling 1d10 for Background...")
                die_results = [prev_result, random.randint(1, 10)]
            roll_report = "Rolled " + str(die_results[0]) + " and " + str(die_results[1]) + "."
            # The player can choose between any single result or the sum of any pair of results.
            # Since there are only two dice, this is a straightforward list: the two results and
            #  their sum.
            bg_options = [min(die_results), max(die_results), sum(die_results)]
            # In case of doubles, remove the duplicate roll:
            if bg_options[0] == bg_options[1]:
                bg_options[1:2] = []
            # To convert to 0-index, subtract 1 from each option.
            bg_indices = [x-1 for x in bg_options]
            # Let the user choose from the options provided by their roll...
            entry_choice = ' '
            entry_options = string.ascii_uppercase[0:len(bg_options) + rerolls]
            if self.UseGUI(inputs):
                # Create an ExpandWindow to ask the user to choose
                answer = IntVar()
                options = [bg_collection[x][0] + " (" + str(x) + ")" for x in bg_indices]
                if rerolls > 0:
                    options += ["REROLL"]
                question = ExpandWindow(self.myWindow,
                                        roll_report + "\nChoose one:",
                                        options,
                                        [BackgroundDetails(x, width=0) for x in bg_indices],
                                        var=answer,
                                        title="Background Selection",
                                        rwidth=bg_width)
                entry_index = answer.get()
            else:
                print(roll_report)
                for i in range(len(entry_options)-rerolls):
                    print("    " + entry_options[i] + ": " + bg_collection[bg_indices[i]][0] + \
                          " (" + str(bg_options[i]) + ")")
                if rerolls > 0:
                    print("    " + entry_options[len(entry_options)-1] + ": REROLL")
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a Background expanded, or an " + \
                              "uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a Background " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options[:-1] and entry_choice not in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        DisplayBackground(bg_indices[entry_index], "    ", width=96)
                entry_index = entry_options.find(entry_choice)
            # Now we have a commitment to a valid choice from the list.
            if entry_index == len(bg_options):
                # User selected to reroll.
                entry_options = "YN"
                entry_choice = ' '
                decision = choose_letter(entry_options,
                                         ' ',
                                         prompt="Do you want to keep any of the previous results? (y/n)",
                                         repeat_message="Please enter Y or N.",
                                         inputs=inputs)
                entry_choice = decision[0]
                inputs = decision[1]
                if entry_choice == 'Y':
                    decision = self.ChooseIndex([str(r) for r in die_results],
                                                prompt="Choose which result to keep:",
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    prev_result = die_results[entry_index]
                rerolls = 0
            else:
                # User selected a background.
                print(bg_collection[bg_indices[entry_index]][0] + " Background selected.")
                return bg_indices[entry_index]
    def ConstructedBackground(self, inputs=[]):
        # Walks the user through selecting a Background from the full list of options.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns the index of the Background selected.
        if len(inputs) > 0:
            print("### ConstructedBackground: inputs=" + str(inputs))
        entry_options = string.ascii_uppercase[0:len(bg_collection)]
        entry_choice = ' '
        if self.UseGUI(inputs):
            # Create an ExpandWindow to prompt the user
            answer = IntVar()
            question = ExpandWindow(self.myWindow,
                                    "Choose a Background from the list:",
                                    [x[0] for x in bg_collection],
                                    [BackgroundDetails(i, width=0) \
                                     for i in range(len(bg_collection))],
                                    var=answer,
                                    title="Background Selection",
                                    rwidth=bg_width)
            entry_index = answer.get()
        else:
            print("Choose a Background from the list:")
            for i in range(len(bg_collection)):
                print("    " + entry_options[i] + ": " + bg_collection[i][0] + " (" + str(i+1) + ")")
            while entry_choice not in entry_options:
                if len(inputs) > 0:
                    print("Enter a lowercase letter to see a Background expanded, or an uppercase " + \
                          "letter to select it.")
                    print("> " + inputs[0])
                    entry_choice = inputs.pop(0)[0]
                else:
                    entry_choice = input("Enter a lowercase letter to see a Background expanded, or " + \
                                         "an uppercase letter to select it.\n")[0]
                if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                    entry_index = entry_options.find(entry_choice.upper())
                    DisplayBackground(entry_index, "    ", width=96)
            entry_index = entry_options.find(entry_choice)
        print(bg_collection[entry_index][0] + " Background selected.")
        return entry_index
    def AddAbility(self, new_ability):
        # Adds a fully defined Ability.
        if new_ability.zone in range(len(status_zones)):
            self.abilities.append(new_ability)
            print("Added " + str(new_ability) + " in " + status_zones[z_num])
            # If we have a GUI, update it
            if isinstance(self.myFrame, HeroFrame):
                self.myFrame.UpdateAll(self)
        else:
            print("Error! Couldn't add " + str(new_ability) + ": no zone specified!")
    def ChooseAbility(self,
                      template_options,
                      zone,
                      triplet_options=[],
                      category_req=-1,
                      add=1,
                      alt_powers=[],
                      stepnum=0,
                      inputs=[]):
        # Lets the user choose an Ability from the list of options and modify it as necessary before
        #  adding it to the hero's specified status zone.
        # triplet_options: the chosen Ability must use one of the specified Powers/Qualities
        # category_req: the chosen Ability must use a die from the specified category
        #  (0 for Quality, 1 for Power)
        # add: 1 if the finished Ability is added to the hero's main sheet, 0 if it should be
        #  returned instead
        # alt_powers: a list of alternate Power dice (e.g., if this Ability is being added to a
        #  Mode or Form where the hero's Powers are different)
        # stepnum: the number of the step of hero creation (1-7) at which this Ability is being
        #  added
        # inputs: a list of text inputs to be used rather than prompting the user
        # Returns:
        #   if add==1: the set of unused abilities.
        #   otherwise: the filled-in Ability
        if len(inputs) > 0:
            print("### ChooseAbility: inputs=" + str(inputs))
        p_dice = self.power_dice
        if len(alt_powers) > 0:
            p_dice = alt_powers
        if zone not in range(len(status_zones)):
            print("Error! " + str(zone) + " is not a valid zone identifier.")
            return template_options
        if category_req in [0,1] and len(triplet_options) > 0:
            matching_options = [t for t in triplet_options if t[0]==category_req]
            if len(matching_options) == 0:
                print("Error! None of the required triplets " + str(triplet_options) + \
                      " match the required category " + str(category_req) + ".")
                if add==1:
                    return template_options
                else:
                    return []
            else:
                triplet_options = matching_options
        # If triplet_options were specified, verify that they're valid powers/qualities...
        if len(triplet_options) > 0:
            triplet_options = ValidPQs(triplet_options)
            if len(triplet_options) == 0:
                print("Error! None of the required triplets " + str(triplet_options) + \
                      " are valid Powers or Qualities.")
                if add==1:
                    return template_options
                else:
                    return []
            # ... and that the hero has at least 1 of them...
            hero_triplets = [d.triplet() for d in p_dice + self.quality_dice]
            triplet_options = [triplet for triplet in triplet_options if triplet in hero_triplets]
            if len(triplet_options) == 0:
                print("Error! " + self.hero_name + " has none of the specified " + \
                      category_plural[DieCategory(triplet_options)] + " (" + \
                      MixedPQs(triplet_options) + ").")
                if add==1:
                    return template_options
                else:
                    return []
            # If triplet_options includes ALL of the hero's dice, then it doesn't actually restrict
            #  the player's choices, and we can forget about it
            if len([x for x in hero_triplets if x not in triplet_options]) == 0:
                triplet_options = []
        # ... then remove any template_options with incompatible requirements
        matching_templates = []
        for a in template_options:
            a_matches = True
            for i in [j for j in range(len(a.pq_options)) if len(a.pq_options[j]) > 0]:
                a_matching_options = [t for t in a.pq_options[i]]
                if len(triplet_options) > 0:
                    # If triplet_options are specified, and pq_options[i] are specified, then the
                    #  only matching options are the ones that fit both
                    a_matching_options = [t for t in a.pq_options[i] if t in triplet_options]
                if category_req in [0,1]:
                    # If category_req is specified, and pq_options[i] are specified, then the only
                    #  matching options are the ones that fit both
                    a_matching_options = [t for t in a.pq_options[i] if t[0]==category_req]
                if len(a_matching_options) == 0:
                    a_matches = False
            if a_matches:
                matching_templates.append(a)
        if len(matching_templates) == 0:
            print("Error! All of the ability templates had power/quality requirements " + \
                  "incompatible with the specified options " + str(triplet_options) + ".")
            if add==1:
                return template_options
            else:
                return []
        else:
            template_options = matching_templates
        ability_template = ""
        if len(template_options) == 0:
            print("Error! No Abilities were provided.")
            if add==1:
                return template_options
            else:
                return []
        elif len(template_options) == 1:
            ability_template = template_options[0]
        else:
            if len(triplet_options) > 1:
                option_text = MixedPQ(triplet_options[0])
                for i in range(1,len(triplet_options)-1):
                    option_text += ", " + MixedPQ(triplet_options[i])
                if option_text != MixedPQ(triplet_options[0]):
                    option_text += ","
                option_text += " or " + MixedPQ(triplet_options[len(triplet_options)-1])
                prompt = "Choose one of these Abilities to add in " + status_zones[zone] + \
                          ", using " + option_text + ":"
            elif len(triplet_options) == 1:
                prompt = "Choose one of these Abilities to add in " + status_zones[zone] + \
                         ", using " + MixedPQ(triplet_options[0]) + ":"
            elif category_req in [0,1]:
                prompt = "Choose one of these Abilities to add in " + status_zones[zone] + \
                         ", using a " + categories_singular[category_req] + ":"
            else:
                prompt = "Choose one of these Abilities to add in " + status_zones[zone] + ":"
            printlong(prompt, 100)
            col_num = 3
            section_length = 24
            if len(template_options) > section_length:
                sections = math.ceil(len(template_options)/section_length)
                entry_options = string.ascii_uppercase[0:sections]
                print("You have a lot of Ability options...")
                columns = [0] * col_num
                for c in range(len(columns)):
                    if c in range(len(template_options)):
                        columns[c] = max([len(str(template_options[i]))+2\
                                          for i in range(len(template_options)) if i%col_num == c])
                for i in range(len(template_options)):
                    as_text = str(template_options[i])
                    while len(as_text) < columns[i%col_num]:
                        as_text += " "
                    if i%section_length == 0:
                        if i%col_num != 0:
                            print()
                        print("    " + entry_options[math.floor(i/section_length)] + ": ", end="")
                    elif i%col_num == 0:
                        print("       ", end="")
                    if i%col_num == col_num-1 or i == len(template_options)-1:
                        print(as_text)
                    else:
                        print(as_text, end="")
                section_list = [str(template_options[s*section_length]) + " through " + \
                                str(template_options[min((s+1)*section_length-1,
                                                         len(template_options)-1)]) \
                                for s in range(sections)]
                decision = self.ChooseIndex(section_list,
                                            prompt="Choose a section of the list to pick from:",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                entry_start = entry_index * section_length
                entry_end = min(entry_start + section_length, len(template_options))
                template_options = template_options[entry_start:entry_end]
            if self.UseGUI(inputs):
                # Create an ExpandWindow to ask the user to choose an ability
                answer = IntVar()
                question = ExpandWindow(self.myWindow,
                                        prompt,
                                        [str(x) for x in template_options],
                                        [x.details() for x in template_options],
                                        var=answer,
                                        title="Hero Creation",
                                        rwidth=a_width)
                entry_index = answer.get()
            else:
                entry_options = string.ascii_uppercase[0:len(template_options)]
                entry_choice = ' '
                for i in range(len(template_options)):
                    print("    " + entry_options[i] + ": " + str(template_options[i]))
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see an ability expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see an ability expanded, " + \
                                             "or an uppercase letter to select it.\n")[0]
                    if entry_choice not in entry_options and entry_choice.upper() in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        template_options[entry_index].display(prefix="    ")
                entry_index = entry_options.find(entry_choice)
            ability_template = template_options[entry_index]
        # The first time we need the user to make a choice for this Ability, we'll display the
        # template text... but not before that, in case they don't have to
        has_displayed = False
        display_str = str(ability_template)
        if ability_template.zone == 3:
            # Out Abilities don't get names
            display_str = self.hero_name + "'s Out Ability"
        # If the ability has power or quality requirements, evaluate those to see if it can be added.
        for i in [0,1]:
            if len(ability_template.required_pqs[i]) > 0:
                matching_pqs = [d.triplet() for d in p_dice + self.quality_dice \
                                if d.triplet() in ability_template.required_pqs[i]]
                if len(matching_pqs) == 0:
                    print("Error! " + self.hero_name + \
                          "doesn't have any of the required Powers/Qualities for this ability (" + \
                          MixedPQs(ability_template.required_pqs[i]) + ").")
                    template_options.remove(ability_template)
                    if add==1:
                        return template_options
                    else:
                        return []
        # If the ability needs a damage category, prompt the user for it
        damage_entry = ability_template.insert_damage
        if ability_template.has_damage and damage_entry == 99:
            if not has_displayed:
                print("OK! Let's fill in " + display_str + "...")
                ability_template.display()
                has_displayed = True
##            print("Choose a damage category for this Ability:")
##            entry_options = "AB"
##            entry_choice = ' '
##            for i in [0,1]:
##                print("    " + entry_options[i] + ": " + damage_categories[i])
##            decision = choose_letter(entry_options, ' ', inputs=inputs)
##            entry_choice = decision[0]
##            inputs = decision[1]
##            damage_entry = entry_options.find(entry_choice)
            # EDIT: use self.ChooseIndex() instead of find()
            decision = self.ChooseIndex(damage_categories[0:2],
                                        prompt=ability_template.details() + "\n\n" +
                                        "Choose a damage category for this Ability:",
                                        title=display_str,
                                        inputs=inputs)
            damage_entry = decision[0]
            inputs = decision[1]
            # Testing...
        # If the ability needs an energy or element, prompt the user for it
        element_num = ability_template.insert_element
        if ability_template.has_element and element_num == 99:
            if ability_template.requires_energy:
                power_die_options = [d for d in p_dice if d.category==1]
                if len(power_die_options) == 0:
                    print("Error! " + self.name + \
                          " doesn't have any Elemental/Energy powers to use with " + \
                          ability_template.name + "!")
                    template_options.remove(ability_template)
                    if add==1:
                        return template_options
                    else:
                        return []
                elif len(power_die_options) == 1:
                    print(self.hero_name + "'s only Elemental/Energy power is " + \
                          str(power_die_options[0]) + ".")
                    element_num = power_die_options[0].index
                else:
                    if not has_displayed:
                        print("OK! Let's fill in " + display_str + "...")
                        ability_template.display()
                        has_displayed = True
                    decision = self.ChooseIndex([str(d) for d in power_die_options],
                                                prompt=ability_template.details() + "\n\n" +
                                                "Choose one of your Elemental/Energy " + \
                                                "Powers for this ability:",
                                                title=display_str,
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    element_num = power_die_options[entry_index].index
            else:
                if not has_displayed:
                    print("OK! Let's fill in " + display_str + "...")
                    ability_template.display()
                    has_displayed = True
                decision = self.ChooseIndex([mixed_collection[1][1][i] \
                                             for i in range(len(mixed_collection[1][1]))],
                                            prompt=ability_template.details() + "\n\n" +
                                            "Choose an energy or element for this Ability:",
                                            title=display_str,
                                            inputs=inputs)
                element_num = decision[0]
                inputs = decision[1]
        # If the ability needs any basic actions, prompt the user for those
        action_ids = ability_template.insert_actions
        if ability_template.has_actions:
            for i in [0,1]:
                if ("%a" + str(i)) in ability_template.text:
                    if not has_displayed:
                        print("OK! Let's fill in " + display_str + "...")
                        ability_template.display()
                        has_displayed = True
                    decision = self.ChooseIndex([basic_actions[j] \
                                                 for j in ability_template.action_options[i]],
                                                prompt=ability_template.details() + "\n\n" +
                                                "Choose a basic action for this Ability:",
                                                title=display_str,
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    action_ids[i] = ability_template.action_options[i][entry_index]
        # If the ability needs any Powers or Qualities, prompt the user for those
        pq_triplets = [x for x in ability_template.insert_pqs]
        pq_names = ["", ""]
        if ability_template.has_pq:
            for i in [0,1]:
                if ("%p" + str(i)) in ability_template.text:
                    category = categories_singular[ability_template.required_categories[i]]
                    die_options = self.quality_dice + p_dice
                    if ability_template.required_categories[i] == 0 or category_req == 0:
                        die_options = self.quality_dice
                    elif ability_template.required_categories[i] == 1 or category_req == 1:
                        die_options = p_dice
                    error = ""
                    if len(die_options) == 0:
                        error = ability_template.name + " requires a " + category + ", but " + \
                                self.hero_name + " doesn't have any " + category + " dice."
                    # If only certain powers/qualities are valid for this slot, narrow the field
                    #  to those
                    if len(ability_template.pq_options[i]) > 0:
                        die_options = [d for d in die_options \
                                       if d.triplet() in ability_template.pq_options[i]]
                        if len(die_options) == 0:
                            error = self.hero_name + " doesn't have any " + category + \
                                    " dice matching the ability's options for this slot (" + \
                                    MixedPQs(ability_template.pq_options[i]) + ")."
                    if len(triplet_options) > 0:
                        die_options = [d for d in die_options if d.triplet() in triplet_options]
                        if len(die_options) == 0:
                            error = self.hero_name + " doesn't have any " + category + \
                                    " dice matching the specified triplet options (" + \
                                    MixedPQs(triplet_options) + ")."
                    if len(die_options) == 0:
                        # No valid options? Fail with an error
                        print("Error! " + error)
                        template_options.remove(ability_template)
                        if add==1:
                            return template_options
                        else:
                            return []
                    elif len(die_options) == 1:
                        # Only 1 valid option? Select it and move on
                        print(self.hero_name + "'s only valid " + category + \
                              " die for this slot is " + str(die_options[0]) + ".")
                        pq_triplets[i] = die_options[0].triplet()
                        if die_options[0].flavorname != die_options[0].name:
                            pq_names[i] = die_options[0].flavorname
                    else:
                        # More than 1 valid option? Prompt the user to choose
                        if not has_displayed:
                            print("OK! Let's fill in " + display_str + "...")
                            ability_template.display()
                            has_displayed = True
                        decision = self.ChooseIndex([str(d) for d in die_options],
                                                    prompt=ability_template.details() + \
                                                    "\n\n" + "Choose a " + category + \
						    " die for this Ability:",
                                                    title=display_str,
                                                    inputs=inputs)
                        entry_index = decision[0]
                        inputs = decision[1]
                        pq_triplets[i] = die_options[entry_index].triplet()
                        if die_options[entry_index].flavorname != die_options[entry_index].name:
                            pq_names[i] = die_options[entry_index].flavorname
        # Phew! We've filled in all the variables for this Ability.
        # Show the user what they've built and prompt them for its name.
        new_ability = Ability(ability_template.name,
                              ability_template.type,
                              ability_template.text,
                              zone,
                              die_names=pq_names,
                              pq_reqs=ability_template.required_pqs,
                              pq_opts=ability_template.pq_options,
                              pq_ids=pq_triplets,
                              element_id=element_num,
                              actions=action_ids,
                              action_choices=ability_template.action_options,
                              categories=ability_template.required_categories,
                              damage_id=damage_entry,
                              energy=ability_template.requires_energy,
                              hero_step=max([0,stepnum]))
        if zone != 3:
            print("OK! " + self.hero_name + "'s new Ability is almost ready:")
            new_ability.display()
            # Green/Yellow/Red Abilities can have custom names
            entry_options = "YN"
            rename_prompt = "Do you want to give " + new_ability.name + " a new name (y/n)?"
            decision = choose_letter(entry_options,
                                     ' ',
                                     prompt=rename_prompt,
                                     repeat_message="Please enter Y or N.",
                                     inputs=inputs)
            entry_choice = decision[0]
            inputs = decision[1]
            if entry_choice == "Y":
                decision = self.EnterText(new_ability.details() + "\n\n" + \
                                          "Enter the new name for this Ability:",
                                          title=display_str,
                                          default=new_ability.name,
                                          inputs=inputs)
                new_ability.flavorname = decision[0]
                inputs = decision[1]
            if add==1:
                print("All set! Adding " + str(new_ability) + " to " + self.hero_name + "'s " + \
                      status_zones[zone] + " zone.")
            else:
                print(str(new_ability) + " is all done!")
        else:
            print("OK! " + self.hero_name + "'s new Ability is ready:")
            new_ability.display()
            # Out Abilities don't need names
            if add==1:
                print("Adding this Ability to " + self.hero_name + "'s " + status_zones[zone] + \
                      " zone.")
            else:
                print(str(new_ability) + " is all done!")
        if add==1:
            self.abilities.append(new_ability)
            template_options.remove(ability_template)
            # If we have a GUI, update it
            if isinstance(self.myFrame, HeroFrame):
                self.myFrame.UpdateAll(self)
            return template_options
        else:
            return new_ability
    def AddPowerSource(self, ps_index, pdice=[], inputs=[]):
        # Walks the user through adding the Powers, Yellow Abilities, and Green Ability
        #  (if applicable) that they get from the specified Power Source.
        # pdice: the set of dice received from the Background step to use in this one.
        #  If not specified here, uses self.ps_dice.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns the set of dice they'll use in the Archetype step.
        prefix = "### AddPowerSource: "
        if len(inputs) > 0:
            print(prefix + "inputs=" + str(inputs))
        if pdice == []:
            pdice = self.ps_dice
        # This is Step 2 of hero creation!
        this_step = 2
        your_ps = ps_collection[ps_index]
        # your_ps is a list of 10 objects:
        # 0: title
        # 1: description
        # 2: list of required powers (if applicable)
        required_powers = your_ps[2]
        # 3: list of optional powers
        optional_powers = your_ps[3]
        # 4: number of Yellow Abilities
        yellow_count = your_ps[4]
        # 5: list of Yellow Ability options
        yellow_options = [a for a in your_ps[5]]
        # 6: number of Green Abilities (if applicable)
        green_count = your_ps[6]
        # 7: list of Green Ability options (if applicable)
        green_options = [a for a in your_ps[7]]
        # 8: index of bonus effect
        ps_bonus = your_ps[8]
        # 9: set of archetype dice
        arc_dice = your_ps[9]
        if self.power_source in range(len(ps_collection)):
            # This hero already has a Power Source
            print("Error! " + self.hero_name + " already has the " + \
                  ps_collection[self.power_source][0] + " Power Source.")
            input()
            # Return the Archetype dice from the existing Power Source.
            return ps_collection[self.power_source][9]
        else:
            # This hero doesn't have a Power Source, so we can add this one.
            self.power_source = ps_index
            print("OK! You've chosen the " + your_ps[0] + " Power Source!")
            print("You have " + str(pdice) + " to assign to Powers.")
            if len(required_powers) > 0:
                # Use ChoosePQ to assign one of pdice to one of required_powers
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                pdice = self.ChoosePQ(required_powers,
                                      pdice,
                                      stepnum=this_step,
                                      inputs=pass_inputs)[0]
            # Use AssignAllPQ to assign each of pdice to one of optional_powers
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AssignAllPQ(optional_powers, pdice, stepnum=this_step, inputs=pass_inputs)
            for i in range(yellow_count):
                # Use ChooseAbility to select and add a Yellow Ability from yellow_options and
                #  update yellow_options to remove that Ability
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                legal_triplets = [x.triplet() for x in self.power_dice] + \
                                 [y.triplet() for y in self.quality_dice]
                # Make a list of abilities the hero has in this zone from this Archetype
                ps_zone_abilities = [x for x in self.abilities \
                                     if x.step == this_step and x.zone == 1]
                print(prefix + "ps_zone_abilities = " + \
                      str([str(x) for x in ps_zone_abilities]))
                if len(ps_zone_abilities) > 0:
                    # Start by making a list of the Powers/Qualities already used in
                    #  ps_zone_abilities:
                    ps_triplets = []
                    for x in ps_zone_abilities:
                        ps_triplets += [y for y in x.insert_pqs if len(y) == 3]
                    # Remove any repeats
                    for i in range(len(ps_triplets)):
                        trip = ps_triplets[i]
                        for j in range(i + 1, len(ps_triplets)):
                            if ps_triplets[j] == trip:
                                del ps_triplets[j]
                    print(prefix + "ps_triplets = " + str(ps_triplets))
                    print(prefix + "(" + str(MixedPQs(ps_triplets)) + ")")
                    # Remove those previously-used triplets from the list of triplets that can be
                    #  used in this ability:
                    while len([x for x in legal_triplets if x in ps_triplets]) > 0:
                        for x in ps_triplets:
                            legal_triplets.remove(x)
                    print(prefix + "legal_triplets = " + str(legal_triplets))
                    print(prefix + "(" + str(MixedPQs(legal_triplets)) + ")")
                yellow_options = self.ChooseAbility(yellow_options,
                                                    1,
                                                    triplet_options=legal_triplets,
                                                    stepnum=this_step,
                                                    inputs=pass_inputs)
            for i in range(green_count):
                # Use ChooseAbility to select and add a Green Ability from green_options and update
                #  green_options to remove that Ability
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                green_options = self.ChooseAbility(green_options,
                                                   0,
                                                   stepnum=this_step,
                                                   inputs=pass_inputs)
            # Evaluate and implement ps_bonus
            if ps_bonus == 1:
                # Training: Next step, add a bonus d8 Quality from your Archetype's list.
                self.arc_bonus_quality = 8
                print("Bonus: Next step, you'll get an extra d" + str(self.arc_bonus_quality) + \
                      " Quality from that Archetype's list.")
            elif ps_bonus == 2:
                # Mystical: Gain a d10 Information Quality.
                print("Bonus: You get a d10 Information Quality.")
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(Category(0,0), [10], stepnum=this_step, inputs=pass_inputs)
            elif ps_bonus == 3:
                # Supernatural: Gain a d10 Power that ISN'T listed.
                print("Bonus: You get a d10 Power that ISN'T on the Supernatural list.")
                power_triplets = [[1,a,b] for b in range(len(mixed_collection[1][a])) \
                                  for a in range(len(mixed_collection[1]))]
                non_optional_powers = [triplet for triplet in power_triplets \
                                       if triplet not in optional_powers]
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(non_optional_powers, [10], stepnum=this_step, inputs=pass_inputs)
            elif ps_bonus == 4:
                # Alien: Upgrade a d6 Power or Quality to d8. If you can't, instead gain 1 more d6
                #  Power from the Alien list.
                d6_pqs = [d for d in self.power_dice + self.quality_dice if d.diesize == 6]
                if len(d6_pqs) == 0:
                    # No d6s to upgrade.
                    print("Bonus: Since you can't upgrade a d6 Power or Quality, " + \
                          "you gain a d6 Power from the Alien list.")
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.ChoosePQ(optional_powers, [6], stepnum=this_step, inputs=pass_inputs)
                elif len(d6_pqs) == 1:
                    # Exactly 1 d6: upgrade it without prompting the user.
                    print("Bonus: Upgrading your d6 in " + d6_pqs[0].flavorname + " to a d8.")
                    d6_pqs[0].SetPrevious(this_step)
                    d6_pqs[0].diesize = 8
                else:
                    # More than 1 d6: user gets to choose which to upgrade.
                    decision = self.ChooseIndex([str(x) for x in d6_pqs],
                                                prompt="Bonus: Choose a d6 Power or Quality to " + \
                                                "upgrade to d8.",
                                                title="Power Source",
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    print("Upgrading " + d6_pqs[entry_index].flavorname + " to d8.")
                    d6_pqs[entry_index].SetPrevious(this_step)
                    d6_pqs[entry_index].diesize = 8
            elif ps_bonus == 5:
                # Genius: Gain 1 d10 Information or Mental Quality
                print("Bonus: You get a d10 Information or Mental Quality.")
                optional_qualities = Category(0,0) + Category(0,1)
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(optional_qualities, [10], stepnum=this_step, inputs=pass_inputs)
            elif ps_bonus == 6:
                # Cosmos: Downgrade a d8/d10/d12 power by 1 die size and upgrade a d6/d8/d10
                #  power by 1 die size.
                print("Bonus: Downgrade one Power by 1 die size and " + \
                      "upgrade another Power by 1 die size.")
                d8_plus_powers = [d for d in self.power_dice if d.diesize > 6]
                downgraded_power = ""
                if len(d8_plus_powers) == 1:
                    print("Downgrading " + str(d8_plus_powers[0]) + " by one size (d" + \
                          str(d8_plus_powers[0].diesize-2) + ").")
                    d8_plus_powers[0].diesize = d8_plus_powers[0].diesize-2
                    downgraded_power = d8_plus_powers[0]
                else:
                    decision = self.ChooseIndex([str(x) for x in d8_plus_powers],
                                                prompt="Choose a Power to downgrade:",
                                                title="Power Source",
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    downgraded_power = d8_plus_powers[entry_index]
                    print("Downgrading " + str(downgraded_power) + " by one size (d" + \
                          str(downgraded_power.diesize-2) + ").")
                    downgraded_power.SetPrevious(this_step)
                    downgraded_power.diesize = downgraded_power.diesize-2
                d10_minus_powers = [d for d in self.power_dice if d.diesize < 12]
                d10_minus_powers.remove(downgraded_power)
                if len(d10_minus_powers) == 1:
                    print("Upgrading " + str(d10_minus_powers[0]) + " by one size (d" + \
                          str(d10_minus_powers[0].diesize+2) + ").")
                    d10_minus_powers[0].diesize = d10_minus_powers[0].diesize + 2
                else:
                    decision = self.ChooseIndex([str(x) for x in d10_minus_powers],
                                                prompt="Choose a Power to upgrade:",
                                                title="Power Source: Cosmos",
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    upgraded_power = d10_minus_powers[entry_index]
                    print("Upgrading " + str(upgraded_power) + " by one size (d" + \
                          str(upgraded_power.diesize+2) + ").")
                    upgraded_power.SetPrevious(this_step)
                    upgraded_power.diesize = upgraded_power.diesize + 2
            elif ps_bonus == 7:
                # Unknown: Gain a d8 Social Quality.
                print("Bonus: You get a d8 Social Quality.")
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(Category(0,3), [8], stepnum=this_step, inputs=pass_inputs)
            elif ps_bonus == 8:
                # The Multiverse: Gain a d6 Power from ANY category.
                print("Bonus: You get a d6 Power from ANY category.")
                power_triplets = AllCategories()
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(power_triplets, [6], stepnum=this_step, inputs=pass_inputs)
            print("That's all for your Power Source! Take " + str(arc_dice) + \
                  " to use in the Archetype step.")
            self.arc_dice = arc_dice
            return arc_dice
    def GuidedPowerSource(self, pdice=[], inputs=[]):
        # Walks the user through randomly selecting a Power Source as specified in the rulebook.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns the index of the selected Power Source.
        if pdice == [] and self.ps_dice == []:
            print("Error! No dice have been specified for this step.")
            return
        elif pdice == []:
            pdice = self.ps_dice
        elif len(pdice) not in [2,3]:
            print("Error! " + str(pdice) + " is not a valid set of Power Source dice.")
            return
        # The user can reroll any number of their dice once per step.
        rerolls = 1
        prev_results = [0 for d in pdice]
        while rerolls >= 0:
            die_results = prev_results
            print("Rolling " + dice_combo(pdice, results=die_results) + " for Power Source:")
            for i in range(len(pdice)):
                if die_results[i] == 0:
                    die_results[i] = random.randint(1, pdice[i])
            ps_options = []
            if len(pdice) == 2:
                roll_report = "Rolled " + str(die_results[0]) + " and " + str(die_results[1]) + "."
                # The player can choose between any single result or the sum of any pair of results.
                # Since there are only two dice, this is a straightforward list: the two results
                #  and their sum.
                ps_options = [min(die_results), max(die_results), sum(die_results)]
                if ps_options[0] == ps_options[1]:
                    ps_options.remove(ps_options[0])
            else:
                roll_report = "Rolled " + str(die_results[0]) + ", " + str(die_results[1]) + \
                              ", and " + str(die_results[2]) + "."
                # The player can choose between any single result or the sum of any pair of results.
                # Since there are exactly three dice, each sum of two dice can be represented as
                #  the sum of all three minus the value of the third.
                ps_options = [x for x in die_results] + [sum(die_results) - y for y in die_results]
                ps_options.sort()
                for i in range(len(ps_options)-1):
                    for j in range(i+1, len(ps_options)):
                        if i < j < len(ps_options):
                            if ps_options[i] == ps_options[j]:
                                del ps_options[j]
            print(roll_report)
            # To convert to 0-index, subtract 1 from each option:
            ps_indices = [x-1 for x in ps_options]
            # Let the user choose from the options provided by their roll...
            entry_choice = ' '
            entry_options = string.ascii_uppercase[0:len(ps_options) + rerolls]
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user
                answer = IntVar()
                options = [ps_collection[i][0] + " (" + str(ps_options[i]) + ")" \
                           for i in ps_indices]
                if rerolls > 0:
                    options += ["REROLL"]
                question = ExpandWindow(self.myWindow,
                                        roll_report + "\nChoose one:",
                                        options,
                                        [PowerSourceDetails(i, width=0) for i in ps_indices],
                                        var=answer,
                                        title="Power Source Selection",
                                        rwidth=ps_width)
                entry_index = answer.get()
            else:
                for i in range(len(entry_options)-rerolls):
                    print("    " + entry_options[i] + ": " + ps_collection[ps_indices[i]][0] + \
                          " (" + str(ps_options[i]) + ")")
                if rerolls > 0:
                    print("    " + entry_options[len(entry_options)-1] + ": REROLL")
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see an option expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see an option " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options[:-1] and \
                       entry_choice not in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        DisplayPowerSource(ps_indices[entry_index], "    ", width=100-len("    "))
                entry_index = entry_options.find(entry_choice)
            # Now we have a commitment to a valid choice from the list.
            if entry_index == len(ps_options):
                # User selected to reroll.
                prev_results = [0 for x in die_results]
                entry_options = "YN"
                entry_choice = ' '
                decision = choose_letter(entry_options,
                                         ' ',
                                         prompt="Do you want to keep any of the previous " + \
                                         "results? (y/n)",
                                         repeat_message="Please enter Y or N.",
                                         inputs=inputs)
                entry_choice = decision[0]
                inputs = decision[1]
                if entry_choice == "Y":
                    for i in range(len(die_results)):
                        entry_choice = ' '
                        decision = choose_letter(entry_options,
                                                 ' ',
                                                 prompt="Do you want to keep " + \
                                                        str(die_results[i]) + " on your d" + \
                                                        str(pdice[i]) + "? (y/n)",
                                                 repeat_message="Please enter Y or N.",
                                                 inputs=inputs)
                        entry_choice = decision[0]
                        inputs = decision[1]
                        if entry_choice == "Y":
                            prev_results[i] = die_results[i]
                rerolls = 0
            else:
                # User selected a Power Source.
                print(ps_collection[ps_indices[entry_index]][0] + " Power Source selected.")
                return ps_indices[entry_index]
    def ConstructedPowerSource(self, inputs=[]):
        # Walks the user through selecting a Power Source from the full list of options.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns the index of the Power Source selected.
        if len(inputs) > 0:
            print("### ConstructedPowerSource: inputs=" + str(inputs))
        entry_options = string.ascii_uppercase[0:len(ps_collection)]
        entry_choice = ' '
        if self.UseGUI(inputs):
            # Create an ExpandWindow to prompt the user.
            answer = IntVar()
            question = ExpandWindow(self.myWindow,
                                    "Choose a Power Source from the list:",
                                    [x[0] for x in ps_collection],
                                    [PowerSourceDetails(i, width=0) \
                                     for i in range(len(ps_collection))],
                                    var=answer,
                                    title="Power Source Selection",
                                    rwidth=ps_width)
            entry_index = answer.get()
        else:
            print("Choose a Power Source from the list:")
            for i in range(len(bg_collection)):
                print("    " + entry_options[i] + ": " + ps_collection[i][0] + " (" + str(i+1) + ")")
            while entry_choice not in entry_options:
                if len(inputs) > 0:
                    print("Enter a lowercase letter to see a Power Source expanded, " + \
                          "or an uppercase letter to select it.")
                    print("> " + inputs[0])
                    entry_choice = inputs.pop(0)[0]
                else:
                    entry_choice = input("Enter a lowercase letter to see a Power Source expanded, " + \
                                         "or an uppercase letter to select it.\n")[0]
                if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                    entry_index = entry_options.find(entry_choice.upper())
                    DisplayPowerSource(entry_index, "    ", width=100-len("    "))
            entry_index = entry_options.find(entry_choice)
        print(ps_collection[entry_index][0] + " Power Source selected.")
        return entry_index
    def AddMode(self,
                zone,
                index,
                stepnum=0,
                inputs=[]):
        # Walks the user through adding a Mode based on the mode_template specified by zone and index.
        # stepnum: the number of the step of hero creation (1-7) at which this Mode is being added
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        if len(inputs) > 0:
            print("### AddMode: inputs=" + str(inputs))
        this_step = max([0, stepnum])
        mode_template = mc_zones[zone][index]
        t_name = mode_template[0]
        t_zone = mode_template[1]
        t_die_sizes = mode_template[2]
        t_die_mods = mode_template[3]
        t_prohibited_actions = mode_template[4]
        t_ability_template = mode_template[5]
        print("OK! Let's fill in your new Mode:")
        DisplayModeTemplate(zone, index, prefix="    ", width=96)
        # For each die size in t_die_sizes, prompt the user to choose a Power to add at that size.
        mode_power_dice = []
        print(self.hero_name + " has the following Power dice:")
        for d in self.power_dice:
            print("    " + str(d))
        for die_size in t_die_sizes:
            remaining_dice = [d for d in self.power_dice if d.name not in \
                              [e.name for e in mode_power_dice]]
            entry_die = ""
            if len(remaining_dice) == 1:
                entry_die = remaining_dice[0]
            else:
                entry_options = string.ascii_uppercase[0:len(remaining_dice)]
                entry_choice = ' '
                decision = self.ChooseIndex([str(x) for x in remaining_dice],
                                            prompt="Choose a Power to add to this mode at d" + \
                                            str(die_size) + ":",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                entry_index = entry_options.find(entry_choice)
                entry_die = remaining_dice[entry_index]
            mp_die = PQDie(entry_die.ispower,
                           entry_die.category,
                           entry_die.index,
                           die_size,
                           flavorname=entry_die.flavorname,
                           stepnum=entry_die.step)
            mp_die.prev_version = entry_die.copy()
            mp_die.steps_modified.append(this_step)
            print(str(mp_die) + " added to " + t_name + ".")
            mode_power_dice.append(mp_die)
        # For each modifier in t_die_mods, prompt the user to choose a Power to add with that
        #  modifier.
        for modifier in t_die_mods:
            mod_text = str(modifier)
            if modifier >=0:
                mod_text = "+" + mod_text
            if abs(modifier) == 1:
                mod_text += " die size"
            else:
                mod_text += " die sizes"
            remaining_dice = [d for d in self.power_dice if d.name not in \
                              [e.name for e in mode_power_dice]]
            entry_die = ""
            if len(remaining_dice) == 1:
                entry_die = remaining_dice[0]
            else:
                entry_options = string.ascii_uppercase[0:len(remaining_dice)]
                entry_choice = ' '
                decision = self.ChooseIndex([str(x) for x in remaining_dice],
                                            prompt="Choose a Power to add to this mode at " + \
                                            mod_text + ":",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                entry_die = remaining_dice[entry_index]
            mp_die_size = entry_die.diesize + 2 * modifier
            if mp_die_size < min(legal_dice):
                mp_die_size = min(legal_dice)
            elif mp_die_size > max(legal_dice):
                mp_die_size = max(legal_dice)
            mp_die = PQDie(entry_die.ispower,
                           entry_die.category,
                           entry_die.index,
                           mp_die_size,
                           flavorname=entry_die.flavorname,
                           stepnum=entry_die.step)
            mp_die.prev_version = entry_die.copy()
            mp_die.steps_modified.append(this_step)
            print(str(mp_die) + " added to " + t_name + ".")
            mode_power_dice.append(mp_die)
        # Have the user fill in the mode's Ability
        m_ability = ""
        pass_inputs = []
        if len(inputs) > 0:
            if str(inputs[0]) != inputs[0]:
                pass_inputs = inputs.pop(0)
        m_ability = self.ChooseAbility([t_ability_template],
                                       zone,
                                       add=0,
                                       alt_powers=mode_power_dice,
                                       stepnum=this_step,
                                       inputs=pass_inputs)
        # Let the user choose whether to customize the name.
        mode_name = t_name
        entry_options = "YN"
        decision = choose_letter(entry_options,
                                 ' ',
                                 prompt="Do you want to give " + t_name + " a new name? (y/n)",
                                 repeat_message="Please enter Y or N.",
                                 inputs=inputs)
        entry_choice = decision[0]
        inputs = decision[1]
        if entry_choice == 'Y':
            decision = self.EnterText("Enter the new name for this Mode:",
                                      inputs=inputs)
            mode_name = decision[0]
            inputs = decision[1]
##            if len(inputs) > 0:
##                print("Enter the new name for this Mode:")
##                print("> " + inputs[0])
##                mode_name = inputs.pop(0)
##            else:
##                mode_name = input("Enter the new name for this Mode:\n")
        new_mode = [mode_name,
                    zone,
                    mode_power_dice,
                    self.quality_dice,
                    self.status_dice,
                    m_ability,
                    t_prohibited_actions,
                    this_step]
        self.other_modes.append(new_mode)
        print("All set! " + mode_name + " added to " + self.hero_name + "'s Mode Sheet in " + \
              status_zones[zone] + ".")
    def DisplayMode(self,
                    index,
                    codename=True,
                    prefix="",
                    width=100,
                    inputs=[]):
        # Displays the attributes of the hero's Mode specified by index.
        # codename: should the hero's codename be displayed with this form?
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        notePrefix = "### Hero.DisplayMode: "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        indent = "    "
        if index not in range(len(self.other_modes)):
            printlong(notePrefix + "Error! " + str(index) + " is not a valid index for any of " + \
                      self.hero_name + "'s " + str(len(self.other_modes)) + " alternate Modes.",
                      prefix=prefix,
                      width=width)
            return
        else:
            mode = self.other_modes[index]
            if codename:
                print(prefix + self.hero_name)
                prefix += indent
            print(prefix + mode[0] + " (" + status_zones[mode[1]] + " Mode)")
            if mode[2] == self.power_dice:
                print(prefix + indent + "[Standard Powers]")
            else:
                print(prefix + indent + "Powers:")
                for d in mode[2]:
                    print(prefix + indent + indent + str(d))
            if mode[3] == self.quality_dice:
                print(prefix + indent + "[Standard Qualities]")
            else:
                print(prefix + indent + "Qualities:")
                for d in mode[3]:
                    print(prefix + indent + indent + str(d))
            if mode[4] in [[0,0,0], self.status_dice]:
                print(prefix + indent + "[Standard Status]")
            else:
                for i in range(3):
                    print(prefix + indent + status_zones[i] + ": " + str(mode[4][i]))
            if len(mode[6]) > 0:
                prohibited_text = mode[6][0]
                for i in range(1, len(mode[6])-1):
                    prohibited_text += ", " + mode[6][i]
                if len(mode[6]) > 2:
                    prohibited_text += ","
                if len(mode[6]) > 1:
                    prohibited_text += " or " + mode[6][len(mode[6])-1]
                print(prefix + indent + "You cannot " + prohibited_text + " in this Mode.")
            print(prefix + indent + "You gain access to this Ability:")
            mode[5].display(prefix=prefix+indent+indent,
                            width=width-len(prefix+indent+indent))
    def ModeDetails(self,
                    index,
                    codename=True,
                    prefix="",
                    width=100,
                    inputs=[]):
        # Returns a string containing the attributes of the hero's Mode specified by index.
        # codename: should the hero's codename be displayed with this form?
        # inputs: a list of text inputs to use automatically instead of prompting the user
        notePrefix = "### Hero.ModeDetails: "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        indent = "    "
        modeString = ""
        if index not in range(len(self.other_modes)):
            printlong(notePrefix + "Error! " + str(index) + " is not a valid index for any of " + \
                      self.hero_name + "'s " + str(len(self.other_modes)) + " alternate Modes.",
                      prefix=prefix,
                      width=width)
            return modeString
        else:
            mode = self.other_modes[index]
            if codename:
                modeString += prefix + self.hero_name + "\n"
                prefix += indent
            modeString += prefix + mode[0] + " (" + status_zones[mode[1]] + " Mode)"
            if mode[2] == self.power_dice:
                modeString += "\n" + prefix + indent + "[Standard Powers]"
            else:
                modeString += "\n" + prefix + indent + "Powers:"
                for d in mode[2]:
                    modeString += "\n" + prefix + indent + indent + str(d)
            if mode[3] == self.quality_dice:
                modeString += "\n" + prefix + indent + "[Standard Qualities]"
            else:
                modeString += "\n" + prefix + indent + "Qualities:"
                for d in mode[3]:
                    modeString += "\n" + prefix + indent + indent + str(d)
            if mode[4] in [[0,0,0], self.status_dice]:
                modeString += "\n" + prefix + indent + "[Standard Status]"
            else:
                for i in range(3):
                    modeString += "\n" + prefix + indent + status_zones[i] + ": " + str(mode[4][i])
            if len(mode[6]) > 0:
                prohibited_text = mode[6][0]
                for i in range(1, len(mode[6])-1):
                    prohibited_text += ", " + mode[6][i]
                if len(mode[6]) > 2:
                    prohibited_text += ","
                if len(mode[6]) > 1:
                    prohibited_text += " or " + mode[6][len(mode[6])-1]
                modeString += "\n" + prefix + indent + "You cannot " + prohibited_text + \
                              " in this Mode."
            modeString += "\n" + prefix + indent + "You gain access to this Ability:"
            modeString += "\n" + mode[5].details(prefix=prefix+indent+indent,
                                                 width=width-len(prefix+indent+indent))
        return modeString
    def DisplayForm(self,
                    index,
                    prefix="",
                    width=100,
                    codename=True,
                    inputs=[]):
        # Displays the attributes of the hero's Form specified by index.
        # codename: should the hero's codename be displayed with this form?
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        notePrefix = "### Hero.DisplayForm: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        if index not in range(len(self.other_forms)):
            print(notePrefix + "Error! " + str(index) + " is not a valid index for any of " + \
                  self.hero_name + "'s " + str(len(self.other_forms)) + " alternate Forms.")
            return
        else:
            form = self.other_forms[index]
            if codename:
                print(prefix + self.hero_name)
                prefix += indent
            if self.archetype_modifier == 1:
                dv_check = [a for a in self.abilities if a.name == "Divided Psyche"]
                dv_ps = None
                if len(dv_check) > 0:
                    dv_ps = dv_check[0]
                if form[6] in [0,1]:
                    print(prefix + form[0] + " (" + status_zones[form[1]] + " Form, " + \
                          self.dv_tags[form[6]] + ")")
                else:
                    print(prefix + form[0] + " (" + status_zones[form[1]] + " Form, [undecided])")
            else:
                print(prefix + form[0] + " (" + status_zones[form[1]] + " Form)")
            if form[2] == self.power_dice:
                print(prefix + indent + "[Standard Powers]")
            elif form[2] == [] and dv_ps:
                print(prefix + indent + "[No Powers (see " + dv_ps.flavorname + ")]")
            else:
                print(prefix + indent + "Powers:")
                for d in form[2]:
                    print(prefix + indent + indent + str(d))
            if form[3] == self.quality_dice:
                print(prefix + indent + "[Standard Qualities]")
            elif form[3] == [] and dv_ps:
                print(prefix + indent + "[No Qualities (see " + dv_ps.flavorname + ")]")
            else:
                print(prefix + indent + "Qualities:")
                for d in form[3]:
                    print(prefix + indent + indent + str(d))
            if form[4] in [[0,0,0], self.status_dice]:
                print(prefix + indent + "[Standard Status]")
            else:
                for i in range(3):
                    print(prefix + indent + status_zones[i] + ": " + str(form[4][i]))
            if len(form[5]) > 1:
                print(prefix + indent + "You gain access to the following Abilities:")
            elif len(form[5]) == 1:
                print(prefix + indent + "You gain access to the following Ability:")
            for i in range(len(form[5])):
                form[5][i].display(prefix=prefix+indent+indent,
                                   width=width-len(prefix+indent+indent))
    def FormDetails(self,
                    index,
                    prefix="",
                    width=100,
                    codename=True,
                    inputs=[]):
        # Returns a string containing the attributes of the hero's Form specified by index.
        # codename: should the hero's codename be displayed with this form?
        # inputs: a list of text inputs to use automatically instead of prompting the user
        notePrefix = "### Hero.FormDetails: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        formString = ""
        if index not in range(len(self.other_forms)):
            print(notePrefix + "Error! " + str(index) + " is not a valid index for any of " + \
                  self.hero_name + "'s " + str(len(self.other_forms)) + " alternate Forms.")
            return
        else:
            form = self.other_forms[index]
            if codename:
                formString = prefix + self.hero_name + "\n"
                prefix += indent
            if self.archetype_modifier == 1:
                dv_check = [a for a in self.abilities if a.name == "Divided Psyche"]
                dv_ps = None
                if len(dv_check) > 0:
                    dv_ps = dv_check[0]
                if form[6] in [0,1]:
                    formString += prefix + form[0] + " (" + status_zones[form[1]] + " Form, " + \
                                  self.dv_tags[form[6]] + ")"
                else:
                    formString += prefix + form[0] + " (" + status_zones[form[1]] + \
                                  " Form, [undecided])"
            else:
                formString += prefix + form[0] + " (" + status_zones[form[1]] + " Form)"
            if form[2] == self.power_dice:
                formString += "\n" + prefix + indent + "[Standard Powers]"
            elif form[2] == [] and dv_ps:
                formString += "\n" + prefix + indent + "[No Powers (see " + dv_ps.flavorname + ")]"
            else:
                formString += "\n" + prefix + indent + "Powers:"
                for d in form[2]:
                    formString += "\n" + prefix + indent + indent + str(d)
            if form[3] == self.quality_dice:
                formString += "\n" + prefix + indent + "[Standard Qualities]"
            elif form[3] == [] and dv_ps:
                formString += "\n" + prefix + indent + "[No Qualities (see " + dv_ps.flavorname + \
                              ")]"
            else:
                formString += "\n" + prefix + indent + "Qualities:"
                for d in form[3]:
                    formString += "\n" + prefix + indent + indent + str(d)
            if form[4] in [[0,0,0], self.status_dice]:
                formString += "\n" + prefix + indent + "[Standard Status]"
            else:
                for i in range(3):
                    formString += "\n" + prefix + indent + status_zones[i] + ": " + str(form[4][i])
            if len(form[5]) > 1:
                formString += "\n" + prefix + indent + \
                              "You gain access to the following Abilities:"
            elif len(form[5]) == 1:
                formString += "\n" + prefix + indent + "You gain access to the following Ability:"
            for i in range(len(form[5])):
                formString += "\n" + form[5][i].details(prefix=prefix+indent+indent,
                                                        width=width-len(prefix+indent+indent))
        return formString
    def ChooseForm(self, zone, stepnum=0, inputs=[]):
        # Walks the user through selecting and adding a Form in the specified status zone.
        # stepnum: the number of the step of hero creation (1-7) at which this Mode is being added
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        if len(inputs) > 0:
            print("### ChooseForm: inputs=" + str(inputs))
        this_step = max([0, stepnum])
        fc_powers = arc_collection[15][5]
        form_options = form_abilities_green
        if zone > 0:
            form_options = form_abilities_green + form_abilities_yellow
        if len(self.other_forms) > 0:
            other_abilities = []
            for i in range(len(self.other_forms)):
                other_abilities.extend(self.other_forms[i][5])
            form_options = [fa for fa in form_options if fa.name not in \
                            [oa.name for oa in other_abilities]]
        entry_options = string.ascii_uppercase[0:len(form_options)]
        entry_choice = ' '
        print("Choose a Form to add in " + status_zones[zone] + ":")
        for i in range(len(form_options)):
            print("    " + entry_options[i] + ": " + form_options[i].name)
        while entry_choice not in entry_options:
            if len(inputs) > 0:
                print("Enter a lowercase letter to see a Form expanded, " + \
                      "or an uppercase letter to select it.")
                print("> " + inputs[0])
                entry_choice = inputs.pop(0)
            else:
                entry_choice = input("Enter a lowercase letter to see a Form expanded, " + \
                                     "or an uppercase letter to select it.\n")[0]
            if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                entry_index = entry_options.find(entry_choice.upper())
                form_options[entry_index].display()
        entry_index = entry_options.find(entry_choice)
        form_ability_template = form_options[entry_index]
        form_name = form_ability_template.name
        print("OK! Let's create the Power list for " + form_ability_template.name + "...")
        form_power_dice = []
        form_ability_template.display(prefix="    ")
        print(self.hero_name + " has the following Powers:")
        for d in self.power_dice:
            print("    " + str(d))
            form_power_dice.append(PQDie(d.ispower,
                                         d.category,
                                         d.index,
                                         d.diesize,
                                         d.flavorname,
                                         stepnum=d.step))
        step_options = "ABCD"
        step_text = ["Swap 2 Power dice",
                     "Replace a Power with a Form-Changer Power",
                     "Show current Powers for this Form",
                     "No further changes"]
        step_choice = ' '
        # The user can swap two power dice, or replace a power die with another Power from the
        #  Form-Changer secondary list, any number of times.
        while step_choice != "D":
            print("Do you want to modify " + self.hero_name + "'s Powers in " + \
                  form_ability_template.name + "?")
            for i in range(len(step_options)):
                print("    " + step_options[i] + ": " + step_text[i])
            decision = choose_letter(step_options, ' ', inputs=inputs)
            step_choice = decision[0]
            inputs = decision[1]
            if step_choice == "A":
                # Swap 2 Power dice
                swap_indices = [99, 99]
                if self.UseGUI(inputs):
                    # Create a SwapWindow to prompt the user
                    dispWidth = 100
                    answer0 = IntVar()
                    answer1 = IntVar()
                    prompt = "Choose 2 Power dice to swap:"
                    title = "Create Form: " + form_ability_template.name
                    question = SwapWindow(self.myWindow,
                                          prompt,
                                          [str(x) for x in form_power_dice],
                                          answer0,
                                          answer1,
                                          title=title,
                                          width=dispWidth)
                    swap_indices = [answer0.get(), answer1.get()]
                else:
                    entry_options = string.ascii_uppercase[0:len(form_power_dice)]
                    entry_choice = ' '
                    decision = self.ChooseIndex([str(x) for x in form_power_dice],
                                                "Choose the first Power die to swap:",
                                                inputs=inputs)
                    swap_indices[0] = decision[0]
                    inputs = decision[1]
                    entry_options = string.ascii_uppercase[0:len(form_power_dice)]
                    entry_choice = ' '
                    for i in range(len(form_power_dice)):
                        print("    " + entry_options[i] + ": " + str(form_power_dice[i]))
                    decision = self.ChooseIndex([str(x) for x in form_power_dice],
                                                "OK! Choose a die to swap with " + \
                                                str(form_power_dice[swap_indices[0]]) + ":",
                                                inputs=inputs)
                    swap_indices[1] = decision[0]
                    inputs = decision[1]
                swap_dice = [form_power_dice[i] for i in swap_indices]
                if swap_dice[0].diesize != swap_dice[1].diesize:
                    d_temp = swap_dice[0].diesize
                    swap_dice[0].diesize = swap_dice[1].diesize
                    swap_dice[1].diesize = d_temp
                    for i in range(2):
                        swap_dice[i].SetPrevious(this_step)
                    print("OK! " + swap_dice[0].flavorname + " is now d" + \
                          str(swap_dice[0].diesize) + " and " + swap_dice[1].flavorname + \
                          " is now d" + str(swap_dice[1].diesize) + ".")
                elif swap_indices[0] == swap_indices[1]:
                    print("You can't swap " + str(form_power_dice[swap_indices[0]]) + \
                          " with itself.")
                else:
                    print(swap_dice[0].name + " and " + swap_dice[1].name + \
                          " already have the same die size (d" + swap_dice[0].diesize + ").")
            elif step_choice == "B":
                # Replace a Power with a Form-Changer Power
                decision = self.ChooseIndex([str(x) for x in form_power_dice],
                                            prompt="Choose a Power die to switch out...",
                                            inputs=inputs)
                die_index = decision[0]
                inputs = decision[1]
                changed_die = form_power_dice[die_index]
                replace_options = [triplet for triplet in fc_powers if triplet not in \
                                   [d.triplet() for d in form_power_dice]]
                decision = self.ChooseIndex([MixedPQ(x) for x in replace_options],
                                            prompt="Choose a Power to replace " + \
                                            changed_die.flavorname + ":",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                # Change changed_die's attributes to those of the newly selected Power
                prev_str = str(changed_die)
                replace_power = replace_options[entry_index]
                changed_die.SetPrevious(this_step)
                changed_die.ispower = replace_power[0]
                changed_die.category = replace_power[1]
                changed_die.index = replace_power[2]
                changed_die.name = MixedPQ(replace_power)
                changed_die.flavorname = changed_die.name
                print("OK! " + prev_str + " is now " + str(changed_die))
            elif step_choice == "C":
                # Display the current Power list for this Form
                print(self.hero_name + "'s current Powers in " + form_ability_template.name + \
                      " are...")
                for i in range(len(form_power_dice)):
                    print("    " + str(form_power_dice[i]))
        if zone == 1:
            # For a Yellow Form, the user can choose up to 2 dice to increase by 1 die size each
            power_indices = [x for x in range(len(form_power_dice))\
                             if form_power_dice[x].diesize < max(legal_dice)]
            upgraded = 0
            entry_options = string.ascii_uppercase[0:len(form_power_dice)+1]
            entry_choice = ' '
            while upgraded < 2 and entry_choice != entry_options[len(power_indices)]:
                decision = self.ChooseIndex([str(form_power_dice[x]) for x in power_indices],
                                            prompt="Choose a Power die to increase by one size" + \
                                            " in this Form:",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                if entry_index in range(len(power_indices)):
                    # User selected a Power to upgrade
                    die_index = power_indices.pop(entry_index)
                    upgrade_die = form_power_dice[die_index]
                    upgrade_die.SetPrevious(this_step)
                    upgrade_die.diesize = upgrade_die.diesize + 2
                    print("OK! " + upgrade_die.flavorname + " is now a d" + \
                          str(upgrade_die.diesize) + " in " + form_name + ".")
                    upgraded += 1
                    entry_choice = ' '
        # Have the user fill in the form's Ability
        f_ability = ""
        pass_inputs = []
        if len(inputs) > 0:
            if str(inputs[0]) != inputs[0]:
                pass_inputs=inputs.pop(0)
        f_ability = self.ChooseAbility([form_ability_template],
                                       zone,
                                       add=0,
                                       alt_powers=form_power_dice,
                                       stepnum=this_step,
                                       inputs=pass_inputs)
        # Let the user choose whether to customize the name.
        form_name = form_ability_template.name
        entry_options = "YN"
        decision = choose_letter(entry_options,
                                 ' ',
                                 prompt="Do you want to give " + form_name + " a new name? (y/n)",
                                 repeat_message="Please enter Y or N",
                                 inputs=inputs)
        entry_choice = decision[0]
        inputs = decision[1]
        if entry_choice == 'Y':
            decision = self.EnterText("Enter the new name for this Form:",
                                      inputs=inputs)
            form_name = decision[0]
            inputs = decision[1]
##            form_name = ""
##            if len(inputs) > 0:
##                print("Enter the new name for this Form:")
##                print("> " + inputs[0])
##                form_name = inputs.pop(0)
##            else:
##                form_name = input("Enter the new name for this Form:\n")
        new_form = [form_name,
                    zone,
                    form_power_dice,
                    self.quality_dice,
                    self.status_dice,
                    [f_ability],
                    -1,
                    this_step]
        if self.archetype_modifier == 1:
            # This is a Divided hero, and each of their Forms should be tagged as Civilian or
            #  Heroic.
            entry_options = string.ascii_uppercase[0:3]
            print(self.hero_name + " is a Divided hero. Is " + form_name + " a " + \
                  self.dv_tags[0] + " or " + self.dv_tags[1] + " form for " + \
                  pronouns[self.pronoun_set][1] + "?")
            decision = self.ChooseIndex([self.dv_tags[0], self.dv_tags[1], "I'll decide later"],
                                        prompt=self.hero_name + " is a Divided hero. Is " + \
                                        form_name + " a " + self.dv_tags[0] + " or " + \
                                        self.dv_tags[1] + " form for " + \
					pronouns[self.pronoun_set][1] + "?",
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            if entry_index < 2:
                new_form[6] = entry_index
        self.other_forms.append(new_form)
        print("All set! " + form_name + " added to " + self.hero_name + "'s Form Sheet in " + \
              status_zones[zone] + ".")
    def AddArchetype(self, arc_index, mod_index=0, a_dice=[], inputs=[]):
        # Walks the user through adding the Powers/Qualities, Abilities, and Principle they gain
        #  from the specified Archetype or Archetype combo.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        if len(inputs) > 0:
            print("### AddArchetype: inputs=" + str(inputs))
        if a_dice == []:
            a_dice = self.arc_dice
        # This is Step 3 of hero creation!
        this_step = 3
        your_arc = arc_simple[arc_index]
        # your_arc is a list of 20 objects:
        # 0: title
        # 1: description
        # 2: list of primary powers/qualities (if applicable)
        # 3: index of what to do if you have the primary power/quality already (if applicable)
        primary_pqs = your_arc[2]
        primary_matches = [d for d in self.power_dice + self.quality_dice \
                           if d.triplet() in primary_pqs]
        primary_category = DieCategory(primary_pqs)
        primary_alt = your_arc[3]
        # 4: number of secondary powers/qualities (if applicable) (2 indicates "1 or more")
        # 5: list of secondary powers/qualities (if applicable)
        secondary_count = your_arc[4]
        secondary_pqs = your_arc[5]
        # 6: list of tertiary powers/qualities
        tertiary_pqs = your_arc[6]
        # 7: list of mandatory abilities (if applicable)
        mandatory_abilities = [a for a in your_arc[7]]
        # 8: number of green abilities to choose
        # 9: number of Yellow Abilities to choose (if applicable)
        green_count = your_arc[8]
        yellow_count = your_arc[9]
        # 10: list of green ability options (if applicable)
        # 11: list of Yellow Ability options (if applicable)
        # 12: list of green-or-Yellow Ability options (if applicable)
        green_abilities = [a for a in your_arc[10]]
        yellow_abilities = [a for a in your_arc[11]]
        mixed_abilities = [a for a in your_arc[12]]
        # 13: whether a green ability is required to use the primary power/quality
        # 14: what category of die is required for the other green ability (if applicable)
        requires_primary = your_arc[13]
        category_required = your_arc[14]
        # 15: requirement for unique Power/Quality dice used in Green Abilities
        # 16: requirement for unique Power/Quality dice used in Yellow Abilities
        green_unique = your_arc[15]
        yellow_unique = your_arc[16]
        # 17: whether all Green Abilities are limited to powers/qualities listed in the Archetype
        green_limited = your_arc[17]
        all_arc_pqs = primary_pqs + secondary_pqs + tertiary_pqs
        # 18: index of Principle category
        r_category = your_arc[18]
        # 19: index of bonus step (if applicable)
        arc_bonus = your_arc[19]
        # Some bonus steps have to be implemented sooner than others
        arc_grants_dice = arc_bonus in [2]
        if self.archetype in range(len(arc_collection)):
            # This hero already has an Archetype
            arc_text = arc_collection[self.archetype][0]
            if self.archetype_modifier in range(1,len(arc_modifiers)):
                arc_text = arc_modifiers[self.archetype_modifier][0] + ":" + arc_text
            print("Error! " + self.hero_name + " already has the " + arc_text + " Archetype.")
            input()
        else:
            # This hero has no Archetype, so we can add this one.
            if mod_index > 0:
                print("OK! You've chosen the " + arc_modifiers[mod_index][0] + ":" + \
                      your_arc[0] + " Archetype.")
            else:
                print("OK! You've chosen the " + your_arc[0] + " Archetype.")
            self.archetype = arc_index
            self.archetype_modifier = mod_index
            print("You get " + str(a_dice) + " to assign to Powers and/or Qualities.")
            entry_choice = ' '
            # Add Powers and Qualities from your base Archetype, regardless of modifiers
            # Start with the primary, if there is one:
            if len(primary_matches) > 0 and primary_alt > 0:
                # This hero already has at least one of the primary Powers/Qualities for this
                #  Archetype.
                ext_report = "This archetype requires one of the following " + \
                             categories_plural[primary_category] + "..."
                primary_names = MixedPQ(primary_pqs[0])
                for triplet in primary_pqs[1:]:
                    primary_names += ", " + MixedPQ(triplet)
                ext_report += "\n" + split_text(primary_names, width=100, prefix="    ")
                ext_report += "\n\nYou already have..."
                ext_names = str(primary_matches[0])
                for d in primary_matches[1:]:
                    ext_names += ", " + str(d)
                ext_report += "\n" + split_text(ext_names, width=100, prefix="    ")
                # primary_alt > 0, so the user gets to make a choice
                if primary_alt == 1 and len(primary_matches) < len(primary_pqs):
                    # Skip or choose another die to gain
                    entry_options = "YN"
                    decision = choose_letter(entry_options,
                                             ' ',
                                             prompt=ext_report + "\n\nDo you want to put one " + \
                                             "of " + str(a_dice) + " into another option " + \
                                             "above? (y/n)",
                                             repeat_message="Please enter Y or N.",
                                             inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                    if entry_choice == 'Y':
                        # Gain one of the primary_pqs that this hero doesn't already have.
                        primary_options = [triplet for triplet in primary_pqs if triplet not in \
                                           [d.triplet() for d in primary_matches]]
                        pass_inputs = []
                        if len(inputs) > 0:
                            if str(inputs[0]) != inputs[0]:
                                pass_inputs = inputs.pop(0)
                        remainders = self.ChoosePQ(primary_options,
                                                   a_dice,
                                                   stepnum=this_step,
                                                   inputs=pass_inputs)
                        a_dice = remainders[1]
                elif primary_alt == 2:
                    # Skip or swap the die with one of the new ones
                    entry_options = "YN"
                    decision = choose_letter(entry_options,
                                             ' ',
                                             prompt=ext_report + "\n\nDo you want to swap one " + \
                                             "of the dice you have above for one of " + \
                                             str(a_dice) + "? (y/n)",
                                             repeat_message="Please enter Y or N.",
                                             inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                    if entry_choice == 'Y':
                        swap_index = 0
                        if len(primary_matches) > 1:
                            # Choose one of primary_matches to swap out.
                            entry_options = string.ascii_uppercase[0:len(primary_matches)]
                            decision = self.ChooseIndex([str(x) for x in primary_matches],
                                                        prompt="Choose a " + \
							       categories_singular[DieCategory([d.triplet() for d in primary_matches])] + \
							       " to change die size:",
                                                        inputs=inputs)
                            swap_index = decision[0]
                            inputs = decision[1]
                        # Swap the die size of primary_matches[swap_index] with the die size of
                        #  one of a_dice.
                        decision = self.ChooseIndex([str(x) for x in a_dice],
                                                    prompt="Choose a new die size for " + \
                                                    str(primary_matches[swap_index]) + ":",
                                                    inputs=inputs)
                        a_die_index = decision[0]
                        inputs = decision[1]
                        primary_matches[swap_index].SetPrevious(this_step)
                        d_temp = a_dice[a_die_index]
                        a_dice[a_die_index] = primary_matches[swap_index].diesize
                        primary_matches[swap_index].diesize = d_temp
                        print("OK! " + self.hero_name + " now has " + \
                              str(primary_matches[swap_index]) + ", and " + str(a_dice) + \
                              " remaining for Powers/Qualities.")
            elif len(primary_pqs)==1:
                # This Archetype has exactly 1 primary power/quality and this hero needs to gain it.
                # print("primary_pqs[0]: " + str(primary_pqs[0]))
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                a_dice = self.ChoosePQDieSize(primary_pqs[0][0],
                                              primary_pqs[0][1:],
                                              a_dice,
                                              stepnum=this_step,
                                              inputs=pass_inputs)
            elif len(primary_pqs) > 1:
                # This Archetype has more than 1 primary power/quality and this hero needs to gain
                #  one of them.
                primary_options = [triplet for triplet in primary_pqs if triplet not in \
                                   [d.triplet() for d in primary_matches]]
                remainders = []
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                remainders = self.ChoosePQ(primary_options,
                                           a_dice,
                                           stepnum=this_step,
                                           inputs=pass_inputs)
                a_dice = remainders[1]
            # Then move on to secondary Powers/Qualities, if there are any:
            if len(secondary_pqs) > 0:
                # Add 1 of the secondary Powers/Qualities:
                remainders = []
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                remainders = self.ChoosePQ(secondary_pqs,
                                           a_dice,
                                           stepnum=this_step,
                                           inputs=pass_inputs)
                a_dice = remainders[1]
                entry_choice = ' '
                # If secondary_count is 2 and there are dice remaining, the user can add as many
                #  more secondary Powers/Qualities as they like
                while secondary_count > 1 and len(a_dice) > 0 and entry_choice != 'N':
                    entry_options = "YN"
                    prompt = "Do you want to add another " + \
                             categories_singular[DieCategory(secondary_pqs)] + \
                             " from this list? (y/n)"
                    names = MixedPQ(secondary_pqs[0])
                    for triplet in secondary_pqs[1:]:
                        names += ", " + MixedPQ(triplet)
                    names = split_text(names, 100)
                    decision = choose_letter(entry_options,
                                             ' ',
                                             prompt=prompt + "\n\n" + names,
                                             repeat_message="Please enter Y or N.",
                                             inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                    if entry_choice == "Y":
                        pass_inputs = []
                        if len(inputs) > 0:
                            if str(inputs[0]) != inputs[0]:
                                pass_inputs = inputs.pop(0)
                        remainders = self.ChoosePQ(secondary_pqs,
                                                   a_dice,
                                                   stepnum=this_step,
                                                   inputs=pass_inputs)
                        a_dice = remainders[1]
            # Finally, if there are dice remaining, assign them to the tertiary Powers/Qualities:
            if len(a_dice) > 0:
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AssignAllPQ(tertiary_pqs, a_dice, stepnum=this_step, inputs=pass_inputs)
            # If the hero's Power Source gave them a bonus Quality from their Archetype, this is
            #  the time to choose it.
            if self.arc_bonus_quality in legal_dice:
                arc_q_triplets = [triplet for triplet in \
                                  primary_pqs + secondary_pqs + tertiary_pqs if triplet[0]==0]
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(arc_q_triplets,
                              [self.arc_bonus_quality],
                              stepnum=step_names.index("Power Source"),
                              inputs=pass_inputs)
            # If this Archetype grants a bonus Power or Quality die, this is the time to choose it.
            if arc_grants_dice:
                if arc_bonus == 2:
                    # Robot/Cyborg: Gain a d10 Technological Power.
                    print("Bonus: You get a d10 Technological Power.")
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.ChoosePQ(Category(1,8), [10], stepnum=this_step, inputs=pass_inputs)
            # Now we start adding Abilities.
            if self.archetype_modifier == 2:
                # If the hero is Modular, they get Modular abilities and Modes instead of the
                #  Abilities from their other Archetype
                # First, if the hero has fewer than 4 Powers, add d6 Powers until they have 4.
                while len(self.power_dice) < 4:
                    print(self.hero_name + " has " + str(len(self.power_dice)) + \
                          " of the 4 Power dice they'll need as a Modular hero. Choose a d6 " + \
                          "Power from any category to fill in the list:")
                    power_triplets = [[1,a,b] for b in range(len(mixed_collection[1][a])) \
                                      for a in range(len(mixed_collection[1]))]
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.ChoosePQ(power_triplets, [6], stepnum=this_step, inputs=pass_inputs)
                # Then add the mandatory Abilities for the Modular archetype:
                mandatory_abilities = [a for a in arc_modular[7]]
                for template in mandatory_abilities:
                    zone = template.zone
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.ChooseAbility([template], zone, stepnum=this_step, inputs=pass_inputs)
                # Then start adding Modes.
                # First, the user gets to choose whether to add a Powerless Mode.
                printlong("You can add a Powerless Mode if there are circumstances where you " + \
                          "could be separated from your power source (like having a Power Suit " + \
                          "that provides all your powers).", 100)
                DisplayModeTemplate(-1,0)
                entry_options = "YN"
                decision = choose_letter(entry_options,
                                         ' ',
                                         prompt="Do you want to add a Powerless Mode? (y/n)",
                                         repeat_message="Please enter Y or N.",
                                         inputs=inputs)
                entry_choice = decision[0]
                inputs = decision[1]
                if entry_choice == 'Y':
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.AddMode(-1, 0, stepnum=this_step, inputs=pass_inputs)
                # Then, they get 1 additional Green Mode.
                entry_options = string.ascii_uppercase[0:len(mc_green)]
                entry_choice = ' '
                print("Choose 1 additional Green Mode:")
                for i in range(len(mc_green)):
                    print("    " + entry_options[i] + ": " + mc_green[i][0])
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a Mode expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a Mode expanded, " + \
                                             "or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        DisplayModeTemplate(0, entry_options.find(entry_choice.upper()))
                entry_index = entry_options.find(entry_choice)
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddMode(0, entry_index, stepnum=this_step, inputs=pass_inputs)
                # Then, they get 2 different Yellow Modes.
                yellow_indices = [i for i in range(len(mc_yellow))]
                for x in range(2):
                    entry_options = string.ascii_uppercase[0:len(yellow_indices)]
                    entry_choice = ' '
                    if x > 0:
                        print("Choose the second Yellow Mode:")
                    else:
                        print("Choose the first Yellow Mode:")
                    for i in range(len(yellow_indices)):
                        print("    " + entry_options[i] + ": " + mc_yellow[yellow_indices[i]][0])
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("Enter a lowercase letter to see a Mode expanded, " + \
                                  "or an uppercase letter to select it.")
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0]
                        else:
                            entry_choice = input("Enter a lowercase letter to see a Mode " + \
                                                 "expanded, or an uppercase letter to select " + \
                                                 "it.\n")[0]
                        if entry_choice.upper() in entry_options and \
                           entry_choice not in entry_options:
                            entry_index = entry_options.find(entry_choice.upper())
                            DisplayModeTemplate(1, yellow_indices[entry_index])
                    entry_index = entry_options.find(entry_choice)
                    mode_index = yellow_indices[entry_index]
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.AddMode(1, mode_index, stepnum=this_step, inputs=pass_inputs)
                    del yellow_indices[entry_index]
                # Finally, they get 1 Red Mode.
                entry_options = string.ascii_uppercase[0:len(mc_red)]
                entry_choice = ' '
                print("Choose a Red Mode:")
                for i in range(len(mc_red)):
                    print("    " + entry_options[i] + ": " + mc_red[i][0])
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a Mode expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a Mode expanded, " + \
                                             "or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        DisplayModeTemplate(2, entry_options.find(entry_choice.upper()))
                entry_index = entry_options.find(entry_choice)
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddMode(2, entry_index, stepnum=this_step, inputs=pass_inputs)
            else:
                # As long as the hero isn't Modular, they get the Abilities from their main
                #  Archetype.
                # Start with the mandatory Abilities for the Archetype, if applicable:
                for template in mandatory_abilities:
                    zone = template.zone
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    legal_triplets = [x.triplet() for x in self.power_dice] + \
                                     [y.triplet() for y in self.quality_dice]
                    # Make a list of abilities the hero has in this zone from this Archetype
                    arc_zone_abilities = [x for x in self.abilities \
                                          if x.step == this_step and x.zone == zone]
                    if len(arc_zone_abilities) > 0:
                        if (zone == 0 and green_unique > 0) or (zone == 1 and yellow_unique > 0):
                            # There's a minimum number of unique Powers/Qualities that need to be
                            #  used in the Archetype abilities for this zone. Find out if it's been
                            #  met, and if not, restrict this Ability to unused ones.
                            # Start by making a list of the Powers/Qualities already used in
                            #  arc_zone_abilities:
                            arc_triplets = []
                            for x in arc_zone_abilities:
                                arc_triplets += [y for y in x.insert_pqs]
                            # Remove any repeats
                            for i in range(len(arc_triplets)):
                                trip = arc_triplets[i]
                                for j in range(i + 1, len(arc_triplets)):
                                    if arc_triplets[j] == trip:
                                        del arc_triplets[j]
                            if (zone == 0 and len(arc_triplets) < green_unique) or \
                               (zone == 1 and len(arc_triplets) < yellow_unique):
                                # This Ability needs to use a Power/Quality that hasn't been used
                                #  in this zone before
                                while len([x for x in legal_triplets if x in arc_triplets]) > 0:
                                    for x in arc_triplets:
                                        legal_triplets.remove(x)
                    if zone == 0 and green_limited:
                        # This is a Green Ability, and Green Abilities from this Archetype use only
                        #  Powers/Qualities from this Archetype
                        legal_triplets = [x for x in legal_triplets if x in all_arc_pqs]
                    self.ChooseAbility([template],
                                       zone,
                                       triplet_options=legal_triplets,
                                       stepnum=this_step,
                                       inputs=pass_inputs)
                # Then move on to the Green Abilities:
                # If mixed_abilities exists, then that's the list of Green Ability options
                if len(mixed_abilities) > 0:
                    green_abilities = mixed_abilities
                for i in range(green_count):
                    # Add another Green Ability from the list.
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    category_req = -1
                    legal_triplets = [x.triplet() for x in self.power_dice] + \
                                     [y.triplet() for y in self.quality_dice]
                    # If this is the first Green Ability and requires_primary, then specify that
                    #  it needs to use one of the primary powers/qualities:
                    if i == 0 and requires_primary:
                        legal_triplets = primary_pqs
                    # If this is the second Green Ability and category_required is 0 or 1, then
                    #  specify that it needs to use a die from the specified category:
                    elif i == 1 and category_required in [0,1]:
                        category_req = category_required
                    # Make a list of abilities the hero has in this zone from this Archetype
                    arc_zone_abilities = [x for x in self.abilities \
                                          if x.step == this_step and x.zone == 0]
                    print("### AddArchetype: len(arc_zone_abilities) for zone=0 is " + \
                          str(len(arc_zone_abilities)))
                    if len(arc_zone_abilities) > 0:
                        print("### AddArchetype: green_unique=" + str(green_unique))
                        if green_unique > 0:
                            # There's a minimum number of unique Powers/Qualities that need to be
                            #  used in the Archetype abilities for this zone. Find out if it's been
                            #  met, and if not, restrict this Ability to unused ones.
                            # Start by making a list of the Powers/Qualities already used in
                            #  arc_zone_abilities:
                            arc_triplets = []
                            for x in arc_zone_abilities:
                                arc_triplets += [y for y in x.insert_pqs]
                            # Remove any repeats
                            for i in range(len(arc_triplets)):
                                trip = arc_triplets[i]
                                for j in range(i + 1, len(arc_triplets)):
                                    if arc_triplets[j] == trip:
                                        del arc_triplets[j]
                            print("### AddArchetype: arc_triplets=" + str(arc_triplets))
                            print("### AddArchetype: len(arc_triplets)=" + str(len(arc_triplets)))
                            if len(arc_triplets) < green_unique:
                                # This Ability needs to use a Power/Quality that hasn't been used
                                #  in this zone before
                                while len([x for x in legal_triplets if x in arc_triplets]) > 0:
                                    for x in arc_triplets:
                                        if x in legal_triplets:
                                            legal_triplets.remove(x)
                    if green_limited:
                        # Green Abilities from this Archetype use only Powers/Qualities from this
                        #  Archetype
                        legal_triplets = [x for x in legal_triplets if x in all_arc_pqs]
                    print("### AddArchetype: legal_triplets=" + str(legal_triplets))
                    # Finally, add the ability
                    green_abilities = self.ChooseAbility(green_abilities,
                                                         0,
                                                         triplet_options=legal_triplets,
                                                         category_req=category_req,
                                                         stepnum=this_step,
                                                         inputs=pass_inputs)
                # Next add the Yellow Abilities, if there are any
                # If mixed_abilities exists, then green_abilities is the list of Yellow Ability
                #  options
                if len(mixed_abilities) > 0:
                    yellow_abilities = green_abilities
                for i in range(yellow_count):
                    # Add another Yellow Ability from the list.
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    legal_triplets = [x.triplet() for x in self.power_dice] + \
                                     [y.triplet() for y in self.quality_dice]
                    # Make a list of abilities the hero has in this zone from this Archetype
                    arc_zone_abilities = [x for x in self.abilities \
                                          if x.step == this_step and x.zone == 1]
                    if len(arc_zone_abilities) > 0:
                        if yellow_unique > 0:
                            # There's a minimum number of unique Powers/Qualities that need to be
                            #  used in the Archetype abilities for this zone. Find out if it's been
                            #  met, and if not, restrict this Ability to unused ones.
                            # Start by making a list of the Powers/Qualities already used in
                            #  arc_zone_abilities:
                            arc_triplets = [[y for y in x.insert_pqs] for x in arc_zone_abilities]
                            # Remove any repeats
                            for i in range(len(arc_triplets)):
                                trip = arc_triplets[i]
                                for j in range(i + 1, len(arc_triplets)):
                                    if arc_triplets[j] == trip:
                                        del arc_triplets[j]
                            if len(arc_triplets) < yellow_unique:
                                # This Ability needs to use a Power/Quality that hasn't been used
                                #  in this zone before
                                while len([x for x in legal_triplets if x in arc_triplets]) > 0:
                                    for x in arc_triplets:
                                        legal_triplets.remove(x)
                    yellow_abilities = self.ChooseAbility(yellow_abilities,
                                                          1,
                                                          triplet_options=legal_triplets,
                                                          stepnum=this_step,
                                                          inputs=pass_inputs)
                # If the hero is a Form-Changer, create their Forms
                if self.archetype == 15:
                    # Add 2 Green Forms and 1 Yellow Form.
                    for f_zone in [0,0,1]:
                        pass_inputs = []
                        if len(inputs) > 0:
                            if str(inputs[0]) != inputs[0]:
                                pass_inputs = inputs.pop(0)
                        self.ChooseForm(f_zone, inputs=pass_inputs)
                # If the hero is a Minion-Maker, select their Minion Forms
                if self.archetype == 13:
                    entry_options = string.ascii_uppercase[0:len(self.quality_dice)]
                    decision = self.ChooseIndex([str(x) for x in self.quality_dice],
                                                prompt="Choose a Quality to determine the number" + \
                                                " of Minion Forms " + self.hero_name + \
                                                " has access to:",
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    max_forms = self.quality_dice[entry_index].diesize
                    if max_forms >= len(min_collection):
                        print("OK! Adding all " + str(len(min_collection)) + \
                              " Minion Forms to " + self.hero_name + "'s Minion Sheet.")
                        for i in range(len(min_collection)):
                            self.min_forms[i] = [s for s in min_collection[i]]
                    else:
                        # The user needs to choose their Minion Forms.
                        min_indices = [i for i in range(len(min_collection))]
                        while len(self.min_forms) < max_forms:
                            entry_options = string.ascii_uppercase[0:len(min_indices)]
                            print("Choose a Minion Form (#" + str(len(self.min_forms) + 1) + \
                                  " of " + str(max_forms) + "):")
                            for i in range(len(min_indices)):
                                printlong(entry_options[i] + ": " + \
                                          MinionFormStr(min_collection[min_indices[i]]),
                                          96, prefix="    ")
                            decision = choose_letter(entry_options, ' ', inputs=inputs)
                            entry_choice = decision[0]
                            inputs = decision[1]
                            entry_index = entry_options.find(entry_choice)
                            # EDIT: Use choose_index(), not find()? printlong complicates things
                            # ...
                            mf_index = min_indices[entry_index]
                            self.min_forms.append(min_collection[min_indices.pop(entry_index)])
                            print("OK! Added " + min_collection[mf_index][0] + " to " + \
                                  self.hero_name + "'s Minion sheet.")
                        self.mf_step = this_step
            # Next, add any bonus content:
            if arc_bonus == 1:
                # Armored: You may use a Materials or Technological Power when determining Health.
                self.health_pqs += Category(1,4) + Category(1,8)
            elif arc_bonus == 2:
                # Robot/Cyborg: You may use a Technological Power when determining Health.
                self.health_pqs += Category(1,8)
            # Then add the Principle:
            if self.archetype_modifier == 1:
                # If the hero is Divided, they take some extra steps here
                entry_options = "YN"
                entry_choice = ' '
                printlong("As a Divided hero, you have two very different forms, such as a " + \
                          "nonpowered civilian form and a powered heroic form.",
                          100)
                print("The default names for these forms are " + self.dv_tags[0] + " and " + \
                      self.dv_tags[1] + ".")
                decision = choose_letter(entry_options,
                                         ' ',
                                         prompt="Do you want to give them custom names? (y/n)",
                                         repeat_message="Please enter Y or N.",
                                         inputs=inputs)
                entry_choice = decision[0]
                inputs = decision[1]
                if entry_choice == "Y":
                    for i in range(len(self.dv_tags)):
                        decision = self.EnterText("Enter a new name for your " + self.dv_tags[i] + \
                                                  " form.",
                                                  inputs=inputs)
                        self.dv_tags[i] = decision[0]
                        inputs = decision[1]
                        if len(self.dv_tags[i]) == 0:
                            self.dv_tags[i] = dv_defaults[i]
                # Choose a method of transition
                entry_options = string.ascii_uppercase[0:len(tr_collection)]
                entry_choice = ' '
                print("Choose a method of transformation between your " + self.dv_tags[0] + \
                      " and " + self.dv_tags[1] + " forms:")
                for i in range(len(tr_collection)):
                    print("    " + entry_options[i] + ": " + tr_collection[i][0])
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a transition method expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a transition " + \
                                             "method expanded, or an uppercase letter to " + \
                                             "select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        DisplayTransitionMethod(entry_options.find(entry_choice.upper()))
                entry_index = entry_options.find(entry_choice)
                tr_method = tr_collection[entry_index]
                print("OK! " + tr_method[0] + " selected.")
                # Use ChooseAbility() to add one of the associated Green Abilities, using a Power
                #  or Quality gained from their base Archetype
                arc_triplets = [triplet for triplet in primary_pqs]
                arc_triplets += [triplet for triplet in secondary_pqs \
                                 if triplet not in arc_triplets]
                arc_triplets += [triplet for triplet in tertiary_pqs \
                                 if triplet not in arc_triplets]
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs=inputs.pop(0)
                self.ChooseAbility(tr_method[2],
                                   0,
                                   triplet_options=arc_triplets,
                                   stepnum=this_step,
                                   inputs=pass_inputs)
                # Then, choose a build option and create your heroic & civilian forms
                build_options = [a_divided_psyche, a_split_form]
                entry_options = string.ascii_uppercase[0:len(build_options)]
                entry_choice = ' '
                print("Choose one as the nature of your divided self:")
                for i in range(len(build_options)):
                    print("    " + entry_options[i] + ": " + build_options[i].name)
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a divided nature expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a divided nature " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        build_options[entry_options.find(entry_choice.upper())].display(prefix="    ",
                                                                                        width=96)
                dv_nature = build_options[entry_options.find(entry_choice)]
                if dv_nature == a_divided_psyche:
                    # Add the Divided Psyche Green Ability
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    self.ChooseAbility([a_divided_psyche],
                                       0,
                                       stepnum=this_step,
                                       inputs=pass_inputs)
                    # Create a Civilian Form with standard Qualities & Status but no Powers
                    cf_name = self.dv_tags[0] + " Form"
                    cf_status = self.status_dice
                    civilian_form = [cf_name,
                                     0,
                                     [],
                                     self.quality_dice,
                                     cf_status,
                                     [],
                                     0,
                                     this_step]
                    self.other_forms.append(civilian_form)
                    print("Added " + self.dv_tags[0] + " Form to " + self.hero_name + \
                          "'s Form Sheet in Green.")
                    # Create a Heroic Form with standard Powers and Status but no Qualities
                    hr_name = self.dv_tags[1] + " Form"
                    hr_status = self.status_dice
                    heroic_form = [hr_name,
                                   0,
                                   self.power_dice,
                                   [],
                                   hr_status,
                                   [],
                                   1,
                                   this_step]
                    self.other_forms.append(heroic_form)
                    print("Added " + self.dv_tags[1] + " Form to " + self.hero_name + \
                          "'s Form Sheet in Green.")
                elif dv_nature == a_split_form:
                    # Split Form isn't really an Ability, just a set of instructions to follow
                    #  during this step
                    if self.archetype == 15:
                        print("I honestly have no idea how this works")
                        # Form-Changer lets you lose and gain Powers when you switch Forms. How
                        #  are you supposed to assign those Powers to either Civilian or Heroic?
                    else:
                        constant_powers = []
                        civilian_powers = []
                        heroic_powers = []
                        unassigned_powers = [d for d in self.power_dice]
                        constant_qualities = []
                        civilian_qualities = []
                        heroic_qualities = []
                        unassigned_qualities = [d for d in self.quality_dice]
                        # Pick 2 Powers to be available in both forms.
                        while len(constant_powers) < 2:
                            entry_options = string.ascii_uppercase[0:len(unassigned_powers)]
                            decision = self.ChooseIndex([str(x) for x in unassigned_powers],
                                                        prompt="Choose a Power for " + \
                                                        self.hero_name + " to have access to in both " + \
                                                        self.dv_tags[0] + " and " + \
                                                        self.dv_tags[1] + " Forms:",
                                                        inputs=inputs)
                            entry_index = decision[0]
                            inputs = decision[1]
                            print("OK! Marking " + str(unassigned_powers[entry_index]) + \
                                  " as a constant Power.")
                            constant_powers.append(unassigned_powers.pop(entry_index))
                        # Pick 2 Qualities to be available in both forms.
                        while len(constant_qualities) < 2:
                            entry_options = string.ascii_uppercase[0:len(unassigned_qualities)]
                            decision = self.ChooseIndex([str(x) for x in unassigned_qualities],
                                                        prompt="Choose a Quality for " + \
                                                        self.hero_name + " to have access to in both " + \
                                                        self.dv_tags[0] + " and " + \
							self.dv_tags[1] + " Forms:",
                                                        inputs=inputs)
                            entry_index = decision[0]
                            inputs = decision[1]
                            print("OK! Marking " + str(unassigned_qualities[entry_index]) + \
                                  " as a constant Quality.")
                            constant_qualities.append(unassigned_qualities.pop(entry_index))
                        # Assign each remaining Power and Quality to either Civilian or Heroic.
                        unassigned_dice = unassigned_powers + unassigned_qualities
                        while len(unassigned_dice) > 0:
                            assigning_die = unassigned_dice.pop(0)
                            entry_options = "AB"
                            decision = self.ChooseIndex(self.dv_tags,
                                                        prompt="Which of " + self.hero_name + \
							       "'s Divided Forms should have access to " + \
                                                               str(assigning_die) + "?",
                                                        inputs=inputs)
                            entry_index = decision[0]
                            inputs = decision[1]
                            print("OK! Marking " + str(assigning_die) + " as a " + \
                                  self.dv_tags[entry_index] + " " + \
                                  categories_singular[assigning_die.ispower] + ".")
                            if entry_index == 0:
                                if assigning_die.ispower:
                                    civilian_powers.append(assigning_die)
                                else:
                                    civilian_qualities.append(assigning_die)
                            else:
                                if assigning_die.ispower:
                                    heroic_powers.append(assigning_die)
                                else:
                                    heroic_qualities.append(assigning_die)
                        # We're leaving self.power_dice and self.quality_dice as complete lists.
                        # The Heroic form gets the Heroic dice plus the Constant ones:
                        hr_power_dice = [d for d in constant_powers + heroic_powers]
                        hr_quality_dice = [d for d in constant_qualities + heroic_qualities]
                        # The Civilian form gets the Civilian dice plus the Constant ones.
                        cf_power_dice = [d for d in constant_powers + civilian_powers]
                        cf_quality_dice = [d for d in constant_qualities + civilian_qualities]
                        # >> Split up the Abilities? <<
                        # ...
                        cf_name = self.dv_tags[0] + " Form"
                        cf_status = self.status_dice
                        civilian_form = [cf_name,
                                         0,
                                         cf_power_dice,
                                         cf_quality_dice,
                                         cf_status,
                                         [],
                                         0,
                                         this_step]
                        self.other_forms.append(civilian_form)
                        print("Added " + self.dv_tags[0] + " Form to " + self.hero_name + \
                              "'s Form Sheet in Green.")
                        hr_name = self.dv_tags[1] + " Form"
                        hr_status = self.status_dice
                        heroic_form = [hr_name,
                                       0,
                                       hr_power_dice,
                                       hr_quality_dice,
                                       hr_status,
                                       [],
                                       1,
                                       this_step]
                        self.other_forms.append(heroic_form)
                        print("Added " + self.dv_tags[1] + " Form to " + self.hero_name + \
                              "'s Form Sheet in Green.")
                if self.archetype == 15:
                    # This hero is a Form-Changer. Any of their Forms that don't currently have a
                    #  Civilian or Heroic tag need to have one assigned.
                    unassigned_forms = [f for f in self.other_forms if f[6] not in [0,1]]
                    for f in unassigned_forms:
                        entry_options = string.ascii_uppercase[0:2]
                        decision = self.ChooseIndex(self.dv_tags,
                                                    prompt=self.hero_name + " is a Divided hero. Is " + \
                                                    f[0] + " a " + self.dv_tags[0] + " or " + \
                                                    self.dv_tags[1] + " form for them?",
                                                    inputs=inputs)
                        entry_index = decision[0]
                        inputs = decision[1]
                        f[6] = entry_index
                        print("OK! " + f[0] + " is now marked as a " + self.dv_tags[f[6]] + \
                              " Form.")
                    if dv_nature == a_divided_psyche:
                        # Your Forms from Form-Changer are now all tagged as either Civilian or
                        #  Heroic.
                        for i in range(len(self.other_forms)):
                            form_editing = self.other_forms[i]
                            if form_editing[6] == 0:
                                # This form is Civilian. Remove its Power list.
                                form_editing[2] = []
                            else:
                                # This form is Heroic. Remove its Quality list.
                                form_editing[3] = []
                # Finally, choose a Principle from the Divided archetype
                r_category = arc_divided[18]
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePrinciple(r_category, stepnum=this_step, inputs=pass_inputs)
            else:
                # As long as your hero isn't Divided, they get their Principle from their main
                #  Archetype
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePrinciple(r_category, stepnum=this_step, inputs=pass_inputs)
            print("That's all for your Archetype!")
    def GuidedArchetype(self, adice=[], inputs=[]):
        # Walks the user through randomly selecting an Archetype as specified in the rulebook.
        # adice: the set of dice provided in the Background step to use in this one.
        #  Defaults to self.arc_dice if not specified.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns [Archetype index, modifier index]
        if len(inputs) > 0:
            print("### GuidedArchetype: inputs=" + str(inputs))
        if adice == [] and self.arc_dice == []:
            print("Error! No dice have been specified for this step.")
            return
        elif adice == []:
            adice = self.arc_dice
        elif len(adice) not in [2,3] or len([d for d in adice if d not in legal_dice]) > 0:
            print("Error! " + str(adice) + " is not a valid set of Archetype dice.")
            return
        # The user can reroll any number of their dice once per step.
        rerolls = 1
        prev_results = [0 for d in adice]
        while rerolls >= 0:
            die_results = prev_results
            print("Rolling " + dice_combo(adice, results=die_results) + " for Archetype:")
            for i in range(len(adice)):
                if die_results[i] == 0:
                    die_results[i] = random.randint(1, adice[i])
            arc_options = []
            if len(adice) == 2:
                roll_report = "Rolled " + str(die_results[0]) + " and " + str(die_results[1]) + "."
                # The player can choose between any single result or the sum of any pair of
                #  results.
                # Since there are only two dice, this is a straightforward list: the two results
                #  and their sum.
                arc_options = [min(die_results), max(die_results), sum(die_results)]
                if arc_options[0] == arc_options[1]:
                    arc_options.remove(arc_options[0])
            else:
                roll_report = "Rolled " + str(die_results[0]) + ", " + str(die_results[1]) + \
                              ", and " + str(die_results[2]) + "."
                # The player can choose between any single result or the sum of any pair of results.
                # Since there are exactly three dice, each sum of two dice can be represented as the
                #  sum of all three minus the value of the third.
                arc_options = [x for x in die_results] + [sum(die_results) - y for y in die_results]
                arc_options.sort()
                for i in range(len(arc_options)-1):
                    for j in range(i+1, len(arc_options)):
                        if i < j < len(arc_options):
                            if arc_options[i] == arc_options[j]:
                                del arc_options[j]
            # To convert to 0-index, subtract 1 from each option:
            arc_indices = [x-1 for x in arc_options]
            # Let the user choose from the options provided by their roll...
            entry_choice = ' '
            entry_options = string.ascii_uppercase[0:len(arc_options) + rerolls]
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user
                answer = IntVar()
                options = [arc_collection[arc_indices[i]][0] + " (" + str(arc_options[i]) + ")" for i in range(len(arc_options))]
                if rerolls > 0:
                    options += ["REROLL"]
                question = ExpandWindow(self.myWindow,
                                        roll_report + "\nChoose one:",
                                        options,
                                        [ArchetypeDetails(i, width=0) for i in arc_indices],
                                        var=answer,
                                        title="Archetype Selection",
                                        rwidth=arc_width)
                entry_index = answer.get()
            else:
                # USe the shell to prompt the user
                print(roll_report)
                for i in range(len(entry_options)-rerolls):
                    print("    " + entry_options[i] + ": " + arc_collection[arc_indices[i]][0] + \
                          " (" + str(arc_options[i]) + ")")
                if rerolls > 0:
                    print("    " + entry_options[len(entry_options)-1] + ": REROLL")
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see an Archetype expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see an Archetype " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options[:len(arc_options)] and \
                       entry_choice not in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        DisplayArchetype(arc_indices[entry_index], "    ", 96)
                entry_index = entry_options.find(entry_choice)
            # Now we have a commitment to a valid choice from the list.
            if entry_index == len(arc_options):
                # User selected to reroll.
                prev_results = [0 for x in die_results]
                entry_options = "YN"
                decision = choose_letter(entry_options,
                                         ' ',
                                         prompt="Do you want to keep any of the previous " + \
                                         "results? (y/n)",
                                         repeat_message="Please enter Y or N.",
                                         inputs=inputs)
                entry_choice = decision[0]
                inputs = decision[1]
                if entry_choice == "Y":
                    for i in range(len(die_results)):
                        decision = choose_letter(entry_options,
                                                 ' ',
                                                 prompt="Do you want to keep " + \
                                                        str(die_results[i]) + " on your d" + \
                                                        str(adice[i]) + "? (y/n)",
                                                 repeat_message="Please enter Y or N.",
                                                 inputs=inputs)
                        entry_choice = decision[0]
                        inputs = decision[1]
                        if entry_choice == "Y":
                            prev_results[i] = die_results[i]
                rerolls = 0
            elif arc_indices[entry_index] in range(len(arc_simple)):
                # User selected a simple Archetype.
                print(arc_collection[arc_indices[entry_index]][0] + " Archetype selected.")
                return [arc_indices[entry_index], 0]
            else:
                # User selected a complex Archetype.
                modifier_index = arc_indices[entry_index] - len(arc_collection) + \
                                 len(arc_modifiers)
                arc_mod = arc_modifiers[modifier_index]
                print(arc_mod[0] + " requires another Archetype to modify.")
                entry_choice = " "
                if modifier_index == 2:
                    # Modular gives the user a choice: reroll their dice, or choose the other
                    #  Archetype from their existing options.
                    entry_options = "YN"
                    decision = choose_letter(entry_options,
                                             ' ',
                                             prompt="Do you want to reroll your Archetype " + \
                                             "dice before choosing your other Archetype? (y/n)",
                                             repeat_message="Please enter Y or N.",
                                             inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                if modifier_index == 1 or entry_choice == 'Y':
                    # Either the modifier is Divided, which requires a reroll, or the modifier is
                    #  Modular and the user has chosen to reroll.
                    print("Rolling " + dice_combo(adice) + " for other Archetype...")
                    die_results = [random.randint(1, x) for x in adice]
                    arc_options = []
                    if len(adice) == 2:
                        roll_report = "Rolled " + str(die_results[0]) + " and " + \
                                      str(die_results[1]) + "."
                        # The player can choose between any single result or the sum of any pair of
                        #  results.
                        # Since there are only two dice, this is a straightforward list: the two
                        #  results and their sum.
                        arc_options = [min(die_results), max(die_results), sum(die_results)]
                        if arc_options[0] == arc_options[1]:
                            arc_options.remove(arc_options[0])
                        if arc_options[-1] not in range(len(arc_simple)):
                            arc_options.remove(arc_options[-1])
                    else:
                        roll_report = "Rolled " + str(die_results[0]) + ", " + \
                                      str(die_results[1]) + ", and " + str(die_results[2]) + "."
                        # The player can choose between any single result or the sum of any pair
                        #  of results.
                        # Since there are exactly three dice, each sum of two dice can be
                        #  represented as the sum of all three minus the value of the third.
                        arc_options = [x for x in die_results] + \
                                      [sum(die_results) - y for y in die_results]
                        arc_options.sort()
                        for i in range(len(arc_options)-1):
                            for j in range(i+1, len(arc_options)):
                                if i < j < len(arc_options):
                                    if arc_options[i] == arc_options[j] or \
                                       arc_options[j] not in range(len(arc_simple)):
                                        del arc_options[j]
                else:
                    # User chose not to reroll.
                    # Remove any results outside the set of simple Archetypes.
                    for i in range(len(arc_options)):
                        if arc_options[i] not in range(len(arc_simple)):
                            del arc_options[i]
                # To convert to 0-index, subtract 1 from each option:
                arc_indices = [x-1 for x in arc_options]
                # Let the user choose from the list of options:
                entry_options = string.ascii_uppercase[0:len(arc_options)]
                entry_choice = ' '
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    answer = IntVar()
                    options = [arc_mod[0] + ":" + arc_simple[arc_indices[i]][0] + " (" + \
                              str(arc_options[i]) + ")" for i in range(len(arc_options))]
                    question = ExpandWindow(self.myWindow,
                                            roll_report + "\nChoose one:",
                                            options,
                                            [ArchetypeDetails(i, width=0) \
                                             for i in arc_indices],
                                            var=answer,
                                            title="Archetype Selection",
                                            rwidth=arc_width)
                    entry_index = answer.get()
                else:
                    print(roll_report)
                    for i in range(len(arc_options)):
                        print("    " + entry_options[i] + ": " + arc_mod[0] + ":" + \
                              arc_simple[arc_indices[i]][0] + " (" + str(arc_options[i]) + ")")
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("Enter a lowercase letter to see an Archetype expanded, " + \
                                  "or an uppercase letter to select it.")
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0]
                        else:
                            entry_choice = input("Enter a lowercase letter to see an " + \
                                                 "Archetype expanded, or an uppercase letter " + \
                                                 "to select it.\n")[0]
                        if entry_choice.upper() in entry_options and \
                           entry_choice not in entry_options:
                            entry_index = entry_options.find(entry_choice.upper())
                            DisplayArchetype(arc_indices[entry_index], "    ", 96)
                    entry_index = entry_options.find(entry_choice)
                # Now we have an option from the list
                arc_index = arc_indices[entry_index]
                print(arc_mod[0] + ":" + arc_collection[arc_index][0] + " Archetype selected.")
                return [arc_index, modifier_index]
    def ConstructedArchetype(self, inputs=[]):
        # Walks the user through selecting an Archetype from the full list of options.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # Returns [Archetype index, modifier index]
        if len(inputs) > 0:
            print("### ConstructedArchetype: inputs=" + str(inputs))
        entry_options = string.ascii_uppercase[0:len(arc_collection)]
        entry_choice = ' '
        if self.UseGUI(inputs):
            # Create an ExpandWindow to prompt the user.
            answer = IntVar()
            question = ExpandWindow(self.myWindow,
                                    "Choose an Archetype from the list:",
                                    [x[0] for x in arc_collection],
                                    [ArchetypeDetails(i, width=0) \
                                     for i in range(len(arc_collection))],
                                    var=answer,
                                    title="Archetype Selection",
                                    rwidth=arc_width)
            entry_index = answer.get()
        else:
            print("Choose an Archetype from the list:")
            for i in range(len(arc_collection)):
                print("    " + entry_options[i] + ": " + arc_collection[i][0] + " (" + str(i+1) + \
                      ")")
            while entry_choice not in entry_options:
                if len(inputs) > 0:
                    print("Enter a lowercase letter to see an Archetype expanded, " + \
                          "or an uppercase letter to select it.")
                    print("> " + inputs[0])
                    entry_choice = inputs.pop(0)[0]
                else:
                    entry_choice = input("Enter a lowercase letter to see an Archetype " + \
                                         "expanded, or an uppercase letter to select it.\n")[0]
                if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                    entry_index = entry_options.find(entry_choice.upper())
                    DisplayArchetype(entry_index, "    ", 96)
            entry_index = entry_options.find(entry_choice)
        print(arc_collection[entry_index][0] + " Archetype selected.")
        if entry_index in range(len(arc_simple)):
            return [entry_index, 0]
        else:
            modifier_index = entry_index - len(arc_collection) + len(arc_modifiers)
            arc_mod = arc_modifiers[modifier_index]
            entry_options = string.ascii_uppercase[0:len(arc_simple)]
            entry_choice = ' '
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user.
                answer = IntVar()
                question = ExpandWindow(self.myWindow,
                                        arc_mod[0] + " modifies another Archetype. Choose " + \
                                        "another Archetype from the list:",
                                        [x[0] for x in arc_simple],
                                        [ArchetypeDetails(i, width=0) \
                                         for i in range(len(arc_simple))],
                                        var=answer,
                                        title="Archetype Selection",
                                        rwidth=arc_width)
                entry_index = answer.get()
            else:
                print(arc_mod[0] + \
                      " modifies another Archetype. Choose another Archetype from the list:")
                for i in range(len(arc_simple)):
                    print("    " + entry_options[i] + ": " + arc_mod[0] + ":" + \
                          arc_simple[i][0] + " (" + str(i+1) + ")")
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see an Archetype expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see an Archetype " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        DisplayArchetype(entry_index, "    ", 96)
                entry_index = entry_options.find(entry_choice)
            print(arc_mod[0] + ":" + arc_simple[entry_index][0] + " Archetype selected.")
            return [entry_index, modifier_index]
    def AddPersonality(self, pn_index, dv_index=99, out_index=99, inputs=[]):
        # Adds the Status dice and Out Ability granted by the specified Personality (or
        #  Personalities, in the case of a Divided hero)
        # inputs: a list of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### AddPersonality: inputs=" + str(inputs))
        # This is Step 4 of hero creation!
        this_step = 4
        your_pn = pn_collection[pn_index]
        if self.personality in range(len(pn_collection)):
            # This hero already has a Personality.
            pn_text = "the " + pn_collection[self.personality][0] + " Personality."
            if self.dv_personality in range(len(pn_collection)):
                pn_text = "the " + pn_collection[self.personality][0] + " Personality in " + \
                          self.dv_tags[1] + " form and the " + \
                          pn_collection[self.dv_personality][0] + " Personality in " + \
                          self.dv_tags[0] + " form."
            print("Error! " + self.hero_name + " already has " + pn_text)
            input()
        else:
            # This hero doesn't have a Personality, so we can add this one.
            self.personality = pn_index
            # Not all Divided heroes take more than one Personality. We'll use has_multiple to
            #  indicate whether this hero is one of them.
            # has_multiple is only true if the hero has the Divided modifier AND dv_index is a
            #  valid Personality index AND index and dv_index don't match
            has_multiple = (self.archetype_modifier == 1 and dv_index in range(len(pn_collection)) \
                            and dv_index != index)
            if has_multiple:
                self.dv_personality = dv_index
                your_dv_pn = pn_collection[self.dv_personality]
                printlong("OK! You've chosen " + your_pn[0] + " as your " + self.dv_tags[1] + \
                          " Personality and " + your_dv_pn[0] + " as your " + self.dv_tags[0] + \
                          " Personality.", 100)
            else:
                print("OK! You've chosen the " + your_pn[0] + " Personality.")
            # Start by giving the hero their Roleplaying Quality at d8.
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.ChoosePQDieSize(0, [4, 0], [8], stepnum=this_step, inputs=pass_inputs)
            # Then fill in their status dice and Out Ability.
            out_options = []
            if has_multiple:
                self.status_dice = [d for d in your_pn[1]]
                dv_status_dice = [d for d in your_dv_pn[1]]
                printlong("You get " + str(self.status_dice) + " as Status dice in " + \
                          self.dv_tags[1] + ", and " + str(dv_status_dice) + " in " + \
                          self.dv_tags[0] + ".", 100)
                for i in range(len(self.other_forms)):
                    form_editing = self.other_forms[i]
                    # If this Form isn't the same dv_tag as the base form, give it the status dice
                    #  from the non-base Personality.
                    if form_editing[6] != 1:
                        form_editing[4] = [x for x in dv_status_dice]
                out_options = [pn[2] for pn in [your_pn, your_dv_pn]]
                if out_options[0] == out_options[1]:
                    del out_options[1]
            else:
                self.status_dice = [d for d in your_pn[1]]
                print("You get " + str(self.status_dice) + " as Status dice.")
                out_options = [your_pn[2]]
            self.status_step = this_step
            if out_index in range(len(out_options)):
                # User already chose which Out Ability to use, probably in ConstructedPersonality()
                #  or GuidedPersonality()
                out_options = [out_options[out_index]]
            # Add the Out Ability (letting the user choose, if there's more than one).
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.ChooseAbility(out_options,
                               3,
                               stepnum=this_step,
                               inputs=pass_inputs)
            # Add any bonus content, if applicable
            your_personalities = [self.personality]
            if has_multiple:
                your_personalities = [self.dv_personality] + your_personalities
            for i in range(len(your_personalities)):
                pn_index = your_personalities[i]
                this_bonus = pn_collection[pn_index][3]
                if this_bonus == 1:
                    # Impulsive: Upgrade one of your Power or Quality dice by one step
                    #  (maximum d12).
                    upgrade_pqs = []
                    matching_forms = self.other_forms
                    impulsive_prompt = "Choose a Power or Quality to upgrade by one size:"
                    if i == 1 or not has_multiple:
                        # Include dice from the base form (always "Heroic" if Divided)
                        upgrade_pqs += [d for d in self.power_dice + self.quality_dice \
                                        if d.diesize < max(legal_dice)]
                    if has_multiple:
                        # Choose the die to upgrade from the set of dice available in the
                        #  corresponding Divided Form.
                        impulsive_prompt = "Choose a " + self.dv_tags[i] + \
                                           " Power or Quality to upgrade by one size:"
                        matching_forms = [form for form in self.other_forms if form[6] == i]
                    for this_form in matching_forms:
                        # Add less-than-maximal Powers and Qualities from this form, if they don't
                        #  already have dice in upgrade_pqs
                        upgrade_pqs += [d for d in this_form[2] + this_form[3] \
                                        if d.triplet() not in [ex.triplet() for ex in upgrade_pqs]]
                    # Check if the hero has Divided Psyche. If so, their Heroic Form can only use
                    #  Powers, regardless of their Quality list.
                    dv_ps_matches = [a for a in self.abilities if a.name == "Divided Psyche"]
                    if len(dv_ps_matches) > 0 and i == 1:
                        upgrade_pqs = [d for d in upgrade_pqs if d.ispower == 1]
                    decision = self.ChooseIndex([str(x) for x in upgrade_pqs],
                                                prompt=impulsive_prompt,
                                                inputs=inputs)
                    entry_index = decision[0]
                    inputs = decision[1]
                    upgrade_die = upgrade_pqs[entry_index]
                    upgrade_triplet = upgrade_die.triplet()
                    if upgrade_triplet[0] == 1:
                        # Upgrading a Power
                        # Find all Power dice matching this triplet that can be upgraded, and
                        #  upgrade them
                        for d in self.power_dice:
                            if d.triplet() == upgrade_triplet and d.diesize < max(legal_dice):
                                d.SetPrevious(this_step)
                                d.diesize += 2
                                if len(self.other_forms) > 0:
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + \
                                          " in base form.")
                                else:
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + \
                                          ".")
                        # Make sure to check other Forms as well
                        for f in self.other_forms:
                            for d in f[2]:
                                if d.triplet() == upgrade_triplet and d.diesize < max(legal_dice):
                                    d.SetPrevious(this_step)
                                    d.diesize += 2
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + \
                                          " in " + f[0] + ".")
                    else:
                        # Upgrading a Quality
                        # Find all Quality dice matching this triplet that can be upgraded, and
                        #  upgrade them
                        for d in self.quality_dice:
                            if d.triplet() == upgrade_triplet and d.diesize < max(legal_dice):
                                d.SetPrevious(this_step)
                                d.diesize += 2
                                if len(self.other_forms) > 0:
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + \
                                          " in base form.")
                                else:
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + ".")
                        # Make sure to check other Forms as well
                        for f in self.other_forms:
                            for d in f[3]:
                                if d.triplet() == upgrade_triplet and d.diesize < max(legal_dice):
                                    d.SetPrevious(this_step)
                                    d.diesize += 2
                                    print("Upgraded " + d.flavorname + " to d" + str(d.diesize) + \
                                          " in " + f[0] + ".")
                elif this_bonus == 2:
                    # Mischievous: You may use any Power or Quality to determine Health.
                    for i in range(len(mixed_collection)):
                        for j in range(len(mixed_collection[i])):
                            self.health_pqs += [triplet for triplet in Category(i, j) \
                                                if triplet not in self.health_pqs]
            print("That's all for your Personality.")
    def GuidedPersonality(self, inputs=[]):
        # Walks the user through randomly choosing Personality(ies) as specified in the rulebook.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### GuidedPersonality: inputs=" + str(inputs))
        multiple_choice = False
        if self.archetype_modifier in [1,99]:
            # If the hero has no assigned Archetype modifier, or if their Archetype modifier is
            #  1 (Divided), then they get to choose whether their hero gets more than 1
            #  Personality.
            multiple_choice = True
        is_multiple = False
        if multiple_choice:
            entry_options = "YN"
            decision = choose_letter(entry_options,
                                     ' ',
                                     prompt="Do you want to use two different Personalities? (y/n)",
                                     repeat_message="Please enter Y or N.",
                                     inputs=inputs)
            entry_choice = decision[0]
            inputs = decision[1]
            is_multiple = (entry_choice == "Y")
        if is_multiple:
            # The rulebook says "you may take two different personalities - one for each of your
            #  forms"... but doesn't specify whether you should ROLL twice when using the Guided
            #  method.
            print("I don't actually know how this works.")
            # ...
            return [99]
        else:
            # Single personality.
            # Returns [personality index]
            # The user can reroll any number of their dice once per step.
            rerolls = 1
            prev_result = 0
            while rerolls >= 0:
                die_results = []
                if prev_result < 1:
                    print("Rolling 2d10 for Personality...")
                    die_results = [random.randint(1, 10), random.randint(1, 10)]
                else:
                    print("Keeping " + str(prev_result) + \
                          " from previous roll. Rolling 1d10 for Personality...")
                    die_results = [prev_result, random.randint(1, 10)]
                print("Rolled " + str(die_results[0]) + " and " + str(die_results[1]) + ".")
                # The player can choose between any single result or the sum of any pair of results.
                # Since there are only two dice, this is a straightforward list: the two results
                #  and their sum.
                pn_options = [min(die_results), max(die_results), sum(die_results)]
                # In case of doubles, remove the duplicate roll:
                if pn_options[0] == pn_options[1]:
                    del pn_options[1]
                # To convert to 0-index, subtract 1 from each option.
                pn_indices = [x-1 for x in pn_options]
                # Let the user choose from the options provided by their roll...
                entry_choice = ' '
                entry_options = string.ascii_uppercase[0:len(pn_options) + rerolls]
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    answer = IntVar()
                    options = [pn_collection[pn_indices[i]][0] + " (" + str(pn_options[i]) + ")" \
                               for i in range(len(pn_indices))]
                    if rerolls > 0:
                        options += ["REROLL"]
                    details = [PersonalityDetails(i, width=0) for i in pn_indices]
                    question = ExpandWindow(self.myWindow,
                                            "Choose one:",
                                            options,
                                            details,
                                            var=answer,
                                            title="Personality Selection",
                                            rwidth=pn_Width)
                    entry_index = answer.get()
                else:
                    for i in range(len(entry_options)-rerolls):
                        print("    " + entry_options[i] + ": " + pn_collection[pn_indices[i]][0] + \
                              " (" + str(pn_options[i]) + ")")
                    if rerolls > 0:
                        print("    " + entry_options[len(entry_options)-1] + ": REROLL")
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("Enter a lowercase letter to see a Personality expanded, " + \
                                  "or an uppercase letter to select it.")
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0]
                        else:
                            entry_choice = input("Enter a lowercase letter to see a Personality " + \
                                                 "expanded, or an uppercase letter to select it.\n")[0]
                        if entry_choice.upper() in entry_options[:-1] and \
                           entry_choice not in entry_options:
                            entry_index = entry_options.find(entry_choice.upper())
                            DisplayPersonality(pn_indices[entry_index], "    ")
                    entry_index = entry_options.find(entry_choice)
                # Now we have a commitment to a valid choice from the list.
                if entry_index == len(pn_options):
                    # User selected to reroll.
                    entry_options = "YN"
                    decision = choose_letter(entry_options,
                                             ' ',
                                             prompt="Do you want to keep any of the previous results? (y/n)",
                                             repeat_message="Please enter Y or N.",
                                             inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                    if entry_choice == 'Y':
                        entry_options = string.ascii_uppercase[0:len(die_results)]
                        decision = self.ChooseIndex([str(x) for x in die_results],
                                                    prompt="Choose which result to keep:",
                                                    inputs=inputs)
                        inputs = decision[1]
                        prev_result = die_results[decision[0]]
                    rerolls = 0
                else:
                    # User selected a personality.
                    print(pn_collection[pn_indices[entry_index]][0] + " Personality selected.")
                    return [pn_indices[entry_index]]
    def ConstructedPersonality(self, inputs=[]):
        # Walks the user through choosing Personality(ies) from the full list of options.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### ConstructedPersonality: inputs=" + str(inputs))
        multiple_choice = False
        if self.archetype_modifier in [1,99]:
            # If the hero has no assigned Archetype modifier, or if their Archetype modifier is 1
            #  (Divided), then they get to choose whether their hero gets more than 1 Personality.
            multiple_choice = True
        is_multiple = False
        if multiple_choice:
            entry_options = "YN"
            decision = choose_letter(entry_options,
                                     ' ',
                                     prompt="Do you want to use two different Personalities? (y/n)",
                                     repeat_message="Please enter Y or N.",
                                     inputs=inputs)
            entry_choice = decision[0]
            inputs = decision[1]
            is_multiple = (entry_choice == "Y")
        if is_multiple:
            # Choose 2 Personalities and 1 Out Ability.
            # Returns [personality index 1, personality index 2, Out Ability index]
            personalities = [99, 99]
            out_options = [None, None]
            pn_indices = [x for x in range(len(pn_collection))]
            for f in [0,1]:
                entry_options = string.ascii_uppercase[0:len(pn_indices)]
                entry_choice = ' '
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    answer = IntVar()
                    options = [pn_collection[x][0] for x in pn_indices]
                    details = [PersonalityDetails(x, width=0) for x in pn_indices]
                    question = ExpandWindow(self.myWindow,
                                            "Choose a Personality for " + self.dv_tags[f] + \
                                            " form:",
                                            options,
                                            details,
                                            var=answer,
                                            title="Personality Selection",
                                            rwidth=pn_width)
                    entry_index = answer.get()
                else:
                    print("OK! Choose a Personality for " + self.dv_tags[f] + " form:")
                    for i in range(len(pn_indices)):
                        print("    " + entry_options[i] + ": " + pn_collection[pn_indices[i]][0])
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("Enter a lowercase letter to see a Personality expanded, " + \
                                  "or an uppercase letter to select it.")
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0]
                        else:
                            entry_choice = input("Enter a lowercase letter to see a Personality " + \
                                                 "expanded, or an uppercase letter to select it.\n")[0]
                        if entry_choice not in entry_options and entry_choice.upper() in entry_options:
                            entry_index = entry_options.find(entry_choice.upper())
                            DisplayPersonality(entry_index)
                    entry_index = entry_options.find(entry_choice)
                print(pn_collection[entry_index][0] + " Personality selected.")
                personalities[f] = entry_index
                out_options[f] = pn_collection[entry_index][2]
            # Now they have two different Personalities- but they can only have one Out Ability.
            out_options = [pn_collection[p][2] for p in personalities]
            out_choice = 99
            if out_options[0] == out_options[1]:
                # Luckily, not every Personality has a unique Out Ability.
                # In this case, both Abilities are the same.
                out_choice = 0
            else:
                # More likely, though, the user needs to choose.
                decision = self.ChooseIndex([out_options[i].name + " (" + \
                                             pn_collection[personalities[i]][0] + ")" \
                                             for i in range(len(personalities))],
                                            prompt="Choose which Out Ability to use:",
                                            inputs=inputs)
                out_choice = decision[0]
                inputs = decision[1]
            personalities.append(out_choice)
            return personalities
        else:
            # Choose 1 Personality.
            # Returns [personality index]
            entry_options = string.ascii_uppercase[0:len(pn_collection)]
            entry_choice = ' '
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user.
                answer = IntVar()
                options = [x[0] for x in pn_collection]
                details = [PersonalityDetails(i, width=0) for i in range(len(pn_collection))]
                question = ExpandWindow(self.myWindow,
                                        "Choose a Personality from the list:",
                                        options,
                                        details,
                                        var=answer,
                                        title="Personality Selection",
                                        rwidth=pn_width)
                entry_index = answer.get()
            else:
                print("OK! Choose a Personality from the list:")
                for i in range(len(pn_collection)):
                    print("    " + entry_options[i] + ": " + pn_collection[i][0])
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a Personality expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a Personality " + \
                                             "expanded, or an uppercase letter to select it.\n")[0]
                    if entry_choice not in entry_options and entry_choice.upper() in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        DisplayPersonality(entry_index)
                entry_index = entry_options.find(entry_choice)
            print(pn_collection[entry_index][0] + " Personality selected.")
            return [entry_index]
    def AddRedAbility(self, retcon_step=0, inputs=[]):
        # Walks the user through picking out a Red Ability from the options available based on
        #  the hero's current Powers and Qualities.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        if len(inputs) > 0:
            print("### AddRedAbility: inputs=" + str(inputs))
        slots_remaining = True
        # This is Step 5 of hero creation!
        this_step = 5
        # ... unless it's the retcon
        if retcon_step != 0:
            this_step = retcon_step
            # Check if this hero already used their Retcon. If so, we have a problem.
            if self.used_retcon:
                print("Error! " + self.hero_name + " already used " + \
                      pronouns[self.pronoun_set][2] + " Retcon.")
                slots_remaining = False
                input()
        else:
            # Count the number of Red Abilities the hero already has from this step. If it's more
            #  than 1, we have a problem.
            rs_abilities = [a for a in self.abilities if a.step == this_step]
            if len(rs_abilities) > 1:
                print("Error! " + self.hero_name + " already added " + str(len(rs_abilities)) + \
                      " Red Abilities in step " + str(this_step) + ".")
                slots_remaining = False
                input()
        if slots_remaining:
            # First, determine which Red Abilities are available
            pq_dice = self.power_dice + self.quality_dice
            pq_triplets = [d.triplet() for d in pq_dice]
            # For each category of Power or Quality that grants Red Ability options, create a list
            #  of dice this hero has that match that category
            pq_sublists = []
            ra_sublists = []
            for i in range(len(ra_collection)):
                for j in range(len(ra_collection[i])):
                    # Create a list of Power/Quality dice and a list of Red Abilities for this
                    #  category
                    pq_sublists.append([])
                    ra_sublists.append([])
                    k = len(pq_sublists)-1
                    # Add each matching Power/Quality die to the Power/Quality list
                    for d in pq_dice:
                        if d.ispower == i and d.category == j:
                            pq_sublists[k].append(d)
                            # Then, check the Red Abilities from the corresponding list in
                            #  ra_collection
                            for ra in ra_collection[i][j]:
                                # If a Red Ability isn't already in the current sublist...
                                if ra not in ra_sublists[k]:
                                    # ... and d is a valid die for that Ability's first slot...
                                    if d.triplet() in ra.required_pqs[0]:
                                        # ... and that Ability has no other requirements, add it
                                        #  to the sublist
                                        if len(ra.required_pqs[1]) == 0:
                                            ra_sublists[k].append(ra)
                                        else:
                                            # If it does have other requirements, make sure at
                                            #  least one of the hero's other dice matches them
                                            other_dice = [x for x in pq_dice if x != d]
                                            has_match = False
                                            for e in other_dice:
                                                if e.triplet() in ra.required_pqs[1]:
                                                    has_match = True
                                            if has_match:
                                                ra_sublists[k].append(ra)
                    # If either the Power/Quality sublist is empty or the Red Ability sublist is
                    #  empty, we can't gain any of these abilities.
                    # Delete both sublists.
                    if len(pq_sublists[k]) == 0 or len(ra_sublists[k]) == 0:
                        del pq_sublists[k]
                        del ra_sublists[k]
            if len(pq_sublists) != len(ra_sublists):
                print("Error! Unequal list lengths")
            if len(pq_sublists) == 0 and self.archetype != 13:
                print("Error! " + self.hero_name + \
                      " has no Powers or Qualities that grant Red Abilities.")
            sublist_strings = [''] * len(pq_sublists)
            if self.archetype == 13:
                # Minion-Maker archetype grants its own list of Red Ability options, which use
                #  Powers but aren't restricted by specific Powers or Qualities
                pq_sublists.append([d for d in self.power_dice])
                ra_sublists.append([rt for rt in ra_minion_maker])
                sublist_strings.append("for Minion-Maker heroes")
                # ...
            # Show the user the list of sublists of Red Abilities and corresponding Powers/Qualities
            if self.UseGUI(inputs):
                # Create an ExpandWindow to prompt the user
                answer = IntVar()
                dispWidth = 100
                details = ["" for i in range(len(pq_sublists))]
                for i in range(len(pq_sublists)):
                    pq_first = pq_sublists[i][0]
                    if len(pq_sublists[i]) > 1 and sublist_strings[i] == "":
                        pq_category = mixed_categories[pq_first.ispower][pq_first.category] + " " + \
                                      categories_singular[pq_first.ispower]
                        pq_options = str(pq_first)
                        for d in pq_sublists[i][1:-1]:
                            pq_options += ", " + str(d)
                        if len(pq_sublists[i]) > 2:
                            pq_options += ","
                        pq_options += " or " + str(pq_sublists[i][-1])
                        if pq_category[0].upper() in "AEIOU":
                            sublist_strings[i] = "using an " + pq_category + " (" + pq_options + ")"
                        else:
                            sublist_strings[i] = "using a " + pq_category + " (" + pq_options + ")"
                    elif sublist_strings[i] == "":
                        sublist_strings[i] = "using " + str(pq_first)
                    details[i] = "Red Abilities " + sublist_strings[i] + ":"
                    for rt in ra_sublists[i]:
                        details[i] += "\n" + rt.details(width=dispWidth)
                question = ExpandWindow(self.myWindow,
                                        "Choose a category to gain a Red Ability from:",
                                        sublist_strings,
                                        details,
                                        var=answer,
                                        title="Red Ability Selection",
                                        rwidth=dispWidth)
                entry_index = answer.get()
            else:
                entry_options = string.ascii_uppercase[0:len(pq_sublists)]
                entry_choice = ' '
                print("Choose a category to gain a Red Ability from:")
                for i in range(len(pq_sublists)):
                    pq_first = pq_sublists[i][0]
                    if len(pq_sublists[i]) > 1 and sublist_strings[i] == "":
                        pq_category = mixed_categories[pq_first.ispower][pq_first.category] + " " + \
                                      categories_singular[pq_first.ispower]
                        pq_options = str(pq_first)
                        for d in pq_sublists[i][1:-1]:
                            pq_options += ", " + str(d)
                        if len(pq_sublists[i]) > 2:
                            pq_options += ","
                        pq_options += " or " + str(pq_sublists[i][-1])
                        if pq_category[0].upper() in "AEIOU":
                            sublist_strings[i] = "using an " + pq_category + " (" + pq_options + ")"
                        else:
                            sublist_strings[i] = "using a " + pq_category + " (" + pq_options + ")"
                    elif sublist_strings[i] == "":
                        sublist_strings[i] = "using " + str(pq_first)
                    print("    " + entry_options[i] + ": " + sublist_strings[i])
                    for rt in ra_sublists[i]:
                        print("            " + str(rt))
                while entry_choice not in entry_options:
                    if len(inputs) > 0:
                        print("Enter a lowercase letter to see a category expanded, " + \
                              "or an uppercase letter to select it.")
                        print("> " + inputs[0])
                        entry_choice = inputs.pop(0)[0]
                    else:
                        entry_choice = input("Enter a lowercase letter to see a category expanded, " + \
                                             "or an uppercase letter to select it.\n")[0]
                    if entry_choice.upper() in entry_options and entry_choice not in entry_options:
                        entry_index = entry_options.find(entry_choice.upper())
                        print("Red Abilities " + sublist_strings[entry_index] + ":")
                        for rt in ra_sublists[entry_index]:
                            rt.display(prefix="    ", width=96)
                entry_index = entry_options.find(entry_choice)
            # Now we have the user's choice of category.
            # Send that set of Red Abilities and the corresponding restrictions on which
            #  Powers/Qualities to use to ChooseAbility to let them pick an Ability to finish and
            #  add.
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.ChooseAbility(ra_sublists[entry_index],
                               2,
                               triplet_options=[d.triplet() for d in pq_sublists[entry_index]],
                               stepnum=this_step,
                               inputs=pass_inputs)
    def AddRetcon(self, inputs=[]):
        # Walks the user through choosing and implementing one of the AddRetcon options defined in
        #  the rulebook.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        # No return value.
        if len(inputs) > 0:
            print("### AddRetcon: inputs=" + str(inputs))
        # This is step 6 of hero creation!
        this_step = 6
        if self.used_retcon:
            print("Error! " + self.hero_name + " already used " + pronouns[self.pronoun_set][2] + \
                  " Retcon.")
            input()
        else:
            step_options = ["Swap 2 Power dice",
                            "Swap 2 Quality dice",
                            "Change the Power/Quality used in an Ability",
                            "Add a d6 Power or Quality from any category",
                            "Upgrade Red status die by one size (maximum d12)",
                            "Change one of your Principles to any other Principle",
                            "Gain another Red Ability"]
            decision = self.ChooseIndex(step_options,
                                        prompt="Choose a Retcon to take:",
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            step_choice = step_options[entry_index]
            if step_choice == "Swap 2 Power dice":
                # Modify this to include Powers from other Modes/Forms?
                # ...
                swap_indices = [99, 99]
                if self.UseGUI(inputs):
                    # Create a SwapWindow to prompt the user
                    dispWidth = 100
                    title = "Retcon"
                    prompt = "Choose 2 different Power dice to swap:"
                    answer0 = IntVar()
                    answer1 = IntVar()
                    question = SwapWindow(self.myWindow,
                                          prompt,
                                          [str(x) for x in self.power_dice],
                                          answer0,
                                          answer1,
                                          width=dispWidth)
                    swap_indices = [answer0.get(), answer1.get()]
                else:
                    decision = self.ChooseIndex([str(x) for x in self.power_dice],
                                                prompt="Choose the first Power die to swap...",
                                                inputs=inputs)
                    swap_indices[0] = decision[0]
                    inputs = decision[1]
                    decision = self.ChooseIndex([str(x) for x in self.power_dice],
                                                prompt="OK! Choose a die to swap with " + \
                                                str(self.power_dice[swap_indices[0]]) + "...",
                                                inputs=inputs)
                    swap_indices[1] = decision[0]
                    inputs = decision[1]
                swap_dice = [self.power_dice[i] for i in swap_indices]
                if swap_dice[0].diesize != swap_dice[1].diesize:
                    for i in range(len(swap_dice)):
                        swap_dice[i].SetPrevious(this_step)
                    d_temp = swap_dice[0].diesize
                    swap_dice[0].diesize = swap_dice[1].diesize
                    swap_dice[1].diesize = d_temp
                    print("OK! " + swap_dice[0].flavorname + " is now d" + \
                          str(swap_dice[0].diesize) + " and " + swap_dice[1].flavorname + \
                          " is now d" + str(swap_dice[1].diesize) + ".")
                    self.used_retcon = True
                elif swap_indices[0] == swap_indices[1]:
                    print("You can't swap " + str(self.power_dice[swap_indices[0]]) + \
                          " with itself.")
                else:
                    print(swap_dice[0].name + " and " + swap_dice[1].name + \
                          " already have the same die size (d" + swap_dice[0].diesize + ").")
            elif step_choice == "Swap 2 Quality dice":
                # Modify this to include Qualities from other Forms?
                # ...
                swap_indices = [99, 99]
                if self.UseGUI(inputs):
                    # Create a SwapWindow to prompt the user
                    dispWidth = 100
                    title = "Retcon"
                    prompt = "Choose 2 different Quality dice to swap:"
                    answer0 = IntVar()
                    answer1 = IntVar()
                    question = SwapWindow(self.myWindow,
                                          prompt,
                                          [str(x) for x in self.quality_dice],
                                          answer0,
                                          answer1,
                                          width=dispWidth)
                    swap_indices = [answer0.get(), answer1.get()]
                else:
                    decision = self.ChooseIndex([str(x) for x in self.quality_dice],
                                                prompt="Choose the first Quality die to swap...",
                                                inputs=inputs)
                    swap_indices[0] = decision[0]
                    inputs = decision[1]
                    decision = self.ChooseIndex([str(x) for x in self.quality_dice],
                                                prompt="OK! Choose a die to swap with " + \
                                                str(self.quality_dice[swap_indices[0]]) + "...",
                                                inputs=inputs)
                    swap_indices[1] = decision[0]
                    inputs = decision[1]
                swap_dice = [self.quality_dice[i] for i in swap_indices]
                if swap_dice[0].diesize != swap_dice[1].diesize:
                    for i in range(len(swap_dice)):
                        swap_dice[i].SetPrevious(this_step)
                    d_temp = swap_dice[0].diesize
                    swap_dice[0].diesize = swap_dice[1].diesize
                    swap_dice[1].diesize = d_temp
                    print("OK! " + swap_dice[0].flavorname + " is now d" + \
                          str(swap_dice[0].diesize) + " and " + swap_dice[1].flavorname + \
                          " is now d" + str(swap_dice[1].diesize) + ".")
                    self.used_retcon = True
                elif swap_indices[0] == swap_indices[1]:
                    print("You can't swap " + str(self.quality_dice[swap_indices[0]]) + \
                          " with itself.")
                else:
                    print(swap_dice[0].name + " and " + swap_dice[1].name + \
                          " already have the same die size (d" + swap_dice[0].diesize + ").")
            elif step_choice == "Change the Power/Quality used in an Ability":
                # Choose an Ability to change
                ability_options = [a for a in self.abilities]
                for f in self.other_forms:
                    ability_options += [a for a in f[5]]
                for m in self.other_modes:
                    ability_options += [a for a in m[5]]
                # If an Ability doesn't use a Power or Quality in its text, it's not a valid
                #  choice here...
                ability_options = [a for a in ability_options if "%p" in a.text]
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    answer = IntVar()
                    options = [str(x) for x in ability_options]
                    details = [x.details(width=100) for x in ability_options]
                    prompt = "Choose an Ability to edit:"
                    question = ExpandWindow(self.myWindow,
                                            prompt,
                                            options,
                                            details,
                                            var=answer,
                                            title="Retcon",
                                            rwidth=100)
                    entry_index = answer.get()
                else:
                    entry_options = string.ascii_uppercase[0:len(ability_options)]
                    entry_choice = ' '
                    print("Choose an Ability to edit:")
                    for i in range(len(ability_options)):
                        print("    " + entry_options[i] + ": " + str(ability_options[i]))
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("Enter a lowercase letter to see an Ability expanded, " + \
                                  "or an uppercase letter to select it.")
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0]
                        else:
                            entry_choice = input("Enter a lowercase letter to see an " + \
                                                 "Ability expanded, or an uppercase letter to " + \
                                                 "select it.\n")[0]
                        if entry_choice not in entry_options and \
                           entry_choice.upper() in entry_options:
                            entry_index = entry_options.find(entry_choice.upper())
                            ability_options[entry_index].display()
                    entry_index = entry_options.find(entry_choice)
                edit_ability = ability_options[entry_index]
                edit_index = 0
                # If the ability uses more than one power/quality, specify which to change
                non_empty_inserts = [x for x in edit_ability.insert_pqs if len(x) > 0]
                if len(non_empty_inserts) > 1:
                    decision = self.ChooseIndex([MixedPQ(x) for x in non_empty_inserts],
                                                prompt="Which Power/Quality would you like to " + \
                                                "replace?",
                                                inputs=inputs)
                    edit_index = decision[0]
                    inputs = decision[1]
                # Find the correct list of powers and qualities to choose a replacement from
                pq_options = self.power_dice + self.quality_dice
                if edit_ability not in self.abilities:
                    found = False
                    for md in self.other_modes:
                        if not found:
                            if edit_ability in md[5]:
                                pq_options = md[3] + md[4]
                                found = True
                    for fm in self.other_forms:
                        if not found:
                            if edit_ability in fm[5]:
                                pq_options = md[3] + md[4]
                                found = True
                # Remove the option that corresponds to the Power/Quality this ability already uses
                replaced_pq = None
                i = 0
                while i in range(len(pq_options)) and replaced_pq == None:
                    print("i=" + str(i))
                    if pq_options[i].triplet() == edit_ability.insert_pqs[edit_index]:
                        replaced_pq = pq_options.pop(i)
                    else:
                        i += 1
                # Have the user choose the replacement Power/Quality
                entry_options = string.ascii_uppercase[0:len(pq_options)]
                decision = self.ChooseIndex([str(x) for x in pq_options],
                                            prompt="Choose a Power or Quality to replace " + \
                                            str(replaced_pq) + " in " + str(edit_ability) + ":",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                new_pq = pq_options[entry_index]
                edit_ability.SetPrevious(this_step)
                edit_ability.insert_pqs[edit_index] = new_pq.triplet()
                print("OK! Replaced " + str(replaced_pq) + " in " + str(edit_ability) + \
                      " with " + str(new_pq) + ".")
                edit_ability.display()
                if isinstance(self.myFrame, HeroFrame):
                    self.myFrame.UpdateAll()
                self.used_retcon = True
            elif step_choice == "Add a d6 Power or Quality from any category":
                # Let the user choose a Power or Quality to add from any category using ChoosePQ
                power_triplets = AllCategories(1)
                quality_triplets = AllCategories(0)
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePQ(power_triplets + quality_triplets,
                              [6],
                              stepnum=this_step,
                              inputs=pass_inputs)
                self.used_retcon = True
            elif step_choice == "Upgrade Red status die by one size (maximum d12)":
                # red_upgrade_sizes: list of individually defined Red status die sizes that can be
                #  upgraded
                red_upgrade_sizes = []
                # red_upgrade_forms: list of indices in self.other_forms that correspond to die
                #  sizes in red_upgrade_sizes
                red_upgrade_forms = []
                base_form = "Base Form"
                if self.status_dice[2] < max(legal_dice):
                    # The Red die in the base form is small enough that it can be upgraded
                    red_upgrade_sizes.append(self.status_dice[2])
                    # Include it in the list of form indices as 99
                    red_upgrade_forms.append(99)
                if self.archetype_modifier == 1:
                    base_form = self.dv_tags[1]
                # Check each alternate Form to see if its Red status die is individually defined,
                #  and if so, whether it can be upgraded
                for i in range(len(self.other_forms)):
                    fm = self.other_forms[i]
                    if fm[4][2] == 0:
                        # This form relies on the base form for its status dice, and won't need to
                        #  be updated if that die is changed
                        base_form += "/" + fm[0]
                    elif fm[4][2] < max(legal_dice):
                        # This form's status dice are individually defined (fm[4][2] != 0)...
                        # ... and the Red one is small enough that it can be upgraded
                        #  (fm[4][2] < max(legal_dice))
                        red_upgrade_sizes.append(fm[4][2])
                        red_upgrade_forms.append(i)
                if len(red_upgrade_sizes) == 0:
                    # None of the hero's Red dice are small enough that they can be upgraded.
                    print("Error! Can't upgrade " + self.hero_name + "'s Red status die (d" + \
                          str(self.status_dice[2]) + ").")
                elif len(red_upgrade_sizes) > 1:
                    # More than one of the hero's Red dice are small enough that they can be
                    #  upgraded.
                    # The rulebook is unclear on how this works- do you upgrade all of them or only
                    #  one?
                    # For now, let the user choose.
                    entry_options = string.ascii_uppercase[0:len(red_upgrade_sizes)+1]
                    print("Which Red status die should be upgraded?")
                    # Options for upgrading the Red die of a specific non-base form
                    for i in range(len(red_upgrade_sizes)):
                        if red_upgrade_forms[i] == 99:
                            print("    " + entry_options[i] + ": d" + str(red_upgrade_sizes[i]) + \
                                  " (" + base_form + ")")
                        else:
                            print("    " + entry_options[i] + ": d" + str(red_upgrade_sizes[i]) + \
                                  " (" + self.other_forms[red_upgrade_forms[i]][0] + ")")
                    # Last option: upgrade all Red dice
                    print("    " + entry_options[-1] + ": All")
                    decision = choose_letter(entry_options, ' ', inputs=inputs)
                    entry_choice = decision[0]
                    inputs = decision[1]
                    entry_index = entry_options.find(entry_choice)
                    # EDIT: Use choose_index(), not find()? print_options would be complex...
                    # ...
                    if entry_index == len(entry_options) - 1:
                        # User chose to upgrade all Red status dice
                        print("Upgrading all of " + self.hero_name + "'s Red status dice...")
                        self.status_dice[2] += 2
                        if this_step not in self.status_steps_modified:
                            self.status_steps_modified.append(this_step)
                        print("Upgraded " + self.hero_name + "'s " + base_form + \
                              " Red status die to d" + str(self.status_dice[2]) + ".")
                        for fm_index in red_upgrade_forms:
                            current_form = self.other_forms[fm_index]
                            current_form[4][2] += 2
                            print("Upgraded " + self.hero_name + "'s " + current_form[0] + \
                                  " Red status die to d" + str(current_form[4][2]) + ".")
                        self.used_retcon = True
                    elif red_upgrade_forms[entry_index] == 99:
                        # User chose to upgrade the base Red status die
                        self.status_dice[2] += 2
                        if this_step not in self.status_steps_modified:
                            self.status_steps_modified.append(this_step)
                        print("Upgraded " + self.hero_name + "'s " + base_form + \
                              " Red status die to d" + str(self.status_dice[2]) + ".")
                        self.used_retcon = True
                    else:
                        # User chose to upgrade an alternate Red status die
                        edit_form = self.other_forms[red_upgrade_forms[entry_index]]
                        edit_form[4][2] += 2
                        print("Upgraded " + self.hero_name + "'s " + edit_form[0] + \
                              " Red status die to d" + edit_form[4][2] + ".")
                        self.used_retcon = True
                elif red_upgrade_forms[0] == 99:
                    # Only one Red die size can be upgraded, and it's from the base form.
                    self.status_dice[2] += 2
                    if this_step not in self.status_steps_modified:
                        self.status_steps_modified.append(this_step)
                    print("Upgraded " + self.hero_name + "'s Red status die to d" + \
                          str(self.status_dice[2]) + ".")
                    for fm in self.other_forms:
                        if fm[4][2] not in [0, self.status_dice[2]]:
                            # These were the same when we started; they should be the same now
                            fm[4][2] = self.status_dice[2]
                    self.used_retcon = True
                else:
                    # Only one Red die size can be upgraded, and it's from an alternate form.
                    edit_form = self.other_forms[red_upgrade_forms[0]]
                    print(self.hero_name + "'s " + base_form + " Red status die (d" + \
                          str(self.status_dice[2]) + ") can't be upgraded, but " + \
                          pronouns[self.pronoun_set][2] + " " + edit_form[0] + \
                          " Red status die (d" + str(edit_form[4][2]) + ") can.")
                    edit_form[4][2] += 2
                    print("Upgraded " + self.hero_name + "'s " + edit_form[0] + \
                          " Red status die to d" + edit_form[4][2] + ".")
                    self.used_retcon = True
            elif step_choice == "Change one of your Principles to any other Principle":
                # Have the user choose a category to add from...
                if self.UseGUI(inputs):
                    # Create an ExpandWindow to prompt the user
                    answer = IntVar()
                    dispWidth = 50
                    options = [rc_names[i] + " Principles" for i in range(len(rc_names))]
                    details = [rc_names[i] + " Principles:" for i in range(len(rc_names))]
                    for i in range(len(rc_names)):
                        for j in range(len(rc_master[i])):
                            details[i] += "\nPrinciple of " + rc_master[i][j][0]
                    question = ExpandWindow(self.myWindow,
                                            "Choose a Principle category:",
                                            options,
                                            details,
                                            var=answer,
                                            title="Retcon: Change a Principle",
                                            rwidth=dispWidth)
                    entry_index = answer.get()
                else:
                    entry_options = string.ascii_uppercase[0:len(rc_master)]
                    entry_choice = ' '
                    print("Choose a Principle category:")
                    for i in range(len(rc_names)):
                        print("    " + entry_options[i] + ": " + rc_names[i] + " Principles:")
                        for j in range(len(rc_master[i])):
                            print("            " + rc_master[i][j][0])
                    while entry_choice not in entry_options:
                        if len(inputs) > 0:
                            print("> " + inputs[0])
                            entry_choice = inputs.pop(0)[0].upper()
                        else:
                            entry_choice = input()[0].upper()
                    entry_index = entry_options.find(entry_choice)
                # Then use ChoosePrinciple to let them choose which to add
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.ChoosePrinciple(entry_index,
                                     stepnum=this_step,
                                     inputs=pass_inputs)
                self.used_retcon = True
            elif step_choice == "Gain another Red Ability":
                # Let the user add another Red Ability using AddRedAbility
                pass_inputs = []
                if len(inputs) > 0:
                    if str(inputs[0]) != inputs[0]:
                        pass_inputs = inputs.pop(0)
                self.AddRedAbility(retcon_step=this_step,
                                   inputs=pass_inputs)
                self.used_retcon = True
        if self.used_retcon:
            self.RefreshFrame()
    def HealthRanges(self):
        # Returns the set of [max, min] pairs representing the health range corresponding to each
        #  of the hero's three status zones.
        ranges = [[]] * 3
        for i in range(len(self.health_zones)):
            zone_min = 1
            if i < 2:
                zone_min = self.health_zones[i+1] + 1
            ranges[i] = [self.health_zones[i], zone_min]
        return ranges
    def AddHealth(self, roll=99, inputs=[]):
        # Walks the user through determining the hero's max Health and ranges for each status zone.
        # roll: the result of 1d8, prepared earlier
        # inputs: a list of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### AddHealth: inputs=" + str(inputs))
        # This is step 7 of hero creation!
        this_step = 7
        if self.health_zones != [0,0,0]:
            # The hero already has defined Health!
            print("Error! " + self.hero_name + " already has maximum Health:")
            rn = self.HealthRanges()
            for i in range(len(rn)):
                print("    " + status_zones[i] + " Zone: " + str(rn[i][0]) + "-" + str(rn[i][1]))
            input()
        else:
            # The hero doesn't have defined Health yet, so we can continue.
            self.health_step = this_step
            # Add up the following:
            # 8...
            # ... die size of an eligible Power or Quality...
            pq_options = self.power_dice + self.quality_dice
            for md in self.other_modes:
                pq_options += [d for d in md[2] if str(d) not in [str(x) for x in pq_options]]
                pq_options += [d for d in md[3] if str(d) not in [str(x) for x in pq_options]]
            for fm in self.other_forms:
                pq_options += [d for d in fm[2] if str(d) not in [str(x) for x in pq_options]]
                pq_options += [d for d in fm[3] if str(d) not in [str(x) for x in pq_options]]
            pq_options = [d for d in pq_options if d.triplet() in self.health_pqs]
            pq_part = 4
            if len(pq_options) == 1:
                pq_report = self.hero_name + "'s only valid Power or Quality for Health is " + \
                            str(pq_options[0]) + "."
                pq_part = pq_options[0].diesize
            elif len(pq_options) == 0:
                pq_report = self.hero_name + " has no eligible Powers or Qualities to use for " + \
                            "Health. Using a d4."
                pq_part = 4
            else:
                decision = self.ChooseIndex([str(x) for x in pq_options],
                                            prompt="Choose a Power or Quality to use for " + \
                                            self.hero_name + "'s max Health:",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                pq_report = "Using " + str(pq_options[entry_index]) + " from " + self.hero_name + \
                            "'s Powers/Qualities."
                pq_part = pq_options[entry_index].diesize
            print("OK! " + pq_report)
            # ... Red status die size ...
            red_options = [self.status_dice[2]]
            red_sources = ["base form"]
            for md in self.other_modes:
                if md[4][2] not in [0] + red_options:
                    red_options.append(md[4][2])
                    red_sources.append(md[0])
            for fm in self.other_forms:
                if fm[4][2] not in [0] + red_options:
                    red_options.append(fm[4][2])
                    red_sources.append(fm[0])
            red_part = 0
            if len(red_options) == 1:
                red_report = self.hero_name + "'s only Red status die size is " + \
                             str(red_options[0]) + "."
                red_part = red_options[0]
            else:
                decision = self.ChooseIndex([str(red_options[i]) + " (" + red_sources[i] + ")" \
                                             for i in range(len(red_options))],
                                            prompt="Choose a Red status die to use for " + \
                                            self.hero_name + "'s max Health:",
                                            inputs=inputs)
                entry_index = decision[0]
                inputs = decision[1]
                red_report = "Using d" + str(red_options[entry_index]) + " from " + \
                             self.hero_name + "'s Red status."
                red_part = red_options[entry_index]
            print("OK! " + red_report)
            # ... and either 4 OR 1d8
            random_part = 4
            random_prompt = pq_report + "\n" + red_report + "\n" + "The total so far is " + \
                            str(8 + pq_part + red_part) + " (8 + " + str(pq_part) + " + " + \
                            str(red_part) + ")." + "\n" + "Which would you like to add?"
            random_options = ["4", "Roll 1d8"]
            decision = self.ChooseIndex(random_options,
                                        prompt=random_prompt,
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            if random_options[entry_index] == "Roll 1d8":
                print("Rolling 1d8 for Health...")
                if roll in range(1,9):
                    random_part = roll
                else:
                    random_part = random.randint(1, 8)
                print("Rolled " + str(random_part) + "!")
            else:
                print("Using 4 for Health.")
            max_health = 8 + pq_part + red_part + random_part
            print(self.hero_name + "'s max Health is " + str(max_health) + ".")
            health_index = max_health - hp_bounds[0][0]
            self.health_zones = [n for n in hp_bounds[health_index]]
            rn = self.HealthRanges()
            for i in range(len(rn)):
                print("    " + status_zones[i] + " Zone: " + str(rn[i][0]) + "-" + str(rn[i][1]))
        self.RefreshFrame()
    def CreateHero(self, health_roll=99, inputs=[]):
        # Walks the user through hero creation from start to finish.
        # inputs: a list of text inputs to use automatically instead of prompting the user
        if len(inputs) > 0:
            print("### CreateHero: inputs=" + str(inputs))
        step_options = ["Guided (roll dice & choose from results)",
                        "Constructed (choose from a table)"]
        indent = "    "
        # Choose a Background:
        print("1. Background")
        if self.background in range(len(bg_collection)):
            # This hero already has a Background
            print(indent + self.hero_name + " already has the " + \
                  bg_collection[self.background][0] + " Background.")
        else:
            bg_index = 99
            decision = self.ChooseIndex(step_options,
                                        prompt="How would you like to choose a Background for " + \
                                        str(self.hero_name) + "?",
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                bg_index = self.GuidedBackground(inputs=pass_inputs)
            else:
                bg_index = self.ConstructedBackground(inputs=pass_inputs)
            # Add the chosen Background
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddBackground(bg_index, inputs=pass_inputs)
        # Choose a Power Source
        print("2. Power Source")
        if self.power_source in range(len(ps_collection)):
            # This hero already has a Power Source
            print(indent + self.hero_name + " already has the " + \
                  ps_collection[self.power_source][0] + " Power Source.")
        else:
            ps_index = 99
            decision = self.ChooseIndex(step_options,
                                        prompt="How would you like to choose a Power Source for " + \
					       self.hero_name + "?",
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                ps_index = self.GuidedPowerSource(inputs=pass_inputs)
            else:
                ps_index = self.ConstructedPowerSource(inputs=pass_inputs)
            # Add the chosen Power Source
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddPowerSource(ps_index, inputs=pass_inputs)
        # Choose an Archetype
        print("3. Archetype")
        if self.archetype in range(len(arc_collection)):
            # This hero already has an Archetype
            arc_text = arc_collection[self.archetype][0]
            if self.archetype_modifier in range(1,len(arc_modifiers)):
                arc_text = arc_modifiers[self.archetype_modifier][0] + ":" + arc_text
            print(indent + self.hero_name + " already has the " + arc_text + " Archetype.")
        else:
            arc_indices = [99, 99]
            decision = self.ChooseIndex(step_options,
                                        prompt="How would you like to choose an Archetype for " + \
					       self.hero_name + "?",
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                arc_indices = self.GuidedArchetype(inputs=pass_inputs)
            else:
                arc_indices = self.ConstructedArchetype(inputs=pass_inputs)
            # Add the chosen Archetype
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddArchetype(arc_indices[0], arc_indices[1], inputs=pass_inputs)
        # Choose one or more Personalities
        print("4. Personality")
        if self.personality in range(len(pn_collection)):
            # This hero already has a Personality.
            pn_text = "the " + pn_collection[self.personality][0] + " Personality."
            if self.dv_personality in range(len(pn_collection)):
                pn_text = "the " + pn_collection[self.personality][0] + " Personality in " + \
                          self.dv_tags[1] + " form and the " + \
                          pn_collection[self.dv_personality][0] + " Personality in " + \
                          self.dv_tags[0] + " form."
            print(indent + self.hero_name + " already has " + pn_text)
        else:
            pn_indices = []
            pn_prompt = "How would you like to choose a Personality for " + self.hero_name + "?"
            if self.archetype_modifier == 1:
                # Divided heroes can have more than one Personality
                pn_prompt = "How would you like to choose Personality/ies for " + \
                            self.hero_name + "?"
            decision = self.ChooseIndex(step_options,
                                        prompt=pn_prompt,
                                        inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                pn_indices = self.GuidedPersonality(inputs=pass_inputs)
                if pn_indices[0] not in range(len(pn_collection)):
                    print("There was a problem with your Guided result. " + \
                          "Let's try the Constructed method.")
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    pn_indices = self.ConstructedPersonality(inputs=pass_inputs)
            else:
                pn_indices = self.ConstructedPersonality(inputs=pass_inputs)
            # Add the chosen Personality/ies
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if len(pn_indices) == 1:
                self.AddPersonality(pn_indices[0],
                                    inputs=pass_inputs)
            elif len(pn_indices) == 2:
                self.AddPersonality(pn_indices[0],
                                    dv_index=pn_indices[1],
                                    inputs=pass_inputs)
            else:
                self.AddPersonality(pn_indices[0],
                                    dv_index=pn_indices[1],
                                    out_index=pn_indices[2],
                                    inputs=pass_inputs)
        # Add 2 Red Abilities
        print("5. Red Abilities")
        rs_abilities = [a for a in self.abilities if a.step == 5]
        if len(rs_abilities) > 1:
            print(indent + self.hero_name + " already added " + str(len(rs_abilities)) + \
                  " Red Abilities in step 5.")
        while len(rs_abilities) < 2:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddRedAbility(inputs=pass_inputs)
            rs_abilities = [a for a in self.abilities if a.step == 5]
        # Take a Retcon
        print("6. Retcon")
        if self.used_retcon:
            print(indent + self.hero_name + " already used " + pronouns[self.pronoun_set][2] + \
                  " Retcon.")
        else:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddRetcon(inputs=pass_inputs)
        # Determine Max Health
        print("7. Health")
        if self.health_zones != [0,0,0]:
            print(indent + self.hero_name + " already has maximum Health (" + \
                  str(self.health_zones[0]) + ").")
        else:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.AddHealth(roll=health_roll, inputs=pass_inputs)
        print("Done!")
    def Abilities(self, zone):
        # Returns the set of Abilities on this hero's main sheet that match the specified zone.
        return [a for a in self.abilities if a.zone == zone]
    def DisplayStep(self, stepnum, prefix="", width=100):
        # Prints the set of attributes (Powers, Qualities, Principles, Abilities, Modes, Forms,
        #  etc.) that the hero gained in the specified step of hero creation.
        # No return value.
        indent = "    "
        if stepnum in range(1,len(step_names)):
            step_powers = [d for d in self.power_dice if d.step == stepnum]
            step_qualities = [d for d in self.quality_dice if d.step == stepnum]
            step_principles = [pri for pri in self.principles if pri.step == stepnum]
            step_abilities = [a for a in self.abilities if a.step == stepnum]
            step_forms = [fm for fm in self.other_forms if fm[7] == stepnum]
            step_modes = [md for md in self.other_modes if md[7] == stepnum]
            any_added = max([len(step_powers),
                             len(step_qualities),
                             len(step_principles),
                             len(step_abilities),
                             len(step_forms),
                             len(step_modes)])
            if stepnum in [self.status_step, self.health_step] or \
               (stepnum == self.mf_step and len(self.min_forms) > 0):
                any_added = 1
            if any_added > 0:
                print(prefix + "Step " + str(stepnum) + " (" + step_names[stepnum] + ") provided:")
                if len(step_principles) > 0:
                    print(prefix + indent + "Principles:")
                    for pri in step_principles:
                        pri.display(prefix=prefix+indent+indent,
                                    width=width-len(prefix)-len(indent)*2,
                                    green=False)
                if len(step_powers) > 0:
                    print(prefix + indent + "Powers:")
                    for d in step_powers:
                        print(prefix + indent + indent + str(d.RetrievePrior(stepnum+1)))
                if len(step_qualities) > 0:
                    print(prefix + indent + "Qualities:")
                    for d in step_qualities:
                        print(prefix + indent + indent + str(d.RetrievePrior(stepnum+1)))
                if stepnum == self.status_step:
                    print(prefix + indent + "Status:")
                    for x in range(len(self.status_dice)):
                        print(prefix + indent + indent + status_zones[x] + ": " + \
                              str(self.status_dice[x]))
                if stepnum == self.health_step:
                    print(prefix + indent + "Health:")
                    rn = self.HealthRanges()
                    for i in range(len(rn)):
                        print(prefix + indent + indent + status_zones[i] + " Zone: " + \
                              str(rn[i][0]) + "-" + str(rn[i][1]))
                for z in range(len(status_zones)):
                    step_zone_abilities = [ab for ab in step_abilities if ab.zone == z]
                    if len(step_zone_abilities) > 0:
                        print(prefix + indent + "Abilities (" + status_zones[z] + "):")
                        for a in step_zone_abilities:
                            a.RetrievePrior(stepnum+1).display(prefix=prefix+indent+indent,
                                                               width=width-len(prefix+indent+indent))
                if stepnum == self.mf_step and len(self.min_forms) > 0:
                    print(prefix + indent + "Minion Forms:")
                    for x in range(len(self.min_forms)):
                        printlong(MinionFormStr(self.min_forms[x]),
                                  width=width-len(prefix+indent+indent),
                                  prefix=prefix+indent+indent)
                if len(step_forms) > 0:
                    print(prefix + indent + "Forms:")
                    for x in range(len(step_forms)):
                        self.DisplayForm(x,
                                         codename=False,
                                         prefix=prefix+indent+indent,
                                         width=width-len(prefix+indent+indent))
                if len(step_modes) > 0:
                    print(prefix + indent + "Modes:")
                    for x in range(len(step_modes)):
                        self.DisplayMode(x,
                                         codename=False,
                                         prefix=prefix+indent+indent,
                                         width=width-len(prefix+indent+indent))
            modified_powers = [d for d in self.power_dice if stepnum in d.steps_modified and \
                               d not in step_powers]
            modified_qualities = [d for d in self.quality_dice if stepnum in d.steps_modified and \
                                  d not in step_qualities]
            modified_abilities = [a for a in self.abilities if stepnum in a.steps_modified and \
                                  a not in step_abilities]
            any_modified = max([len(modified_powers),
                                len(modified_qualities),
                                len(modified_abilities)])
            if stepnum in self.status_steps_modified:
                any_modified = 1
            if any_modified > 0:
                print(prefix + "Step " + str(stepnum) + " modified:")
                if len(modified_powers) > 0:
                    print(prefix + indent + "Powers:")
                    for d in modified_powers:
                        print(prefix + indent + indent + str(d.RetrievePrior(stepnum+1)))
                if len(modified_qualities) > 0:
                    print(prefix + indent + "Qualities:")
                    for d in modified_qualities:
                        print(prefix + indent + indent + str(d.RetrievePrior(stepnum+1)))
                if stepnum in self.status_steps_modified:
                    print(prefix + indent + "Status:")
                    for x in range(len(self.status_dice)):
                        print(prefix + indent + indent + status_zones[x] + ": " + \
                              str(self.status_dice[x]))
                for z in range(len(status_zones)):
                    modified_zone_abilities = [ab for ab in modified_abilities if ab.zone == z]
                    if len(modified_zone_abilities) > 0:
                        print(prefix + indent + "Abilities (" + status_zones[z] + "):")
                        for a in modified_zone_abilities:
                            a.RetrievePrior(stepnum+1).display(prefix=prefix+indent+indent,
                                                               width=width - \
                                                               len(prefix+indent+indent))
            # ...
        else:
            print(prefix + "Error! " + str(stepnum) + " is not a valid step of hero creation.")
    def DisplaySteps(self, prefix="", width=100):
        # Iterates through DisplayStep for all steps of hero creation
        # No return value
        for i in range(1, len(step_names)):
            self.DisplayStep(i, prefix=prefix, width=width)
    def display(self, prefix="", width=100):
        # Prints a full list of the hero's mechanical attributes: codename, name, Principles,
        #  Powers, Qualities, Status, Health ranges, Abilities, etc.
        # No return value.
        indent = "    "
        if self.hero_name == "":
            print(prefix + "[unnamed hero]")
        else:
            print(prefix + "Hero Name:  " + self.hero_name)
        if self.alias != "":
            print(prefix + "Alias:      " + self.alias)
        bg_text = ps_text = arc_text = pn_text = "[none]"
        if self.background in range(len(bg_collection)):
            bg_text = bg_collection[self.background][0]
        if self.power_source in range(len(ps_collection)):
            ps_text = ps_collection[self.power_source][0]
        if self.archetype in range(len(arc_collection)):
            arc_text = arc_collection[self.archetype][0]
            if self.archetype_modifier > 0 and \
               self.archetype_modifier in range(len(arc_modifiers)):
                arc_text = arc_modifiers[self.archetype_modifier][0] + ":" + arc_text
        if self.personality in range(len(pn_collection)):
            pn_text = pn_collection[self.personality][0]
            if self.dv_personality in range(len(pn_collection)):
                pn_text = pn_collection[self.dv_personality][0] + " (" + self.dv_tags[0] + \
                          ") / " + pn_collection[self.personality][0] + " (" + self.dv_tags[1] + \
                          ")"
        print(prefix + indent + "Background:    " + bg_text)
        print(prefix + indent + "Power Source:  " + ps_text)
        print(prefix + indent + "Archetype:     " + arc_text)
        print(prefix + indent + "Personality:   " + pn_text)
        if len(self.principles) > 0:
            print(prefix + indent + "Principles:")
            for pri in self.principles:
                pri.display(prefix=prefix+indent+indent,
                            width=width-len(prefix+indent+indent),
                            green=False)
        if len(self.power_dice) > 0:
            print(prefix + indent + "Powers:")
            for d in self.power_dice:
                print(prefix + indent + indent + str(d))
        if len(self.quality_dice) > 0:
            print(prefix + indent + "Qualities:")
            for d in self.quality_dice:
                print(prefix + indent + indent + str(d))
        if self.status_dice != [0,0,0]:
            print(prefix + indent + "Status:")
            for i in range(len(self.status_dice)):
                print(prefix + indent + indent + status_zones[i] + ": " + str(self.status_dice[i]))
        if self.health_zones != [0,0,0]:
            print(prefix + indent + "Health:")
            rn = self.HealthRanges()
            for i in range(len(rn)):
                print(prefix + indent + indent + status_zones[i] + " Zone: " + str(rn[i][0]) + \
                      "-" + str(rn[i][1]))
        for z in range(len(status_zones)):
            zone_abilities = self.Abilities(z)
            if len(zone_abilities) > 0:
                print(prefix + indent + "Abilities (" + status_zones[z] + "):")
                for a in zone_abilities:
                    a.display(prefix=prefix+indent+indent,
                              width=width-len(prefix+indent+indent))
        if len(self.min_forms) > 0:
            print(prefix + indent + "Minion Forms:")
            for x in range(len(self.min_forms)):
                printlong(MinionFormStr(self.min_forms[x]),
                          width=width-len(prefix+indent+indent),
                          prefix=prefix+indent+indent)
        if len(self.other_forms) > 0:
            print(prefix + indent + "Forms:")
            # Form-Changer grants 2 Green Forms and 1 Yellow Form, each with 1 Ability
            # Divided grants 2 Green Forms, each with no Abilities
            # To separate the two categories, display Forms with no Abilities before ones with
            #  Abilities
            for x in range(len(self.other_forms)):
                if len(self.other_forms[x][5]) == 0:
                    self.DisplayForm(x,
                                     codename=False,
                                     prefix=prefix+indent+indent,
                                     width=width-len(prefix+indent+indent))
            for x in range(len(self.other_forms)):
                if len(self.other_forms[x][5]) > 0:
                    self.DisplayForm(x,
                                     codename=False,
                                     prefix=prefix+indent+indent,
                                     width=width-len(prefix+indent+indent))
        if len(self.other_modes) > 0:
            print(prefix + indent + "Modes:")
            for x in range(len(self.other_modes)):
                self.DisplayMode(x,
                                 codename=False,
                                 prefix=prefix+indent+indent,
                                 width=width-len(prefix+indent+indent))
    def details(self, prefix="", width=100):
        # Returns a string containing a full list of the hero's mechanical attributes: codename,
        #  name, characteristics, Principles, Powers, Qualities, Status, Health ranges, Abilities,
        #  etc.
        indent = "    "
        notePrefix = "### Hero.details: "
        heroString = ""
        if self.hero_name == "":
            heroString += prefix + "[unnamed hero]"
        else:
            heroString += prefix + "Hero Name:  " + self.hero_name
        if self.alias != "":
            heroString += "\n" + prefix + "Alias:      " + self.alias
        bg_text = ps_text = arc_text = pn_text = "[none]"
##        print(notePrefix + "self.background = " + str(self.background))
        if self.background in range(len(bg_collection)):
            bg_text = bg_collection[self.background][0]
##        print(notePrefix + "self.power_source = " + str(self.power_source))
        if self.power_source in range(len(ps_collection)):
            ps_text = ps_collection[self.power_source][0]
##        print(notePrefix + "self.archetype = " + str(self.archetype))
        if self.archetype in range(len(arc_collection)):
            arc_text = arc_collection[self.archetype][0]
##            print(notePrefix + "self.archetype_modifier = " + str(self.archetype_modifier))
            if self.archetype_modifier > 0 and \
               self.archetype_modifier in range(len(arc_modifiers)):
                arc_text = arc_modifiers[self.archetype_modifier][0] + ":" + arc_text
##        print(notePrefix + "self.personality = " + str(self.personality))
        if self.personality in range(len(pn_collection)):
            pn_text = pn_collection[self.personality][0]
            if self.dv_personality in range(len(pn_collection)):
                pn_text = pn_collection[self.dv_personality][0] + " (" + self.dv_tags[0] + \
                          ") / " + pn_collection[self.personality][0] + " (" + self.dv_tags[1] + \
                          ")"
        heroString += "\n" + prefix + indent + "Background:    " + bg_text
        heroString += "\n" + prefix + indent + "Power Source:  " + ps_text
        heroString += "\n" + prefix + indent + "Archetype:     " + arc_text
        heroString += "\n" + prefix + indent + "Personality:   " + pn_text
        if len(self.principles) > 0:
            heroString += "\n" + prefix + indent + "Principles:"
            for pri in self.principles:
                heroString += "\n" + pri.details(prefix=prefix+indent+indent,
                                                 width=width-len(prefix+indent+indent),
                                                 green=False,
                                                 breaks=1)
        if len(self.power_dice) > 0:
            heroString += "\n" + prefix + indent + "Powers:"
            for d in self.power_dice:
                heroString += "\n" + prefix + indent + indent + str(d)
        if len(self.quality_dice) > 0:
            heroString += "\n" + prefix + indent + "Qualities:"
            for d in self.quality_dice:
                heroString += "\n" + prefix + indent + indent + str(d)
        if self.status_dice != [0,0,0]:
            heroString += "\n" + prefix + indent + "Status:"
            for i in range(len(self.status_dice)):
                heroString += "\n" + prefix + indent + indent + status_zones[i] + ": " + \
                              str(self.status_dice[i])
        if self.health_zones != [0,0,0]:
            heroString += "\n" + prefix + indent + "Health:"
            rn = self.HealthRanges()
            for i in range(len(rn)):
                heroString += "\n" + prefix + indent + indent + status_zones[i] + " Zone: " + \
                              str(rn[i][0]) + "-" + str(rn[i][1])
        for z in range(len(status_zones)):
            zone_abilities = self.Abilities(z)
            if len(zone_abilities) > 0:
                heroString += "\n" + prefix + indent + "Abilities (" + status_zones[z] + "):"
                for a in zone_abilities:
                    heroString += "\n" + a.details(prefix=prefix+indent+indent,
                                                   width=width-len(prefix+indent+indent))
        if len(self.min_forms) > 0:
            heroString += "\n" + prefix + indent + "Minion Forms:"
            for x in range(len(self.min_forms)):
                heroString += "\n" + split_text(MinionFormStr(self.min_forms[x]),
                                                width=width-len(prefix+indent+indent),
                                                prefix=prefix+indent+indent)
        if len(self.other_forms) > 0:
            heroString += "\n" + prefix + indent + "Forms:"
            # Form-Changer grants 2 Green Forms and 1 Yellow Form, each with 1 Ability
            # Divided grants 2 Green Forms, each with no Abilities
            # To separate the two categories, display Forms with no Abilities before ones with
            #  Abilities
            for x in range(len(self.other_forms)):
                if len(self.other_forms[x][5]) == 0:
                    heroString += "\n" + self.FormDetails(x,
                                                          codename=False,
                                                          prefix=prefix+indent+indent,
                                                          width=width-len(prefix+indent+indent))
            for x in range(len(self.other_forms)):
                if len(self.other_forms[x][5]) > 0:
                    heroString += "\n" + self.FormDetails(x,
                                                          codename=False,
                                                          prefix=prefix+indent+indent,
                                                          width=width-len(prefix+indent+indent))
        if len(self.other_modes) > 0:
            heroString += "\n" + prefix + indent + "Modes:"
            for x in range(len(self.other_modes)):
                heroString += "\n" + self.ModeDetails(x,
                                                      codename=False,
                                                      prefix=prefix+indent+indent,
                                                      width=width-len(prefix+indent+indent))
        return heroString
        

# Sample heroes, for testing purposes...
# Shikari is an Interstellar Genetic Flier with no Archetype modifier.
def Create_Shikari():
    shikari = Hero("Shikari", "Shikari Lonestar", 0)
    shikari.CreateHero(health_roll=2,
                       inputs=["b",
                               ["Q"],
                               [[["i",["a"]],["b"]],["K","y","d","What new threat is as prepared for this harsh environment as you are?","f"]],
                               "b",
                               ["C"],
                               [[["o",["a"]],["h",["a"]],["c",[["y","Warskin"]]]],["A","b","y","Advance Tracking"],["A","a","y","Know the Way"],["A","a","y","Warrior's Instinct"]],
                               "b",
                               ["H"],
                               [["a",["b"]],["b",["a"]],"n",[["i"]],["D","y","Watch Your Sprocking Head"],["A","f","y","Coming Through!"],["A","d","y","Follow Me!"],["J","n"]],
                               "b",
                               ["I"],
                               [[["Y","Lone Star Legion"]]],
                               ["F",["D","y","End of the Road"]],
                               ["H",["E","y","Obstacle Avoidance"]],
                               ["g",["C",["D","y","Protective Escort"]]],
                               ["b","b"]])
    print()
    shikari.display()
    return shikari

# Ultra Boy is a Criminal Radiation Modular:Physical Powerhouse.
def Create_Ultra_Boy():
    jo = Hero("Ultra Boy", "Jo Nah", 1)
    jo.CreateHero(health_roll=6,
                  inputs=["b",
                          ["L"],
                          [[["a",["a"]],["c"]],["L","n"]],
                          "b",
                          ["I"],
                          [[["a"],["a",[["y","Legion Flight Ring"]]],["e"]],["C","b","y","Yoink!"],["A","b","y","That Tickles"],["C","a","y","Zap!"]],
                          "b",
                          ["T","C"],
                          [["a"],["f",["b"]],[["f"]],
                           ["f","y","I'm On It"],
                           ["y","'Scuse Me"],
                           ["y","Now I'm Mad"],
                           "n",
                           "A",
                           ["a","b","c","a",["c","y","Who Let You Play With These?"],"y","Ultra Speed"],
                           "D",
                           ["b","c","a","b",["c","y","Sprock These Two In Particular"],"y","Flash Vision"],
                           "D",
                           ["d","a","a","a",["d","y","Everybody Behind Me!"],"y","Ultra Invulnerability"],
                           "B",
                           ["d","b",["a","y","Was That Important?"],"y","Ultra Strength"],
                           ["D","n"]],
                          "b",
                          ["O"],
                          [[["y","Gangster Made Good"]],["c"]],
                          ["F",["C","y","Ring-Sling"]],
                          ["A",["A","y","Street Smarts"]],
                          ["e"],
                          ["b","b"]])
    print()
    jo.display()
    return jo

# Chameleon is an Interstellar Alien Form-Changer with no Archetype modifier.
def Create_Chameleon():
    cham = Hero("Chameleon", "Reep Daggle", 1)
    cham.CreateHero(inputs=["b",
                            ["Q"],
                            [[["k",["a"]],["k"]],["D", "n"]],
                            "b",
                            ["N"],
                            [[["a","p",["a"]],["a","a",["b", ["y","Legion Flight Ring"]]],["a","b"]],["C","c","y","Slippery"],["A","a","y","Excellent Listener"],"b"],
                            "b",
                            ["P"],
                            [["h"],
                             ["n"],
                             "n",
                             [["n"]],
                             ["a","n"],
                             ["y","Improvise"],
                             ["B", "a", "y", "Distracting Strike"],
                             ["C","a","a","b","a","b","e","b","e","b","d",["e","y","Natural Weaponry"],"y","Beast Form"],
                             ["D","a","b","e","b","e","q","d",["a","y","Critical Discovery"],"y","Stealth Form"],
                             ["G","a","a","d","a","b","e","b","e","l","d","d","a",["d","y","Who Do You Think I Am!?"],"y","Imitation Form"],
                             ["K","n"]],
                            "b",
                            ["O"],
                            [[["y","Frontline Ambassador"]],["a"]],
                            ["A",["B","a","y","Lateral Thinking"]],
                            ["F",["B","a","y","Change for the Better"]],
                            ["f","c",["E","n",["B"]]],
                            ["b","a"]])
    print()
    cham.display()
    return cham

# Lori Morning is an Anachronistic Relic Divided:Form-Changer who uses Divided Psyche.
def Create_Future_Girl():
    lori = Hero("Future Girl", "Lori Morning", 0)
    lori.CreateHero(health_roll=1, inputs=["b",
                                           ["N"],
                                           [[["C",["A"]],["H"]],["L","N"]],
                                           "b",
                                           ["G"],
                                           [[["A","D",["A",["Y","HERO Dial"]]],["A","E",["A"]],["A","B"]],["B","C","Y","Natural Heroism"],["B","B","Y","Synthetic Power"],["A","A","Y","One-Hour Superpower"]],
                                           "b",
                                           ["S","P"],
                                           [["H",["A"]],
                                            ["T",["A"]],
                                            "N",
                                            [["C"]],
                                            ["y","Redial"],
                                            ["y","Dial ICE"],
                                            ["B","Y","Collect Call"],
                                            ["A","a","c","d","a","a","b","b","b","b","b","e","i","d",["b","y","Where Was I?"],"y","Mobile Hero","B"],
                                            ["D","a","a","c","a","c","b","b","b","o","b","e","q","d",["b","y","Wrap It Up"],"y","Capture Hero","C"],
                                            ["B","a","a","b","a","c","d","b","e","c","b","c","c","d","e","c",["e","y","Lights Out"],"y","Powerhouse Hero","B"],
                                            "N",
                                            "B",
                                            ["y","Dial H for Hero"],
                                            "A",
                                            ["Y","Unlisted Numbers"],
                                            "B",
                                            ["H","n"]],
                                           "b",
                                           ["N","D"],
                                           [[["Y","Future Girl"]],["e"]],
                                           ["B",["B","Y","Please Hold"]],
                                           ["F",["A","Y","Wrong Number"]],
                                           ["e"],
                                           ["a","b"]])
    print()
    lori.display()
    return lori

# Knockout (credit to NovaSpark#2117) is a Medical Alien Divided:Robot/Cyborg who uses Split Form.
def Create_Knockout():
    knockout = Hero("Knockout", "n/a", 1)
    knockout.CreateHero(inputs=["b",
                                ["M"],
                                [["b"],[["b",["a"]],["f"]],["E","n"]],
                                "b",
                                ["N"],
                                [[["a","b",["b",["y","Doctor's Tools"]]],["a","a",["a",["y","Aston Martin"]]],["b","l"]],["B","c","y","Field Treatment"],["B","b","y","Watch the Paint!"]],
                                "b",
                                ["S","J"],
                                [["a","a"],"y",["h"],"n",[["b"]],["D","e","y","Touch Up"],["D","b","y","12-Car Pileup"],["C","a","y",'Say "Ahh!"'],["b"],"y","Vehicle","Robot","B",["y","Robot in Disguise"],"B","D","D","D","B","B","A","B","B","B","B",["H","n"]],
                                "b",
                                ["N","T"],
                                [[["Y","Mad Doctor"]],["e"]],
                                ["D",["C","y","Peel Out"]],
                                ["D",["A","y","Anesthetic"]],
                                ["g",["C",["C","y","You Scratch My Paint, I Scratch Yours"]]],
                                ["c","a"]])
    print()
    knockout.display()
    return knockout

# The second Architect is a Dynasty Relic Minion-Maker with no Archetype modifier.
def Create_Architect():
    kim = Hero("The Architect", "Kimberly Harris", 0)
    kim.CreateHero(health_roll=6,
                   inputs=["B",
                           ["R"],
                           [[["b"],["b"]],["K","n"]],
                           "B",
                           ["E"],
                           [[["a","a",["a"]],["a","a",["a"]],["a","y"]],["A","a","y","Environmental Planning"],["B","b","y","Aerial Survey"],["c"]],
                           "B",
                           ["N"],
                           [["Q",["a"]],"n",[["i"],["g"]],["d","y","Concept Art"],["a","y","Detailing"],["C","d","y","Revision"],"C","a","a","a","a","a","a","a","a","a","a",["F","y","E","Overcome by applying your knowledge of the workings and limitations of your powers. Use your Max die. You and each of your allies gain a hero point.","F"]],
                           "B",
                           ["M"],
                           [[["Y", "Super Mom"]]],
                           ["H",["A","D","y","Economy of Scale"]],
                           ["E",["A","y","Blot Out"]],
                           ["G",["G",["F","y","Constructive Criticism"]]],
                           ["A","B"]])
    print()
    kim.display()
    return kim

# Spark is an Unremarkable Accident Blaster who uses some element/energy-limited Abilities.
def Create_Spark():
    spark = Hero("Spark", "Ayla Ranzz", 0)
    spark.CreateHero(health_roll=7,
                     inputs=["b",
                             ["E"],
                             [[["i",["b"]],["d"]],["e","E","n"]],
                             "b",
                             ["a","A"],
                             [[["b","g",["a"]],["a","r",["a"]],["a","a"]],["A","a","b","y","Charge!"],["A","c","y","Made You Look"],["B","a","y","Electric Atmosphere"]],
                             "b",
                             ["E"],
                             [["c",["a"]],["j"],["D","b","y","Thread the Needle"],["C","a","y","Enough for Everyone"],["B","d","y","Complete Circuit"],["A","y","No Fear"],["B","y","a","Lightning","b","You have an affinity for electricity. You can interact with the lightning with ease.","e","Overcome a challenge involving Electricity. Use your Max die. You and each of your allies gain a hero point.","f"]],
                             "b",
                             ["P"],
                             [[["Y","Bright Lights"]],["d"]],
                             ["D",["A","y","Finishing Strike"]],
                             ["G",["B","y","Living Battery"]],
                             ["G",["A",["B","y","Struck by Inspiration"]]],
                             ["b","b"]])
    print()
    spark.display()
    return spark

class SampleMaker:
    def __init__(self):
        self.shikari = None
        self.jo = None
        self.cham = None
        self.lori = None
        self.knockout = None
        self.kim = None
        self.ayla = None
        self.codenames = ["Shikari",
                          "Ultra Boy",
                          "Chameleon",
                          "Future Girl",
                          "Knockout",
                          "The Architect",
                          "Spark"]
    def getShikari(self):
        if self.shikari == None:
            self.shikari = Create_Shikari()
        return self.shikari
    def getJo(self):
        if self.jo == None:
            self.jo = Create_Ultra_Boy()
        return self.jo
    def getCham(self):
        if self.cham == None:
            self.cham = Create_Chameleon()
        return self.cham
    def getLori(self):
        if self.lori == None:
            self.lori = Create_Future_Girl()
        return self.lori
    def getKnockout(self):
        if self.knockout == None:
            self.knockout = Create_Knockout()
        return self.knockout
    def getKim(self):
        if self.kim == None:
            self.kim = Create_Architect()
        return self.kim
    def getAyla(self):
        if self.ayla == None:
            self.ayla = Create_Spark()
        return self.ayla
        
class SampleGUI:
    def __init__(self, parent):
        self.myParent = parent
        self = Frame(parent)
        self.pack()

        self.shikari_button = Button(self,
                                     text="Shikari",
                                     command=Create_Shikari)
        self.shikari_button.pack(side=LEFT)

        self.ultra_boy_button = Button(self,
                                       text="Ultra Boy",
                                       command=Create_Ultra_Boy)
        self.ultra_boy_button.pack(side=LEFT)

        self.chameleon_button = Button(self,
                                       text="Chameleon",
                                       command=Create_Chameleon)
        self.chameleon_button.pack(side=LEFT)

        self.future_girl_button = Button(self,
                                         text="Future Girl",
                                         command=Create_Future_Girl)
        self.future_girl_button.pack(side=LEFT)

        self.knockout_button = Button(self,
                                      text="Knockout",
                                      command=Create_Knockout)
        self.knockout_button.pack(side=LEFT)

        self.architect_button = Button(self,
                                       text="The Architect II",
                                       command=Create_Architect)
        self.architect_button.pack(side=LEFT)

        self.spark_button = Button(self,
                                   text="Spark",
                                   command=Create_Spark)
        self.spark_button.pack(side=LEFT)

class HeroFrame(Frame):
    # A container displaying all the mechanical information about a Hero.
    def __init__(self, parent, hero=None, width=160, height=52):
        Frame.__init__(self, parent)
        notePrefix = "HeroFrame: "
        self.zoneColors = ["PaleGreen1", "LightGoldenrod1", "IndianRed1"]
        self.myParent = parent
        self.numCols = 32
        self.numRows = 52
        self.width = width
        self.height = height
        self.columnWidth = max(1, math.floor(self.width/self.numCols))
        self.rowHeight = max(1, math.floor(self.height/self.numRows))
##        print(notePrefix + "width=" + str(self.width))
##        print(notePrefix + "columnWidth=" + str(self.columnWidth))
##        print(notePrefix + "height=" + str(self.height))
##        print(notePrefix + "rowHeight=" + str(self.rowHeight))
        self.SetHero(hero)
        titleRelief = RAISED
        # Set up Hero Name and Alias labels spanning rows 1-2
        self.nameTitles = [None, None]
        self.nameValues = [None, None]
        self.nameTitleText = ["Hero Name:", "Alias:"]
        firstRow = 1
        firstCol = 1
        groupWidth = 8
        groupHeight = 2
        for i in range(len(self.nameTitles)):
            self.nameTitles[i] = Label(self,
                                       background="orange",
                                       text=self.nameTitleText[i],
                                       anchor=W, relief=titleRelief,
                                       width=self.columnWidth*groupWidth,
                                       height=self.rowHeight*groupHeight)
            self.nameValues[i] = Label(self,
                                       background="white",
                                       anchor=W,
                                       width=self.columnWidth*groupWidth,
                                       height=self.rowHeight*groupHeight)
            self.nameTitles[i].grid(row=firstRow,
                                    column=firstCol+i*2*groupWidth,
                                    rowspan=groupHeight,
                                    columnspan=groupWidth,
                                    sticky=E+W)
            self.nameValues[i].grid(row=firstRow,
                                    column=firstCol+(i*2+1)*groupWidth,
                                    rowspan=groupHeight,
                                    columnspan=groupWidth,
                                    sticky=E+W)
        # Set up hero Characteristic labels for the left half of rows 3-6
        self.charTitleText = ["Background:", "Power Source:", "Archetype:", "Personality:"]
        self.charTitles = [None for i in range(4)]
        self.charValues = [None for i in range(4)]
        firstRow += groupHeight
        firstCol = 1
        titleWidth = 3
        valueWidth = 5
        groupHeight = 2
        charRelief = GROOVE
        glue = N+E+S+W
        for i in range(len(self.charTitles)):
            self.charTitles[i] = Label(self,
                                       background="orange",
                                       text=self.charTitleText[i],
                                       anchor=W,
                                       relief=titleRelief,
                                       width=self.columnWidth*titleWidth,
                                       height=self.rowHeight*groupHeight)
            self.charValues[i] = Label(self,
                                       background="white",
                                       anchor=W,
                                       relief=charRelief,
                                       width=self.columnWidth*valueWidth,
                                       height=self.rowHeight*groupHeight)
##            print(notePrefix + str(self.charTitleText[i]) + " label starts at row " + \
##                  str(firstRow+math.floor(i/2)*groupHeight) + " and spans " + str(groupHeight) + \
##                  " rows")
            self.charTitles[i].grid(row=firstRow+math.floor(i/2)*groupHeight,
                                    column=firstCol+(i%2)*(titleWidth+valueWidth),
                                    rowspan=groupHeight,
                                    columnspan=titleWidth,
                                    sticky=glue)
            self.charValues[i].grid(row=firstRow+math.floor(i/2)*groupHeight,
                                    column=firstCol+titleWidth+(i%2)*(titleWidth+valueWidth),
                                    rowspan=groupHeight,
                                    columnspan=valueWidth,
                                    sticky=glue)
        # Left half of row 7 deliberately left blank
        # Set up Power and Quality labels for the first 10 columns of rows 8-25
        self.pqTitles = [None for i in range(4)]
        self.pqValues = [[None for i in range(4)] for i in range(len(self.myHeroPowers))]
        self.pqTitleText = ["Powers", "Die", "Qualities", "Die"]
        pqRelief = GROOVE
        sectionWidths = [4, 1]
        pqDiceValues = [["" for a in range(len(self.pqTitles))] \
                        for a in range(len(self.myHeroPowers))]
        firstRow = 8
        firstCol = 1
        sectionTargets = [W, CENTER]
        sectionReasons = [LEFT, CENTER]
        groupHeight = 2
        for i in range(len(self.pqTitles)):
            groupWidth = sectionWidths[i%2]
            groupCol = firstCol + (i%2)*sectionWidths[0] + math.floor(i/2)*sum(sectionWidths)
            target = sectionTargets[i%2]
            reason = sectionReasons[i%2]
            self.pqTitles[i] = Label(self,
                                     background="orange",
                                     text=self.pqTitleText[i],
                                     anchor=target,
                                     justify=reason,
                                     relief=titleRelief,
                                     width=self.columnWidth*groupWidth,
                                     height=self.rowHeight*groupHeight)
            self.pqTitles[i].grid(row=firstRow,
                                  column=groupCol,
                                  rowspan=groupHeight,
                                  columnspan=groupWidth,
                                  sticky=E+W)
            for j in range(len(pqDiceValues)):
                self.pqValues[j][i] = Label(self,
                                            background="white",
                                            anchor=target,
                                            justify=reason,
                                            relief=pqRelief,
                                            width=self.columnWidth*groupWidth,
                                            height=self.rowHeight*groupHeight)
                self.pqValues[j][i].grid(row=firstRow+(j+1)*groupHeight,
                                         column=groupCol,
                                         rowspan=groupHeight,
                                         columnspan=groupWidth,
                                         sticky=N+S+E+W)
        # EDIT: Set up hero Status die labels for columns 11-13 of rows 8-25
        titleRow = 8
        firstCol = 11
        groupWidth = 3
        titleHeight = 2
        statusRelief = SUNKEN
        statusBG = "gray80"
        self.statusTitle = Label(self,
                                 background=statusBG,
                                 text="Status Dice",
                                 width=self.columnWidth*groupWidth,
                                 height=self.rowHeight*titleHeight)
        self.statusTitle.grid(row=titleRow,
                              column=firstCol,
                              rowspan=titleHeight,
                              columnspan=groupWidth,
                              sticky=N+E+W)
        self.statusValues = [None for i in range(3)]
        firstRow = titleRow + titleHeight + 1
        groupHeight = 5
        for i in range(len(self.statusValues)):
            self.statusValues[i] = Label(self,
                                         background=self.zoneColors[i],
                                         relief=statusRelief,
                                         width=self.columnWidth*groupWidth,
                                         height=self.rowHeight*groupHeight)
            self.statusValues[i].grid(row=firstRow+i*groupHeight,
                                      column=firstCol,
                                      rowspan=groupHeight,
                                      columnspan=groupWidth,
                                      sticky=N+E+S+W)
        # Set up hero Health labels in columns 15-16 of rows 8-25
        titleRow = 8
        titleCol = 15
        titleWidth = 2
        titleHeight = 2
        self.healthTitle = Label(self,
                                 background=statusBG,
                                 text="Health Range",
                                 anchor=E,
                                 width=self.columnWidth*titleWidth,
                                 height=self.rowHeight*titleHeight)
        self.healthTitle.grid(row=titleRow,
                              column=titleCol,
                              rowspan=titleHeight,
                              columnspan=titleWidth,
                              sticky=N+E+W)
        self.healthValues = [None for i in range(3)]
        firstRow = titleRow + titleHeight + 1
        firstCol = 15
        groupWidth = 2
        groupHeight = 3
        groupVSpace = 5
        for i in range(len(self.healthValues)):
            self.healthValues[i] = Label(self,
                                         background=self.zoneColors[i],
                                         relief=statusRelief,
                                         width=self.columnWidth*groupWidth,
                                         height=self.rowHeight*groupHeight)
            self.healthValues[i].grid(row=firstRow+i*groupVSpace,
                                      column=firstCol,
                                      rowspan=groupHeight,
                                      columnspan=groupWidth,
                                      sticky=N+E+S+W)
        # Left half of row 26 intentionally left blank
        # Set up hero Principle labels in left half of rows 27-52
        self.prinSectionNames = ["During Roleplaying", "Minor Twist", "Major Twist"]
        self.prinTitles = [None for i in range(len(self.myHeroPrinciples))]
        self.prinSectionTitles = [[None for i in range(len(self.prinSectionNames))] \
                                  for i in range(len(self.myHeroPrinciples))]
        self.prinSectionValues = [[None for i in range(len(self.prinSectionNames))] \
                                  for i in range(len(self.myHeroPrinciples))]
        firstRow = 27
        firstCol = 1
        groupWidth = 8
        titleWidth = 6
        titleHeight = 1
        mainTitleHeight = 2
        sectionHeight = 4
        sectionRelief = GROOVE
        sectionWrap = math.floor(self.columnWidth*groupWidth*1.25)
        self.principleWrap = sectionWrap
        for i in range(len(self.myHeroPrinciples)):
            groupCol = firstCol+i*groupWidth
            self.prinTitles[i] = Label(self,
                                       background="orange",
                                       text="Principle of ",
                                       anchor=W,
                                       relief=titleRelief,
                                       width=self.columnWidth*titleWidth,
                                       height=self.rowHeight*mainTitleHeight)
            self.prinTitles[i].grid(row=firstRow,
                                    column=groupCol,
                                    rowspan=mainTitleHeight,
                                    columnspan=titleWidth,
                                    sticky=N+E+S+W)
            for j in range(len(self.prinSectionTitles[i])):
                titleRow = firstRow + mainTitleHeight + j*(titleHeight + sectionHeight)
                sectionRow = titleRow + titleHeight
                self.prinSectionTitles[i][j] = Label(self,
                                                     background="white",
                                                     text=self.prinSectionNames[j],
                                                     relief=sectionRelief,
                                                     width=self.columnWidth*groupWidth,
                                                     height=self.rowHeight*titleHeight)
                self.prinSectionTitles[i][j].grid(row=titleRow,
                                                  column=groupCol,
                                                  rowspan=titleHeight,
                                                  columnspan=groupWidth,
                                                  sticky=N+E+S+W)
                self.prinSectionValues[i][j] = Label(self,
                                                     background="white",
                                                     width=self.columnWidth*groupWidth,
                                                     height=self.rowHeight*sectionHeight)
                self.prinSectionValues[i][j].grid(row=sectionRow,
                                                  column=groupCol,
                                                  rowspan=sectionHeight,
                                                  columnspan=groupWidth,
                                                  sticky=N+E+S+W)
        # EDIT: Set up hero Ability labels in the right half of rows 3-52
        self.abilityTitles = [None for i in range(3)]
        self.abilityTitleText = ["Name", "Type", "Text"]
        self.prinAbilityValues = [[None for i in range(3)] for j in range(len(self.myPrinAbilities))]
        self.zoneAbilityValues = [[[None for i in range(3)] \
                                   for j in range(len(self.myZoneAbilities[k]))] \
                                  for k in range(len(self.myZoneAbilities))]
        self.outAbilityValue = None
        firstRow = 3
        firstCol = 17
        sectionWidths = [4, 2, 10]
        sectionAnchors = [E, CENTER, W]
        sectionReasons = [RIGHT, CENTER, LEFT]
        titleHeight = 1
        abilityRelief = GROOVE
        for i in range(len(self.abilityTitleText)):
            self.abilityTitles[i] = Label(self,
                                          background="orange",
                                          text=self.abilityTitleText[i],
                                          anchor=sectionAnchors[i],
                                          relief=titleRelief,
                                          width=self.columnWidth*sectionWidths[i],
                                          height=self.rowHeight*titleHeight)
##            print(notePrefix + str(self.abilityTitleText[i]) + " label starts at row " + \
##                  str(firstRow) + " and spans " + str(titleHeight) + " rows")
            self.abilityTitles[i].grid(row=firstRow,
                                       column=firstCol+sum(sectionWidths[:i]),
                                       rowspan=titleHeight,
                                       columnspan=sectionWidths[i])
        # Principle Abilities start after Green Abilities
        greenRows = 0
        abilityMultiplier = 1.2
        self.abilityWraps = [math.floor(a*abilityMultiplier*self.columnWidth) \
                             for a in sectionWidths]
        greenRows = len(self.myZoneAbilities[0])
##        print("Total rows in Green Abilities: " + str(greenRows))
        prinRow = firstRow + titleHeight + greenRows
        thisRow = prinRow
        prinHeight = 0
        for i in range(len(self.myPrinAbilities)):
            rowsNeeded = 1
            for j in range(len(self.abilityTitleText)):
                self.prinAbilityValues[i][j] = Label(self,
                                                     background=self.zoneColors[0],
                                                     anchor=sectionAnchors[j],
                                                     justify=sectionReasons[j],
                                                     relief=abilityRelief,
                                                     width=self.columnWidth*sectionWidths[j],
                                                     height=self.rowHeight*rowsNeeded)
                self.prinAbilityValues[i][j].grid(row=thisRow,
                                                  column=firstCol+sum(sectionWidths[:j]),
                                                  rowspan=rowsNeeded,
                                                  columnspan=sectionWidths[j],
                                                  sticky=N+S+E+W)
            thisRow += rowsNeeded
            prinHeight += rowsNeeded
        firstRows = [5, 26, 38]
        thisRow = firstRow + titleHeight
        for z in range(len(self.myZoneAbilities)):
            if z == 1:
                thisRow = prinRow + prinHeight
            for a in range(len(self.myZoneAbilities[z])):
                rowsNeeded = 1
                for s in range(len(self.zoneAbilityValues[z][a])):
                    self.zoneAbilityValues[z][a][s] = Label(self,
                                                            background=self.zoneColors[z],
                                                            anchor=sectionAnchors[s],
                                                            justify=sectionReasons[s],
                                                            relief=abilityRelief,
                                                            width=self.columnWidth*sectionWidths[s],
                                                            height=self.rowHeight*rowsNeeded)
                    self.zoneAbilityValues[z][a][s].grid(row=thisRow,
                                                         column=firstCol+sum(sectionWidths[:s]),
                                                         rowspan=rowsNeeded,
                                                         columnspan=sectionWidths[s],
                                                         sticky=N+S+E+W)
                thisRow += rowsNeeded
        rowsNeeded = 1
        self.outAbilityValue = Label(self,
                                     background="gray50",
                                     anchor=W,
                                     justify=LEFT,
                                     width=self.columnWidth*sum(sectionWidths),
                                     height=rowsNeeded)
        self.outAbilityValue.grid(row=thisRow,
                                  column=firstCol,
                                  rowspan=rowsNeeded,
                                  columnspan=sum(sectionWidths),
                                  sticky=N+E+S+W)
        self.reliefOptions = [SUNKEN, RAISED, GROOVE, RIDGE, FLAT]
        self.reliefIndex = 4
        buttonColumn = 33
        firstButtonRow = 8
        prevButtons = 0
        self.buttonWidth = 4
        self.buttonHeight = 2
        self.stepAnchor = W
        self.stepReason = LEFT
        self.modeButton = Button(self,
                                 text="Modes ("+str(self.myModeCount)+")",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=self.LaunchModeWindow)
        self.modeButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=buttonColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        prevButtons += 1
        if self.myModeCount == 0:
            self.modeButton.grid_remove()
        self.formButton = Button(self,
                                 text="Forms ("+str(self.myFormCount)+")",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=self.LaunchFormWindow)
        self.formButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=buttonColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        prevButtons += 1
        if self.myFormCount == 0:
            self.formButton.grid_remove()
        self.minionButton = Button(self,
                                 text="Minions ("+str(self.myMinionCount)+")",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=self.LaunchMinionWindow)
        self.minionButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=buttonColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        prevButtons += 1
        if self.myMinionCount == 0:
            self.minionButton.grid_remove()
        self.nameButton = Button(self,
                                 anchor=self.stepAnchor,
                                 justify=self.stepReason,
                                 text="0. Edit Names",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=self.AddHeroNames)
        self.nameButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=buttonColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        prevButtons += 1
        self.backgroundButton = Button(self,
                                       anchor=self.stepAnchor,
                                       justify=self.stepReason,
                                       text="1. Add Background",
                                       width=self.columnWidth*self.buttonWidth,
                                       height=self.rowHeight*self.buttonHeight,
                                       command=self.AddHeroBackground)
        self.backgroundButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                   column=buttonColumn,
                                   rowspan=self.buttonHeight,
                                   columnspan=self.buttonWidth)
        prevButtons += 1
        self.powerSourceButton = Button(self,
                                        anchor=self.stepAnchor,
                                        justify=self.stepReason,
                                        text="2. Add Power Source",
                                        width=self.columnWidth*self.buttonWidth,
                                        height=self.rowHeight*self.buttonHeight,
                                        command=self.AddHeroPowerSource)
        self.powerSourceButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                    column=buttonColumn,
                                    rowspan=self.buttonHeight,
                                    columnspan=self.buttonWidth)
        prevButtons += 1
        self.archetypeButton = Button(self,
                                      anchor=self.stepAnchor,
                                      justify=self.stepReason,
                                      text="3. Add Archetype",
                                      width=self.columnWidth*self.buttonWidth,
                                      height=self.rowHeight*self.buttonHeight,
                                      command=self.AddHeroArchetype)
        self.archetypeButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                  column=buttonColumn,
                                  rowspan=self.buttonHeight,
                                  columnspan=self.buttonWidth)
        prevButtons += 1
        self.personalityButton = Button(self,
                                        anchor=self.stepAnchor,
                                        justify=self.stepReason,
                                        text="4. Add Personality",
                                        width=self.columnWidth*self.buttonWidth,
                                        height=self.rowHeight*self.buttonHeight,
                                        command=self.AddHeroPersonality)
        self.personalityButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                    column=buttonColumn,
                                    rowspan=self.buttonHeight,
                                    columnspan=self.buttonWidth)
        prevButtons += 1
        self.redAbilityButton = Button(self,
                                       anchor=self.stepAnchor,
                                       justify=self.stepReason,
                                       text="5. Add Red Abilities",
                                       width=self.columnWidth*self.buttonWidth,
                                       height=self.rowHeight*self.buttonHeight,
                                       command=self.AddHeroRedAbilities)
        self.redAbilityButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                   column=buttonColumn,
                                   rowspan=self.buttonHeight,
                                   columnspan=self.buttonWidth)
        prevButtons += 1
        self.retconButton = Button(self,
                                   anchor=self.stepAnchor,
                                   justify=self.stepReason,
                                   text="6. Retcon",
                                   width=self.columnWidth*self.buttonWidth,
                                   height=self.rowHeight*self.buttonHeight,
                                   command=self.AddHeroRetcon)
        self.retconButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                               column=buttonColumn,
                               rowspan=self.buttonHeight,
                               columnspan=self.buttonWidth)
        prevButtons += 1
        self.healthButton = Button(self,
                                   anchor=self.stepAnchor,
                                   justify=self.stepReason,
                                   text="7. Health",
                                   width=self.columnWidth*self.buttonWidth,
                                   height=self.rowHeight*self.buttonHeight,
                                   command=self.AddHeroHealth)
        self.healthButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                               column=buttonColumn,
                               rowspan=self.buttonHeight,
                               columnspan=self.buttonWidth)
        prevButtons += 1
        self.printButton = Button(self,
                                  text="Display Text",
                                  width=self.columnWidth*self.buttonWidth,
                                  height=self.rowHeight*self.buttonHeight,
                                  command=lambda arg1=-1 : \
                                  print(self.myHero.details(width=arg1)))
        self.printButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                              column=buttonColumn,
                              rowspan=self.buttonHeight,
                              columnspan=self.buttonWidth)
        prevButtons += 1
        self.stepsButton = Button(self,
                                  text="Display Steps",
                                  width=self.columnWidth*self.buttonWidth,
                                  height=self.rowHeight*self.buttonHeight,
                                  command=self.DisplayHeroSteps)
        self.stepsButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                              column=buttonColumn,
                              rowspan=self.buttonHeight,
                              columnspan=self.buttonWidth)
        prevButtons += 1
        self.saveButton = Button(self,
                                 text="Save as TXT",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=self.SaveTxt)
        self.saveButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=buttonColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        # Hide all creation step buttons by default
        self.backgroundButton.grid_remove()
        self.powerSourceButton.grid_remove()
        self.archetypeButton.grid_remove()
        self.personalityButton.grid_remove()
        self.redAbilityButton.grid_remove()
        self.retconButton.grid_remove()
        self.healthButton.grid_remove()
        if isinstance(self.myHero, Hero):
            # Display ONLY the button for the first hero creation step that ISN'T complete for this
            #  hero
            rs_abilities = [a for a in self.myHero.abilities if a.step == 5]
            self.completeSteps = [self.myHero.background in range(len(bg_collection)),
                                  self.myHero.power_source in range(len(ps_collection)),
                                  self.myHero.archetype in range(len(arc_collection)),
                                  self.myHero.personality in range(len(pn_collection)),
                                  len(rs_abilities) > 1,
                                  self.myHero.used_retcon,
                                  self.myHero.health_zones != [0,0,0]]
            self.firstIncomplete = 99
            if False in self.completeSteps:
                self.firstIncomplete = self.completeSteps.index(False)
            if self.firstIncomplete == 0:
                self.backgroundButton.grid()
            elif self.firstIncomplete == 1:
                self.powerSourceButton.grid()
            elif self.firstIncomplete == 2:
                self.archetypeButton.grid()
            elif self.firstIncomplete == 3:
                self.personalityButton.grid()
            elif self.firstIncomplete == 4:
                self.redAbilityButton.grid()
            elif self.firstIncomplete == 5:
                self.retconButton.grid()
            elif self.firstIncomplete == 6:
                self.healthButton.grid()
        # ...
        toolboxColumn = buttonColumn + self.buttonWidth
        prevButtons = 0
##        # Button for updating relief option (for design purposes)
##        self.reliefButton = Button(self,
##                                   text=str(self.reliefOptions[self.reliefIndex]),
##                                   width=self.columnWidth*self.buttonWidth,
##                                   height=self.rowHeight*self.buttonHeight,
##                                   command=self.UpdateRelief)
##        self.reliefButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
##                               column=toolboxColumn,
##                               rowspan=self.buttonHeight,
##                               columnspan=self.buttonWidth)
##        prevButtons += 1
##        # Button for modifying wrap length in ability Text labels (for design purposes)
##        self.wrapButton = Button(self,
##                                 text=str(self.principleWrap),
##                                 width=self.columnWidth*self.buttonWidth,
##                                 height=self.rowHeight*self.buttonHeight,
##                                 command=self.UpdateWrap)
##        self.wrapButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
##                             column=toolboxColumn,
##                             rowspan=self.buttonHeight,
##                             columnspan=self.buttonWidth)
##        prevButtons += 1
        # Button for switching to another hero (for testing purposes)
        self.forwardButton = Button(self,
                                    text="Next Hero >>",
                                    width=self.columnWidth*self.buttonWidth,
                                    height=self.rowHeight*self.buttonHeight,
                                    command=self.SwitchHero)
        self.forwardButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                                column=toolboxColumn,
                                rowspan=self.buttonHeight,
                                columnspan=self.buttonWidth)
        prevButtons += 1
        self.backButton = Button(self,
                                 text="<< Prev Hero",
                                 width=self.columnWidth*self.buttonWidth,
                                 height=self.rowHeight*self.buttonHeight,
                                 command=lambda arg1=-1 : self.SwitchHero(arg1))
        self.backButton.grid(row=firstButtonRow+self.buttonHeight*prevButtons,
                             column=toolboxColumn,
                             rowspan=self.buttonHeight,
                             columnspan=self.buttonWidth)
        prevButtons += 1
        self.sampleIndex = -1
        if self.myHeroNames[0] in factory.codenames:
            self.sampleIndex = factory.codenames.index(self.myHeroNames[0])
        self.UpdateAll(hero)
    def RangeText(self, zone):
        # Returns the text representation of the health range for the specified status zone if legal
        #  and valid, and "" otherwise
        t = ""
        if zone in range(len(self.myHeroHealth)):
            z_max = self.myHeroHealth[zone]
            z_min = 1
            if zone + 1 in range(len(self.myHeroHealth)):
                z_min = self.myHeroHealth[zone+1] + 1
            if z_max > z_min:
                t = str(z_max) + "-" + str(z_min)
        return t
    def UpdateRelief(self):
        self.reliefIndex = (self.reliefIndex+1)%len(self.reliefOptions)
        newRelief = self.reliefOptions[self.reliefIndex]
        for i in range(len(self.prinSectionValues)):
            for j in range(len(self.prinSectionValues[i])):
                self.prinSectionValues[i][j].config(relief=newRelief)
                self.prinSectionValues[i][j].update_idletasks()
        self.reliefButton.config(text=str(newRelief))
    def UpdateWrap(self):
        self.principleWrap += 5
        for i in range(len(self.prinSectionValues)):
            for j in range(len(self.prinSectionValues[i])):
                flatText = self.prinSectionValues[i][j]["text"].replace("\n", " ")
                newSplit = split_text(flatText, width=self.principleWrap)
                self.prinSectionValues[i][j]["text"] = newSplit
                self.prinSectionValues[i][j].update_idletasks()
        self.wrapButton["text"] = str(self.principleWrap)
        self.wrapButton.update_idletasks()
    def SwitchHero(self, update=1):
        if self.myHeroNames[0] == "Spark":
            self.UpdateAll(factory.getKim())
        else:
            self.UpdateAll(factory.getAyla())
        # Shikari, Jo, Cham, Lori, Knockout, Kim, Ayla
        self.sampleIndex = (self.sampleIndex + update) % 7
        if self.sampleIndex == 0:
            self.UpdateAll(factory.getShikari())
        elif self.sampleIndex == 1:
            self.UpdateAll(factory.getJo())
        elif self.sampleIndex == 2:
            self.UpdateAll(factory.getCham())
        elif self.sampleIndex == 3:
            self.UpdateAll(factory.getLori())
        elif self.sampleIndex == 4:
            self.UpdateAll(factory.getKnockout())
        elif self.sampleIndex == 5:
            self.UpdateAll(factory.getKim())
        elif self.sampleIndex == 6:
            self.UpdateAll(factory.getAyla())
    def Empty(self):
        # Clears all hero attributes
        self.myHero = None
        self.myHeroNames = ["", ""]
        self.myHeroChars = ["" for i in range(4)]
        self.myHeroPowers = [None for i in range(8)]
        self.myHeroQualities = [None for i in range(8)]
        self.myHeroStatus = [0,0,0]
        self.myHeroHealth = [0,0,0]
        self.myHeroPrinciples = [None for i in range(2)]
        self.myPrinAbilities = [None for i in range(2)]
        self.myZoneAbilities = [[None for i in range(6)],
                                [None for i in range(4)],
                                [None for i in range(4)]]
        self.myOutAbility = None
        self.myFormCount = 0
        self.myModeCount = 0
        self.myMinionCount = 0
    def SetHero(self, hero=None):
        # Sets all hero attributes
        self.Empty()
        if isinstance(hero, Hero):
            self.myHero = hero
            self.myHero.SetFrame(self)
            self.myHeroNames = [hero.hero_name, hero.alias]
            if self.myHero.background in range(len(bg_collection)):
                self.myHeroChars[0] = bg_collection[self.myHero.background][0]
            if self.myHero.power_source in range(len(ps_collection)):
                self.myHeroChars[1] = ps_collection[self.myHero.power_source][0]
            if self.myHero.archetype in range(len(arc_collection)):
                self.myHeroChars[2] = arc_collection[self.myHero.archetype][0]
                if self.myHero.archetype_modifier in range(len(arc_modifiers)) and \
                   self.myHero.archetype_modifier > 0:
                    self.myHeroChars[2] = arc_modifiers[self.myHero.archetype_modifier][0] + ":" + \
                                          self.myHeroChars[2]
            if self.myHero.personality in range(len(pn_collection)):
                self.myHeroChars[3] = pn_collection[self.myHero.personality][0]
                if self.myHero.dv_personality in range(len(pn_collection)):
                    self.myHeroChars[3] += "/" + pn_collection[self.myHero.dv_personality][0]
            # Add as many Power dice as will fit, or as few as exist, to myHeroPowers, leaving the
            #  rest None
            if len(hero.power_dice) <= len(self.myHeroPowers):
                self.myHeroPowers[0:len(hero.power_dice)] = [x for x in hero.power_dice]
            else:
                print("Error! Too many Power dice (" + str(len(hero.power_dice)) + " > " + \
                      str(len(self.myHeroPowers)) + ")")
                print("Displaying the first " + str(len(self.myHeroPowers)) + " Powers (" + \
                      str(hero.power_dice[0]) + " through " + \
                      str(hero.power_dice[len(self.myHeroPowers)-1]) + ")")
                self.myHeroPowers = [x for x in hero.power_dice[0:len(self.myHeroPowers)]]
            # Add as many Quality dice as will fit, or as few as exist, to myHeroQualities, leaving
            #  the rest None
            if len(hero.quality_dice) <= len(self.myHeroQualities):
                self.myHeroQualities[0:len(hero.quality_dice)] = [x for x in hero.quality_dice]
            else:
                print("Error! Too many Quality dice (" + str(len(hero.quality_dice)) + " > " + \
                      str(len(self.myHeroQualities)) + ")")
                print("Displaying the first " + str(len(self.myHeroQualities)) + " Qualities (" + \
                      str(hero.quality_dice[0]) + " through " + \
                      str(hero.quality_dice[len(self.myHeroQualities)-1]) + ")")
                self.myHeroQualities = [x for x in hero.quality_dice[0:len(self.myHeroQualities)]]
            self.myHeroStatus = hero.status_dice
            self.myHeroHealth = hero.health_zones
            # Add as many Principles as will fit, or as few as exist, to myHeroPrinciples, leaving
            #  the rest None
            if len(hero.principles) <= len(self.myHeroPrinciples):
                self.myHeroPrinciples[0:len(hero.principles)] = [x for x in hero.principles]
            else:
                print("Error! Too many Principles (" + str(len(hero.principles)) + " > " + \
                      str(len(self.myHeroPrinciples)) + ")")
                print("Displaying the first " + str(len(self.myHeroPrinciples)) + " Principles (" + \
                      str(hero.principles[0]) + " through " + \
                      str(hero.principles[len(self.myHeroPrinciples)-1]) + ")")
            # Find all valid Abilities that are Principles 
            givenPrinAbilities = [a for a in hero.abilities if a.name.startswith("Principle of ")]
            # Put as many as will fit, or as few as exist, into self.myPrinAbilities, leaving the
            #  rest None
            if len(givenPrinAbilities) <= len(self.myPrinAbilities):
                self.myPrinAbilities[0:len(givenPrinAbilities)] = [x for x in givenPrinAbilities]
            else:
                print("Error! Too many Principle Abilities: " + str(len(givenPrinAbilities)) + \
                      " > " + str(len(self.myPrinAbilities)))
                print("Displaying first " + str(len(self.myPrinAbilities)) + \
                      " Principle Abilities: " + str(givenPrinAbilities[0]) + " through " + \
                      str(givenPrinAbilities[len(self.myPrinAbilities)-1]) + ")")
                self.myPrinAbilities = [x for x in givenPrinAbilities[0:len(self.myPrinAbilities)]]
            for z in range(len(self.myZoneAbilities)):
                # Find all valid Abilities that have zone z and aren't Principles
                givenZoneAbilities = [a for a in hero.abilities \
                                      if a.zone == z and not a.name.startswith("Principle of ")]
                # Put as many as will fit, or as few as exist, into self.myZoneAbilities[z], leaving
                #  the rest None
                if len(givenZoneAbilities) <= len(self.myZoneAbilities[z]):
                    self.myZoneAbilities[z][0:len(givenZoneAbilities)] = [x for x in givenZoneAbilities]
                else:
                    print("Error! Too many " + status_zones[z] + " Abilities: " + \
                          str(len(givenZoneAbilities)) + " > " + str(len(self.myZoneAbilities[z])))
                    print("Displaying first " + str(len(self.myZoneAbilities[z])) + " " + \
                          status_zones[z] + " Abilities: " + str(givenZoneAbilities[0]) + \
                          " through " + str(givenZoneAbilities[len(self.myZoneAbilities)-1]) + ")")
                    self.myZoneAbilities[z] = [x for x in \
                                               givenZoneAbilities[0:len(self.myZoneAbilities[z])]]
            givenOutAbilities = [a for a in hero.abilities if a.zone == 3]
            if len(givenOutAbilities) > 0:
                self.myOutAbility = givenOutAbilities[0]
            if len(givenOutAbilities) > 1:
                print("Error! Too many Out Abilities: " + str(len(givenOutAbilities)))
                print("Displaying first Out Ability: " + givenOutAbilities[0].disptext())
            self.myFormCount = len(self.myHero.other_forms)
            self.myModeCount = len(self.myHero.other_modes)
            self.myMinionCount = len(self.myHero.min_forms)
    def UpdateAll(self, hero=None):
        self.SetHero(hero)
        for i in range(len(self.nameTitles)):
            self.nameValues[i].config(text=self.myHeroNames[i])
        for i in range(len(self.charTitles)):
            self.charValues[i].config(text=self.myHeroChars[i])
        sectionWidths = [4, 1]
        pqDiceValues = [["" for a in range(len(self.pqTitles))] for a in range(len(self.myHeroPowers))]
        for x in range(len(self.myHeroPowers)):
            if isinstance(self.myHeroPowers[x], PQDie):
                pqDiceValues[x][0] = split_text(self.myHeroPowers[x].flavorname,
                                                sectionWidths[0]*self.columnWidth)
                pqDiceValues[x][1] = str(self.myHeroPowers[x].diesize)
            if isinstance(self.myHeroQualities[x], PQDie):
                pqDiceValues[x][2] = split_text(self.myHeroQualities[x].flavorname,
                                                sectionWidths[0]*self.columnWidth)
                pqDiceValues[x][3] = str(self.myHeroQualities[x].diesize)
        for i in range(len(self.pqTitles)):
            for j in range(len(pqDiceValues)):
##                print("pqValues[" + str(j) + "][" + str(i) + "]: text=" + \
##                      str(self.pqValues[j][i]["text"]) + ", anchor=" + \
##                      str(self.pqValues[j][i]["anchor"]) + ", justify=" + \
##                      str(self.pqValues[j][i]["justify"]))
                self.pqValues[j][i].config(text=pqDiceValues[j][i])
##                print("pqValues[" + str(j) + "][" + str(i) + "]: text=" + \
##                      str(self.pqValues[j][i]["text"]) + ", anchor=" + \
##                      str(self.pqValues[j][i]["anchor"]) + ", justify=" + \
##                      str(self.pqValues[j][i]["justify"]))
        for i in range(len(self.statusValues)):
            disp = ""
            if self.myHeroStatus[i] in legal_dice:
                disp = str(self.myHeroStatus[i])
            self.statusValues[i].config(text=disp)
        for i in range(len(self.healthValues)):
            self.healthValues[i].config(text=self.RangeText(i))
        for i in range(len(self.myHeroPrinciples)):
            title = "Principle of "
            dr = ""
            minor = ""
            major = ""
            if isinstance(self.myHeroPrinciples[i], Principle):
                title = "Principle of " + self.myHeroPrinciples[i].title
                dr = self.myHeroPrinciples[i].during_roleplaying
                minor = self.myHeroPrinciples[i].minor_twist
                major = self.myHeroPrinciples[i].major_twist
            sectionValues = [dr, minor, major]
            sectionValues = [split_text(x, width=self.principleWrap) for x in sectionValues]
            self.prinTitles[i].config(text=title)
            for j in range(len(self.prinSectionTitles[i])):
                self.prinSectionValues[i][j].config(text=sectionValues[j])
        firstRow = 3
        firstCol = 17
        sectionWidths = [4, 2, 10]
        titleHeight = 1
        greenRows = 0
        for a in self.myZoneAbilities[0]:
            rowCount = 1
            if isinstance(a, Ability):
                textRows = split_text(a.dispText(), width=self.abilityWraps[2])
                nameRows = split_text(a.name, width=self.abilityWraps[0])
                rowCount = 1 + max(len([x for x in textRows if x == "\n"]),
                                   len([y for y in nameRows if y == "\n"]))
            greenRows += rowCount
##        print("Total rows in Green Abilities: " + str(greenRows))
        prinRow = firstRow + titleHeight + greenRows
        thisRow = prinRow
        prinHeight = 0
        for i in range(len(self.myPrinAbilities)):
            sectionValues = ["" for a in range(len(self.abilityTitleText))]
            rowsNeeded = 1
            if isinstance(self.myPrinAbilities[i], Ability):
                sectionValues = [self.myPrinAbilities[i].flavorname,
                                 self.myPrinAbilities[i].type,
                                 self.myPrinAbilities[i].dispText()]
                sectionValues = [split_text(sectionValues[j], self.abilityWraps[j]) \
                                 for j in range(len(sectionValues))]
                rowsNeeded = 1 + max([len([x for x in y if x == "\n"]) for y in sectionValues])
            rword = " rows"
            if rowsNeeded == 1:
                rword = " row"
##            print(str(self.myPrinAbilities[i]) + " starts at row #" + str(thisRow) + \
##                  " and takes up " + str(rowsNeeded) + rword)
            for j in range(len(self.abilityTitleText)):
                self.prinAbilityValues[i][j].config(text=sectionValues[j],
                                                    height=self.rowHeight*rowsNeeded)
                self.prinAbilityValues[i][j].grid(row=thisRow,
                                                  column=firstCol+sum(sectionWidths[:j]),
                                                  rowspan=rowsNeeded,
                                                  columnspan=sectionWidths[j],
                                                  sticky=N+S+E+W)
            thisRow += rowsNeeded
            prinHeight += rowsNeeded
        firstRows = [5, 26, 38]
        thisRow = firstRow + titleHeight
        for z in range(len(self.myZoneAbilities)):
            if z == 1:
                thisRow = prinRow + prinHeight
            for a in range(len(self.myZoneAbilities[z])):
                sectionValues = ["" for x in range(len(self.abilityTitleText))]
                rowsNeeded = 1
                if isinstance(self.myZoneAbilities[z][a], Ability):
                    sectionValues = [self.myZoneAbilities[z][a].flavorname,
                                     self.myZoneAbilities[z][a].type,
                                     self.myZoneAbilities[z][a].dispText()]
                    sectionValues = [split_text(sectionValues[j], self.abilityWraps[j]) \
                                     for j in range(len(sectionValues))]
                    rowsNeeded = 1 + max([len([x for x in y if x == "\n"]) for y in sectionValues])
                rword = " rows"
                if rowsNeeded == 1:
                    rword = " row"
##                print(str(self.myZoneAbilities[z][a]) + " starts at row #" + str(thisRow) + \
##                      " and takes up " + str(rowsNeeded) + rword)
                for s in range(len(self.zoneAbilityValues[z][a])):
                    self.zoneAbilityValues[z][a][s].config(text=sectionValues[s],
                                                           height=self.rowHeight*rowsNeeded)
                    self.zoneAbilityValues[z][a][s].grid(row=thisRow,
                                                         column=firstCol+sum(sectionWidths[:s]),
                                                         rowspan=rowsNeeded,
                                                         columnspan=sectionWidths[s],
                                                         sticky=N+S+E+W)
                thisRow += rowsNeeded
        outText = ""
        rowsNeeded = 1
        if isinstance(self.myOutAbility, Ability):
            outText = split_text(self.myOutAbility.dispText(), sum(self.abilityWraps))
            rowsNeeded = 1 + len([x for x in outText if x == "\n"])
        self.outAbilityValue.config(text=outText, height=rowsNeeded)
        self.outAbilityValue.grid(row=thisRow,
                                  column=firstCol,
                                  rowspan=rowsNeeded,
                                  columnspan=sum(sectionWidths),
                                  sticky=N+E+S+W)
        self.modeButton.config(text="Modes ("+str(self.myModeCount)+")")
        self.formButton.config(text="Forms ("+str(self.myFormCount)+")")
        self.minionButton.config(text="Minions ("+str(self.myMinionCount)+")")
        # Hide the Forms button if it's not relevant, otherwise show it
        if self.myFormCount == 0:
            self.formButton.grid_remove()
        else:
            self.formButton.grid()
        # Hide the Modes button if it's not relevant, otherwise show it
        if self.myModeCount == 0:
            self.modeButton.grid_remove()
        else:
            self.modeButton.grid()
        # Hide the Minion Forms button if it's not relevant, otherwise show it
        if self.myMinionCount == 0:
            self.minionButton.grid_remove()
        else:
            self.minionButton.grid()
        # Hide all creation step buttons by default
        self.backgroundButton.grid_remove()
        self.powerSourceButton.grid_remove()
        self.archetypeButton.grid_remove()
        self.personalityButton.grid_remove()
        self.redAbilityButton.grid_remove()
        self.retconButton.grid_remove()
        self.healthButton.grid_remove()
        # ...
        if isinstance(self.myHero, Hero):
            # Display ONLY the button for the first hero creation step that ISN'T complete for this hero
            rs_abilities = [a for a in self.myHero.abilities if a.step == 5]
            self.completeSteps = [self.myHero.background in range(len(bg_collection)),
                                  self.myHero.power_source in range(len(ps_collection)),
                                  self.myHero.archetype in range(len(arc_collection)),
                                  self.myHero.personality in range(len(pn_collection)),
                                  len(rs_abilities) > 1,
                                  self.myHero.used_retcon,
                                  self.myHero.health_zones != [0,0,0]]
            self.firstIncomplete = 99
            if False in self.completeSteps:
                self.firstIncomplete = self.completeSteps.index(False)
            if self.firstIncomplete == 0:
                self.backgroundButton.grid()
            elif self.firstIncomplete == 1:
                self.powerSourceButton.grid()
            elif self.firstIncomplete == 2:
                self.archetypeButton.grid()
            elif self.firstIncomplete == 3:
                self.personalityButton.grid()
            elif self.firstIncomplete == 4:
                self.redAbilityButton.grid()
            elif self.firstIncomplete == 5:
                self.retconButton.grid()
            elif self.firstIncomplete == 6:
                self.healthButton.grid()
        # ...
    def LaunchModeWindow(self):
        notePrefix = "HeroFrame: LaunchModeWindow: "
        print(notePrefix + "activated for " + self.myHeroNames[0] + " (" + \
              str(len(self.myHero.other_modes)) + " other Modes)")
        # If the hero has other Modes, create a new Toplevel window with a ModeFrame featuring
        #  them, and use this frame's wait_window method to ignore input while that one is open
        if len(self.myHero.other_modes) > 0:
            myModeWindow = ModeWindow(self, title=self.myHeroNames[0] + " Modes", hero=self.myHero)
        else:
            messagebox.showerror("Error", self.myHeroNames[0] + " has no other Modes.")
        # Otherwise, create a simple dialog window that informs the user there's been a problem
    def LaunchFormWindow(self):
        notePrefix = "HeroFrame: LaunchFormWindow: "
        print(notePrefix + "activated for " + self.myHeroNames[0] + " (" + \
              str(len(self.myHero.other_forms)) + " other Forms)")
        # If the hero has other Forms, create a new Toplevel window with a FormFrame featuring
        #  them, and use this frame's wait_window method to ignore input while that one is open
        if len(self.myHero.other_forms) > 0:
            myFormWindow = FormWindow(self, title=self.myHeroNames[0] + " Forms", hero=self.myHero)
        else:
            messagebox.showerror("Error", self.myHeroNames[0] + " has no other Forms.")
        # Otherwise, create a simple dialog window that informs the user there's been a problem
    def LaunchMinionWindow(self):
        notePrefix = "HeroFrame: LaunchMinionWindow: "
        print(notePrefix + "activated for " + self.myHeroNames[0] + " (" + \
              str(len(self.myHero.min_forms)) + " minion forms)")
        # If the hero has Minion Forms, create a new Toplevel window with a MinionFrame featuring
        #  them, and use this frame's wait_window method to ignore input while that one is open
        if len(self.myHero.min_forms) > 0:
            myMinionWindow = MinionWindow(self,
                                          title=self.myHeroNames[0] + " Minion Sheet",
                                          hero=self.myHero)
        else:
            messagebox.showerror("Error", self.myHeroNames[0] + " has no minion forms.")
        # Otherwise, create a simple dialog window that informs the user there's been a problem
    def AddHeroBackground(self, inputs=[]):
        # Walk the user through adding a Background to their hero.
        notePrefix = "### HeroFrame: AddHeroBackground: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + " inputs=" + str(inputs))
        step_options = ["Guided (roll dice & choose from results)",
                        "Constructed (choose from a table)"]
        print("1. Background")
        if self.myHero.background in range(len(bg_collection)):
            # This hero already has a Background
            messagebox.showerror("Error", self.myHero.hero_name + " already has the " + \
                                 bg_collection[self.myHero.background][0] + " Background.")
        else:
            bg_index = 99
            decision = self.myHero.ChooseIndex(step_options,
                                               prompt="How would you like to choose a Background for " + \
                                                      self.myHero.hero_name + "?",
                                               inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                bg_index = self.myHero.GuidedBackground(inputs=pass_inputs)
            else:
                bg_index = self.myHero.ConstructedBackground(inputs=pass_inputs)
            # Add the chosen Background
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddBackground(bg_index, inputs=pass_inputs)
            self.UpdateAll(self.myHero)
    def AddHeroPowerSource(self, inputs=[]):
        # Walk the user through adding a Power Source to their hero.
        notePrefix = "### HeroFrame: AddHeroPowerSource: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        step_options = ["Guided (roll dice & choose from results)",
                        "Constructed (choose from a table)"]
        print("2. Power Source")
        if self.myHero.power_source in range(len(ps_collection)):
            # This hero already has a Power Source
            messagebox.showerror("Error", self.myHero.hero_name + " already has the " + \
                                 ps_collection[self.myHero.power_source][0] + " Power Source.")
        else:
            ps_index = 99
            decision = self.myHero.ChooseIndex(step_options,
                                               prompt="How would you like to choose a Power " + \
                                               "Source for " + self.myHero.hero_name + "?",
                                               inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                ps_index = self.myHero.GuidedPowerSource(inputs=pass_inputs)
            else:
                ps_index = self.myHero.ConstructedPowerSource(inputs=pass_inputs)
            # Add the chosen Power Source
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddPowerSource(ps_index, inputs=pass_inputs)
            self.UpdateAll(self.myHero)
    def AddHeroArchetype(self, inputs=[]):
        # Walk the user through adding an Archetype to their hero.
        notePrefix = "### HeroFrame: AddHeroArchetype: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        step_options = ["Guided (roll dice & choose from results)",
                        "Constructed (choose from a table)"]
        print("3. Archetype")
        if self.myHero.archetype in range(len(arc_collection)):
            # This hero already has an Archetype
            arc_text = arc_collection[self.myHero.archetype][0]
            if self.myHero.archetype_modifier in range(1,len(arc_modifiers)):
                arc_text = arc_modifiers[self.myHero.archetype_modifier][0] + ":" + arc_text
            print(indent + self.myHero.hero_name + " already has the " + arc_text + " Archetype.")
        else:
            arc_indices = [99, 99]
            decision = self.myHero.ChooseIndex(step_options,
                                               prompt="How would you like to choose an " + \
                                               "Archetype for " + self.myHero.hero_name + "?",
                                               inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                arc_indices = self.myHero.GuidedArchetype(inputs=pass_inputs)
            else:
                arc_indices = self.myHero.ConstructedArchetype(inputs=pass_inputs)
            # Add the chosen Archetype
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddArchetype(arc_indices[0], arc_indices[1], inputs=pass_inputs)
            self.UpdateAll(self.myHero)
    def AddHeroPersonality(self, inputs=[]):
        # Walks the user through adding a Personality (or Personalities) to their hero.
        notePrefix = "### HeroFrame: AddHeroPersonality: "
        indent = "    "
        if len(inputs) > 0:
            print(notePrefix + "inputs=" + str(inputs))
        step_options = ["Guided (roll dice & choose from results)",
                        "Constructed (choose from a table)"]
        print("4. Personality")
        if self.myHero.personality in range(len(pn_collection)):
            # This hero already has a Personality.
            pn_text = "the " + pn_collection[self.myHero.personality][0] + " Personality."
            if self.myHero.dv_personality in range(len(pn_collection)):
                pn_text = "the " + pn_collection[self.myHero.personality][0] + \
                          " Personality in " + self.myHero.dv_tags[1] + " form and the " + \
                          pn_collection[self.myHero.dv_personality][0] + " Personality in " + \
                          self.myHero.dv_tags[0] + " form."
            print(indent + self.myHero.hero_name + " already has " + pn_text)
        else:
            pn_indices = []
            pn_prompt = "How would you like to choose a Personality for " + \
                        self.myHero.hero_name + "?"
            if self.myHero.archetype_modifier == 1:
                # Divided heroes can have more than one Personality
                pn_prompt = "How would you like to choose Personality/ies for " + \
                            self.myHero.hero_name + "?"
            decision = self.myHero.ChooseIndex(step_options,
                                               prompt=pn_prompt,
                                               inputs=inputs)
            entry_index = decision[0]
            inputs = decision[1]
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if step_options[entry_index].startswith("Guided"):
                pn_indices = self.myHero.GuidedPersonality(inputs=pass_inputs)
                if pn_indices[0] not in range(len(pn_collection)):
                    print("There was a problem with your Guided result. " + \
                          "Let's try the Constructed method.")
                    pass_inputs = []
                    if len(inputs) > 0:
                        if str(inputs[0]) != inputs[0]:
                            pass_inputs = inputs.pop(0)
                    pn_indices = self.myHero.ConstructedPersonality(inputs=pass_inputs)
            else:
                pn_indices = self.myHero.ConstructedPersonality(inputs=pass_inputs)
            # Add the chosen Personality/ies
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            if len(pn_indices) == 1:
                self.myHero.AddPersonality(pn_indices[0],
                                    inputs=pass_inputs)
            elif len(pn_indices) == 2:
                self.myHero.AddPersonality(pn_indices[0],
                                           dv_index=pn_indices[1],
                                           inputs=pass_inputs)
            else:
                self.myHero.AddPersonality(pn_indices[0],
                                           dv_index=pn_indices[1],
                                           out_index=pn_indices[2],
                                           inputs=pass_inputs)
        self.UpdateAll(self.myHero)
    def AddHeroRedAbilities(self, inputs=[]):
        # Add 2 Red Abilities
        notePrefix = "### HeroFrame: AddHeroRedAbilities: "
        indent = "    "
        print("5. Red Abilities")
        rs_abilities = [a for a in self.myHero.abilities if a.step == 5]
        if len(rs_abilities) > 1:
            print(indent + self.myHero.hero_name + " already added " + str(len(rs_abilities)) + \
                  " Red Abilities in step 5.")
        while len(rs_abilities) < 2:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddRedAbility(inputs=pass_inputs)
            rs_abilities = [a for a in self.myHero.abilities if a.step == 5]
        self.UpdateAll(self.myHero)
    def AddHeroRetcon(self, inputs=[]):
        # Take a Retcon
        notePrefix = "### HeroFrame: AddHeroRetcon: "
        indent = "    "
        print("6. Retcon")
        if self.myHero.used_retcon:
            print(indent + self.myHero.hero_name + " already used " + \
                  pronouns[self.myHero.pronoun_set][2] + " Retcon.")
        else:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddRetcon(inputs=pass_inputs)
        self.UpdateAll(self.myHero)
    def AddHeroHealth(self, health_roll=99, inputs=[]):
        # Determine Max Health
        notePrefix = "### HeroFrame: AddHeroRetcon: "
        indent = "    "
        print("7. Health")
        if self.myHero.health_zones != [0,0,0]:
            print(indent + self.myHero.hero_name + " already has maximum Health (" + \
                  str(self.myHero.health_zones[0]) + ").")
        else:
            pass_inputs = []
            if len(inputs) > 0:
                if str(inputs[0]) != inputs[0]:
                    pass_inputs = inputs.pop(0)
            self.myHero.AddHealth(roll=health_roll, inputs=pass_inputs)
        print("Done!")
        self.UpdateAll(self.myHero)
    def AddHeroNames(self, inputs=[]):
        # Let the user edit the hero's codename, civilian name, and pronouns
        notePrefix = "### HeroFrame: AddHeroNames: "
        indent = "    "
        if not isinstance(self.myHero, Hero):
            self.SetHero(Hero())
        prompt = "Enter a codename for this hero.\n(Feel free to use a placeholder; you can " + \
                 "change this at any time.)"
        textVar = StringVar(self, self.myHero.hero_name)
        question = EntryWindow(self.myParent,
                               prompt,
                               textVar,
                               title="Hero Creation")
        self.myHero.hero_name = textVar.get()
        self.UpdateAll(self.myHero)
        prompt = "Enter a civilian name for " + self.myHero.hero_name + ".\n(Feel free to use " + \
                 "a placeholder; you can change this at any time.)"
        textVar = StringVar(self, self.myHero.alias)
        question = EntryWindow(self.myParent,
                               prompt,
                               textVar,
                               title="Hero Creation")
        self.myHero.alias = textVar.get()
        self.UpdateAll(self.myHero)
        pronoun_options = [x[0] + "/" + x[1] for x in pronouns]
        pronoun_choice = IntVar(self, self.myHero.pronoun_set)
        prompt = "Which pronouns should be used for " + self.myHero.hero_name + "?\n(You can " + \
                 "change this at any time.)"
        question = SelectWindow(self.myParent,
                                prompt,
                                pronoun_options,
                                pronoun_choice,
                                title="Hero Creation")
        self.myHero.pronoun_set = pronoun_choice.get()
        self.UpdateAll(self.myHero)
    def DisplayHeroSteps(self, inputs=[]):
        # Prints the set of attributes (Powers, Qualities, Principles, Abilities, Modes, Forms,
        #  etc.) that the hero gained in each step of hero creation.
        if isinstance(self.myHero, Hero):
            self.myHero.DisplaySteps()
    def SaveTxt(self, inputs=[]):
        # Let the user save the hero's attributes to a txt file.
        notePrefix = "### HeroFrame.SaveTxt: "
        indent = "    "
        prompt = "Name a file to save " + self.myHero.hero_name + "'s details in.\nDO NOT " + \
                 "name a .txt file that already exists " + \
                 "in this folder. It WILL be overwritten."
        textVar = StringVar(self, self.myHero.hero_name)
        question = EntryWindow(self.myParent,
                               prompt,
                               textVar,
                               title="Save Hero")
        fname = textVar.get() + ".txt"
        heroFile = open(fname, mode='w')
        heroFile.write(self.myHero.details(width=-1))
        heroFile.close()

class SubWindow(Toplevel):
    # A class for subordinate windows
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
    def activate(self, contents):
        self.contents = contents
        self.initial_focus = self.body(self.contents)
        self.contents.grid(row=0, column=0, padx=5, pady=5)
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (self.parent.winfo_rootx()+50, self.parent.winfo_rooty()+20))
        self.initial_focus.focus_set()
        self.wait_window(self)
    def body(self, master):
        pass
    def cancel(self, event=None):
        # pass focus back to parent window
        self.parent.focus_set()
        self.destroy()

class ModeWindow(SubWindow):
    def __init__(self, parent, title=None, hero=None):
        SubWindow.__init__(self, parent, title)
        if isinstance(hero, Hero):
            self.myHero = hero
        else:
            self.myHero = None
        self.myModeFrame = ModeFrame(self, hero=self.myHero)
        self.activate(self.myModeFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class ModeFrame(Frame):
    def __init__(self, parent, hero=None, width=105, height=27, printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        notePrefix = "ModeFrame: __init__: "
        self.numRows = 16
        self.numCols = 26
        self.width = width
        self.height = height
        self.columnWidth = max(1, math.floor(self.width/self.numCols))
        self.rowHeight = max(1, math.floor(self.height/self.numRows))
        if printing:
            print(notePrefix + "width=" + str(self.width))
            print(notePrefix + "columnWidth=" + str(self.columnWidth))
            print(notePrefix + "height=" + str(self.height))
            print(notePrefix + "rowHeight=" + str(self.rowHeight))
        self.SetHero(hero)
        self.zoneColors = ["PaleGreen", "LightGoldenrod", "IndianRed"]
        self.mainColorIndex = 1
        self.darkColorIndex = 3
        self.sectionTitles = ["Power", "Die", "Name", "Type", "Text"]
        self.sectionTargets = [W, CENTER, E, CENTER, W]
        self.sectionReasons = [LEFT, CENTER, RIGHT, CENTER, LEFT]
        self.titleBG = "orange"
        self.titleRelief = RAISED
        self.headerRelief = RAISED
        self.dieRelief = GROOVE
        self.abilityRelief = GROOVE
        self.headerGlue = N+E+S+W
        self.rulesGlue = N+E+S+W
        self.powerGlue = E+W
        self.abilityGlue = N+S
        self.sectionWidths = [4, 1, 5, 2, 9]
        self.powerModifier = 1
        self.powerWrap = math.floor(self.sectionWidths[0]*self.columnWidth*self.powerModifier)
        self.rulesModifier = 1
        self.rulesWrap = math.floor(sum(self.sectionWidths[2:])*self.columnWidth*self.rulesModifier)
        self.abilityModifier = 1
        self.abilityWraps = [math.floor(x*self.columnWidth*self.abilityModifier) \
                             for x in self.sectionWidths[2:]]
        self.headerHeight = 1
        self.powerHeight = 1
        self.bufferHeight = 1
        self.myModeHeaders = [None for i in range(self.myModeCount)]
        self.myRuleValues = [None for i in range(self.myModeCount)]
        self.mySectionHeaders = [[None for j in range(5)] for i in range(self.myModeCount)]
        self.myPowerValues = [[[None, None] for j in range(4)] for i in range(self.myModeCount)]
        self.myAbilityValues = [[None, None, None] for i in range(self.myModeCount)]
        self.myBuffers = [None for i in range(self.myModeCount-1)]
        self.myColumnBuffers = [None for i in range(self.myModeCount)]
        thisRow = 1
        firstCol = 1
        for i in range(self.myModeCount):
            topRow = thisRow
            if printing:
                print(notePrefix + self.myModeNames[i] + " starts at row " + str(topRow) + \
                      ", column " + str(firstCol))
            leftHeight = 0
            rightHeight = 0
##            print(notePrefix + "displaying " + self.myModeNames[i])
            modeBase = "cyan"
            if self.myModeZones[i] in range(len(self.zoneColors[0])):
                modeBase = self.zoneColors[self.myModeZones[i]]
            modeColor = modeBase + str(self.mainColorIndex)
            headerColor = modeBase + str(self.darkColorIndex)
            # Create the section heading labels (to be placed later)
            for j in range(len(self.sectionTitles)):
                self.mySectionHeaders[i][j] = Label(self,
                                                    background=self.titleBG,
                                                    anchor=self.sectionTargets[j],
                                                    justify=self.sectionReasons[j],
                                                    relief=self.titleRelief,
                                                    text=self.sectionTitles[j],
                                                    width=self.sectionWidths[j]*self.columnWidth,
                                                    height=self.powerHeight*self.rowHeight)
                if printing:
                    print(notePrefix + self.sectionTitles[j] + " label is the size of " + \
                          str(self.powerHeight) + " rows and " + str(self.sectionWidths[j]) + \
                          " columns")
            # Display Mode Name across the full first row of the section
            self.myModeHeaders[i] = Label(self,
                                          background=headerColor,
                                          anchor=W,
                                          justify=LEFT,
                                          relief=self.headerRelief,
                                          text=self.myModeNames[i],
                                          width=sum(self.sectionWidths)*self.columnWidth,
                                          height=self.headerHeight*self.rowHeight)
            self.myModeHeaders[i].grid(row=topRow,
                                       column=firstCol,
                                       rowspan=self.headerHeight,
                                       columnspan=sum(self.sectionWidths),
                                       sticky=self.headerGlue)
            if printing:
                print(notePrefix + self.myModeNames[i] + " header starts at row " + str(topRow) + \
                      ", column " + str(firstCol) + " and takes up " + str(self.headerHeight) + \
                      " rows and " + str(sum(self.sectionWidths)) + " columns")
            leftHeight += self.headerHeight
            rightHeight += self.headerHeight
            # Place Power headings across columns 1-5 of the second row
            for j in range(2):
                self.mySectionHeaders[i][j].grid(row=topRow+leftHeight,
                                                 column=firstCol+sum(self.sectionWidths[0:j]),
                                                 rowspan=self.powerHeight,
                                                 columnspan=self.sectionWidths[j])
                if printing:
                    print(notePrefix + self.mySectionHeaders[i][j]["text"] + \
                          " label starts at row " + str(topRow+leftHeight) + ", column " + \
                          str(firstCol+sum(self.sectionWidths[0:j])) + " and takes up " + \
                          str(self.powerHeight) + " rows and " + str(self.sectionWidths[j]) + \
                          " columns")
            leftHeight += self.powerHeight
            # Display Power dice across columns 1-5 of the third through sixth rows
            for j in range(len(self.myModePowers[i])):
                thisPower = self.myModePowers[i][j]
                thisPowerText = ""
                thisPowerDie = ""
                thisPowerHeight = 1
                if isinstance(thisPower, PQDie):
                    thisPowerText = split_text(thisPower.flavorname, self.powerWrap)
                    thisPowerDie = str(thisPower.diesize)
                    thisPowerHeight = max(self.powerHeight,
                                          1 + len([x for x in thisPowerText if x == "\n"]))
                thisPowerValues = [thisPowerText, thisPowerDie]
                for k in range(len(self.myPowerValues[i][j])):
                    self.myPowerValues[i][j][k] = Label(self,
                                                        background=modeColor,
                                                        anchor=self.sectionTargets[k],
                                                        justify=self.sectionReasons[k],
                                                        relief=self.dieRelief,
                                                        text=thisPowerValues[k],
                                                        width=self.sectionWidths[k]*self.columnWidth,
                                                        height=thisPowerHeight)
                    self.myPowerValues[i][j][k].grid(row=topRow+leftHeight,
                                                     column=firstCol+sum(self.sectionWidths[0:k]),
                                                     rowspan=thisPowerHeight,
                                                     columnspan=self.sectionWidths[k],
                                                     sticky=self.powerGlue)
                    if printing:
                        print(notePrefix + self.myPowerValues[i][j][k]["text"] + \
                              " label starts at row " + str(topRow+leftHeight) + ", column " + \
                              str(firstCol+sum(self.sectionWidths[0:k])) + " and takes up " + \
                              str(thisPowerHeight) + " rows and " + str(self.sectionWidths[k]) + \
                              " columns")
                leftHeight += thisPowerHeight
            # Display mode rules across columns 6-21 starting at the second row
            thisRulesSections = [split_text(x, width=self.rulesWrap) \
                                 for x in self.myModeRules[i].split("\n")]
            thisRulesText = "\n".join(thisRulesSections)
            thisRulesHeight = 1 + len([x for x in thisRulesText if x == "\n"])
            self.myRuleValues[i] = Label(self,
                                         background=modeColor,
                                         anchor=W,
                                         justify=LEFT,
                                         text=thisRulesText,
                                         width=sum(self.sectionWidths[2:])*self.columnWidth,
                                         height=thisRulesHeight*self.rowHeight)
            self.myRuleValues[i].grid(row=topRow+rightHeight,
                                      column=firstCol+sum(self.sectionWidths[0:2]),
                                      rowspan=thisRulesHeight,
                                      columnspan=sum(self.sectionWidths[2:]),
                                      sticky=self.rulesGlue)
            if printing:
                print(notePrefix + self.myModeNames[i] + " rules label starts at row " + \
                      str(topRow+rightHeight) + ", column " + \
                      str(firstCol+sum(self.sectionWidths[0:2])) + " and takes up " + \
                      str(thisRulesHeight) + " rows and " + str(sum(self.sectionWidths[2:])) + \
                      " columns")
            rightHeight += thisRulesHeight
            # Place Ability section headers across columns 6-21 in the row after the end of the
            #  mode rules
            for j in range(2,5):
                self.mySectionHeaders[i][j].grid(row=topRow+rightHeight,
                                                 column=firstCol+sum(self.sectionWidths[0:j]),
                                                 rowspan=self.headerHeight,
                                                 columnspan=self.sectionWidths[j],
                                                 sticky=self.headerGlue)
                if printing:
                    print(notePrefix + self.mySectionHeaders[i][j]["text"] + \
                          " label starts at row " + str(topRow+leftHeight) + ", column " + \
                          str(firstCol+sum(self.sectionWidths[0:j])) + " and takes up " + \
                          str(self.powerHeight) + " rows and " + str(self.sectionWidths[j]) + \
                          " columns")
            rightHeight += self.headerHeight
            # Display Ability sections across columns 6-21 starting 2 rows after the end of the
            #  mode rules
            thisAbilityName = ""
            thisAbilityType = ""
            thisAbilityText = ""
            if isinstance(self.myModeAbilities[i], Ability):
                thisAbilityName = self.myModeAbilities[i].flavorname
                thisAbilityType = self.myModeAbilities[i].type
                thisAbilityText = self.myModeAbilities[i].dispText()
            thisAbilitySections = [thisAbilityName, thisAbilityType, thisAbilityText]
            thisAbilitySections = [split_text(thisAbilitySections[i], self.abilityWraps[i]) \
                                   for i in range(len(thisAbilitySections))]
            thisAbilityHeight = 1 + max([len([x for x in y if x == "\n"]) for y in thisAbilitySections])
            for j in range(len(self.myAbilityValues[i])):
                self.myAbilityValues[i][j] = Label(self,
                                                   background=modeColor,
                                                   anchor=self.sectionTargets[j+2],
                                                   justify=self.sectionReasons[j+2],
                                                   relief=self.abilityRelief,
                                                   text=thisAbilitySections[j],
                                                   width=self.sectionWidths[j+2]*self.columnWidth,
                                                   height=thisAbilityHeight*self.rowHeight)
                self.myAbilityValues[i][j].grid(row=topRow+rightHeight,
                                                column=firstCol+sum(self.sectionWidths[0:j+2]),
                                                rowspan=thisAbilityHeight,
                                                columnspan=self.sectionWidths[j+2],
                                                sticky=self.abilityGlue)
                if printing:
                    print(notePrefix + self.myAbilityValues[i][j]["text"] + \
                          " label starts at row " + str(topRow+rightHeight) + ", column " + \
                          str(firstCol+sum(self.sectionWidths[0:j+2])) + " and takes up " + \
                          str(thisAbilityHeight) + " rows and " + str(self.sectionWidths[j+2]) + \
                          " columns")
            rightHeight += thisAbilityHeight
            # If the two section heights are uneven, create a buffer to extend the shorter column
            cBufferRow = -1
            cBufferCol = -1
            cBufferWidth = -1
            cBufferHeight = -1
            cBufferGlue = N+E+S+W
            if leftHeight < rightHeight:
                cBufferRow = topRow + leftHeight
                cBufferCol = firstCol
                cBufferWidth = sum(self.sectionWidths[0:2])
                cBufferHeight = rightHeight - leftHeight
                cBufferGlue = self.powerGlue
            elif rightHeight < leftHeight:
                cBufferRow = topRow + rightHeight
                cBufferCol = firstCol + sum(self.sectionWidths[0:2])
                cBufferWidth = sum(self.sectionWidths[2:])
                cBufferHeight = leftHeight - rightHeight
                cBufferGlue = self.abilityGlue
            if leftHeight != rightHeight:
                self.myColumnBuffers[i] = Label(self,
                                                background=modeColor,
                                                text=" ",
                                                width=cBufferWidth*self.columnWidth,
                                                height=cBufferHeight*self.rowHeight)
                self.myColumnBuffers[i].grid(row=cBufferRow,
                                             column=cBufferCol,
                                             rowspan=cBufferHeight,
                                             columnspan=cBufferWidth,
                                             sticky=cBufferGlue)
                if printing:
                    print(notePrefix + self.myModeNames[i] + " column buffer starts at row " + \
                          str(cBufferRow) + ", column " + str(cBufferCol) + " and takes up " + \
                          str(cBufferHeight) + " rows and " + str(cBufferWidth) + " columns")
            # If there's another Mode after this one, display an empty Label across the next empty
            #  row, and update thisRow for the next pass
            if i < self.myModeCount-1:
                if printing:
                    print(notePrefix + self.myModeNames[i] + " topRow=" + str(topRow) + \
                          ", leftHeight=" + str(leftHeight) + ", rightHeight=" + str(rightHeight))
                bufferRow = topRow + max(leftHeight, rightHeight)
                if printing:
                    print(notePrefix + self.myModeNames[i] + " bufferRow=" + str(bufferRow))
                self.myBuffers[i] = Label(self,
                                          text=" ",
                                          width=sum(self.sectionWidths)*self.columnWidth,
                                          height=self.bufferHeight*self.rowHeight)
                self.myBuffers[i].grid(row=bufferRow,
                                       column=firstCol,
                                       rowspan=self.bufferHeight,
                                       columnspan=sum(self.sectionWidths),
                                       sticky=N+E+S+W)
                if printing:
                    print(notePrefix + self.myModeNames[i] + " buffer starts at row " + \
                          str(bufferRow) + ", column " + str(firstCol) + " and takes up " + \
                          str(self.bufferHeight) + " rows and " + str(sum(self.sectionWidths)) + \
                          " columns")
                thisRow = bufferRow + self.bufferHeight
    def Empty(self):
        # Clears all hero attributes
        self.myHero = None
        self.myModeCount = 0
        self.myModeNames = []
        self.myModeZones = []
        self.myModePowers = []
        self.myModeRules = []
        self.myModeAbilities = []
    def SetHero(self, hero=None):
        # Sets all hero attributes
        self.Empty()
        if isinstance(hero, Hero):
            self.myHero = hero
            self.myModeCount = len(hero.other_modes)
            self.myModeNames = ["" for i in range(self.myModeCount)]
            self.myModeZones = [-1 for i in range(self.myModeCount)]
            self.myModePowers = [[None for j in range(4)] for i in range(self.myModeCount)]
            self.myModeRules = ["" for i in range(self.myModeCount)]
            self.myModeAbilities = [None for i in range(self.myModeCount)]
            for i in range(self.myModeCount):
                thisMode = hero.other_modes[i]
                self.myModeNames[i] = str(thisMode[0])
                self.myModeZones[i] = thisMode[1]
                if len(thisMode[2]) <= len(self.myModePowers[i]):
                    self.myModePowers[i][0:len(thisMode[2])] = [x for x in thisMode[2]]
                else:
                    print(notePrefix + "Error! Too many " + self.myModeNames[i] + " Powers: " + \
                          str(len(thisMode[2])) + " > " + str(len(self.myModePowers[i])))
                    print(notePrefix + "Displaying the first " + str(len(self.myModePowers[i])) + \
                          " Powers (" + str(thisMode[2][0]) + " through " + \
                          str(thisMode[2][len(self.myModePowers[i])-1]) + ")")
                    self.myModePowers[i] = [x for x in thisMode[2][0:len(self.myModePowers[i])]]
                if isinstance(thisMode[5], Ability):
                    self.myModeAbilities[i] = thisMode[5]
                rulesText = ""
                if len(thisMode[6]) > 0:
                    rulesText = "You cannot " + thisMode[6][0]
                    for j in range(1, len(thisMode[6])-1):
                        rulesText += ", " + thisMode[6][i]
                    if len(thisMode[6]) > 2:
                        rulesText += ","
                    if len(thisMode[6]) > 1:
                        rulesText += " or " + thisMode[6][len(thisMode[6])-1]
                    rulesText += " in this Mode."
                    if isinstance(self.myModeAbilities[i], Ability):
                        rulesText += "\n"
                if isinstance(self.myModeAbilities[i], Ability):
                    rulesText += "You gain access to the following Ability:"
                self.myModeRules[i] = rulesText

class MinionWindow(SubWindow):
    def __init__(self, parent, title=None, hero=None):
        SubWindow.__init__(self, parent, title)
        if isinstance(hero, Hero):
            self.myHero = hero
        else:
            self.myHero = None
        self.myMinionFrame = MinionFrame(self, hero=self.myHero)
        self.activate(self.myMinionFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class MinionFrame(Frame):
    def __init__(self, parent, hero=None, width=160, printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        notePrefix = "MinionFrame: __init__: "
        self.SetHero(hero)
        self.numRows = 14 + self.myMinionCount
        self.numCols = 16
        self.width = width
        self.columnWidth = max(1,math.floor(self.width/self.numCols))
        self.rowHeight = 1.6875
        self.height = math.ceil(self.rowHeight*self.numRows)
        if printing:
            print(notePrefix + "numRows: " + str(self.numRows))
            print(notePrefix + "height: " + str(self.height))
            print(notePrefix + "width: " + str(self.width))
            print(notePrefix + "columnWidth: " + str(self.columnWidth))
        self.sizeHeaders = ["Key Die Value", "Die Size", "Sample Forms"]
        self.sizeWidths = [2, 1, 13]
        self.sizeText = [["0 or less", "1-3", "4-7", "8-11", "12 or more"],
                         ["d4", "d6", "d8", "d10", "d12"],
                         ["Sphere or disc",
                          "Small animal or insect",
                          "Small humanoid or large animal",
                          "Standard humanoid or large machine",
                          "Massive humanoid or immense animal"]]
        self.sizeRules = "When you create a Minion with an ability during a scene, you choose \
which of the basic actions it can take (Attack, Boost, Defend, Hinder, or Overcome). It acts like \
a minion under your control and takes its action at the beginning of your turn. The size of the \
minion die is based on the result of your roll:"
        self.formHeaders = ["Name", "Bonus Required", "Description"]
        self.formWidths = [2, 2, 12]
        self.formRules = "When creating a minion, you may discard a bonus on you or a willing ally to give \
your minion one of the following upgrades:"
        self.rulesModifier = 1
        self.rulesWrap = math.floor(sum(self.sizeWidths)*self.columnWidth*self.rulesModifier)
        self.titleModifier = 1
        self.titleWrap = math.floor(sum(self.formWidths[0:1])*self.columnWidth*self.titleModifier)
        self.sizeModifier = 1
        self.sizeWraps = [math.floor(w*self.columnWidth*self.sizeModifier) for w in self.sizeWidths]
        self.formModifier = 1
        self.formWraps = [math.floor(w*self.columnWidth*self.formModifier) for w in self.formWidths]
        self.titleBG = "orange"
        self.rulesBG = "khaki"
        self.headerBG = "cyan"
        self.tableBG = "white"
        self.headerRelief = RAISED
        self.rulesRelief = GROOVE
        self.titleRelief = RAISED
        self.tableRelief = GROOVE
        self.headerGlue = E+S+W
        self.rulesGlue = N+E+S+W
        self.titleGlue = E+S+W
        self.tableGlue = E+S+W
        # Display minion size rules in columns 1-16 of rows 1-2
        self.myMinionSizeRules = Label(self,
                                       background=self.rulesBG,
                                       anchor=W,
                                       justify=LEFT,
                                       relief=self.rulesRelief,
                                       text=split_text(self.sizeRules, self.rulesWrap),
                                       width=sum(self.sizeWidths)*self.columnWidth,
                                       height=math.floor(2*self.rowHeight))
        self.myMinionSizeRules.grid(row=1,
                                    column=1,
                                    rowspan=2,
                                    columnspan=sum(self.sizeWidths),
                                    sticky=self.rulesGlue)
        # Display Minion Sizes title in columns 1-4 of row 3
        self.myMinionSizeTitle = Label(self,
                                       background=self.titleBG,
                                       anchor=W,
                                       justify=LEFT,
                                       relief=self.titleRelief,
                                       text=split_text("Minion Sizes", self.titleWrap),
                                       width=sum(self.formWidths[0:2])*self.columnWidth,
                                       height=math.floor(self.rowHeight))
        self.myMinionSizeTitle.grid(row=3,
                                    column=1,
                                    rowspan=1,
                                    columnspan=sum(self.formWidths[0:2]),
                                    sticky=self.titleGlue)
        # Display minion size column headers in row 4
        self.myMinionSizeHeaders = [None for i in self.sizeHeaders]
        for i in range(len(self.myMinionSizeHeaders)):
            thisHeader = Label(self,
                               background=self.headerBG,
                               anchor=W,
                               justify=LEFT,
                               relief=self.headerRelief,
                               text=split_text(self.sizeHeaders[i], self.sizeWraps[i]),
                               width=self.sizeWidths[i]*self.columnWidth,
                               height=math.floor(self.rowHeight))
            self.myMinionSizeHeaders[i] = thisHeader
            self.myMinionSizeHeaders[i].grid(row=4,
                                             column=1+sum(self.sizeWidths[0:i]),
                                             rowspan=1,
                                             columnspan=self.sizeWidths[i],
                                             sticky=self.headerGlue)
        # Display minion size column entries in rows 5-9
        self.myMinionSizeEntries = [[None for i in range(len(self.sizeText[0]))] for j in range(len(self.sizeText))]
        for c in range(len(self.myMinionSizeEntries)):
            for r in range(len(self.myMinionSizeEntries[c])):
                thisEntry = Label(self,
                                  background=self.tableBG,
                                  anchor=W,
                                  justify=LEFT,
                                  relief=self.tableRelief,
                                  text=split_text(self.sizeText[c][r], self.sizeWraps[c]),
                                  width=self.sizeWidths[c]*self.columnWidth,
                                  height=math.floor(self.rowHeight))
                self.myMinionSizeEntries[c][r] = thisEntry
                self.myMinionSizeEntries[c][r].grid(row=5+r,
                                                    column=1+sum(self.sizeWidths[0:c]),
                                                    rowspan=1,
                                                    columnspan=self.sizeWidths[c],
                                                    sticky=self.tableGlue)
        # Insert buffer between rows 9 and 12
        # ...
        # Display minion form rules in columns 1-16 of row 12
        self.myMinionFormRules = Label(self,
                                       background=self.rulesBG,
                                       anchor=W,
                                       justify=LEFT,
                                       relief=self.rulesRelief,
                                       text=split_text(self.formRules, self.rulesWrap),
                                       width=sum(self.formWidths)*self.columnWidth,
                                       height=math.floor(self.rowHeight))
        self.myMinionFormRules.grid(row=12,
                                    column=1,
                                    rowspan=1,
                                    columnspan=sum(self.formWidths),
                                    sticky=self.rulesGlue)
        # Display Minion Forms title in columns 1-4 of row 13
        self.myMinionFormTitle = Label(self,
                                       background=self.titleBG,
                                       anchor=W,
                                       justify=LEFT,
                                       relief=self.titleRelief,
                                       text=split_text("Minion Forms", self.titleWrap),
                                       width=sum(self.formWidths[0:2])*self.columnWidth,
                                       height=math.floor(self.rowHeight))
        self.myMinionFormTitle.grid(row=13,
                                    column=1,
                                    rowspan=1,
                                    columnspan=sum(self.formWidths[0:2]),
                                    sticky=self.titleGlue)
        # Display minion form column headers in row 14
        self.myMinionFormHeaders = [None for i in self.formHeaders]
        for i in range(len(self.myMinionFormHeaders)):
            thisHeader = Label(self,
                               background=self.headerBG,
                               anchor=W,
                               justify=LEFT,
                               relief=self.headerRelief,
                               text=split_text(self.formHeaders[i], self.formWraps[i]),
                               width=self.formWidths[i]*self.columnWidth,
                               height=math.floor(self.rowHeight))
            self.myMinionFormHeaders[i] = thisHeader
            self.myMinionFormHeaders[i].grid(row=14,
                                             column=1+sum(self.formWidths[0:i]),
                                             rowspan=1,
                                             columnspan=self.formWidths[i],
                                             sticky=self.headerGlue)
        # Display minion form column entries in rows 15-[14+self.myMinionCount]
        self.myMinionFormEntries = [[None,None,None] for i in range(self.myMinionCount)]
        for r in range(self.myMinionCount):
            for c in range(len(self.myMinionInfo[r])):
                thisEntry = Label(self,
                                  background=self.tableBG,
                                  anchor=W,
                                  justify=LEFT,
                                  relief=self.tableRelief,
                                  text=split_text(self.myMinionInfo[r][c], self.formWraps[c]),
                                  width=self.formWidths[c]*self.columnWidth,
                                  height=math.floor(self.rowHeight))
                self.myMinionFormEntries[r][c] = thisEntry
                self.myMinionFormEntries[r][c].grid(row=15+r,
                                                    column=1+sum(self.formWidths[0:c]),
                                                    rowspan=1,
                                                    columnspan=self.formWidths[c],
                                                    sticky=self.tableGlue)
    def Empty(self):
        # Clears all hero attributes
        self.myHero = None
        self.myMinionCount = 0
        self.myMinionInfo = []
    def SetHero(self, hero=None):
        # Sets all hero attributes
        if isinstance(hero, Hero):
            self.myHero = hero
            self.myMinionCount = len(self.myHero.min_forms)
            self.myMinionInfo = [["","",-1] for i in range(self.myMinionCount)]
            for i in range(self.myMinionCount):
                thisMinion = self.myHero.min_forms[i]
                self.myMinionInfo[i] = [str(thisMinion[0]), "+" + str(thisMinion[2]), str(thisMinion[1])]

class FormWindow(SubWindow):
    def __init__(self, parent, title=None, hero=None):
        SubWindow.__init__(self, parent, title)
        if isinstance(hero, Hero):
            self.myHero = hero
        else:
            self.myHero = None
        self.myFormFrame = FormFrame(self, hero=self.myHero)
        self.activate(self.myFormFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class FormFrame(Frame):
    def __init__(self, parent, hero=None, width=104, printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        notePrefix = "FormFrame: __init__: "
        self.numCols = 28
        self.width = width
        self.columnWidth = max(1,math.floor(self.width/self.numCols))
##        print(notePrefix + "width: " + str(self.width))
##        print(notePrefix + "columnWidth: " + str(self.columnWidth))
        self.SetHero(hero)
        self.numRows = 11 * self.myFormCount - 1
        # ...
        self.rowHeight = 1
        self.height = max(1,self.numRows*self.rowHeight)
        self.zoneColors = ["PaleGreen", "LightGoldenrod", "IndianRed"]
        self.mainColorIndex = 1
        self.darkColorIndex = 2
        self.titleBG = "orange"
        self.diceBG = "white"
        self.titleRelief = RAISED
        self.diceRelief = GROOVE
        self.statusRelief = SUNKEN
        self.abilityRelief = GROOVE
        self.rulesGlue = N+E+S+W
        self.diceGlue = N+E+S+W
        self.titleGlue = E+S+W
        self.abilityGlue = N+E+S+W
        self.upperWidths = [4, 1, 4, 1, 2, 16]
        self.lowerWidths = [4, 1, 4, 1, 2, 5, 2, 9]
        self.reasons = [LEFT, CENTER, LEFT, CENTER, CENTER, RIGHT, CENTER, LEFT]
        self.targets = [W, CENTER, W, CENTER, CENTER, E, CENTER, W]
        self.headerText = ["Powers", "Die", "Qualities", "Die", "Status", "Name", "Type", "Text"]
        self.nameModifier = 1
        self.nameWrap = math.floor(sum(self.upperWidths)*self.columnWidth*self.nameModifier)
        self.pqModifier = 1
        self.pqWrap = math.floor(self.upperWidths[0]*self.columnWidth*self.pqModifier)
        self.abilityModifiers = [1,1,1]
        self.abilityWraps = [math.floor(self.lowerWidths[x+5]*self.columnWidth*self.abilityModifiers[x]) for x in range(len(self.abilityModifiers))]
        # Form name labels are organized by form
        self.myFormNames = [None for x in range(self.myFormCount)]
        # Header labels are organized by form, then by category (in headerText)
        self.myHeaders = [[None for x in range(len(self.headerText))] for y in range(self.myFormCount)]
        # Status die labels are organized by form, then by zone
        self.myStatusDice = [[None for x in range(len(self.zoneColors))] for y in range(self.myFormCount)]
        # Power/Quality die labels are organized by form, then by column (in headerText[0:4]),
        #  then by row
        self.myPQDice = [[[None for x in range(8)] for y in range(4)] for z in range(self.myFormCount)]
        # Ability labels are organized by form, then by Ability (in thisForm[5]), then by section
        #  (in headerText[4:])
        self.myAbilities = [[[None for x in range(3)] for y in range(len(self.myFormInfo[z][5]))] for z in range(self.myFormCount)]
        firstRow = 1
        for i in range(self.myFormCount):
            thisForm = self.myFormInfo[i]
            thisName = thisForm[0]
            thisBG = self.zoneColors[thisForm[1]] + str(self.mainColorIndex)
            # leftHeight starts with 1 for form name plus 1 for Power headers
            leftHeight = 2
            # If this form has Powers, leftHeight adds the height of each Power
            for p in thisForm[2]:
                leftHeight += 1 + len([x for x in split_text(p.flavorname, self.pqWrap) if x == "\n"])
            # centerHeight starts with 1 for form name plus 1 for Quality headers
            centerHeight = 2
            # If this form has Qualities, centerHeight adds the height of each Quality
            for q in thisForm[3]:
                centerHeight += 1 + len([x for x in split_text(q.flavorname, self.pqWrap) if x == "\n"])
            # rightHeight starts with 1 for form name plus 2 for description
            rightHeight = 3
            # If this form has Abilities, rightHeight adds 1 for Ability headers...
            if len(thisForm[5]) > 0:
                rightHeight += 1
            # ... plus the height of each Ability
            for a in thisForm[5]:
                rightHeight += 1 + max(len([x for x in split_text(a.flavorname, self.abilityWraps[0]) if x == "\n"]),
                                       len([x for x in split_text(a.dispText(), self.abilityWraps[2]) if x == "\n"]))
            # rightHeight always needs to have room for form name, status header, and 3 status dice
            rightHeight = max(rightHeight, 5)
##            print(notePrefix + thisName + " leftHeight: " + str(leftHeight))
##            print(notePrefix + thisName + " centerHeight: " + str(centerHeight))
##            print(notePrefix + thisName + " rightHeight: " + str(rightHeight))
            # Display the form name (and divided tag if applicable) across the top row
            if self.isDivided:
                thisName += " (" + self.myDividedTags[thisForm[6]] + ")"
##            print(notePrefix + "displaying " + thisName + " for form #" + str(i))
            self.myFormNames[i] = Label(self,
                                        background=thisBG,
                                        anchor=W,
                                        justify=LEFT,
                                        text=thisName,
                                        width=self.numCols*self.columnWidth,
                                        height=self.rowHeight)
            self.myFormNames[i].grid(row=firstRow,
                                     column=1,
                                     rowspan=1,
                                     columnspan=sum(self.upperWidths),
                                     sticky=self.rulesGlue)
            # Display Power, Quality, and Status headers across columns 1-12 of the second row
            for j in range(5):
                self.myHeaders[i][j] = Label(self,
                                             background=self.titleBG,
                                             anchor=self.targets[j],
                                             justify=self.reasons[j],
                                             relief=self.titleRelief,
                                             text=self.headerText[j],
                                             width=self.upperWidths[j]*self.columnWidth,
                                             height=self.rowHeight)
                self.myHeaders[i][j].grid(row=firstRow+1,
                                          column=1+sum(self.upperWidths[0:j]),
                                          rowspan=1,
                                          columnspan=self.upperWidths[j],
                                          sticky=self.diceGlue)
            # Display status dice across columns 11-12 of the third through fifth rows
            for j in range(len(self.zoneColors)):
                self.myStatusDice[i][j] = Label(self,
                                                background=self.zoneColors[j] + str(self.darkColorIndex),
                                                anchor=self.targets[4],
                                                justify=self.reasons[4],
                                                relief=self.statusRelief,
                                                text=str(thisForm[4][j]),
                                                width=self.upperWidths[4]*self.columnWidth,
                                                height=self.rowHeight)
                self.myStatusDice[i][j].grid(row=firstRow+2+j,
                                             column=1+sum(self.upperWidths[0:4]),
                                             rowspan=1,
                                             columnspan=self.upperWidths[4],
                                             sticky=self.diceGlue)
            # Display Power and Quality dice across columns 1-10 of the third through
            #  [2+max(len(powers),len(qualities))]th rows
            pqHeights = [1 for x in range(8)]
            for r in range(len(pqHeights)):
                for c in range(2,4):
                    if r < len(thisForm[c]):
                        if isinstance(thisForm[c][r], PQDie):
                            pqHeights[r] = max(pqHeights[r],
                                               1 + len([x for x in split_text(thisForm[c][r].flavorname, self.pqWrap) if x == "\n"]))
##                    print(notePrefix + thisName + " row " + str(r) + ", column " + str(c) + \
##                          " height: " + str(pqHeights[r]))
            for j in range(4):
                columnText = ["" for k in range(max(len(thisForm[2]),len(thisForm[3])))]
                diceIndex = 2
                if j >= 2:
                    diceIndex = 3
                columnDice = thisForm[diceIndex]
                for d in range(len(columnDice)):
                    if isinstance(columnDice[d], PQDie):
                        if j%2 == 0:
                            columnText[d] = split_text(columnDice[d].flavorname, self.pqWrap)
                        else:
                            columnText[d] = str(columnDice[d].diesize)
##                print(notePrefix + thisName + " " + self.headerText[j] + " justify: " + \
##                      str(self.reasons[j]))
                for k in range(len(columnText)):
                    self.myPQDice[i][j][k] = Label(self,
                                                   background=self.diceBG,
                                                   anchor=self.targets[j],
                                                   justify=self.reasons[j],
                                                   relief=self.diceRelief,
                                                   text=columnText[k],
                                                   width=self.upperWidths[j]*self.columnWidth,
                                                   height=self.rowHeight*pqHeights[k])
                    self.myPQDice[i][j][k].grid(row=firstRow+2+sum(pqHeights[0:k]),
                                                column=1+sum(self.upperWidths[0:j]),
                                                rowspan=pqHeights[k],
                                                columnspan=self.upperWidths[j],
                                                sticky=self.diceGlue)
            # If thisForm has associated Abilities...
            if len(thisForm[5]) > 0:
                # Display Ability headers across columns 13-28 of the fourth row
                for j in range(5, len(self.headerText)):
                    self.myHeaders[i][j] = Label(self,
                                                 background=self.titleBG,
                                                 anchor=self.targets[j],
                                                 justify=self.reasons[j],
                                                 relief=self.titleRelief,
                                                 text=self.headerText[j],
                                                 width=self.lowerWidths[j]*self.columnWidth,
                                                 height=self.rowHeight)
                    self.myHeaders[i][j].grid(row=firstRow+3,
                                              column=1+sum(self.lowerWidths[0:j]),
                                              rowspan=1,
                                              columnspan=self.lowerWidths[j],
                                              sticky=self.titleGlue)
                thisRow = firstRow + 4
                # For each Ability associated with this form...
                for j in range(len(thisForm[5])):
                    thisAbility = thisForm[5][j]
                    # Get the max height of the text boxes for this Ability. That will be the
                    #  rowspan of these labels.
                    abilityHeight = 1 + max(len([x for x in split_text(thisAbility.flavorname, self.abilityWraps[0]) if x == "\n"]),
                                            len([x for x in split_text(thisAbility.dispText(), self.abilityWraps[2]) if x == "\n"]))
##                    print(notePrefix + thisName + " " + thisAbility.flavorname + " abilityHeight: " + \
##                          str(abilityHeight))
                    thisAbilityText = [split_text(thisAbility.flavorname, self.abilityWraps[0]),
                                       thisAbility.type,
                                       split_text(thisAbility.dispText(), self.abilityWraps[2])]
                    for k in range(3):
                        self.myAbilities[i][j][k] = Label(self,
                                                          background=thisBG,
                                                          anchor=self.targets[5+k],
                                                          justify=self.reasons[5+k],
                                                          relief=self.abilityRelief,
                                                          text=thisAbilityText[k],
                                                          width=self.lowerWidths[5+k],
                                                          height=abilityHeight)
                        self.myAbilities[i][j][k].grid(row=thisRow,
                                                       column=1+sum(self.lowerWidths[0:5+k]),
                                                       rowspan=abilityHeight,
                                                       columnspan=self.lowerWidths[5+k],
                                                       sticky=self.abilityGlue)
                    thisRow += abilityHeight
            # ...
            firstRow += max(leftHeight, centerHeight, rightHeight) + 1
        # ...
    def Empty(self):
        # Clears all hero attributes
        self.myHero = None
        self.myFormCount = 0
        self.isDivided = False
        self.myDividedTags = []
        self.myFormInfo = []
        # ...
    def SetHero(self, hero=None):
        # Sets all hero attributes
        if isinstance(hero, Hero):
            self.myHero = hero
            self.myFormCount = len(self.myHero.other_forms)
            self.isDivided = (self.myHero.archetype_modifier == 1)
            self.myDividedTags = [x for x in self.myHero.dv_tags]
            # Shallow copy all the hero's forms, but sort them by zone for display purposes
            # Form-Changer grants 2 Green Forms and 1 Yellow Form, each with 1 Ability
            # Divided grants 2 Green Forms, each with no Abilities
            # To separate the two categories, display Green Forms with no Abilities before ones with
            #  Abilities
            self.myFormInfo = [[x for x in y] for y in self.myHero.other_forms if y[1] == 0 and len(y[5]) <= 0] + \
                              [[x for x in y] for y in self.myHero.other_forms if y[1] == 0 and len(y[5]) > 0] + \
                              [[x for x in y] for y in self.myHero.other_forms if y[1] == 1] + \
                              [[x for x in y] for y in self.myHero.other_forms if y[1] == 2]
            # For each form, if the status dice are empty, replace them with the hero's main
            #  status dice
            for i in range(self.myFormCount):
                if self.myFormInfo[i][4] == [0,0,0]:
                    self.myFormInfo[i][4] = [x for x in self.myHero.status_dice]

class ModeWindow(SubWindow):
    def __init__(self, parent, title=None, hero=None):
        SubWindow.__init__(self, parent, title)
        if isinstance(hero, Hero):
            self.myHero = hero
        else:
            self.myHero = None
        self.myModeFrame = ModeFrame(self, hero=self.myHero)
        self.activate(self.myModeFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class SelectWindow(SubWindow):
    def __init__(self, parent, prompt, options, var=None, title=None):
        SubWindow.__init__(self, parent, title)
        self.myPrompt = prompt
        self.myOptions = [str(x) for x in options]
        if isinstance(var, IntVar):
            self.myVariable = var
        else:
            self.myVariable = None
        self.mySelectFrame = SelectFrame(self, self.myPrompt, self.myOptions, self.myVariable)
        self.initial_focus = self.mySelectFrame
        self.activate(self.mySelectFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class SelectFrame(Frame):
    # A frame that poses a multiple-choice question to the user and reports the answer.
    # prompt: the text of the question
    # print_options -> self.myOptions: the list of texts of each answer
    # destination -> self.myDestination: the variable to save the index of the chosen answer to
    def __init__(self, parent, prompt, print_options, destination, printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        self.myPrompt = prompt
        self.myOptions = [str(x).replace("\n"," ") for x in print_options]
        self.myDestination = destination
        self.myString = StringVar(self, self.myOptions[destination.get()])
        self.myPromptLabel = Label(self,
                                   anchor=W,
                                   justify=LEFT,
                                   text=self.myPrompt,
                                   height=1+len([x for x in self.myPrompt if x == "\n"]))
        self.myPromptLabel.grid(row=0,
                                column=0,
                                rowspan=1,
                                columnspan=3,
                                sticky=N+E+S+W)
        self.myOptionMenu = OptionMenu(self,
                                       self.myString,
                                       *self.myOptions)
        self.myOptionMenu.config(anchor=W,
                                 justify=LEFT)
        self.myOptionMenu.grid(row=1,
                               column=0,
                               rowspan=1,
                               columnspan=3,
                               sticky=N+E+S+W)
        self.myOKButton = Button(self,
                                 anchor=CENTER,
                                 justify=CENTER,
                                 text="OK",
                                 padx=2,
                                 command=self.finish)
        self.myOKButton.grid(row=2,
                             column=1,
                             rowspan=1,
                             columnspan=1,
                             sticky=N+E+S+W)
        # Bind the Enter key to the same method as the OK button
        self.bind("<Return>", self.finish)
    def finish(self, *args):
        if len(self.myOptions) > 0:
            answer = self.myOptions.index(self.myString.get())
            if answer in range(len(self.myOptions)):
##                print(self.myPrompt)
##                for i in range(len(self.myOptions)):
##                    print(str(i) + ": " + self.myOptions[i])
##                print(str(answer))
                # Return self.myAnswer to the destination
                self.myDestination.set(answer)
                # Destroy this window...
                if isinstance(self.myParent, SubWindow):
                    self.myParent.cancel()
                # ...
            else:
                print("SelectFrame.finish: Invalid value of answer (" + str(answer) + ")")
        else:
            print("SelectFrame.finish: Invalid length of self.myOptions (" + \
                  str(len(self.myOptions)) + ")")
        # ...

class EntryWindow(SubWindow):
    def __init__(self, parent, prompt, var=None, title=None):
        SubWindow.__init__(self, parent, title)
        self.myPrompt = prompt
        if isinstance(var, StringVar):
            self.myVariable = var
        else:
            self.myVariable = None
        self.myEntryFrame = EntryFrame(self, self.myPrompt, self.myVariable)
        self.activate(self.myEntryFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0)
        return master

class EntryFrame(Frame):
    # A frame that asks the user for a line of text and returns the answer.
    # prompt -> self.myPrompt: the text of the question.
    # destination -> self.myDestination: the variable to save the user's response to
    def __init__(self, parent, prompt, destination, printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        self.myPrompt = prompt
        self.myText = StringVar(self, destination.get())
        self.myDestination = destination
        self.myPromptLabel = Label(self,
                                   anchor=W,
                                   justify=LEFT,
                                   text=self.myPrompt,
                                   height=1+len([x for x in self.myPrompt if x == "\n"]))
        self.myPromptLabel.grid(row=0,
                                column=0,
                                rowspan=1,
                                columnspan=3,
                                sticky=N+E+S+W)
        # Create Entry widget
        self.myTextEntry = Entry(self,
                                 justify=LEFT,
                                 textvariable=self.myText)
        self.myTextEntry.grid(row=1,
                              column=0,
                              rowspan=1,
                              columnspan=3,
                              sticky=N+E+S+W)
        # ...
        self.myOKButton = Button(self,
                                 anchor=CENTER,
                                 justify=CENTER,
                                 text="OK",
                                 padx=2,
                                 command=self.finish)
        self.myOKButton.grid(row=2,
                             column=1,
                             rowspan=1,
                             columnspan=1,
                             sticky=N+E+S+W)
        # Bind the Enter key to the same method as the OK button
        self.bind("<Return>", self.finish)
        self.myTextEntry.bind("<Return>", self.finish)
        # Give focus to myTextEntry immediately
        self.initial_focus = self.myTextEntry
        self.initial_focus.focus_set()
    def finish(self, *args):
        if self.myText.get():
            # Return self.myText to the destination
            print("EntryFrame.finish: passing '" + self.myText.get() + "'")
            self.myDestination.set(self.myText.get())
            # Destroy this window
            if isinstance(self.myParent, SubWindow):
                self.myParent.cancel()
        else:
            print("EntryFrame.finish: no text entered")

class ExpandWindow(SubWindow):
    def __init__(self,
                 parent,
                 prompt,
                 options,
                 details,
                 var=None,
                 title=None,
                 rwidth=100):
        SubWindow.__init__(self, parent, title)
        self.myPrompt = prompt
        self.myOptions = [str(x) for x in options]
        self.myDetails = [str(x) for x in details]
        if isinstance(var, IntVar):
            self.myVariable = var
        else:
            self.myVariable = None
        self.myExpandFrame = ExpandFrame(self,
                                         self.myPrompt,
                                         self.myOptions,
                                         self.myDetails,
                                         self.myVariable,
                                         width=rwidth)
        self.activate(self.myExpandFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0, sticky=N+E+S+W)
        return master

class ExpandFrame(Frame):
    # A frame that poses a multiple-choice question to the user and reports the answer. Use if
    #  individual options are complex and need more than one line to fully display.
    # prompt: the text of the question
    # print_options -> self.myOptions: the list of texts of each answer
    # expand_options -> self.myDetails: the set of messages to display when each answer is selected
    # destination -> self.myDestination: the IntVar to save the index of the chosen answer to
    # width -> self.myDispWidth: the width (in characters) of the section that displays info from
    #  self.myDetails
    def __init__(self,
                 parent,
                 prompt,
                 print_options,
                 expand_options,
                 destination,
                 width=100,
                 printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        self.myPrompt = str(prompt)
        self.myOptions = [str(x).replace("\n"," ") for x in print_options]
        # myDestination: IntVar, written to only in finish()
        self.myDestination = destination
        # myAnswer: IntVar, written to in expand()
        self.myAnswer = IntVar()
        # myString: StringVar, written to by OptionMenu directly
        self.myString = StringVar(self, self.myOptions[self.myDestination.get()])
        self.myDispWidth = width
        self.myDispBuffer = math.floor(0.43 * self.myDispWidth - 20)
        self.myDispWrap = self.myDispWidth + self.myDispBuffer
        self.myDetails = [str(x) for x in expand_options]
        self.myPromptLabel = Label(self,
                                   anchor=NW,
                                   justify=LEFT,
                                   text=self.myPrompt,
                                   height=1+len([x for x in self.myPrompt if x == "\n"]))
        self.myPromptLabel.grid(row=0,
                                column=0,
                                rowspan=1,
                                columnspan=3,
                                sticky=N+E+S+W)
        self.myOptionMenu = OptionMenu(self,
                                       self.myString,
                                       *self.myOptions,
                                       command=self.expand)
        self.myOptionMenu.config(anchor=W,
                                 justify=LEFT)
        self.myOptionMenu.grid(row=1,
                               column=0,
                               rowspan=1,
                               columnspan=3,
                               sticky=E+W)
        self.myOKButton = Button(self,
                                 anchor=CENTER,
                                 justify=CENTER,
                                 text="OK",
                                 padx=2,
                                 command=self.finish)
        self.myOKButton.grid(row=2,
                             column=1,
                             rowspan=1,
                             columnspan=1,
                             sticky=E+W)
        self.myBufferLabel = Label(self,
                                   anchor=W,
                                   text="")
        self.myBufferLabel.grid(row=3,
                                column=0,
                                rowspan=1,
                                columnspan=3,
                                sticky=N+E+S+W)
        self.myBPlusButton = Button(self,
                                    anchor=CENTER,
                                    justify=CENTER,
                                    text="+B",
                                    padx=1,
                                    command=self.plusbuffer)
        self.myBMinusButton = Button(self,
                                     anchor=CENTER,
                                     justify=CENTER,
                                     text="-B",
                                     padx=1,
                                     command=self.minusbuffer)
        self.myBPlusButton.grid(row=4,
                                column=0,
                                rowspan=1,
                                columnspan=1,
                                sticky=N+E+S+W)
        self.myBMinusButton.grid(row=4,
                                 column=1,
                                 rowspan=1,
                                 columnspan=1,
                                 sticky=N+E+S+W)
        self.myWPlusButton = Button(self,
                                    anchor=CENTER,
                                    justify=CENTER,
                                    text="+W",
                                    padx=1,
                                    command=self.pluswidth)
        self.myWMinusButton = Button(self,
                                     anchor=CENTER,
                                     justify=CENTER,
                                     text="-W",
                                     padx=1,
                                     command=self.minuswidth)
        self.myWPlusButton.grid(row=5,
                                column=0,
                                rowspan=1,
                                columnspan=1,
                                sticky=N+E+S+W)
        self.myWMinusButton.grid(row=5,
                                 column=1,
                                 rowspan=1,
                                 columnspan=1,
                                 sticky=N+E+S+W)
        detailsHeight = max([1 + len([x for x in y if x == "\n"]) for y in self.myDetails])
        self.myDispLabel = Label(self,
                                 anchor=NW,
                                 justify=LEFT,
                                 text="",
                                 width=self.myDispWidth,
                                 relief=GROOVE)
        if detailsHeight < 40:
            self.myDispLabel.config(height=detailsHeight)
        self.myDispLabel.grid(row=0,
                              column=4,
                              rowspan=len(self.myOptions)+3,
                              sticky=N+E+S+W)
        self.expand()
        # Bind the Enter key to the same method as the OK button
        self.bind("<Return>", self.finish)
    def expand(self, event=None):
        index = self.myOptions.index(self.myString.get())
        dispText = ""
        if index in range(len(self.myDetails)):
            dispText = split_text(self.myDetails[index], width=self.myDispWrap)
            # Testing: if the option at index is the name of an Archetype, call ArchetypeDetails
            #  to get the expanded text; repeat for Power Sources and Backgrounds
##            if self.myOptions[index] in [x[0] for x in arc_collection]:
##                arc_index = [x[0] for x in arc_collection].index(self.myOptions[index])
##                dispText = ArchetypeDetails(arc_index, width=self.myDispWrap)
##            elif self.myOptions[index] in [x[0] for x in ps_collection]:
##                ps_index = [x[0] for x in ps_collection].index(self.myOptions[index])
##                dispText = PowerSourceDetails(ps_index, width=self.myDispWrap)
##            elif self.myOptions[index] in [x[0] for x in bg_collection]:
##                bg_index = [x[0] for x in bg_collection].index(self.myOptions[index])
##                dispText = BackgroundDetails(bg_index, width=self.myDispWrap)
        self.myDispLabel.config(text=dispText)
        self.myAnswer.set(index)
    def plusbuffer(self, event=None):
        self.myDispBuffer += 5
        self.myDispWrap = self.myDispWidth + self.myDispBuffer
        self.expand()
        print("### ExpandFrame.plusbuffer: myDispBuffer = " + str(self.myDispBuffer) + \
              ", myDispWrap = " + str(self.myDispWrap))
    def minusbuffer(self, event=None):
        self.myDispBuffer -= 5
        self.myDispWrap = self.myDispWidth + self.myDispBuffer
        self.expand()
        print("### ExpandFrame.minusbuffer: myDispBuffer = " + str(self.myDispBuffer) + \
              ", myDispWrap = " + str(self.myDispWrap))
    def pluswidth(self, event=None):
        self.myDispWidth += 5
        self.myDispWrap = self.myDispWidth + self.myDispBuffer
        self.myDispLabel.config(width=self.myDispWidth)
        self.expand()
        print("### ExpandFrame.pluswidth: myDispWidth = " + str(self.myDispWidth) + \
              ", myDispWrap = " + str(self.myDispWrap))
    def minuswidth(self, event=None):
        self.myDispWidth -= 5
        self.myDispWrap = self.myDispWidth + self.myDispBuffer
        self.myDispLabel.config(width=self.myDispWidth)
        self.expand()
        print("### ExpandFrame.minuswidth: myDispWidth = " + str(self.myDispWidth) + \
              ", myDispWrap = " + str(self.myDispWrap))
    def finish(self, *args):
        if len(self.myOptions) > 0:
            if self.myAnswer.get() in range(len(self.myOptions)):
                print(self.myPrompt)
##                for i in range(len(self.myOptions)):
##                    print(str(i) + ": " + self.myOptions[i])
##                print(str(self.myAnswer.get()))
                # Return self.myAnswer to the destination
                self.myDestination.set(self.myAnswer.get())
                # Destroy this window...
                if isinstance(self.myParent, SubWindow):
                    self.myParent.cancel()
            else:
                print("ExpandFrame.finish: Invalid value at self.myAnswer (" + \
                      str(self.myAnswer.get()) + ")")
        else:
            print("ExpandFrame.finish: Invalid length of self.myOptions (" + \
                  str(len(self.myOptions)) + ")")

class SwapWindow(SubWindow):
    def __init__(self,
                 parent,
                 prompt,
                 options,
                 var0,
                 var1,
                 title=None,
                 width=100):
        SubWindow.__init__(self, parent, title)
        self.myPrompt = str(prompt)
        self.myOptions = [str(x) for x in options]
        self.myVariables = [None, None]
        if isinstance(var0, IntVar):
            self.myVariables[0] = var0
        else:
            self.myVariables[0] = IntVar()
        if isinstance(var1, IntVar):
            self.myVariables[1] = var1
        else:
            self.myVariables[1] = IntVar()
        self.mySwapFrame = SwapFrame(self,
                                     self.myPrompt,
                                     self.myOptions,
                                     self.myVariables,
                                     width=width)
        self.activate(self.mySwapFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0, sticky=N+E+S+W)
        return master

class SwapFrame(Frame):
    # Asks the user to choose 2 different entries from a list, returns the selected indices
    # prompt: the text prompt to display
    # options: the list of options
    # destinations: the IntVars to return the indices to
    # width: a maximum width (ignored if any of options are longer)
    def __init__(self,
                 parent,
                 prompt,
                 options,
                 destinations,
                 width=100,
                 printing=False):
        Frame.__init__(self, parent)
        self.myParent = parent
        self.myOptions = [str(x) for x in options]
        self.myWidth = max(width, max([len(s) for s in self.myOptions]))
        self.myPrompt = split_text(str(prompt), self.myWidth)
        self.myDestinations = [x for x in destinations[0:2]]
        self.myAnswers = [StringVar() for x in range(2)]
        self.myPromptLabel = Label(self,
                                   anchor=W,
                                   justify=LEFT,
                                   text=self.myPrompt,
                                   height=1+len([x for x in self.myPrompt if x == "\n"]))
        self.myPromptLabel.grid(row=0,
                                column=0,
                                rowspan=1,
                                columnspan=3,
                                sticky=N+E+S+W)
        self.myOptionMenus = [None for x in range(2)]
        for i in range(2):
            self.myAnswers[i].set(self.myOptions[i])
            self.myDestinations[i].set(-1)
            self.myOptionMenus[i] = OptionMenu(self, self.myAnswers[i], *self.myOptions)
            self.myOptionMenus[i].grid(row=i+1,
                                       column=0,
                                       rowspan=1,
                                       columnspan=3,
                                       sticky=N+E+S+W)
        self.myOKButton = Button(self,
                                 anchor=CENTER,
                                 justify=CENTER,
                                 text="OK",
                                 padx=2,
                                 command=self.finish)
        self.myOKButton.grid(row=3,
                             column=1,
                             rowspan=1,
                             columnspan=1,
                             sticky=N+E+S+W)
        # Bind the Enter key to the same method as the OK button
        self.bind("<Return>", self.finish)
    def finish(self, *args):
        if len(self.myOptions) > 0:
            for i in range(2):
                if self.myAnswers[i].get() in self.myOptions:
                    answerIndex = self.myOptions.index(self.myAnswers[i].get())
                    # Pass the value of self.myAnswer to the destination
                    self.myDestinations[i].set(answerIndex)
                else:
                    print("SwapFrame.finish: Invalid value at self.myAnswers[" + str(i) + \
                          "] (" + str(self.myAnswers[i].get()) + ")")
            # If both options are valid and they don't match...
            if self.myDestinations[0].get() >= 0 and \
               self.myDestinations[1].get() >= 0 and \
               self.myDestinations[0].get() != self.myDestinations[1].get():
                print("SwapFrame.finish: returning " + str(self.myDestinations[0].get()) + \
                      " and " + str(self.myDestinations[1].get()))
                # Destroy this window
                if isinstance(self.myParent, SubWindow):
                    self.myParent.cancel()
            elif self.myDestinations[0].get() == self.myDestinations[1].get():
                print("SwapFrame.finish: invalid selections (both " + \
                      str(self.myDestinations[0].get()) + ")")
        else:
            print("SwapFrame.finish: Invalid length of self.myOptions (" + \
                  str(len(self.myOptions)) + ")")

class PrincipleWindow(SubWindow):
    def __init__(self,
                 parent,
                 principle,
                 titleVar,
                 roleplayingVar,
                 minorVar,
                 majorVar,
                 greenVar,
                 title=None,
                 width=100):
        SubWindow.__init__(self, parent, title)
        if isinstance(principle, Principle):
            self.myPrinciple = principle
        else:
            self.myPrinciple = Principle(0,0)
        self.myPrincipleFrame = PrincipleFrame(self,
                                               self.myPrinciple,
                                               titleVar,
                                               roleplayingVar,
                                               minorVar,
                                               majorVar,
                                               greenVar,
                                               width=width)
        self.activate(self.myPrincipleFrame)
    def body(self, master):
        self.container = master
        master.grid(row=0, column=0, sticky=N+E+S+W)
        return master

class PrincipleFrame(Frame):
    def __init__(self,
                 parent,
                 principle,
                 titleVar,
                 roleplayingVar,
                 minorVar,
                 majorVar,
                 greenVar,
                 width=100):
        Frame.__init__(self, parent)
        self.myParent = parent
        self.myPrinciple = principle
        self.prinSectionNames = ["Title: Principle of ",
                                 "During Roleplaying",
                                 "Minor Twist",
                                 "Major Twist",
                                 "Green Ability"]
        self.prinSectionVars = [titleVar,
                                roleplayingVar,
                                minorVar,
                                majorVar,
                                greenVar]
        self.prinSectionVars[0].set(self.myPrinciple.title)
        self.prinSectionVars[1].set(self.myPrinciple.during_roleplaying)
        self.prinSectionVars[2].set(self.myPrinciple.minor_twist)
        self.prinSectionVars[3].set(self.myPrinciple.major_twist)
        self.prinSectionVars[4].set(self.myPrinciple.green_ability)
        self.entryWidth = max(width, max([len(x.get()) for x in self.prinSectionVars]))
        self.mySectionLabels = [None for i in range(len(self.prinSectionNames))]
        self.mySectionEntries = [None for i in range(len(self.prinSectionNames))]
        for i in range(len(self.prinSectionNames)):
            self.mySectionLabels[i] = Label(self,
                                            anchor=E,
                                            justify=RIGHT,
                                            background="white",
                                            text=self.prinSectionNames[i],
                                            padx=2)
            self.mySectionLabels[i].grid(row=i,
                                         column=0,
                                         sticky=N+E+S+W)
            self.mySectionEntries[i] = Entry(self,
                                             justify=LEFT,
                                             textvariable=self.prinSectionVars[i],
                                             width=self.entryWidth)
            self.mySectionEntries[i].grid(row=i,
                                          column=1,
                                          columnspan=4,
                                          sticky=N+E+S+W)
        self.myOKButton = Button(self,
                                 anchor=CENTER,
                                 justify=CENTER,
                                 text="OK",
                                 padx=2,
                                 command=self.finish)
        self.myOKButton.grid(row=len(self.prinSectionNames),
                             column=2,
                             sticky=N+E+S+W)
        # Bind the Enter key to the same method as the OK button
        self.bind("<Return>", self.finish)
    def finish(self, *args):
        complete = True
        for i in range(len(self.prinSectionNames)):
            if self.prinSectionVars[i].get() == "":
                self.mySectionLabels[i].config(background="red")
                complete = False
            else:
                self.mySectionLabels[i].config(background="white")
        if complete:
            category = self.myPrinciple.category
            index = self.myPrinciple.index
            step = self.myPrinciple.step
            self.myPrinciple = Principle(category,
                                         index,
                                         title=self.prinSectionVars[0].get(),
                                         roleplaying=self.prinSectionVars[1].get(),
                                         minor=self.prinSectionVars[2].get(),
                                         major=self.prinSectionVars[3].get(),
                                         green=self.prinSectionVars[4].get(),
                                         stepnum=step)
            print("PrincipleFrame.finish: returning " + str(self.myPrinciple) + ":")
            self.myPrinciple.display()
            # Destroy this window
            if isinstance(self.myParent, SubWindow):
                self.myParent.cancel()
            

factory = SampleMaker()

root = Tk()
root.geometry("+0+0")

##gui = SampleGUI(root)

# Testing HeroFrame

# Using the sample heroes
##firstHero = factory.getCham()
##disp_frame = HeroFrame(root, hero=firstHero)
##disp_frame.grid(row=0, column=0, columnspan=12)
##root.mainloop()

# Using a partially constructed hero
##platypus = Hero(codename="Platypus", civ_name="Chaz Villette")
##disp_frame = HeroFrame(root, hero=platypus)
##disp_frame.grid(row=0, column=0, columnspan=12)
##platypus.AddBackground(6, inputs=[[["E",["A"]],["H"]],["I","n"]])
##platypus.AddPowerSource(2, inputs=[[["G",["A"]],["Q"]],
##                                   ["B","A","y","Recalculate"],
##                                   ["A","B","y","Raise the Mirror"],
##                                   ["A","A","y","Statistical Inference"]])
##platypus.AddArchetype(1, inputs=[["b"],
##                                 [["g",["b"]],["b"]],
##                                 ["B","c","y","No One Here But You"],
##                                 ["B","y","Reflection"],
##                                 ["A","c","y","Behind the Scenes"],
##                                 ["M","n"]])
##platypus.AddPersonality(0, inputs=[[["y", "Wind-Up Boogeyman"]],["a"]])
##platypus.AddRedAbility(retcon_step=0, inputs=["C",["B","y","Stand Up On It"]])
##platypus.AddRedAbility(retcon_step=0, inputs=["E",["F","y","In Their Own Words"]])
##platypus.AddRetcon(inputs=["f","d",["G","n",["b"]]])
##platypus.AddHealth(inputs=["a"])
##root.mainloop()

# Using a not-yet-constructed hero
dispFrame = HeroFrame(root)
dispFrame.grid(row=0, column=0, columnspan=12)
root.mainloop()
