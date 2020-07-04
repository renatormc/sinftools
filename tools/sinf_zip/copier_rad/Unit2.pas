unit Unit2;

interface

type
  TForm1 = class
    lblMessage: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    pgbGeneral: TProgressBar;
    pgbCurrent: TProgressBar;
    btnChooseFolder: TButton;
    Timer1: TTimer;
    OpenDialog1: TOpenDialog;
    procedure Timer1Timer(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure ShowBlinkingMessage(mess: String);
    procedure HideBlinkingMessage;
    procedure btnChooseFolderClick(Sender: TObject);
    procedure CopyFiles;
  private
    message: String;
    drive: String;
    config: TJSONObject;
    execfile: String;

  public
    { Public declarations }
  end;

implementation

end.
