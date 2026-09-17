
def test_login_valid():
    assert authenticate_user("testuser", "testpassword") == True

def test_login_invalid():
    assert authenticate_user("user", "wrongpassword") == False

def authenticate_user(username, password):
    if username in users and users[username] == password:
        return True
    return False

users = {"testuser": "testpassword"}

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def test_valid_file():
    assert is_valid_file("test.txt") == True
    assert is_valid_file("image.png") == True
    assert is_valid_file("document.pdf") == True
    assert is_valid_file("photo.jpg") == True
    assert is_valid_file("graphic.jpeg") == True
    assert is_valid_file("animation.gif") == True

def test_invalid_file():
    assert is_valid_file("test.exe") == False
    assert is_valid_file("image.bmp") == False
    assert is_valid_file("document.docx") == False

def is_valid_file(file):
    return '.' in file and file.split('.')[-1] in ALLOWED_EXTENSIONS


test_valid_file()
test_invalid_file()