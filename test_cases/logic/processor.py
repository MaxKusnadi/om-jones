import unittest

from bot.database import Database
from bot.logic.processor import Processor
from bot.modelMappers.user import UserMapper


class TestProcessor(unittest.TestCase):

    def setUp(self):
        Database.clear_db()
        self.processor = Processor()

        mapper = UserMapper()
        male1 = mapper.create_user("123", "M", "K", "male")
        male2 = mapper.create_user("123", "M", "K", "male")
        male3 = mapper.create_user("123", "M", "K", "male")

        female1 = mapper.create_user("123", "M", "K", "female")
        female2 = mapper.create_user("123", "M", "K", "female")
        female3 = mapper.create_user("123", "M", "K", "female")

        other1 = mapper.create_user("123", "M", "K", "gay")
        other2 = mapper.create_user("123", "M", "K", "gay")
        other3 = mapper.create_user("123", "M", "K", "gay")

        self.males = mapper.get_all_males()
        self.females = mapper.get_all_females()
        self.others = mapper.get_other_genders()

    def test_get_match_for_male(self):
        u = self.processor.get_match_for_male()

        self.assertTrue(u in self.females or u in self.others)
        self.assertFalse(u in self.males)

    def test_get_match_for_female(self):
        u = self.processor.get_match_for_female()

        self.assertTrue(u in self.males or u in self.others)
        self.assertFalse(u in self.females)

    def test_get_match_for_others(self):
        u = self.processor.get_match_for_others()

        self.assertTrue(u in self.females or u in self.males)
        self.assertFalse(u in self.others)


class TestProcessorEmptyList(unittest.TestCase):

    def setUp(self):
        Database.clear_db()
        self.processor = Processor()
        mapper = UserMapper()
        self.males = mapper.get_all_males()
        self.females = mapper.get_all_females()
        self.others = mapper.get_other_genders()

    def test_get_match_for_male(self):
        self.assertRaises(IndexError, self.processor.get_match_for_male)

    def test_get_match_for_female(self):
        self.assertRaises(IndexError, self.processor.get_match_for_female)

    def test_get_match_for_others(self):
        self.assertRaises(IndexError, self.processor.get_match_for_others)
