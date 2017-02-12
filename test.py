import unittest

from test_cases.models.user import TestUser
from test_cases.modelMappers.user import (TestUserMapperCreate,
                                          TestUserMapperRead,
                                          TestUserMapperReadGender,
                                          TestUserMapperUpdate)

if __name__ == '__main__':
    unittest.main()
