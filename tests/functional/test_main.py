def test_landing_page(test_client):
  """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
  response = test_client.get('/')
  # print(response)
  assert b'Have you tried virtual trading?' in response.data
  assert response.status_code == 200
