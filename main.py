from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

#Q1

class StudentNumber(BaseModel):
    student_number: str


def Student_Number(student_number: str):
    if len(student_number) != 11:
        raise HTTPException(detail="Student number must be equal to 11 digits.",status_code=status.HTTP_400_BAD_REQUEST)

    if not (400 <= int(student_number[:3]) <= 402):
        raise HTTPException(detail="The first three digits must be between 400 and 402.",status_code=status.HTTP_404_NOT_FOUND)

    if int(student_number[3:9]) != 114150:
        raise HTTPException(detail="The middle digits must be 114150.",status_code=status.HTTP_403_FORBIDDEN)

    if not (1 <= int(student_number[9:]) <= 99):
        raise HTTPException(detail="The last two digits must be between 01 and 99.",status_code=status.HTTP_404_NOT_FOUND)
    return student_number


@app.get("/student_number/{student_number}")
def index(student_number: str):   #path Parameter
    if Student_Number(student_number) == student_number:
        return {"message": f"student number is valid: {student_number}"}


@app.get("/student_number/")
def index(student_number: str):   #Query Parameter
    if Student_Number(student_number) == student_number:
        return {"message": f"student number is valid: {student_number}"}


@app.post("/student_number/")
def index(num: StudentNumber):    #Request Body
    number = Student_Number(num.student_number)
    if Student_Number(number) == number:
        return {"message": f"student number is valid: {number}"}

#Q2

persian_letters = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
forbidden_letters = "|\؟!@#$%^&*()_+=-`~}{][';:/?.؟×!>,<1234567890"


class UserName(BaseModel):
    name: str


def UserName(name: str):
    if not name:
        raise HTTPException(detail="Inter a name", status_code=status.HTTP_400_BAD_REQUEST)
    if len(name) > 10:
        raise HTTPException(detail="Name must be less than 11 digits.", status_code=status.HTTP_400_BAD_REQUEST)
    for char in name:
        if char in forbidden_letters:
            raise HTTPException(detail="using of numbers and special symbols is forbidden", status_code=status.HTTP_403_FORBIDDEN)
        if char not in persian_letters:
            raise HTTPException(detail="Name must be in Persian", status_code=status.HTTP_404_NOT_FOUND)
    return name

@app.get("/name/{name}")
def index(name:UserName):
    name = name.name
    if UserName(name) == name:
        return {"message": f"name is valid: {name}"}

#Q3

def kabise(year: int, month: int, day: int):
    days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

    if (year % 33 == 1 or year % 33 == 5 or year % 33 == 9 or
            year % 33 == 13 or year % 33 == 17 or year % 33 == 22 or
            year % 33 == 26 or year % 33 == 30):  #بررسی کبیسه بودن سال مورد نظر
        days_in_month[11] = 30  #در سال کبیسه اسفند ماه 30 روز دارد

    if 1 <= month <= 12 and 1 <= day <= days_in_month[month - 1]:
        return True
    return False

def valid_date(birth_date: str):
    if len(birth_date) == 10 and birth_date[4] == '/' and birth_date[7] == '/':
        year, month, day = birth_date.split('/')
        if year.isdigit() and month.isdigit() and day.isdigit():
            return birth_date
    raise HTTPException(detail="فرمت تاریخ یا مقادیر وارد شده معتبر نیست.", status_code=status.HTTP_404_NOT_FOUND)


@app.get("/birthdate/{birthdate}")
def index(birth_date: str):
    if valid_date(birth_date) == birth_date:
        return {"message": f"Birth date is valid: {birth_date}"}

#Q4

def Serial_number(serial_number: str):
    if len(serial_number) != 10:
        raise HTTPException(detail="Serial number must be equal to 10 digits.",status_code=status.HTTP_400_BAD_REQUEST)

    if serial_number[0] not in persian_letters:
        raise HTTPException(detail="The 1st digit must be a Persian letter.", status_code=status.HTTP_403_FORBIDDEN)

    region_code = serial_number[1:3]  #یک عدد دو رقمی
    unique_number = serial_number[4:] #یک عدد شش رقمی

    if serial_number[3] != "/":
        raise HTTPException(detail="invalid parameter. 4th digit must be /.",status_code=status.HTTP_403_FORBIDDEN)

    if not region_code.isdigit() or not (1 <= int(region_code) <= 99):
        raise HTTPException(detail="The 2nd and 3rd digits must be number between 01 and 99.", status_code=status.HTTP_404_NOT_FOUND)

    if not unique_number.isdigit() or not (1 <= int(unique_number) <= 999999):
        raise HTTPException(detail="The last 6 digits must be number between 000001 and 999999.", status_code=status.HTTP_404_NOT_FOUND)
    return serial_number

