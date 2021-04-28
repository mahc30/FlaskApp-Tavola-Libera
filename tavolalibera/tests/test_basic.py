import os
import tempfile
import pathlib
import re
import unittest
from tavolalibera import app, db
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    # executed after each test
    def tearDown(self):
        pass
    
###############
#### tests ####
###############
# 200 OK
# 400 Bad Request
# 401 Unauthorized
# 403 Forbidden ("The server understood the request, but is refusing to fulfill it")
# 404 Not Found
# 409 Error: Duplicate
###############
    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_registration_password_missing(self):
        response = self.register('UNIT_TEST_USER', '', '', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados') 
        
    def test_invalid_user_registration_username_missing(self):
        response = self.register('', 'UNIT_TEST_PASSWORD', 'ContraseñaDistintajeje', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados') 
        
    def test_invalid_user_registration_different_passwords(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'ContraseñaDistintajeje', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados') 
        
    def test_invalid_user_registration_username_exists(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')
 
    def test_invalid_user_registration_forbidden_characters(self):
        response = self.register('B̴̡̢̯̟̬̪̜͔̰̌A̷͓͇̫͈̥͑̓͐͗͌́̑̚͜͠͝͝D̸̢͙̻̞̉̓̾̓̌̎̄͛̽́͜͜ ̶̨̳͈̝͓̲̬̼̣̗͖̫͉̓̌͛́͜ͅŰ̶̢̞͖̙͔̘̟͉̗͖͂̓̐̇̀̎͜͝Ş̵͔̘͇̒̕E̸͚͍͑̀̆̈́͋̑̄̀̃́͘͝͝Ř̸̝̭̝̼͎̬̟̉̄̉̅͛̓̄́͘  ///', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')
        response = self.register('UNIT_TEST_USER', '{´*-_.ñ{¿?#4;.}', '{´*-_.ñ{¿?#4;.}', 1, 'UNIT_TEST_ANSWER')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados') 
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, '!"#$%&/()=?¡^^^@')
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados') 
    
    def test_valid_user_login(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.login('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_user_login_wrong_password(self):
        response = self.register('UNIT_TEST_USER_FAIL', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.login('UNIT_TEST_USER_FAIL', 'UNIT_TEST_WRONG_PASSWORD')
        self.assert_flash_message(response, 'Usuario o Contraseña Incorrectos')
      
    def test_invalid_user_login_no_password(self):
        response = self.login('UNIT_TEST_USER_FAIL', '')
        self.assert_flash_message(response, 'Usuario o Contraseña Incorrectos')
        
    def test_invalid_user_login_no_username(self):
        response = self.login('', 'UNIT_TEST_PASSWORD')
        self.assert_flash_message(response, 'Usuario o Contraseña Incorrectos')
    
    def test_invalid_user_login_user_doesnt_exist(self):
        response = self.login('UNIT_TEST_USER_FAIL', 'UNIT_TEST_PASSWORD')
        self.assert_flash_message(response, 'Usuario o Contraseña Incorrectos')
    
    def test_invalid_user_login_forbidden_characters(self):
        response = self.login('B̴̡̢̯̟̬̪̜͔̰̌A̷͓͇̫͈̥͑̓͐͗͌́̑̚͜͠͝͝D̸̢͙̻̞̉̓̾̓̌̎̄͛̽́͜͜ ̶̨̳͈̝͓̲̬̼̣̗͖̫͉̓̌͛́͜ͅŰ̶̢̞͖̙͔̘̟͉̗͖͂̓̐̇̀̎͜͝Ş̵͔̘͇̒̕E̸͚͍͑̀̆̈́͋̑̄̀̃́͘͝͝Ř̸̝̭̝̼͎̬̟̉̄̉̅͛̓̄́͘  ///', 'UNIT_TEST_PASSWORD')
        self.assert_flash_message(response, 'Usuario o Contraseña Incorrectos')
        
    def test_valid_user_reset_password(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.reset_password("UNIT_TEST_USER", 'UNIT_TEST_ANSWER' , "Cambio", "Cambio")
        self.assertEqual(response.status_code, 200)
        response = self.login('UNIT_TEST_USER', 'Cambio')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_user_reset_password_different_password(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.reset_password("UNIT_TEST_USER",'UNIT_TEST_ANSWER' , "Cambio", "FAIL")
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')
    
    def test_invalid_user_reset_password_wrong_security_answer(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.reset_password("UNIT_TEST_USER",'FAIL' , "Cambio", "Cambio")
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')
    
    def test_invalid_user_reset_password_forbidden_characters(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.reset_password("UNIT_TEST_USER",'UNIT_TEST_ANSWER' , "Cam-bio", "Cam-bio")
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')
    
    def test_invalid_user_reset_password_username_doesnt_exist(self):
        response = self.register('UNIT_TEST_USER', 'UNIT_TEST_PASSWORD', 'UNIT_TEST_PASSWORD', 1, 'UNIT_TEST_ANSWER')
        self.assertEqual(response.status_code, 200)
        response = self.reset_password("Don Domo Din Dueño del Domodin de Dimsdale donde se presenta Crash Nebula",'UNIT_TEST_ANSWER' , "Cam-bio", "Cam-bio")
        self.assert_flash_message(response, 'Ocurrió un error. Por favor verifique los datos ingresados')

########################
#### helper methods ####
########################
 
    def register(self, username, password, confirm_password, security_question, security_answer):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, confirm_password=confirm_password, security_question = security_question, security_answer = security_answer),
            follow_redirects=True
        )
 
    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username,
                      password=password),
            follow_redirects=True
        )
 
    def reset_password(self, username, security_answer, new_password, confirm_password):
        return self.app.post(
            '/forgot_password',
            data=dict(username=username,
                      security_answer= security_answer,
                      new_password=new_password,
                      confirm_password=confirm_password),
            follow_redirects=True
        )
    
    def assert_flash_message(self, response, expected_message):
        self.assertTrue(re.search(expected_message, response.get_data(as_text=True)))
    
if __name__ == "__main__":
    unittest.main()
    
'''    
    
    
'''