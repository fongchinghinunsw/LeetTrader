def test_landing(client):
  """ test the landing page """

  rv = client.get('/')
  assert b'Have you tried virtual trading?' in rv.data
