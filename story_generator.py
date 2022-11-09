# Simple Fairy Tales
# Exposition -> rising action -> climax -> falling action -> denouement

import random
import time

class Girl:
    pronouns = {
        "subjective": "she",
        "objective": "her",
        "possessive dependent": "her",
        "possessive independent": "hers",
        "reflexive": "herself"
        }

    names = ['Lily', 'Alice', 'Belle', 'Katie', 'Julia', 'Dee', 'Hailey', 'Amanda', 'Lucy']

    def __init__(self):
        self.name = random.choice(self.names)

class Boy:
    pronouns = {
        "subjective": "he",
        "objective": "him",
        "possessive dependent": "his",
        "possessive independent": "his",
        "reflexive": "himself"
        }

    names = ['John', 'Ben', 'Mark', 'Will', 'Robert', 'Tim', 'Liam', 'Karl', 'Albert', 'Michael']

    def __init__(self):
        self.name = random.choice(self.names)

class Character:
    interests = [('eating', 'apples'), ('playing', 'piano'),
    ('taking', 'photos'), ('reading', 'comics'), ('playing', 'baseball'),
    ('drawing', 'portraits'), ('weaving', 'friendship bracelets')]

    def __init__(self):
        character = random.choice((Boy, Girl))()
        self.__dict__ = character.__dict__

        self.pronouns = character.pronouns
        self.noun = character.__class__.__name__.lower()

class Protagonist(Character):
    def __init__(self):
        super().__init__()
        self._likes = random.choice(self.interests)

    @property
    def likes(self):
        return self._likes[0] + " " + self._likes[1]

    @property
    def item(self):
        return self._likes[1]

class Antagonist(Character):
    relations = ['parent', 'teacher', 'older sibling', 'best friend',
        'significant other', 'younger sibling']

    def __init__(self):
        super().__init__()
        self.relation = random.choice(self.relations)

class Event:
    def __init__(self, actions=[]):
        self.actions = actions

    def choose(self):
        return random.choice(self.actions)

class Story:
    def __init__(self, keys={}):
        self.lines = []
        self.key_map = keys

    def read(self, delay=1):
         for line in self.lines:
            print(line)
            time.sleep(delay)

    def add_line(self, inp, punc=""):
        parsed_inp = []
        for token in inp:
            if token[0] == '!':
                parsed_inp.append(self.key_map[token[1:]])
            else:
                parsed_inp.append(token)
        self.lines.append(" ".join(parsed_inp)+punc)

def generate_story():
    protag = Protagonist()
    antag = Antagonist()

    retaliations = [f"punted {protag.pronouns['objective']} into the ocean",
        f"cursed {protag.name} to have red hair",
        f"stole {protag.pronouns['possessive dependent']} {protag.item}",
        f"destroyed {protag.pronouns['possessive dependent']} {protag.item}"]
    retaliation = Event(retaliations)

    inciting_incidents = ["wanted to run away",
        f"forgot to do {protag.pronouns['possessive dependent']} homework",
        f"stopped hanging out with {protag.pronouns['possessive dependent']} {antag.relation} {antag.name}",
        f"decided to move to the other side of the country to follow {protag.pronouns['possessive dependent']} dream",
        f"yeeted {protag.pronouns['reflexive']} out the window and shattered it"]
    inciting = Event(inciting_incidents)

    climax_events = ["summoned a pegasus from heaven and rode it into battle",
    f"went to talk to {antag.name}",
    f"gave {antag.name} an apology gift to be the bigger person",
    f"hit {antag.name} with a car",
    f"sprayed {antag.name} with a squirt bottle"]
    climax = Event(climax_events)

    conclusions = ["died", "broke down and gave a heartfelt apology",
    "disappeared and was never seen again", "grudgingly apologized", "moved to another city"]
    end = Event(conclusions)

    code_map = {'p_noun': protag.noun, 'p_name': protag.name, 'likes': protag.likes, 'p_subj': protag.pronouns['subjective'],
                'p_possdep': protag.pronouns['possessive dependent'], 'a_name': antag.name, 'a_rel': antag.relation,
                'a_subj': antag.pronouns['subjective'], 'a_possdep': protag.pronouns['possessive dependent'], 'item':protag.item.title(),
                'ret': retaliation.choose(), 'incite': inciting.choose(), 'cli': climax.choose(), 'end': end.choose()}

    story = Story(code_map)

    title = ["!p_name", "and the", "!item"]
    story.add_line(title)

    byline = ["By Lauren Wong"]
    story.add_line(byline)

    story.add_line([])

    sentence_1 = ["Once upon a time, there was a", "!p_noun", "named", "!p_name", "who loved", "!likes"]
    story.add_line(sentence_1, '.')

    # In fact, she loved eating apples so much that she started blowing off her friend John to do so.
    sentence_2 = ["In fact,", "!p_subj", "loved", "!likes", "so much that", "!p_subj", "!incite"]
    story.add_line(sentence_2, '.')

    sentence_3 = ["However,", "!p_possdep", "!a_rel", "!a_name", "didn't like that, so", "!a_subj", "!ret"]
    story.add_line(sentence_3, '.')

    sentence_4 = ["!p_name", "regretted", "!p_possdep", "behavior but knew this couldn't continue, so", "!p_subj", "!cli"]
    story.add_line(sentence_4, '.')

    sentence_5 = ["!a_name", "!end", "and", "!p_name", "lived happily ever after"]
    story.add_line(sentence_5, '.')

    story.add_line(["The End"], '.')

    return story

if __name__ == '__main__':
    story = generate_story()
    story.read(3)
