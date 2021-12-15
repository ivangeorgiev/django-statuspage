import pytest
import unittest
from unittest import mock
import datetime
from djangostatuspage import shortcuts

pytestmark = [pytest.mark.unit]

class TestCamelCaseSplit:
    """Test cases for camel_case_split function"""

    @pytest.mark.parametrize("input,expected", [
            ('PascalCase', ['Pascal', 'Case']),
            ('camelCase', ['camel', 'Case']),
            ('Ucfirst', ['Ucfirst']),
            ('lowercase', ['lowercase']),
            ('', ['']),
            ('ABBR', ['A','B','B','R']),
    ])
    def test_called_with(self, input, expected):
        result = shortcuts.camel_case_split(input)
        assert result == expected


class TestMultiCaseSplit:
    """Test cases for multi_case_split function"""

    @pytest.mark.parametrize("input,expected", [
            ('PascalCase', ['Pascal', 'Case']),
            ('camelCase', ['camel', 'Case']),
            ('Ucfirst', ['Ucfirst']),
            ('snake_case', ['snake', 'case']),
            ('kebap-case', ['kebap', 'case']),
            ('lowercase', ['lowercase']),
            ('mixed-PacalCase_snake_case-camelCase', ['mixed','Pacal','Case','snake','case','camel','Case']),
            ('', ['']),
            ('-stripped-empty---Between-', ['stripped', 'empty', 'Between'])
    ])
    def test_called_with(self, input, expected):
        result = shortcuts.multi_case_split(input)
        assert result == expected



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

