Option Explicit

Dim shell, command
Set shell = CreateObject("WScript.Shell")

shell.CurrentDirectory = "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\scripts"
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\scripts\wabi_sabi_startup.ps1"""
shell.Run command, 0, False
