from com.sun.star.beans import PropertyValue


def dictToProperties(dictionary):  # normally I'd just import this
    """
    Utitlity to convert a dictionary to properties
    """
    props = []
    for key in dictionary:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = dictionary[key]
        props.append(prop)
    return tuple(props)