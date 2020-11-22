Feature('vote');

const expect = require('chai').expect;
const {I} = inject();

Scenario('Verify a successful call', async () => {
	const res = await I.sendGetRequest('https://example-voting-app-vote.herokuapp.com/');
	expect(res.status).to.eql(200);
});

Scenario('I vote cats!', ({I}) => {
  I.amOnPage('https://example-voting-app-vote.herokuapp.com/');
  I.seeElement('//*[@id="a"]');
  I.seeElement('//*[@id="b"]');
  I.scrollPageToBottom();
  I.seeElement('//*[@id="hostname"');
});

