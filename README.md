# ShellyOS Desktop Environment

基於 Windows \ Windows PE 的 Python 桌面環境開源項目。

## 建構
 > 考慮到 Windows 為封閉原始碼且包含著作權之軟體，我不會直接提供ISO或WIM，僅提供PE製作方式：
1. 請安裝和使用 Microsoft 官方的 Windows PE 製作工具 (Windows ADK)
2. 使用`copype`指令複製PE所需文件，如：
```
copype amd64 C:\Users\Jack\shellyostest\
```
3. 透過DISM工具掛載此文件，或使用[DISM++工具](https://github.com/Chuyu-Team/Dism-Multi-language/releases)
4. 安裝以下cab，通常位於`C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Windows Preinstallation Environment\amd64\WinPE_OCs`
或`自訂的安裝位置\Windows Preinstallation Environment\amd64\WinPE_OCs`：
```
WinPE-Fonts-Legacy.cab
WinPE-StorageWMI.cab
WinPE-NetFx.cab
WinPE-HTA.cab
WinPE-SecureStartup.cab
WinPE-WMI.cab
```
以下為語言包，\zh-tw\lp.cab可選安裝
```
WinPE-FontSupport-ZH-TW.cab
\zh-tw\lp.cab
```
5. (可選)如果使用DISM++，請把時區設為Taipei Startand Time；如果使用DISM工具，請輸入
```
DISM /Image:".\mount" /Set-AllIntl:zh-TW
```
6. 請在掛載資料夾下建立以下資料夾：
```
bin
Document
recycle
```
7. 將下載的 ShellyOS Release 文件全部解壓縮進bin，請不要以這種情況將文件複製進去：
```
C:\Users\Jack\shellyostest\mount\bin\ShellyOS 3.1.415.926\
```
一定要確保解壓縮的文件在bin目錄下而非多套一層資料夾
8. 進入掛載資料夾\Windows\System32\，修改`winpeshl.ini`為下列內容：
```
[LaunchApp]
AppPath = %SYSTEMDRIVE%\bin\main.exe
```
9. 取消掛載並保存，如果是DISM++，**一定要記得儲存**，然後退出；如果是DISM，指令如下：
```
DISM /Unmount-Image /MountDir:".\mount" /Commit
```
10. 使用MakePEMedia指令建立ISO：
```
MakeWinPEMedia /iso C:\Users\Jack\shellyostest\ C:\Users\Jack\shellyostest\isofile.iso
```

## 使用：
 > 建議使用虛擬機
1. 請在其他PE環境下格式化磁碟機，建議使用DiskGenius
2. 使用DISM++工具釋放鏡像，位置將會是(假設光碟已經掛載或插入)：
```
光碟槽位\sources\boot.wim
```
3. 勾選`新增 Boot`，然後直接下一步
4. 重新啟動即可進入已安裝到本機磁碟機的PE

## 授權 License

本專案採用 Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) 授權。

您可以自由地：
- 分享 — 在任何媒介以任何形式複製、重發本作品
- 修改 — 重混、轉換、改作本作品

但必須遵守以下條件：
- 署名 — 您必須給予適當的署名（建議，沒有的話也沒差）
- 非商業性 — 不得將本作品用於商業目的
- 相同方式分享 — 若您改作，必須採用相同的授權條款

> ShellyOS 是用愛發電的作品，請尊重它的初衷。  
> 本專案不包含任何微軟專有元件，僅供教育、學習與娛樂用途。

完整授權條款請見：[CC授權官方網站之解釋](https://creativecommons.org/licenses/by-nc-sa/1.0/)
