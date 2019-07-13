from lunchscraper import lunchscraper

def test_controller_user_add():
    Object = lunchscraper.controller.User()
    Object.clear()
    result = Object.add("test_email@test.test")
    
    assert type(result) == dict

def test_controller_user_get():
    Object = lunchscraper.controller.User()
    Object.clear()
    Object.add("test1@test.test")
    Object.add("test2@test.test")
    result = Object.get()
    
    assert len(result) == 2

def test_app_get_recipients():
    Object = lunchscraper.lunchScraper()
    result = Object.get_recipients()
    
    assert type(result) == list and type(result[0]) == dict

def test_app_add_menu():
    Object = lunchscraper.lunchScraper()
    Object.scrape_restaurants()
    result = Object.menus
    
    assert type(result) == list and len(result) > 1
    
def test_app_send_message():
    Object = lunchscraper.lunchScraper()
    Object.scrape_restaurants()
    
    Users = lunchscraper.controller.User()
    Users.clear()
    new_user = Users.add("kotek.vojtech@gmail.com")
    verification = Users.verify( new_user['token'] )
    
    result = Object.send_messages_html()
    
    assert result == True and verification == True
    
def test_app_render_email():
    Object = lunchscraper.lunchScraper()
    menus = [
        {
            'name': "TEST RESTAURANT ONE",
            'url': "https://google.com",
            'menu': ["ONE","TWO","THREE" ],
        }
    ]
    data = {
        'title': "Daily Menu for TEST",
        'notice': {
            'title': "Dont' Panic!",
            'text': "This is merely a pytest.",
        },
        'recipient': {
            'email': "email@email.com",
            'url': "https://google.com",
        },
        'menus': menus,
    }   
    result = Object.render_email('master.html', data)
    
    values = [
        menus[0]['name'], menus[0]['url'], menus[0]['menu'][0], menus[0]['menu'][1],
        data['title'], data['recipient']['email'],
    ]
    
    def has_values(body, values):
        for value in values:
            if value not in body:
                print("Value not found in email:", value)
                return False
        return True
    
    assert has_values(result, values) == True
