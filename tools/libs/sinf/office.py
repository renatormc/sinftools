
import win32com.client as win32
import pythoncom

def getApp(name, visible=False):
    clsid = f"{name}.Application"
    clsid = pythoncom.CoCreateInstanceEx(clsid, None, pythoncom.CLSCTX_SERVER,
                                        None, (pythoncom.IID_IDispatch,))[0]
    if win32.gencache.is_readonly:
        # fix for "freezed" app: py2exe.org/index.cgi/UsingEnsureDispatch
        win32.encache.is_readonly = False
        win32.gencache.Rebuild()

    app = win32.gencache.EnsureDispatch(clsid)
    app.Visible = visible
    return app
if __name__ == "__main__":

    excel = office.getApp("Excel", visible=True)
    excel.Workbooks.Open(r'J:\laudos\trabalhando\10148.2018\midia\C1\2018-08-29.16-01-02\Samsung GSM_SM-J500M Galaxy J5\Relatório.xlsx')