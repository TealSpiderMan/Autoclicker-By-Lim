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
; Support BOTH PyInstaller modes. The one that doesn't exist is skipped.
; Folder mode (from spec): dist\autoclicker by Lim\*
Source: "{#DistDirFolder}\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion skipifsourcedoesntexist; \
    Check: DirExists(ExpandConstant('{#DistDirFolder}'))
; One-file mode: dist\autoclicker by Lim.exe
Source: "{#DistExePath}"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist; \
    Check: FileExists(ExpandConstant('{#DistExePath}'))

[Icons]
; Create shortcuts only if the EXE can be found in one of the expected locations
Name: "{group}\\{#MyAppName}"; Filename: "{code:MainExePath}"; IconFilename: "{code:MainExePath}"; Check: MainExeExists
Name: "{group}\\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
; Always create a desktop icon by default; user can delete later if unwanted
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{code:MainExePath}"; Check: MainExeExists

[Run]
Filename: "{code:MainExePath}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent; Check: MainExeExists

[Code]
function MainExePath(Param: string): string;
begin
  if FileExists(ExpandConstant('{app}\\{#ExeName}')) then
  begin
    Result := ExpandConstant('{app}\\{#ExeName}');
  end
  else if FileExists(ExpandConstant('{app}\\autoclicker by Lim\\{#ExeName}')) then
  begin
    Result := ExpandConstant('{app}\\autoclicker by Lim\\{#ExeName}');
  end
  else
  begin
    Result := '';
  end;
end;

function MainExeExists(): Boolean;
begin
  Result := FileExists(MainExePath(''));
end;
