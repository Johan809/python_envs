import io
import uuid
import zipfile
from datetime import datetime

def getOld(nacDate: str):
    today = datetime.now()
    birthday = datetime.strptime(nacDate, "%Y-%m-%d")
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def getSign(nacDate: datetime.date):
    month = nacDate.month
    day = nacDate.day

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


def getDate(_date: str):
    if "-" in _date:
        withDash = int(_date.split('-')[0])
        if withDash > 1000:
            resultDate = datetime.strptime(_date, "%Y-%m-%d")
            return resultDate
        elif withDash <= 31:
            resultDate = datetime.strptime(_date, "%d-%m-%Y")
            return resultDate

    elif "/" in _date:
        withSlash = int(_date.split('/')[0])
        if withSlash > 1000:
            resultDate = datetime.strptime(_date, "%Y/%m/%d")
            return resultDate
        elif withSlash <= 31:
            resultDate = datetime.strptime(_date, "%d/%m/%Y")
            return resultDate


def generate_token():
    return str(uuid.uuid4()).replace('-', '')


def serverAnswer(status: bool, msg: str, args={}):
    _arg = False
    if args != {}:
        _arg = True
    a = {'ok': status, 'msg': msg, 'arg': args}
    b = {'ok': status, 'msg': msg}
    return a if _arg else b

def zipfiles(filenames):
    zip_filename = "archive.zip"

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)

        # Add file, at correct path
        zf.write(fpath, fname)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp
