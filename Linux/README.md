# Project SyphonV1.2
Extract browser infomation and writes to a CSV file

<img src="https://raw.githubusercontent.com/darkseid-security/ProjectSyphon/main/img/theft.jpg">

[Project Syphon]

Modern web browser dumping tool.

Windows Scripts:
- cookie_dump.py = dumps cookie data
- credit_dump.py = dumps credit card data
- password_dump.py = dumps password data
- sneakyfox.py = copies firefox password and web data files works on both windows and linux
- exfiltration.py = exfiltrates data over FTP/SSH works on both windows and linux
- personal_info.py = dumps personal info

[*New Feature] Linux Scripts:
- dump_cookies.py = dump chrome,brave and opera cookies
- credit_dump.py = dump chrome,brave and opera credit card details
- passwords.py = dump chrome,brave and opera passwords
- profile_data.py = dump chrome,brave and opera profile infomation stored in the browser
- sneakyfox.py = copies firefox password and web data files works on both windows and linux
- exfiltration.py = exfiltrates data over FTP/SSH works on both windows and linux

Supported browsers:
- Google Chrome version 80+
- Opera
- Firefox(all versions)
- Microsoft Edge
- Brave
- Chromium

Supported operating systems:
- All Windows systems
- Firefox
- [*New Feature] Linux

Features:
- Decrypts all Data
- No decryption needed for Firefox browsers(all stored in key3.db/key4.db)
- Dump credit cards
- Dump saved email and passwords
- Dump cookie data
- Dump personal infomation such as address,name,company,city,state,zipcode,email address and phone number
- Copy all firefox stored info
- Exfiltrate files over encrypted FTP or SSH connections(will only upload files that exist)
- Bypasses AV(compile with --noupx option to avoid AV detection)
- [*New Feature] Added support for Linux browsers
- [*New Feature] Extracts keyring encryption keys if used(Linux only)

TODO:
- Close CMD on windows after script has run
- Fix issue with personal_info writing to csv order

Demo:
https://www.youtube.com/watch?v=9cbxARZa9lw
