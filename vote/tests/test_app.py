import pytest

@pytest.fixture
@app.route("/", methods=['POST', 'GET'])
def test_app_countvote():
    vote = None 
    mock_voter_id = 1
    mock_vote = option_a
    vote = app.count_vote(mock_vote, mock_voter_id)
    assert vote == 'Cats'
