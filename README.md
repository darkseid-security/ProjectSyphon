# Project SyphonV1.1
Extract browser infomation

<img src="https://raw.githubusercontent.com/darkseid-security/ProjectSyphon/main/img/theft.jpg">

[Project Syphon]

Modern web browser dumping tool.

Scripts:
- cookie_dump.py = dumps cookie data
- credit_dump.py = dumps credit card data
- password_dump.py = dumps password data
- sneakyfox.py = copies firefox password and web data files works on both windows and linux
- exfiltration.py = exfiltrates data over FTP/SSH works on both windows and linux
- personal_info.py = dumps personal info

Supported browsers:
- Google Chrome version 80+
- Opera
- Firefox(all versions)
- Microsoft Edge

Supported operating systems:
- All Windows systems
- Firefox supports Linux aswell 

Features:
- Decrypts all Data
- No decryption needed for Firefox browsers(all stored in key3.db/key4.db)
- Dump credit cards
- Dump saved email and passwords
- Dump cookie data
- Copy all firefox stored info
- Exfiltrate files over encrypted FTP or SSH connections(will only upload files that exist)
- Dump personal infomation such as address,name,company,city,state,zipcode,email address and phone number

TODO:
- Build support for modern linux browsers
- Build support for chrome versions <80
- Close CMD on windows after script has run
