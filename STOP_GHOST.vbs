' Ghost Tab Cycler - Force Stop
' ================================
' Double-click this to force-kill the ghost tab app
' if the End hotkey isn't working for some reason.

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

' Terminate any running ghost_tab process
WshShell.Run "powershell -WindowStyle Hidden -Command ""Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*ghost_tab*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }""", 0, True

Set WshShell = Nothing
