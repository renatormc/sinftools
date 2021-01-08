from pyexcel_ods import get_data

data = get_data("/home/renato/Temp/laudo/data/data.ods")
var  = data['Variables'][0]
print(type(var))
