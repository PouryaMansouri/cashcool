import re


def validate_organization_nikename(value):
    regex_pattern = re.compile(
        "^(?=.{1,40}$)[\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC]+(?:[-'\s][\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC]+)*$")
    if regex_pattern.match(value):
        return True
    return False


def validate_organization_name(value):
    regex_pattern = re.compile("^[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)*$")
    if regex_pattern.match(value):
        return True
    return False
