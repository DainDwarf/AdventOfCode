import pytest
from day04 import *


inp="""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

def test_one():
    res = part_one(inp)
    assert res == 2


class TestPartTwo:
    """Tests given for part 2 permit testing various bits of it."""

    @pytest.mark.parametrize("byr, expected", [
        ("2002", True),
        ("2003", False),
    ])
    def test_byr(self, byr, expected):
        assert SecurePassport._validations['byr'](byr) is expected

    @pytest.mark.parametrize("hgt, expected", [
        ("60in", True),
        ("190cm", True),
        ("190in", False),
        ("190", False),
    ])
    def test_hgt(self, hgt, expected):
        assert SecurePassport._validations['hgt'](hgt) is expected

    @pytest.mark.parametrize("hcl, expected", [
        ("#123abc", True),
        ("#123abz", False),
        ("123abc", False),
    ])
    def test_hcl(self, hcl, expected):
        assert SecurePassport._validations['hcl'](hcl) is expected

    @pytest.mark.parametrize("ecl, expected", [
        ("brn", True),
        ("wat", False),
    ])
    def test_ecl(self, ecl, expected):
        assert SecurePassport._validations['ecl'](ecl) is expected

    @pytest.mark.parametrize("pid, expected", [
        ("000000001", True),
        ("0123456789", False),
    ])
    def test_pid(self, pid, expected):
        assert SecurePassport._validations['pid'](pid) is expected

    @pytest.mark.parametrize("desc, expected", [
        ("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"         , False),
        ("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"           , False),
        ("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"    , False),
        ("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"            , False),
        ("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"            , True ),
        ("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"   , True ),
        ("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"    , True ),
        ("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"           , True ),
    ])
    def test_passports(self, desc, expected):
        assert SecurePassport.from_batch(desc).is_valid is expected
