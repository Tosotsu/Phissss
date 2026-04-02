// Listen for tab updates (when a user visits a new site)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // Only trigger when the page is fully loaded and has a valid URL
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
        
        console.log("Checking URL:", tab.url);

        // Send to our Flask Backend
        fetch('http://127.0.0.1:5000/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: tab.url })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Scan Result:", data);

            if (data.status === "DANGEROUS") {
                // INJECT WARNING BANNER
                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    function: showWarning,
                    args: [data.source, data.risk_score, data.message]
                });
            }
        })
        .catch(error => console.error('Error connecting to backend:', error));
    }
});

// This function runs INSIDE the web page
function showWarning(source, score, message) {
    // Create a scary red overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(139, 0, 0, 0.95);
        color: white;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: Arial, sans-serif;
        text-align: center;
    `;

    const title = document.createElement('h1');
    title.innerText = "⚠️ DANGER: PHISHING DETECTED";
    title.style.fontSize = "40px";

    const details = document.createElement('p');
    details.innerText = `Source: ${source}\nRisk Score: ${(score * 100).toFixed(1)}%\n\n${message}`;
    details.style.fontSize = "20px";

    const btn = document.createElement('button');
    btn.innerText = "I understand the risk, Proceed anyway";
    btn.style.marginTop = "20px";
    btn.style.padding = "10px 20px";
    btn.style.cursor = "pointer";
    btn.onclick = () => overlay.remove();

    overlay.appendChild(title);
    overlay.appendChild(details);
    overlay.appendChild(btn);
    document.body.appendChild(overlay);
}