object Form1: TForm1
  Left = 0
  Top = 0
  AlphaBlend = True
  BorderIcons = [biSystemMenu, biMinimize]
  Caption = 'Copiar arquivos'
  ClientHeight = 226
  ClientWidth = 777
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  Padding.Left = 5
  Padding.Top = 5
  Padding.Right = 5
  Padding.Bottom = 5
  OldCreateOrder = False
  Position = poScreenCenter
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object lblMessage: TLabel
    Left = 5
    Top = 5
    Width = 767
    Height = 25
    Align = alTop
    Alignment = taCenter
    Caption = 'Insira m'#237'dia 1'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clMaroon
    Font.Height = -21
    Font.Name = 'Tahoma'
    Font.Style = [fsBold]
    ParentFont = False
    ExplicitWidth = 145
  end
  object Label2: TLabel
    Left = 5
    Top = 30
    Width = 767
    Height = 13
    Align = alTop
    Caption = 'Progresso geral'
    Visible = False
    ExplicitWidth = 75
  end
  object Label3: TLabel
    Left = 5
    Top = 78
    Width = 767
    Height = 13
    Align = alTop
    Caption = 'Progresso da m'#237'dia corrente'
    Visible = False
    ExplicitWidth = 134
  end
  object pgbGeneral: TProgressBar
    Left = 5
    Top = 43
    Width = 767
    Height = 35
    Align = alTop
    TabOrder = 0
    Visible = False
  end
  object pgbCurrent: TProgressBar
    Left = 5
    Top = 91
    Width = 767
    Height = 35
    Align = alTop
    TabOrder = 1
    Visible = False
  end
  object btnChooseFolder: TButton
    Left = 5
    Top = 144
    Width = 767
    Height = 77
    Align = alBottom
    Caption = 'Escolher pasta'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clNavy
    Font.Height = -19
    Font.Name = 'Tahoma'
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 2
    OnClick = btnChooseFolderClick
  end
  object Memo1: TMemo
    Left = 5
    Top = 126
    Width = 767
    Height = 89
    Align = alTop
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -20
    Font.Name = 'Terminal'
    Font.Style = [fsBold]
    Lines.Strings = (
      
        'Os arquivos ser'#227'o copiados e em seguida extra'#237'dos para uma pasta' +
        ' de sua '
      'escolha. '
      'Clique no bot'#227'o abaixo para escolher uma pasta.')
    ParentFont = False
    ReadOnly = True
    TabOrder = 3
  end
  object Timer1: TTimer
    Interval = 300
    OnTimer = Timer1Timer
    Left = 496
    Top = 8
  end
  object OpenDialog1: TOpenDialog
    Left = 432
    Top = 8
  end
end