@app.get("/serial_number/{serial_number}")
def index(serial_number: str):
    if Serial_number(serial_number) == serial_number:
        return {"message": f"student number is valid: {serial_number}"}

#Q5

valid_province = "اردبیل زنجان کرمانشاه ایلام همدان بوشهر تهران یزد اصفهان کرمان سمنان قم قزوین"

def valid_provinces(province: str):
    if province not in valid_province:
        raise HTTPException(detail="province name is not valid", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return province

@app.get("/province/{province}")
def index(province: str):
    if valid_provinces(province) == province:
        return {"message": f"Province name is valid:{province}"}

#Q6

valid_city = ["کاشان", "گلپایگان", "لنجان", "مبارکه", "نائین", "نجف‌آباد", "نطنز", "بهمئی", "دنا", "گچساران",
"آبیک", "بوئین‌زهرا", "تاکستان", "قزوین",
"آستارا", "آستانه‌اشرفیه", "اَملَش", "بندرانزلی", "رشت", "رضوانشهر", "رودبار", "رودسر",
"سیاهکل", "شفت", "صومعه‌سرا", "طوالش", "فومن", "لاهیجان", "لنگرود", "ماسال",
"اردبیل", "بیله‌سوار", "پارس‌آباد", "خلخال", "سرعین", "کوثر", "گِرمی", "مِشگین‌شهر", "نَمین", "نیر",
"ابهر", "ایجرود", "خدابنده", "خرمدره", "زنجان", "طارم", "ماه‌نشان",
"اسکو", "اهر", "بستان‌آباد", "بناب", "تبریز", "جلفا", "چاراویماق", "سراب", "شبستر", "عجب‌شیر", "کلیبر", "مراغه", "مرند", "ملکان", "میانه", "ورزقان", "هریس", "هشترود",
"ارومیه", "اشنویه", "بوکان", "پیرانشهر", "تکاب", "چالدران", "خوی", "سردشت", "سلماس", "شاهین‌دژ", "ماکو", "مهاباد", "میاندوآب", "نقده",
"بانه", "بیجار", "دیواندره", "سروآباد", "سقز", "سنندج", "قروه", "کامیاران", "مریوان",
"اسلام‌آباد غرب", "پاوه", "ثلاث باباجانی", "جوانرود", "دالاهو", "روانسر", "سرپل ذهاب", "سنقر", "صحنه", "قصر شیرین", "کرمانشاه", "کنگاور", "گیلانغرب", "هرسین",
"آبدانان", "ایلام", "ایوان", "دره‌شهر", "دهلران", "شیروان و چرداول", "مهران",
"آستانه", "الیگودرز", "بروجرد", "پل‌دختر", "خرم‌آباد", "دورود", "دلفان", "سلسله", "کوهدشت",
"آباده", "ارسنجان", "استهبان", "اقلید", "بوانات", "پاسارگاد", "جهرم", "خرم‌بید", "خنج", "داراب", "زرین‌دشت", "سپیدان", "شیراز", "فراشبند", "فسا", "فیروزآباد", "قیر و کارزین", "کازرون", "لارستان", "لامِرد", "مرودشت", "مُهر", "ممسنی", "میمند", "نی‌ریز",
"بافت", "بردسیر", "بم", "جیرفت", "رابر", "راور", "رفسنجان", "رودبار جنوب", "زرند", "سیرجان", "شهر بابک", "عنبرآباد", "قلعه گنج", "کرمان", "کوهبنان", "کهنوج", "منوجان",
"اسفراین", "بجنورد", "جاجرم", "شیروان", "فاروج",
"آزادشهر", "آق‌قلا", "بندر گز", "ترکمن", "رامیان", "علی‌آباد", "کردکوی", "کلاله", "گرگان", "گنبد کاووس", "مراوه‌تپه", "مینودشت",
"آمل", "بابل", "بابلسر", "بهشهر", "تنکابن", "جویبار", "چالوس", "رامسر", "ساری", "سوادکوه", "قائم‌شهر", "گلوگاه", "محمودآباد", "نکا", "نور", "نوشهر",
"اراک", "آشتیان", "تفرش", "خمین", "دلیجان", "زرندیه", "ساوه", "شازند", "کمیجان", "محلات",
"ابوموسی", "بستک", "بندر عباس", "بندر لنگه", "جاسک", "حاجی‌آباد", "خمیر", "رودان", "قشم", "گاوبندی", "میناب",
"اردستان", "اصفهان", "برخوار", "تیران و کرون", "چادگان", "خمینی‌شهر", "خوانسار", "سمیرم", "شاهین‌شهر و میمه", "شهرضا", "سده لنجان", "فلاورجان"]

def Valid_city(city: str):
    if city not in valid_city:
        raise HTTPException(detail="city name is not valid", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return city

@app.get("/city/{city}")
def index(city: str):
    if Valid_city(city) == city:
        return {"message": f"City name is valid:{city}"}

#Q7

class Address(BaseModel):
    address: str

def useraddress(address: str):
    if not address:
        raise HTTPException(detail="Inter an address.", status_code=status.HTTP_400_BAD_REQUEST)
    if len(address) > 100:
        raise HTTPException(detail="Address too long. Its must be less than 100 digits.", status_code=status.HTTP_400_BAD_REQUEST)
    if len(address) < 10:
        raise HTTPException(detail="Address too short. Its must be more than 10 digits.", status_code=status.HTTP_400_BAD_REQUEST)
    return address

@app.get("/address/{address}")
def index(add: Address):
    if useraddress(add.address) == add.address:
        return {"message": f"Your address is: {add.address} "}

#Q8

class PostNumber(BaseModel):
    post_number: str

def Postnumber(post_number: str):
    if not post_number.isdigit() or len(post_number) != 10:
        raise HTTPException(detail="Post number invalid. Its must be numbers and be 10 digits.", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return post_number

@app.get("/post_number/{post_number}")
def index(post: PostNumber):
    if Postnumber(post.post_number) == post.post_number:
        return {"message": f"student number is valid: {post.post_number}"}

#Q9

class PhoneNum(BaseModel):
    phone: str

def Phone(phone: str):
    if len(phone) != 13:
        raise HTTPException(detail="Phone number must be equal to 13 digits.",status_code=status.HTTP_400_BAD_REQUEST)
    if phone[:3] != "098":
        raise HTTPException(detail="The 1st part of number must be 098.", status_code=status.HTTP_403_FORBIDDEN)

    region_number1 = phone[3:6]   #اولین عدد سه رقمی(پیش شماره)
    region_number2 = phone[6:9]   #دومین عدد سه رقمی(اعداد میانی)
    unique_number = phone[9:]     #چهار رقم آخر

    if not region_number1.isdigit() or not 900 <= int(region_number1) <= 999:
        raise HTTPException(detail="The 2nd part of number must be between 900 and 999.", status_code=status.HTTP_400_BAD_REQUEST)
    if not region_number2.isdigit() or not 000 <= int(region_number2) <= 999:
        raise HTTPException(detail="The 3rd part of number must be between 100 and 999.", status_code=status.HTTP_400_BAD_REQUEST)
    if not unique_number.isdigit() or not 0000 <= int(unique_number) <= 9999:
        raise HTTPException(detail="The  last 4 digits of number must be between 1000 and 9999.", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return phone

@app.get("/phone/{phone}")
def index(num: PhoneNum):
    number = num.number
    if Phone(number) == number:
        return {"message": f"Your phone number is valid:, {number} "}

#Q10

code_number = ["041", '044', '045', '031', '026', '084', '077', '021', '038', '056', '051', '058', '061', '024', '023', "054",
               " 071", "028", "025", "087", '034', "083", "074", '017', '013', '066', '011', '086', '076', '081', "035"]
code_number2 = ["33", "32", "34", "42", "43", "44", "52", "53", "54", "50", "40", "30", "36"]

class telephone(BaseModel):
    telephone: str

def Telephone(telephone: str):
    if len(telephone) != 11:
        raise HTTPException(detail="Phone number must be equal to 11 digits.",status_code=status.HTTP_400_BAD_REQUEST)
    if telephone[:3] not in code_number:
        raise HTTPException(detail="The 1st part of number must be in code numbers.", status_code=status.HTTP_403_FORBIDDEN)

    region_number1 = telephone[3:5]   #اولین عدد دو رقمی(کد شهر)
    region_number2 = telephone[5:7]   #دومین عدد دو رقمی
    unique_number = telephone[7:]     #چهار رقم آخر

    if not region_number1.isdigit() or not region_number1 in code_number2:
        raise HTTPException(detail="The 2nd part of number must be in valid coded.", status_code=status.HTTP_400_BAD_REQUEST)
    if not region_number2.isdigit() or not 10 <= int(region_number2) <= 99:
        raise HTTPException(detail="The 3rd part of number must be between 10 and 99.", status_code=status.HTTP_400_BAD_REQUEST)
    if not unique_number.isdigit() or not 0000 <= int(unique_number) <= 9999:
        raise HTTPException(detail="The  last 4 digits of number must be between 1000 and 9999.", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return telephone

@app.get("/telephone/{telephone}")
def index(num: telephone):
    number = num.telephone
    if Telephone(number) == number:
        return {"message": f"Your phone number is valid:, {number} "}

#Q11

valid_collage = ["علم انسانی","فنی و مهندسی","علوم پایه","دامپزشکی", "اقتصاد","کشاورزی","منابع طبیعی"]

def Collage(collage: str):
    if collage not in valid_collage:
        raise HTTPException(detail="collage name is not valid", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return collage

@app.get("/collage/{collage}")
def index(collage: str):
    if Collage(collage) == collage:
        return {"message": f"collage name is valid:{collage}"}

#Q12

valid_lesson = ["مهندسی عمران","مهندسی هوافضا","مهندسی صنایع","مهندسی مکانیک",
                "مهندسی نفت", "مهندسی کامپیوتر","مهندسی معماری","مهندسی برق"]

def Lesson(lesson: str):
    if lesson not in valid_lesson:
        raise HTTPException(detail="lesson name is not valid", status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return lesson

@app.get("/lesson/{lesson}")
def index(lesson: str):
    if Lesson(lesson) == lesson:
        return {"message": f"lesson name is valid:{lesson}"}

#Q13

valid_input = "مجرد  متاهل"

class Marital(BaseModel):
    marital: str

def marital(marital: str):
    if not marital:
        raise HTTPException(detail="وضعیت تاهل خود را وارد کنید. ", status_code=status.HTTP_404_NOT_FOUND)
    if marital not in valid_input:
        raise HTTPException(detail="ورودی نامعتبر است. محدداً امتحان کنید", status_code=status.HTTP_404_NOT_FOUND)
    else:
        return marital

@app.get("/marital/{marital}")
def index(pre: Marital):
    if marital(pre.marital) == pre.marital:
        return {f" وضعیت تاهل: {pre.marital}"}

#Q14

def valid_code(CodeMelli: str):
    if not CodeMelli.isdigit() or len(CodeMelli) != 10:
        raise HTTPException(detail="code melli must be number and 10 digits", status_code=status.HTTP_400_BAD_REQUEST)

    if CodeMelli.count(CodeMelli[0]) == len(CodeMelli): #شرط تکراری نبود ارقام
        raise HTTPException(detail="code melli is invalid", status_code=status.HTTP_400_BAD_REQUEST)

    total = sum(int(CodeMelli[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    check_digit = int(CodeMelli[9])

    if remainder < 2 and check_digit == remainder:
        return True
    elif CodeMelli == "0123456789":
        return False        
    elif remainder >= 2 and check_digit == 11 - remainder:
        return True
    else:
        return False


@app.get("/CodeMelli/{CodeMelli}")
def index(CodeMelli: str):
    if valid_code(CodeMelli) == True:
        return {"massage": "code melli is Valid"}
    else:
        raise HTTPException(detail="code melli is Invalid", status_code=status.HTTP_404_NOT_FOUND)


#Q15

class Data(BaseModel):
    student_number: str
    name: str
    birth_date: str
    serial_number: str
    province: str
    city: str
    address: str
    post_number: str
    phone: str
    telephone: str
    college: str
    lesson: str
    marital: str
    CodeMelli: str


@app.post("/general")
def general(data: Data):
     errors = []

    student_number_error = Student_Number(data.student_number)
    if student_number_error != data.student_number:
        errors.append(student_number_error)

    username_error = UserName(data.name)
    if username_error != data.name:
        errors.append(username_error)

    date_error = valid_date(data.birth_date)
    if date_error != data.birth_date:
        errors.append(date_error)

    serial_number_error = Serial_number(data.serial_number)
    if serial_number_error != data.serial_number:
        errors.append(serial_number_error)

    province_error = valid_provinces(data.province)
    if province_error != data.province:
        errors.append(province_error)

    city_error = Valid_city(data.city)
    if city_error != data.city:
        errors.append(city_error)

    address_error = useraddress(data.address)
    if address_error != data.address:
        errors.append(address_error)

    PostNumber_error = Postnumber(data.post_number)
    if PostNumber_error != data.post_number:
        errors.append(PostNumber_error)

    phone_error = Phone(data.phone)
    if phone_error != data.phone:
        errors.append(phone_error)

    telephone_error = Telephone(data.telephone)
    if telephone_error != data.telephone:
        errors.append(telephone_error)

    collage_error = Collage(data.college)
    if collage_error != data.college:
        errors.append(collage_error)

    lesson_error = Lesson(data.lesson)
    if lesson_error != data.lesson:
        errors.append(lesson_error)

    marital_error = marital(data.marital)
    if marital_error != data.marital:
        errors.append(marital_error)

    Codemelli_error = valid_code(data.CodeMelli)
    if Codemelli_error != data.CodeMelli:
        errors.append(Codemelli_error)

    if errors:
        return {"errors": errors}
    else:
        return {"massage": "No errors found"}
