# test/advisor_test.py

import os
import pytest

from app.robo_advisor import to_usd, get_response, transform_response, csv_writer, get_decision

def test_to_usd():
    # function should add dollar sign and transform numeric object into string
    assert to_usd(4.50) == '$4.50'
    # function should round to two decimal places
    assert to_usd(4.5) == '$4.50'
    assert to_usd(4.5555) == '$4.56'
    # function should apply commas for numbers greater than 1,000
    assert to_usd(1234567890.5555) == '$1,234,567,890.56'

