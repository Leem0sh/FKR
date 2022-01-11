import unittest

import pytest
from pydantic import parse_obj_as, ValidationError, BaseModel

from api import channel_preparation
from src.models import ResultModel, MathModel
from unittest import IsolatedAsyncioTestCase
from src.service import operation_add


class MyTestCase(unittest.TestCase):
    def test_models(
            self
    ):
        results = [1, 2, 3]
        for result in results:
            rm = ResultModel(result=result)
            self.assertIsInstance(rm, BaseModel)
            self.assertEqual(rm.result, result)

    def test_channel_preparation1(self):

        cid = "123456abcd"
        channels = channel_preparation(cid)
        self.assertEqual(channels, (f"{cid}.OK", f"{cid}.NOT_OK"))


    def test_channel_preparation2(self):

        cid = "123456abcd"
        channels = channel_preparation(cid)
        self.assertNotEqual(channels, (f"{cid}.NOT_OK", f"{cid}.OK"))




class Test(IsolatedAsyncioTestCase):

    async def test_operation_add1(self):
        model = MathModel(val1=0, val2=2)
        expected_value = 2
        result_model = await operation_add(model)
        self.assertEqual(expected_value, result_model.result)


    async def test_operation_add2(self):
        model = MathModel(val1=-10, val2=2)
        expected_value = -8
        result_model = await operation_add(model)
        self.assertEqual(expected_value, result_model.result)


    async def test_operation_add3(self):
        model = MathModel(val1=-10, val2=2)
        expected_value = 8
        result_model = await operation_add(model)
        self.assertNotEqual(expected_value, result_model.result)



def test_validation_error():
    with pytest.raises(ValidationError):
        MathModel(val1="a", val2=2)

def test_validation_error2():
    with pytest.raises(ValidationError):
        MathModel(val1="x")


if __name__ == '__main__':
    unittest.main()
