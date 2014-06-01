#! /usr/bin/env python

import csv, json, os, sys
from collections import OrderedDict

try:
    import pyaml
except ImportError:
    print 'Please install pyaml. `pip install pyaml`.'
    sys.exit()

def is_year(val):
    try:
        val = int(val)
        return val >= 2013
    except:
        return False
    return False

def int_or_none(val):
    try:
        val = int(val)
        return val
    except:
        return None

def float_or_none(val):
    try:
        val = float(val)
        return val
    except:
        return None

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join('..', BASE_DIR, '_data'))
API_DIR = os.path.abspath(os.path.join('..', BASE_DIR, 'api'))

districts = OrderedDict()
schools = {}

for item in os.listdir(BASE_DIR):
    if os.path.isdir(item) and is_year(item):
        folder = item
        if os.path.exists(os.path.join(BASE_DIR, folder, 'District_Profile.csv')):
            print 'processing District_Profile'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'District_Profile.csv'), 'rU'))
            for row in reader:
                if row.get('DISTRICT', False):
                    district_id = row.get('DISTRICT')
                    if not row.get('DISTRICT') == '0':
                        district_id = district_id.lstrip('0')
                    if district_id:
                        obj = OrderedDict()
                        obj['name'] = row.get('DISTRICT NAME', '')
                        obj['nces_id'] = None
                        obj['grades_served'] = row.get('Grades served', '').split('-')
                        obj['number_schools'] = int_or_none(row.get('Number of schools'))
                        obj['administrators'] = int_or_none(row.get('Administrators'))
                        obj['teachers'] = int_or_none(row.get('Teachers'))
                        obj['membership'] = OrderedDict()
                        obj['membership']['average_daily'] = int_or_none(row.get('Average Daily Membership'))
                        obj['membership']['total'] = int_or_none(row.get('Total'))
                        obj['membership']['white'] = {
                            'total':    int_or_none(row.get('White')),
                            'male':     int_or_none(row.get('White Male')),
                            'female':   int_or_none(row.get('White Female')),
                        }
                        obj['membership']['african_american'] = {
                            'total':    int_or_none(row.get('African American')),
                            'male':     int_or_none(row.get('African American Male')),
                            'female':   int_or_none(row.get('African American Female')),
                        }
                        obj['membership']['hispancic'] = {
                            'total':    int_or_none(row.get('Hispanic')),
                            'male':     int_or_none(row.get('Hispanic Male')),
                            'female':   int_or_none(row.get('Hispanic Female')),
                        }
                        obj['membership']['asian'] = {
                            'total':    int_or_none(row.get('Asian')),
                            'male':     int_or_none(row.get('Asian Male')),
                            'female':   int_or_none(row.get('Asian Female')),
                        }
                        obj['membership']['native_american'] = {
                            'total':    int_or_none(row.get('Native American')),
                            'male':     int_or_none(row.get('Native American Male')),
                            'female':   int_or_none(row.get('Native American Female')),
                        }
                        obj['membership']['limited_english_proficient'] = int_or_none(row.get('Limited English Proficient'))
                        obj['membership']['exempt_from_reading_assessment'] = int_or_none(row.get('Number Exempt from Reading Assessment'))
                        obj['membership']['students_with_disabilities'] = int_or_none(row.get('Students with Disabilities'))
                        obj['membership']['free_lunch_eligible'] = int_or_none(row.get('Free eligible'))
                        obj['membership']['reduced_lunch_eligible'] = int_or_none(row.get('Reduced eligible'))
                        obj['membership']['free_reduced_lunch_eligible'] = int_or_none(row.get('Free reduced eligible'))
                        obj['membership']['title_i'] = int_or_none(row.get('Title I'))
                        obj['funding'] = OrderedDict()
                        obj['funding']['per_pupal_expenditures_per_ada'] = int_or_none(row.get('Per Pupil Expenditures per ADA'))
                        obj['funding']['state_per_pupal_expenditures_per_ada'] = int_or_none(row.get('State Per Pupil Expenditures per ADA'))
                        obj['funding']['local_funding_percentage'] = float_or_none(row.get('Local Funding PCT'))
                        obj['funding']['state_funding_percentage'] = float_or_none(row.get('State Funding PCT'))
                        obj['funding']['federal_funding_percentage'] = float_or_none(row.get('Federal Funding PCT'))
                        obj['schools'] = []
                        districts[district_id] = obj

        if os.path.exists(os.path.join(BASE_DIR, folder, 'District_Achievement.csv')):
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'District_Achievement.csv'), 'rU'))
            print 'processing District_Achievement'
            for row in reader:
                district_id = row.get('DISTRICT ID')
                if not district_id == '0':
                    district_id = district_id.lstrip('0')
                if district_id in districts:
                    district = districts[district_id]
                    district['achievements'] = OrderedDict()
                    district['achievements']['math'] = OrderedDict()
                    district['achievements']['math']['3_year_average'] = int_or_none(row.get('Math 3yr Average NCE'))
                    district['achievements']['math']['grade'] = row.get('Math Grade')
                    district['achievements']['math']['trend'] = row.get('Math Trend')
                    district['achievements']['reading'] = OrderedDict()
                    district['achievements']['reading']['3_year_average'] = int_or_none(row.get('Reading 3yr Average NCE'))
                    district['achievements']['reading']['grade'] = row.get('Reading Grade')
                    district['achievements']['reading']['trend'] = row.get('Reading Trend')
                    district['achievements']['social_studies'] = OrderedDict()
                    district['achievements']['social_studies']['3_year_average'] = int_or_none(row.get('Social Studies 3yr Average NCE'))
                    district['achievements']['social_studies']['grade'] = row.get('Social Studies Grade')
                    district['achievements']['social_studies']['trend'] = row.get('Social Studies Trend')
                    district['achievements']['science'] = OrderedDict()
                    district['achievements']['science']['3_year_average'] = int_or_none(row.get('Science 3yravg cur'))
                    district['achievements']['science']['grade'] = row.get('Social Studies Grade')
                    district['achievements']['science']['trend'] = row.get('Social Studies Trend')

                    district['act'] = OrderedDict()
                    district['act']['3_year'] = OrderedDict()
                    district['act']['3_year']['composite'] = float_or_none(row.get('ACT 3yr composite'))
                    district['act']['3_year']['english'] = float_or_none(row.get('ACT 3yr english'))
                    district['act']['3_year']['reading'] = float_or_none(row.get('ACT 3yr Reading'))
                    district['act']['3_year']['math'] = float_or_none(row.get('ACT 3yr math'))
                    district['act']['3_year']['science'] = float_or_none(row.get('ACT 3yr science'))
                    district['act']['1_year'] = OrderedDict()
                    district['act']['1_year']['composite'] = float_or_none(row.get('ACT 1yr composite'))
                    district['act']['1_year']['english'] = float_or_none(row.get('ACT 1yr english'))
                    district['act']['1_year']['reading'] = float_or_none(row.get('ACT 1yr Reading'))
                    district['act']['1_year']['math'] = float_or_none(row.get('ACT 1yr math'))
                    district['act']['1_year']['science'] = float_or_none(row.get('ACT 1yr science'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'District_Attendance_and_Graduation.csv')):
            print 'processing District_Attendance_and_Graduation'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'District_Attendance_and_Graduation.csv'), 'rU'))
            for row in reader:
                district_id = row.get('District')
                if district_id == '000':
                    district_id = '0'
                else:
                    district_id = district_id.lstrip('0')
                if district_id in districts:
                    district = districts[district_id]
                    district['attendance_rate'] = OrderedDict()
                    district['attendance_rate']['k_8'] = float_or_none(row.get('K 8 Attendance Rate PCT'))
                    district['attendance_rate']['overall'] = float_or_none(row.get('Attendance Rate PCT'))
                    district['dropout_rate'] = OrderedDict()
                    district['dropout_rate']['cohort'] = float_or_none(row.get('Cohort Dropout  PCT'))
                    district['dropout_rate']['event'] = float_or_none(row.get('Event Dropout PCT'))
                    district['graduation_rate'] = OrderedDict()
                    district['graduation_rate']['all'] = float_or_none(row.get('All grad rate'))
                    district['graduation_rate']['nclb_percentage'] = float_or_none(row.get('Graduation Rate NCLB PCT'))
                    district['graduation_rate']['white'] = float_or_none(row.get('White grad rate'))
                    district['graduation_rate']['african_american'] = float_or_none(row.get('African American grad rate'))
                    district['graduation_rate']['hispancic'] = float_or_none(row.get('Hispanic grad rate'))
                    district['graduation_rate']['asian'] = float_or_none(row.get('Asian grad rate'))
                    district['graduation_rate']['native_american'] = float_or_none(row.get('Native American grad rate'))
                    district['graduation_rate']['male'] = float_or_none(row.get('Male grad rate'))
                    district['graduation_rate']['female'] = float_or_none(row.get('Female grad rate'))
                    district['graduation_rate']['economically_disadvantaged'] = float_or_none(row.get('Economically Disadvantaged grad rate'))
                    district['graduation_rate']['students_with_disabilities'] = float_or_none(row.get('Students with Disabilities grad rate'))
                    district['graduation_rate']['limited_english_proficient'] = float_or_none(row.get('Limited English Proficient grad rate'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'District_Base.csv')):
            print 'processing District_Base'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'District_Base.csv'), 'rU'))
            for row in reader:
                district_id = row.get('system')
                if district_id == '000':
                    district_id = '0'
                else:
                    district_id = district_id.lstrip('0')
                if district_id in districts:
                    district = districts[district_id]
                    if not district.get('accountability'):
                        district['accountability'] = OrderedDict()
                    subject = row.get('subject').lower()
                    if not subject in district['accountability']:
                        district['accountability'][subject] = OrderedDict()
                    grade = row.get('grade').replace(' through ', '_').replace(' Grades', '').lower()
                    if not grade in district['accountability'][subject]:
                        district['accountability'][subject][grade] = OrderedDict()
                    subgroup = row.get('subgroup').lower().replace(' students', '').replace(' ', '_').replace('/', '_')
                    district['accountability'][subject][grade][subgroup] = OrderedDict()
                    district['accountability'][subject][grade][subgroup]['valid_tests'] = int_or_none(row.get('valid_tests'))
                    district['accountability'][subject][grade][subgroup]['below_basic_percentage'] = float_or_none(row.get('pct_below_bsc'))
                    district['accountability'][subject][grade][subgroup]['below_basic'] = int_or_none(row.get('n_below_bsc'))
                    district['accountability'][subject][grade][subgroup]['basic_percentage'] = float_or_none(row.get('pct_bsc'))
                    district['accountability'][subject][grade][subgroup]['basic'] = int_or_none(row.get('n_bsc'))
                    district['accountability'][subject][grade][subgroup]['proficient_percentage'] = float_or_none(row.get('pct_prof'))
                    district['accountability'][subject][grade][subgroup]['proficient'] = int_or_none(row.get('n_prof'))
                    district['accountability'][subject][grade][subgroup]['advanced_percentage'] = float_or_none(row.get('pct_adv'))
                    district['accountability'][subject][grade][subgroup]['advanced'] = int_or_none(row.get('n_adv'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'State_Base.csv')):
            print 'processing State_Base'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'State_Base.csv'), 'rU'))
            for row in reader:
                district_id = ''
                if district_id in districts:
                    district = districts[district_id]
                    if not district.get('accountability'):
                        district['accountability'] = OrderedDict()
                    subject = row.get('subject').lower()
                    if not subject in district['accountability']:
                        district['accountability'][subject] = OrderedDict()
                    grade = row.get('grade').replace(' through ', '_').replace(' Grades', '').lower()
                    if not grade in district['accountability'][subject]:
                        district['accountability'][subject][grade] = OrderedDict()
                    subgroup = row.get('subgroup').lower().replace(' students', '').replace(' ', '_').replace('/', '_')
                    district['accountability'][subject][grade][subgroup] = OrderedDict()
                    district['accountability'][subject][grade][subgroup]['valid_tests'] = int_or_none(row.get('valid_tests'))
                    district['accountability'][subject][grade][subgroup]['below_basic_percentage'] = float_or_none(row.get('pct_below_bsc'))
                    district['accountability'][subject][grade][subgroup]['below_basic'] = int_or_none(row.get('n_below_bsc'))
                    district['accountability'][subject][grade][subgroup]['basic_percentage'] = float_or_none(row.get('pct_bsc'))
                    district['accountability'][subject][grade][subgroup]['basic'] = int_or_none(row.get('n_bsc'))
                    district['accountability'][subject][grade][subgroup]['proficient_percentage'] = float_or_none(row.get('pct_prof'))
                    district['accountability'][subject][grade][subgroup]['proficient'] = int_or_none(row.get('n_prof'))
                    district['accountability'][subject][grade][subgroup]['advanced_percentage'] = float_or_none(row.get('pct_adv'))
                    district['accountability'][subject][grade][subgroup]['advanced'] = int_or_none(row.get('n_adv'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'School_Master.csv')):
            print 'processing School_Master'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'School_Master.csv'), 'rU'))
            for row in reader:
                lea_id = row.get('LEA Id').lstrip('0')
                if lea_id in districts:
                    district = districts[lea_id]
                    if not district.get('nces_id'):
                        district['nces_id'] = row.get('LEA NCES')
                    school = OrderedDict()
                    school['lea_id'] = row.get('LEA Id').lstrip('0')
                    school['lea_nces_id'] = row.get('LEA NCES')
                    school['nces_id'] = district.get('nces_id') + row.get('SCH NCES')
                    school['id'] = row.get('School No').lstrip('0')
                    school['name'] = row.get('School Name')
                    school['type'] = int_or_none(row.get('Sch Type'))
                    school['url'] = row.get('Wed Address', row.get('Web Address', None))
                    school['phone'] = row.get('Phone')
                    school['mailing_address'] = OrderedDict()
                    school['mailing_address']['street_address'] = row.get('Mailing Add 1')
                    school['mailing_address']['extended_address'] = row.get('Mailing Add 2')
                    school['mailing_address']['locality'] = row.get('City')
                    school['mailing_address']['region'] = row.get('State')
                    school['mailing_address']['postal_code'] = row.get('Zip')
                    school['physical_address'] = OrderedDict()
                    school['physical_address']['street_address'] = row.get('Location Addr 1')
                    school['physical_address']['extended_address'] = row.get('Location Add 2')
                    school['physical_address']['locality'] = row.get('City')
                    school['physical_address']['region'] = row.get('State')
                    school['physical_address']['postal_code'] = row.get('Zip')
                    school['is_charter'] = row.get('Charter Status') == 'YES'

                    schools[school['lea_id'] + school['id']] = school

        if os.path.exists(os.path.join(BASE_DIR, folder, 'School_Profile.csv')):
            print 'processing School_Profile'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'School_Profile.csv'), 'rU'))
            for row in reader:
                school_id = row.get('DISTRICT').lstrip('0') + row.get('SCHOOL NO').lstrip('0')
                if school_id in schools:
                    school = schools[school_id]
                    grades_served = row.get('Grades served', '').replace('Pre-Kindergarten', 'PK').replace('PreK-3-', 'PK-').replace('PreK-4-', 'PK-').replace('Kindergarten', 'K')
                    school['grades_served'] = filter(None, grades_served.strip('-').split('-'))
                    school['safe_school'] = row.get('SAFE SCHOOL') == 'Safe School'
                    school['membership'] = OrderedDict()
                    school['membership']['average_daily'] = int_or_none(row.get('Average Daily Membership'))
                    school['membership']['total'] = int_or_none(row.get('Total'))
                    school['membership']['white'] = {
                        'total':    int_or_none(row.get('White')),
                        'male':     int_or_none(row.get('White Male')),
                        'female':   int_or_none(row.get('White Female')),
                    }
                    school['membership']['african_american'] = {
                        'total':    int_or_none(row.get('African American')),
                        'male':     int_or_none(row.get('African American Male')),
                        'female':   int_or_none(row.get('African American Female')),
                    }
                    school['membership']['hispancic'] = {
                        'total':    int_or_none(row.get('Hispanic')),
                        'male':     int_or_none(row.get('Hispanic Male')),
                        'female':   int_or_none(row.get('Hispanic Female')),
                    }
                    school['membership']['asian'] = {
                        'total':    int_or_none(row.get('Asian')),
                        'male':     int_or_none(row.get('Asian Male')),
                        'female':   int_or_none(row.get('Asian Female')),
                    }
                    school['membership']['native_american'] = {
                        'total':    int_or_none(row.get('Native American')),
                        'male':     int_or_none(row.get('Native American Male')),
                        'female':   int_or_none(row.get('Native American Female')),
                    }
                    school['membership']['limited_english_proficient'] = int_or_none(row.get('Limited English Proficient'))
                    school['membership']['exempt_from_reading_assessment'] = int_or_none(row.get('Number Exempt from Reading Assessment'))
                    school['membership']['students_with_disabilities'] = int_or_none(row.get('Students with Disabilities'))
                    school['membership']['free_lunch_eligible'] = int_or_none(row.get('Free eligible'))
                    school['membership']['reduced_lunch_eligible'] = int_or_none(row.get('Reduced eligible'))
                    school['membership']['free_reduced_lunch_eligible'] = int_or_none(row.get('Free reduced eligible'))
                    school['membership']['title_i'] = int_or_none(row.get('Title I'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'School_Base.csv')):
            print 'processing School_Base'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'School_Base.csv'), 'rU'))
            for row in reader:
                school_id = row.get('system').lstrip('0') + row.get('school').lstrip('0')
                if school_id in schools:
                    school = schools[school_id]
                    if not school.get('accountability'):
                        school['accountability'] = OrderedDict()
                    subject = row.get('subject').lower()
                    if not subject in school['accountability']:
                        school['accountability'][subject] = OrderedDict()
                    grade = row.get('grade').replace(' through ', '_').replace(' Grades', '').lower()
                    if not grade in school['accountability'][subject]:
                        school['accountability'][subject][grade] = OrderedDict()
                    subgroup = row.get('subgroup').lower().replace(' students', '').replace(' ', '_').replace('/', '_')
                    school['accountability'][subject][grade][subgroup] = OrderedDict()
                    school['accountability'][subject][grade][subgroup]['valid_tests'] = int_or_none(row.get('valid_tests'))
                    school['accountability'][subject][grade][subgroup]['below_basic_percentage'] = float_or_none(row.get('pct_below_bsc'))
                    school['accountability'][subject][grade][subgroup]['below_basic'] = float_or_none(row.get('n_below_bsc'))
                    school['accountability'][subject][grade][subgroup]['basic_percentage'] = float_or_none(row.get('pct_bsc'))
                    school['accountability'][subject][grade][subgroup]['basic'] = float_or_none(row.get('n_bsc'))
                    school['accountability'][subject][grade][subgroup]['proficient_percentage'] = float_or_none(row.get('pct_prof'))
                    school['accountability'][subject][grade][subgroup]['proficient'] = float_or_none(row.get('n_prof'))
                    school['accountability'][subject][grade][subgroup]['advanced_percentage'] = float_or_none(row.get('pct_adv'))
                    school['accountability'][subject][grade][subgroup]['percentage'] = float_or_none(row.get('n_adv'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'School_Achievement.csv')):
            print 'processing School_Achievement'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'School_Achievement.csv'), 'rU'))
            for row in reader:
                school_id = row.get('DISTRICT ID').lstrip('0') + row.get('SCHOOL ID').lstrip('0')
                if school_id in schools:
                    school = schools[school_id]
                    school['achievements'] = OrderedDict()
                    school['achievements']['math'] = OrderedDict()
                    school['achievements']['math']['3_year_average'] = int_or_none(row.get('Math 3yr Average NCE'))
                    school['achievements']['math']['grade'] = row.get('Math Grade')
                    school['achievements']['math']['trend'] = row.get('Math Trend')
                    school['achievements']['reading'] = OrderedDict()
                    school['achievements']['reading']['3_year_average'] = int_or_none(row.get('Reading 3yr Average NCE'))
                    school['achievements']['reading']['grade'] = row.get('Reading Grade')
                    school['achievements']['reading']['trend'] = row.get('Reading Trend')
                    school['achievements']['social_studies'] = OrderedDict()
                    school['achievements']['social_studies']['3_year_average'] = int_or_none(row.get('Social Studies 3yr Average NCE'))
                    school['achievements']['social_studies']['grade'] = row.get('Social Studies Grade')
                    school['achievements']['social_studies']['trend'] = row.get('Social Studies Trend')
                    school['achievements']['science'] = OrderedDict()
                    school['achievements']['science']['3_year_average'] = int_or_none(row.get('Science 3yravg cur'))
                    school['achievements']['science']['grade'] = row.get('Social Studies Grade')
                    school['achievements']['science']['trend'] = row.get('Social Studies Trend')

                    school['act'] = OrderedDict()
                    school['act']['3_year'] = OrderedDict()
                    school['act']['3_year']['composite'] = float_or_none(row.get('ACT 3yr composite'))
                    school['act']['3_year']['english'] = float_or_none(row.get('ACT 3yr english'))
                    school['act']['3_year']['reading'] = float_or_none(row.get('ACT 3yr Reading'))
                    school['act']['3_year']['math'] = float_or_none(row.get('ACT 3yr math'))
                    school['act']['3_year']['science'] = float_or_none(row.get('ACT 3yr science'))
                    school['act']['1_year'] = OrderedDict()
                    school['act']['1_year']['composite'] = float_or_none(row.get('ACT 1yr composite'))
                    school['act']['1_year']['english'] = float_or_none(row.get('ACT 1yr english'))
                    school['act']['1_year']['reading'] = float_or_none(row.get('ACT 1yr Reading'))
                    school['act']['1_year']['math'] = float_or_none(row.get('ACT 1yr math'))
                    school['act']['1_year']['science'] = float_or_none(row.get('ACT 1yr science'))

        if os.path.exists(os.path.join(BASE_DIR, folder, 'School_Attendance_and_Graduation.csv')):
            print 'processing School_Attendance_and_Graduation'
            reader = csv.DictReader(open(os.path.join(BASE_DIR, folder, 'School_Attendance_and_Graduation.csv'), 'rU'))
            for row in reader:
                school_id = row.get('District').lstrip('0') + row.get('SCHOOL ID').lstrip('0')
                if school_id in schools:
                    school = schools[school_id]
                    school['promotion_rate'] = OrderedDict()
                    school['promotion_rate']['k_8'] = float_or_none(row.get('K-8 Promotion Rate %'))
                    school['attendance_rate'] = OrderedDict()
                    school['attendance_rate']['k_8'] = float_or_none(row.get('K-8 Attendance Rate %'))
                    school['attendance_rate']['overall'] = float_or_none(row.get('Attendance Rate %'))
                    school['dropout_rate'] = OrderedDict()
                    school['dropout_rate']['cohort'] = float_or_none(row.get('Cohort Dropout %'))
                    school['dropout_rate']['event'] = float_or_none(row.get('Event Dropout %'))
                    school['graduation_rate'] = OrderedDict()
                    school['graduation_rate']['all'] = float_or_none(row.get('All grad rate'))
                    school['graduation_rate']['nclb_percentage'] = float_or_none(row.get('Graduation Rate NCLB %'))
                    school['graduation_rate']['white'] = float_or_none(row.get('White grad rate'))
                    school['graduation_rate']['african_american'] = float_or_none(row.get('African American grad rate'))
                    school['graduation_rate']['hispancic'] = float_or_none(row.get('Hispanic grad rate'))
                    school['graduation_rate']['asian'] = float_or_none(row.get('Asian grad rate'))
                    school['graduation_rate']['native_american'] = float_or_none(row.get('Native American grad rate'))
                    school['graduation_rate']['male'] = float_or_none(row.get('Male grad rate'))
                    school['graduation_rate']['female'] = float_or_none(row.get('Female grad rate'))
                    school['graduation_rate']['economically_disadvantaged'] = float_or_none(row.get('Economically Disadvantaged grad rate'))
                    school['graduation_rate']['students_with_disabilities'] = float_or_none(row.get('Students with Disabilities grad rate'))
                    school['graduation_rate']['limited_english_proficient'] = float_or_none(row.get('Limited English Proficient grad rate'))

