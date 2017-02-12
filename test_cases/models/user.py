import unittest

from bot.models.user import User


class TestUser(unittest.TestCase):

    def test_set_get(self):
        user = User("abc", "Max", "Kusnadi", "male")

        assert(user.fb_id == "abc")
        assert(user.first_name == "Max")
        assert(user.last_name == "Kusnadi")
        assert(user.gender == "male")
        assert(user.is_authorized == True)
        assert(user.__repr__() == '<id abc - Max Kusnadi Gender: male>')
