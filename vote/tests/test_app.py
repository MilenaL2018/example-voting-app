def test_hello():
    assert False


@app.route("/", methods=['POST', 'GET'])
def test_count_vote(vote, voter_id):
    mock_voter_id = 1
    mock_vote = option_a
    vote = count_vote(mock_vote, mock_voter_id)
    assert vote == option_a
