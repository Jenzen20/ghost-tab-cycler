' Ghost Tab Cycler - Hidden Launcher
' =====================================
' This VBScript launches ghost_tab.py using pythonw.exe
' (the windowless Python interpreter) so NO console window appears.
' Double-click this file to start the hidden app.
'
' Hotkeys:
'   Ctrl+Pause (or Pause/Break) = Toggle cycling ON/OFF
'   End = Quit the app

Dim WshShell, scriptDir, pythonwPath, scriptPath

Set WshShell = CreateObject("WScript.Shell")

' Get directory where this .vbs file lives
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Path to pythonw in the local venv (no console window)
pythonwPath = scriptDir & "\venv\Scripts\pythonw.exe"

' Path to the main script
scriptPath = scriptDir & "\ghost_tab.py"

' Check if venv exists
If Not CreateObject("Scripting.FileSystemObject").FileExists(pythonwPath) Then
    MsgBox "Virtual environment not found!" & vbCrLf & vbCrLf & _
           "Please run setup first:" & vbCrLf & _
           "  1. Double-click setup.bat (or follow instructions in README.md)" & vbCrLf & _
           "  2. Double-click START_GHOST.vbs again", _
           vbExclamation, "Ghost Tab Cycler"
    WScript.Quit
End If

' Launch completely hidden (0 = hidden window, False = don't wait)
WshShell.Run """" & pythonwPath & """ """ & scriptPath & """", 0, False

Set WshShell = Nothing
