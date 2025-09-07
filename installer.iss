; Inno Setup script to package "autoclicker by Lim" into an installer
; 1) Build the EXE first via PyInstaller (see README)
; 2) Then compile this script with Inno Setup (ISCC)

#define MyAppName "autoclicker by Lim"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Lim"
#define MyAppURL "https://github.com/"  
; Update to your repo URL if desired

; Path where PyInstaller places the build output
; The spec name sets the app folder under dist to the app name
#define DistDirFolder SourcePath + "dist\\autoclicker by Lim"      
#define DistExePath   SourcePath + "dist\\autoclicker by Lim.exe"  
#define ExeName "autoclicker by Lim.exe"

[Setup]
AppId={{3F1E8E9B-4B6F-4D6C-9F6E-2E0B4A9FC1C3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=autoclicker-by-lim-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=icon\\acbl.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Files]
; Select build mode at compile time and FAIL if nothing to package
#ifexist "{#DistExePath}"
Source: "{#DistExePath}"; DestDir: "{app}"; Flags: ignoreversion
#define InstalledExeRelPath "{#ExeName}"
#else
#ifexist "{#DistDirFolder}\\{#ExeName}"
Source: "{#DistDirFolder}\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
#define InstalledExeRelPath "autoclicker by Lim\\{#ExeName}"
#else
#error "No build output found in dist/. Run PyInstaller before compiling the installer."
#endif
#endif

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#InstalledExeRelPath}"; IconFilename: "{app}\\{#InstalledExeRelPath}"
Name: "{group}\\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
; Always create a desktop icon by default; user can delete later if unwanted
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#InstalledExeRelPath}"

[Run]
Filename: "{app}\\{#InstalledExeRelPath}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
