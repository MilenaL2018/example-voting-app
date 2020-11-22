Feature('vote');

Scenario('I vote cats!', ({I}) => {
  I.amOnPage('https://example-voting-app-vote.herokuapp.com/');
  I.seeElement('//*[@id="a"]');
  I.seeElement('//*[@id="b"]');
  I.scrollPageToBottom();
  I.seeElement('//*[@id="hostname"');
});

