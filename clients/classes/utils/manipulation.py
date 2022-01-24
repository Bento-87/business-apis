import datetime
class Convert():

    def ToDateTime(_datetime, _format='%a, %d %b %Y %H:%M:%S %Z'):
        return datetime.datetime.strptime(_datetime, _format)

    def ToDate(_date, _format='%Y-%m-%d'):
        return datetime.datetime.strptime(_date, _format).date()
    
    def DateTimeToDate(_datetime):
        if "datetime" not in str(type(_datetime)):
            return "Necessario um objeto do tipo datetime"
        return datetime.date(_datetime.year, _datetime.month, _datetime.day)

    def DateToString(_date, _format='%Y-%m-%d'):
        if "datetime.datetime" in str(type(_date)):
            return datetime.date(_date.year, _date.month, _date.day).strftime(_format)
        elif "datetime.date" in str(type(_date)):
            return datetime.datetime(_date.year, _date.month, _date.day).strftime(_format)

    def DateToDateTime(_datetime):
        if "datetime.date" not in str(type(_datetime)):
            return "Necessario um objeto do tipo date"
        return datetime.datetime(_datetime.year, _datetime.month, _datetime.day)

    def TypeDate (_date):
        #Verifica se é um date nos tipos predefinidos, usando uma string
        try:
            if "datetime.date" in str(type(Convert.ToDate(_date))):
                return "date"
        except:
            None
        try:
            if "datetime.date" in str(type(Convert.ToDate(_date,'%d-%m-%Y'))):
                return "datef"
        except:
            None
        try:
            if "datetime.date" in str(type(Convert.ToDateTime(_date))):
                return "datetime"
        except:
            None

class Validation():

    def ValDate(date):
        if Convert.TypeDate(date) == "date":
            return date
        elif Convert.TypeDate(date) == "datef":
            return Convert.ToDate(date,'%d-%m-%Y')
        elif Convert.TypeDate(date) == "datetime":
            return Convert.DateTimeToDate(Convert.ToDateTime(date))
        else:
            return None

   