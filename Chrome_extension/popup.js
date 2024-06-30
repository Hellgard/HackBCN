document.getElementById('toggle-btn').addEventListener('click', () => {
  console.log('Toggling scraping');
  chrome.runtime.sendMessage({ action: 'toggleScraping' });
});

document.getElementById('launch').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'launch' });
});
