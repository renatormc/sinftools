class GlobalFunctions:

    @staticmethod
    def to_table(value, per_row):
        return [value[i * per_row:(i + 1) * per_row] for i in range((len(value) + per_row - 1) // per_row)]

    @staticmethod
    def remove_nulls(items, attrib):
        res = []
        for item in items:
            if item is None:
                continue
            if isinstance(item, dict):
                if item[attrib] is not None:
                    res.append(item)
                continue
            if getattr(item, attrib) is not None:
                res.append(item)
        return res

    @staticmethod
    def male_female(data, male_option, female_option):
        if 'category' in data.keys():
            if data['category'] == 'M':
                return male_option
            else:
                return female_option
        if (data['category'] == 'M'):
            return male_option
        else:
            return female_option

    @staticmethod
    def not_null_or(value, default):
        if not value:
            return default
        return value

    @staticmethod
    def plural(value, n):
        if n > 1:
            return f"{value}s"
        return value

    @staticmethod
    def ifplural(value, plural, singular=""):
        """Verifica se uma lista possui mais de um elemento e retorna um valor plural ou singular"""
        if isinstance(value, list):
            return plural if len(value) > 1 else singular
        return plural if value > 1 else singular

    @staticmethod
    def count_qtd(value, field=None):
        qtd = 0
        for item in value:
            if isinstance(item, dict):
                qtd += item[field]
            elif isinstance(item, int):
                qtd += item
        return qtd

    @staticmethod
    def case_(var, options):
        if var in options.keys():
            return options[var]
        if 'default' in options.keys():
            return options['default']


global_functions = [getattr(GlobalFunctions, func) for func in dir(
    GlobalFunctions) if callable(getattr(GlobalFunctions, func)) and not func.startswith("__")]
