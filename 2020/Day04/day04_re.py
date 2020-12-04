import re


"""This seems like a job for... Regular Expressions! I mean, if you are a mad man/woman"""


part_one = re.compile(r"""
    ((byr|iyr|eyr|hgt|hcl|ecl|pid|cid):\S*[\ \n]){8}  # with cid
  | ((byr|iyr|eyr|hgt|hcl|ecl|pid)    :\S*[\ \n]){7}  # cid is optional
""" , re.X |  re.MULTILINE)


_byr = r"byr:(19[2-9]\d|200[0-2])[\ \n]"
_iyr = r"iyr:(201\d|2020)[\ \n]"
_eyr = r"eyr:(202\d|2030)[\ \n]"
_hgt = r"hgt:((1[5-8]\d|19[0-3])cm|(59|6\d|7[0-6])in)[\ \n]"
_hcl = r"hcl:#[0-9a-f]{6}[\ \n]"
_ecl = r"ecl:(amb|blu|brn|gry|grn|hzl|oth)[\ \n]"
_pid = r"pid:\d{9}[\ \n]"
_cid = r"cid:\S*[\ \n]"


_all_fields = r'(' + r'|'.join((_byr, _iyr, _eyr, _hgt, _hcl, _ecl, _pid, _cid)) + r')'
_all_fields_no_cid = r'(' + r'|'.join((_byr, _iyr, _eyr, _hgt, _hcl, _ecl, _pid)) + r')'

_full_stuff = r'(' + _all_fields+r"{8}|"+_all_fields_no_cid+r"{7}" + r')'

print(_full_stuff)

part_two = re.compile(_full_stuff, re.MULTILINE)

if __name__ == '__main__':
    content = open("input").read()
    one = len(part_one.findall(content))
    two = len(part_two.findall(content))
    print(one, two)
