import config

class PosProcessor:

    def subdoc(self, doc, cur, name):
        name = name.strip()
        path = (config.subdocs_temp_dir / f"{name}.odt").absolute()
        if path.exists():
            cur.setString("")
            cur.gotoEnd(False)
            cur.insertDocumentFromURL(path.as_uri(), ())

    def exec(self, funcname, *args, **kargs):
        if funcname == "subdoc":
            self.subdoc(*args, **kargs)
            return True
        else:
            return False


