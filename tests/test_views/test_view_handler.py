from project.views.view_handler import handle_500

def test_handler_404(client,db):
    response = client.get('/notexist')
    assert response.status_code == 404
    assert b'Sorry, but this page/item cannot be found' in response.data
    
def test_handler_500(client, db):
    response, code = handle_500(500)
    assert code == 500
    assert 'Sorry, but the server was a problem' in response