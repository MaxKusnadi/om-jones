import unittest

from bot.database import Database
from bot.modelMappers.user import UserMapper


class TestUserMapperCreate(unittest.TestCase):

    def setUp(self):
        Database.clear_db()

    def test_create_user(self):
        mapper = UserMapper()
        u = mapper.create_user("123", "Max", "Kusnadi", "Male")

        assert(u.fb_id == "123")
        assert(u.first_name == "Max")
        assert(u.last_name == "Kusnadi")
        assert(u.gender == "Male")


class TestUserMapperRead(unittest.TestCase):

    def setUp(self):
        Database.clear_db()
        self.mapper = UserMapper()
        self.u = self.mapper.create_user("123", "Max", "Kusnadi", "Male")

    def test_get_user_by_fb_id(self):
        u = self.mapper.get_user_by_fb_id("123")

        assert(u.fb_id == "123")
        assert(u.first_name == "Max")
        assert(u.last_name == "Kusnadi")
        assert(u.gender == "Male")

    def test_get_user_by_invalid_fb_id(self):
        self.assertRaises(ValueError, self.mapper.get_user_by_fb_id, "222")

    def test_get_all_users(self):
        users = self.mapper.get_all_users()
        self.assertTrue(self.u in users)


class TestUserMapperReadGender(unittest.TestCase):

    def setUp(self):
        Database.clear_db()
        self.mapper = UserMapper()
        self.male = self.mapper.create_user("123", "Max", "Kusnadi", "male")
        self.female = self.mapper.create_user("456", "Cindy",
                                              "Amelia", "female")
        self.other = self.mapper.create_user("789", "Bob", "Papatuli", "gay")

    def test_all_males(self):
        males = self.mapper.get_all_males()
        self.assertTrue(self.male in males)
        self.assertFalse(self.female in males)
        self.assertFalse(self.other in males)

    def test_all_females(self):
        females = self.mapper.get_all_females()
        self.assertTrue(self.female in females)
        self.assertFalse(self.male in females)
        self.assertFalse(self.other in females)

    def test_all_others(self):
        males = self.mapper.get_other_genders()
        self.assertTrue(self.other in males)
        self.assertFalse(self.female in males)
        self.assertFalse(self.male in males)


class TestUserMapperUpdate(unittest.TestCase):

    def setUp(self):
        Database.clear_db()
        self.mapper = UserMapper()
        self.u = self.mapper.create_user("123", "Max", "Kusnadi", "Male")

    def test_update_user_by_fb_id(self):
        u = self.mapper.update_user_authorization("123", True)

        assert(u.is_authorized == True)

    def test_update_user_by_invalid_fb_id(self):
        self.assertRaises(
            ValueError, self.mapper.update_user_authorization, "2225", True)
