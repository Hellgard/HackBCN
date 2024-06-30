// Function to send current URL to Flask API
function sendCurrentURLToAPI(url) {
    fetch('http://localhost:5000/api/extension', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ current_url: url }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received response from Flask API:', data);
        // Handle response data as needed
    })
    .catch(error => console.error('Error sending URL to Flask API:', error));
}

// Example: Fetch current URL using chrome.tabs API
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var currentUrl = tabs[0].url;
    console.log('Current URL:', currentUrl);
    
    // Send current URL to Flask API
    sendCurrentURLToAPI(currentUrl);
});
