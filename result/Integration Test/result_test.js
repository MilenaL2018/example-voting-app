Feature('result');

const expect = require('chai').expect;
const {I} = inject();

Scenario('Verify a successful call', async () => {
	const res = await I.sendGetRequest('/');
	expect(res.status).to.eql(200);
});

Scenario('I vote cats!', (I) => {
  I.click('Cats');
  I.see('Cats vs Dogs!', 'h3');
  I.click({css: 'button .a'});
  I.seeElement('fa fa-check-circle');
  I.scrollPageToBottom();
  I.seeElement("hostname");
});
