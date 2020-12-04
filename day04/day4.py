import re

required_fields = ['byr','iyr','eyr','hgt','hcl','ecl','pid']


def fields_not_in_line(line, search_fields):
    line_fields = [x.split(':')[0] for x in line.strip().split()]
    return [f1 for f1 in search_fields if f1 not in line_fields]

haircolorhex = re.compile('\d|[a-f]')

def fields_not_valid_in_line(line, search_fields):
    leftover_fields = set(search_fields)
    for x in line.strip().split():
        (field_name, field_value) = x.strip().split(':')
        if field_name == 'byr':
            try:
                birthyear = int(field_value)
                if birthyear >= 1920 and birthyear <= 2002:
                    leftover_fields.remove(field_name)
            except ValueError:
                pass
        elif field_name == 'iyr':
            try:
                issueyear = int(field_value)
                if issueyear >= 2010 and issueyear <= 2020:
                    leftover_fields.remove(field_name)
            except ValueError:
                pass
        elif field_name == 'eyr':
            try:
                expyear = int(field_value)
                if expyear >= 2020 and expyear <= 2030:
                    leftover_fields.remove(field_name)
            except ValueError:
                pass
        elif field_name == 'hgt':
            try:
                height = int(field_value[:-2])
                unit = field_value[-2:]
                if unit == 'cm':
                    if height >= 150 and height <= 193:
                        leftover_fields.remove(field_name)
                elif unit == 'in':
                    if height >= 59 and height <= 76:
                        leftover_fields.remove(field_name)
            except ValueError:
                pass
        elif field_name == 'hcl':
            if len(field_value) == 7 and field_value[0] == '#':
                allowed = [str(a) for a in range(10)]
                allowed.extend(['a','b','c','d','e','f'])
                if len([x for x in field_value[1:] if x not in allowed]) == 0:
                    leftover_fields.remove(field_name)
        elif field_name == 'ecl':
            if field_value in ['amb','blu','brn','gry','grn','hzl','oth']:
                leftover_fields.remove(field_name)
        elif field_name == 'pid':
            if len(field_value) == 9:
                try:
                    if int(field_value) >= 0:
                        leftover_fields.remove(field_name)
                except ValueError:
                    pass
    return list(leftover_fields)
            
def valid_passports_in(filename):
    num_valid = 0
    passport_done = False
    with open(filename, 'r') as f:
        search_fields = required_fields
        for line in f:
            if len(line.strip()) == 0:
                # new passport
                search_fields = required_fields
                passport_done = False
            elif not passport_done:
                search_fields = fields_not_valid_in_line(line, search_fields)
                if len(search_fields) == 0:
                    # passport's done and valid
                    num_valid += 1
                    passport_done = True
    return num_valid
        
print(valid_passports_in('input4.txt'))
