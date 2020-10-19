def test_landing_page(client):
    """ Just a useless test... """

    print(client)
    rv = client.get('/')
    print(rv)
    print(type(rv))
    assert b'Have you tried virtual trading?' in rv.data
