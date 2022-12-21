from datetime import datetime

ZodiacalSigns = [
	'aries', 'libra', 'tauro',
	'escorpio', 'geminis', 'sagitario',
	'cancer', 'capricornio', 'leo',
	'acuario', 'virgo', 'piscis'
]


def getOld(nacDate: str):
    today = datetime.now()
    birthday = datetime.strptime(nacDate, "%Y-%m-%d")
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def todayDate(date: str):
    today_year = datetime.now()
    return f'{date} del año {today_year.year}'


def getSign(nacDate: str):
    month = int(nacDate.split('-')[1])
    day = int(nacDate.split('-')[2])

    if ((day >= 21 and month == 3) or (day <= 20 and month == 4)):
        sign = 0
    elif ((day >= 24 and month == 9) or (day <= 23 and month == 10)):
        sign = 1
    elif ((day >= 21 and month == 4) or (day <= 21 and month == 5)):
        sign = 2
    elif ((day >= 24 and month == 10) or (day <= 22 and month == 11)):
        sign = 3
    elif ((day >= 22 and month == 5) or (day <= 21 and month == 6)):
        sign = 4
    elif ((day >= 23 and month == 11) or (day <= 21 and month == 12)):
        sign = 5
    elif ((day >= 21 and month == 6) or (day <= 23 and month == 7)):
        sign = 6
    elif ((day >= 22 and month == 12) or (day <= 20 and month == 1)):
        sign = 7
    elif ((day >= 24 and month == 7) or (day <= 23 and month == 8)):
        sign = 8
    elif ((day >= 21 and month == 1) or (day <= 19 and month == 2)):
        sign = 9
    elif ((day >= 24 and month == 8) or (day <= 23 and month == 9)):
        sign = 10
    elif ((day >= 20 and month == 2) or (day <= 20 and month == 3)):
        sign = 11

    return ZodiacalSigns[sign].capitalize()


def getLetters(word):
    vocals = 'aeouiAEOUI'
    constants = 'bcdfghjklmnñpqrstvwxyzBCDFGHJKLMNÑPQRSTVWXYZ'
    vocals_word = set([c for c in word if c in vocals])
    consts_word = set([c for c in word if c in constants])
    return {'Vocales': len(vocals_word), 'Consonantes': len(consts_word)}


def getIRS(salary: float):
    anual = salary*12
    if (anual < 416220.00):
        escala = 0
        retencion = 0
        exdente = 0
    elif (anual > 416220.00 and anual < 624329.00):
        escala = 0.15
        retencion = 0
        exdente = anual - 416220.00
    elif (anual > 624329.00 and anual < 867123.01):
        escala = 0.20
        retencion = 31216.01
        exdente = anual - 624329.00
    elif (anual > 867123.01):
        escala = 0.25
        retencion = 79776.00
        exdente = anual - 867123.01

    isr = (exdente * escala) + retencion
    return {'ISR Mensual': round(isr/12, 2)}


def getLiteral(nota: int):
    if (nota >= 90):
        literal = 'A'
    elif (nota >= 80 and nota <= 89):
        literal = 'B'
    elif (nota >= 70 and nota <= 79):
        literal = 'C'
    elif (nota <= 69):
        literal = 'F'

    return {'Calificacion Literal': literal}


def Zod_or_Date(zodiac: str):
    posYear = zodiac.split('-')[0]
    if (posYear.isdigit()):
        NewZodiac = getSign(zodiac).lower()
        return NewZodiac
    else:
        if zodiac in ZodiacalSigns:
            return zodiac
