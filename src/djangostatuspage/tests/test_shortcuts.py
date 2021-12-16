import datetime
import enum
import unittest
from unittest import mock

import pytest

from djangostatuspage import shortcuts

pytestmark = [pytest.mark.unit]


class TestCamelCaseSplit:
    """Test cases for camel_case_split function"""
    @pytest.mark.parametrize('data,expected', [
        ('PascalCase', ['Pascal', 'Case']),
        ('camelCase', ['camel', 'Case']),
        ('Ucfirst', ['Ucfirst']),
        ('lowercase', ['lowercase']),
        ('', ['']),
        ('ABBR', ['A', 'B', 'B', 'R']),
    ])
    def test_called_with(self, data, expected):
        result = shortcuts.camel_case_split(data)
        assert result == expected


class TestGetEnumChoices:
    """Test cases for get_enum_choices function"""
    class MyEnum(enum.Enum):
        OPTION_1 = 1
        OPTION_2 = 2

    def test_called(self):
        data = self.MyEnum
        expect = [(1, 'Option 1'), (2, 'Option 2')]
        result = shortcuts.get_enum_choices(data)
        assert result == expect


class TestMultiCaseSplit:
    """Test cases for multi_case_split function"""
    @pytest.mark.parametrize('data,expected', [
        ('PascalCase', ['Pascal', 'Case']),
        ('camelCase', ['camel', 'Case']),
        ('Ucfirst', ['Ucfirst']),
        ('snake_case', ['snake', 'case']),
        ('kebap-case', ['kebap', 'case']),
        ('lowercase', ['lowercase']),
        ('mixed-PacalCase_snake_case-camelCase',
         ['mixed', 'Pacal', 'Case', 'snake', 'case', 'camel', 'Case']),
        ('', ['']),
        ('-stripped-empty---Between-', ['stripped', 'empty', 'Between']),
    ])
    def test_called_with(self, data, expected):
        result = shortcuts.multi_case_split(data)
        assert result == expected

    def test_name(self):
        parts = shortcuts.multi_case_split('Manual')
        assert 'Manual' == ' '.join(parts).lower().capitalize()


class TestMakeVerboseName:
    """Test cases for the make_verbose_name function"""
    @pytest.mark.parametrize('data,expect', [
        ('the-Name_here', 'The name here'),
    ])
    def test_called(self, data, expect):
        result = shortcuts.make_verbose_name(data)
        assert result == expect


class TestUtcNow(unittest.TestCase):
    """Test cases for the utc_now function"""
    @mock.patch('datetime.datetime')
    def test_returns_result_from_datetime_replace(self, dt_mock):
        utcnow_mock = mock.Mock()
        replace_mock = mock.Mock()
        expect_result = mock.Mock()
        replace_mock.return_value = expect_result
        utcnow_mock.return_value.replace = replace_mock
        dt_mock.utcnow = utcnow_mock

        result = shortcuts.utc_now()

        utcnow_mock.assert_called_once_with()
        replace_mock.assert_called_once_with(tzinfo=datetime.timezone.utc)
        assert result is expect_result
