"""Test cases of endpoints"""
def test_get_homepage(client):
    """Case: Get method of homepage"""
    resp = client.get("/")
    assert resp[2]['Content-Type'] == "text/html"
    assert resp[1] == "200 OK"

def test_post_homepage(client):
    """Case: Post method of homepage"""
    resp = client.post("/", data={"word": "zengin"})
    assert resp[2]['Content-Type'] == "text/json"
    assert resp[1] == "200 OK"

def test_get_builder(client):
    """Case: Get method of builder"""
    resp = client.get("/builder")
    assert resp[2]['Content-Type'] == "text/html"
    assert resp[1] == "200 OK"

def test_post_builder(client):
    """Case: Post method of builder"""
    resp = client.post("/builder", data={"budget": "200000000"})
    assert resp[2]['Content-Type'] == "text/json"
    assert resp[1] == "200 OK"

def test_static_css(client):
    """Case: Get method of static using css"""
    resp = client.get("/static/css/navbar-top.css")
    assert resp[2]['Content-Type'] == "text/css"
    assert resp[1] == "200 OK"

def test_static_js(client):
    """Case: Get method of static using js"""
    resp = client.get("/static/js/search.js")
    assert resp[2]['Content-Type'] == "application/javascript"
    assert resp[1] == "200 OK"

def test_static_plain(client):
    """Case: Get method of static using plain file"""
    resp = client.get("/static/js/search2")
    assert resp[2]['Content-Type'] == "text/plain"
    assert resp[1] == "404 Not Found"

def test_static_not_found(client):
    """Case: Get method of static using FileNotFound"""
    resp = client.get("/static/css/lorem.css")
    assert resp[2]['Content-Type'] == "text/css"
    assert resp[1] == "404 Not Found"

def test_not_found(client):
    """Case: not_found_view with lorem/ path"""
    resp = client.get("/lorem")
    assert resp[2]['Content-Type'] == "text/plain"
    assert resp[1] == "404 Not Found"