districts_by_nces = OrderedDict()
schools_by_nces = OrderedDict()

statewide = districts['0']
del districts['0']
statewide['districts'] = []

print 'sorting districts'
for district_id in sorted(districts.keys()):
    district = districts[district_id]
    districts_by_nces[district.get('nces_id')] = district
    statewide['districts'].append({
        "name": district.get('name'),
        "nces_id": district.get('nces_id'),
    })

print 'sorting schools'
for school_id in sorted(schools.keys()):
    school = schools[school_id]
    schools_by_nces[school.get('nces_id')] = school
    if school.get('lea_nces_id') in districts_by_nces:
        district = districts_by_nces[school.get('lea_nces_id')]
        district['schools'].append({
            "name": school.get('name'),
            "nces_id": school.get('nces_id'),
        })
        statewide['schools'].append({
            "name": school.get('name'),
            "nces_id": school.get('nces_id'),
            "district_nces_id": school.get('lea_nces_id'),
        })

print 'outputting statewide'
f = open(os.path.join(DATA_DIR, 'statewide.yml'), 'w')
f.write(pyaml.dump(statewide))
f.close()

f = open(os.path.join(API_DIR, 'statewide.json'), 'w')
f.write(json.dumps(statewide))
f.close()

print 'outputting districts'
f = open(os.path.join(DATA_DIR, 'districts.yml'), 'w')
f.write(pyaml.dump(statewide.get('districts', [])))
f.close()

f = open(os.path.join(API_DIR, 'districts.json'), 'w')
f.write(json.dumps(statewide.get('districts', [])))
f.close()

print 'outputting schools'
f = open(os.path.join(DATA_DIR, 'schools.yml'), 'w')
f.write(pyaml.dump(statewide.get('schools', [])))
f.close()

f = open(os.path.join(API_DIR, 'schools.json'), 'w')
f.write(json.dumps(statewide.get('schools', [])))
f.close()

if not os.path.exists(os.path.join(API_DIR, 'districts')):
    os.mkdir(os.path.join(API_DIR, 'districts'))
if not os.path.exists(os.path.join(API_DIR, 'schools')):
    os.mkdir(os.path.join(API_DIR, 'schools'))

print 'outputting individual districts'
for district_id in districts_by_nces:
    district = districts_by_nces[district_id]
    if district_id:
        f = open(os.path.join(API_DIR, 'districts', '%s.json' % district_id), 'w')
        f.write(json.dumps(district))
        f.close()

print 'outputting individual schools'
for school_id in schools_by_nces:
    school = schools_by_nces[school_id]
    if school_id:
        f = open(os.path.join(API_DIR, 'schools', '%s.json' % school_id), 'w')
        f.write(json.dumps(school))
        f.close()
