from wtforms import Field
from wtforms.widgets import TextInput
from datetime import datetime
from helpers import convert_to_bytes, str2timedelta, filesize2human


class SDateTimeField(Field):
    widget = TextInput()

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return self.data.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return u''

    def process_formdata(self, valuelist):
        try:
            self.data = datetime.strptime(valuelist[0], "%d/%m/%Y %H:%M:%S")
        except Exception as e:
            self.data = None
            raise ValueError(
                "O valor deve ser um valor de data/hora válido (ex: 12/12/2019 12:15:13)")


class STimeIntervalField(Field):
    widget = TextInput()

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return str(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        try:
            self.data = str2timedelta(valuelist[0])
        except Exception as e:
            self.data = None
            raise ValueError(
                'O campo deve conter um valor de tempo (ex: 01:02:13)')


class SFileSizeField(Field):
    widget = TextInput()

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return filesize2human(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        try:
            self.data = convert_to_bytes(valuelist[0])
        except Exception as e:
            self.data = None
            raise ValueError(
                'O campo deve conter um valor numérico e uma unidade (ex: 50B, 12KB, 30MB, 2,6GB)')
