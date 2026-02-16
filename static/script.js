document.getElementById('scanForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // UI Reset
    const btn = document.getElementById('scanBtn');
    const status = document.getElementById('status');
    const resultsList = document.getElementById('resultsList');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const foundCount = document.getElementById('foundCount');
    const timer = document.getElementById('timer');
    
    btn.disabled = true;
    btn.innerText = "SCANNING...";
    status.innerText = "SCANNING";
    status.className = "status-badge scanning";
    resultsList.innerHTML = '';
    progressBar.style.width = '0%';
    progressText.innerText = '0%';
    foundCount.innerText = '0';
    timer.innerText = '0.0s';

    let openPorts = 0;
    let startTime = Date.now();
    let timerInterval = setInterval(() => {
        let elapsed = (Date.now() - startTime) / 1000;
        timer.innerText = elapsed.toFixed(1) + 's';
    }, 100);

    // Build URL with params
    const formData = new FormData(this);
    const params = new URLSearchParams(formData);
    const eventSource = new EventSource(`/scan?${params.toString()}`);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.type === 'progress') {
            const percentage = Math.round((data.current / data.total) * 100);
            progressBar.style.width = percentage + '%';
            progressText.innerText = percentage + '%';
        } else if (data.type === 'result') {
            openPorts++;
            foundCount.innerText = openPorts;
            addResultItem(data.port);
        } else if (data.type === 'complete') {
            clearInterval(timerInterval);
            timer.innerText = data.duration.toFixed(2) + 's';
            finalizeScan();
            eventSource.close();
        } else if (data.type === 'error') {
            alert(data.message);
            finalizeScan();
            eventSource.close();
        } else if (data.type === 'info') {
            console.log(data.message);
        }
    };

    eventSource.onerror = function() {
        console.error("EventSource failed.");
        finalizeScan();
        eventSource.close();
    };

    function finalizeScan() {
        btn.disabled = false;
        btn.innerText = "INITIATE SCAN";
        status.innerText = "COMPLETE";
        status.className = "status-badge complete";
        clearInterval(timerInterval);
    }

    function addResultItem(port) {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = `
            <div>
                <span class="port-number">PORT ${port}</span>
                <span class="service-name">Service: Unknown</span>
            </div>
            <span class="badge">OPEN</span>
        `;
        resultsList.appendChild(div);
    }
});
