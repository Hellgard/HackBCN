
let isScrapingEnabled = false;


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  console.log('Toggling scraping');
  console.log('isScrapingEnabled:', isScrapingEnabled);
  isScrapingEnabled = !isScrapingEnabled;
  console.log('isScrapingEnabled:', isScrapingEnabled);
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: scrapePage,
      args: [isScrapingEnabled]
    });
  });
  console.log('Sending');
  if (message.type === 'scrapedData') {
    console.log('Sending scraped data to server:', message.data);
    fetch('http://localhost:5000/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error))

  }

});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'launch') {
    console.log('Launching');
    fetch('http://localhost:5000/launch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    })
  }
});

function scrapePage(enabled) {
  if (!enabled) {
    console.log('Scraping is disabled');
    return;
  }
  let pageData = {
    title: document.title,
    url: window.location.href,
    content: document.body.innerText
  };
  console.log('Scraped data:', pageData);
  chrome.runtime.sendMessage({ type: 'scrapedData', data: pageData });
}
