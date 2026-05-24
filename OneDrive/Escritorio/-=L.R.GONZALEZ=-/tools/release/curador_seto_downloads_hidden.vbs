Option Explicit

Dim shell
Dim command
Dim exitCode

Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
command = """C:\Users\L-Tyr\AppData\Local\Programs\Python\Python311\pythonw.exe"" tools\release\curador_automation.py absorb --root downloads --recursive --write-index --write-fichas --write-atlas --archive-absorbed --apply-safe-deletes"

' Window style 0 keeps the scheduled curador intake invisible. Calling
' pythonw.exe directly avoids the transient cmd.exe/conhost.exe window created
' by the previous .cmd entrypoint while preserving the same curador arguments.
exitCode = shell.Run(command, 0, True)
WScript.Quit exitCode
