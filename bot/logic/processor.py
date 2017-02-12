import logging
import random

from bot.modelMappers.user import UserMapper


class Processor(object):

    def __init__(self):
        self.mapper = UserMapper()

    def get_match_for_male(self):
        females = self.mapper.get_all_females()
        others = self.mapper.get_other_genders()
        combined = list(females) + list(others)
        try:
            choice = random.choice(combined)
        except IndexError as err:
            logging.error(err)
            raise err
        else:
            return choice

    def get_match_for_female(self):
        males = self.mapper.get_all_males()
        others = self.mapper.get_other_genders()
        combined = list(males) + list(others)
        try:
            choice = random.choice(combined)
        except IndexError as err:
            logging.error(err)
            raise err
        else:
            return choice

    def get_match_for_others(self):
        females = self.mapper.get_all_females()
        males = self.mapper.get_all_males()
        combined = list(females) + list(males)
        try:
            choice = random.choice(combined)
        except IndexError as err:
            logging.error(err)
            raise err
        else:
            return choice
