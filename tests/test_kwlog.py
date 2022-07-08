from unittest.mock import MagicMock

import kwlog
import pytest


def test_create_logger():
    get_logger = kwlog.logging.getLogger = MagicMock()
    kwlog.get_logger('-')
    get_logger.assert_called_once_with('-')


@pytest.mark.parametrize(
    'input, expected',
    [
        (lambda x: x.info(), ""),
        (lambda x: x.info('msg'), "msg"),
        (lambda x: x.info('msg', None), "None - msg"),
        (lambda x: x.info('msg', '1'), "1 - msg"),
        (lambda x: x.info('msg', 0), "0 - msg"),
        (lambda x: x.info('msg', 1), "1 - msg"),
        (lambda x: x.info('msg', []), "[] - msg"),
        (lambda x: x.info('msg', ['x']), "['x'] - msg"),
        (lambda x: x.info('msg', {'a': 1}), "{'a': 1} - msg"),
        (lambda x: x.info('msg', set(['x'])), "{'x'} - msg"),
        (lambda x: x.info('msg', '1', 'two'), "1 two - msg"),
        (lambda x: x.info(a=1), "a=1"),
        (lambda x: x.info(a=0), "a=0"),
        (lambda x: x.info(a=None), "a=None"),
        (lambda x: x.info(a=1, b=2), "a=1 b=2"),
        (lambda x: x.info('msg', a=1), "msg | a=1"),
        (lambda x: x.info('msg', a=1, b=2), "msg | a=1 b=2"),
        (lambda x: x.info('msg', a=1, b=None), "msg | a=1 b=None"),
        (lambda x: x.info('msg', b="2"), "msg | b=\"2\""),
        (lambda x: x.info('msg', b=""), "msg | b=\"\""),
        (lambda x: x.info('msg', c=[]), "msg | c=[]"),
        (lambda x: x.info('msg', c=[3, None]), "msg | c=[3, None]"),
        (lambda x: x.info('msg', c=[3, '4']), "msg | c=[3, '4']"),
        (lambda x: x.info('msg', d={}), "msg | d={}"),
        (lambda x: x.info('msg', d={'five': 5}), "msg | d={'five': 5}"),
        (lambda x: x.info('msg', d={'five': '5'}), "msg | d={'five': '5'}"),
        (
            lambda x: x.info('x', d={'a': {'e': None}}),
            "x | d={'a': {'e': None}}",
        ),
        (
            lambda x: x.info('msg', a=1, b="2", c=[3, 4], d={'five': 5}),
            "msg | a=1 b=\"2\" c=[3, 4] d={'five': 5}",
        ),
    ],
)
def test_formatting(input, expected):
    get_logger = kwlog.logging.getLogger = MagicMock()
    input(kwlog.get_logger('-'))
    get_logger.return_value.info.assert_called_once_with(expected)
