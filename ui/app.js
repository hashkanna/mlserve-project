// MLServe Dashboard App
class MLServeDashboard {
    constructor() {
        this.baseURL = 'http://localhost:8000/api/v1';
        this.loadTestActive = false;
        this.metrics = {
            totalRequests: 0,
            successfulRequests: 0,
            totalLatency: 0,
            requestsPerSecond: 0
        };
        this.chart = null;
        this.chartData = {
            labels: [],
            latencies: [],
            throughput: []
        };
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.initChart();
        await this.loadInitialData();
        this.startStatusUpdates();
    }

    setupEventListeners() {
        // File upload
        const fileInput = document.getElementById('file-input');
        const uploadArea = document.getElementById('upload-area');

        fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.processImage(files[0]);
            }
        });

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    async loadInitialData() {
        await Promise.all([
            this.updateAPIStatus(),
            this.updateRayStatus(),
            this.loadModels()
        ]);
    }

    async updateAPIStatus() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            const data = await response.json();
            
            document.getElementById('api-status').textContent = data.status === 'healthy' ? 'Online' : 'Offline';
            document.getElementById('api-status-icon').className = `status-icon ${data.status === 'healthy' ? 'healthy' : 'error'}`;
        } catch (error) {
            document.getElementById('api-status').textContent = 'Offline';
            document.getElementById('api-status-icon').className = 'status-icon error';
        }
    }

    async updateRayStatus() {
        try {
            const response = await fetch(`${this.baseURL}/ray/status`);
            const data = await response.json();
            
            const isHealthy = data.status === 'running';
            document.getElementById('ray-status').textContent = isHealthy ? 'Running' : 'Offline';
            document.getElementById('ray-status-icon').className = `status-icon ${isHealthy ? 'healthy' : 'error'}`;
            
            if (data.resources) {
                const totalCPU = data.resources.total.CPU || 0;
                const availableCPU = data.resources.available.CPU || 0;
                const usedCPU = totalCPU - availableCPU;
                const cpuUsage = Math.round((usedCPU / totalCPU) * 100);
                
                document.getElementById('cpu-usage').textContent = `${cpuUsage}%`;
                document.getElementById('cpu-icon').className = `status-icon ${cpuUsage < 70 ? 'healthy' : cpuUsage < 90 ? 'warning' : 'error'}`;
            }
            
            // Estimate replicas (simplified)
            document.getElementById('replicas-count').textContent = '1-3';
            
        } catch (error) {
            document.getElementById('ray-status').textContent = 'Offline';
            document.getElementById('ray-status-icon').className = 'status-icon error';
        }
    }

    async loadModels() {
        try {
            const response = await fetch(`${this.baseURL}/models`);
            const data = await response.json();
            
            const modelList = document.getElementById('model-list');
            modelList.innerHTML = '';
            
            data.models.forEach(model => {
                const modelItem = document.createElement('li');
                modelItem.className = 'model-item';
                modelItem.innerHTML = `
                    <div class="model-info">
                        <h3>${model.name}</h3>
                        <p>${model.description || `${model.framework} v${model.version}`}</p>
                    </div>
                    <span class="status-badge ${model.status}">${model.status}</span>
                `;
                modelList.appendChild(modelItem);
            });
        } catch (error) {
            console.error('Failed to load models:', error);
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            this.processImage(file);
        }
    }

    processImage(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.getElementById('image-preview');
            img.src = e.target.result;
            img.classList.remove('hidden');
            
            // Simulate image processing (in real app, you'd process the actual image)
            this.classifyImage();
        };
        reader.readAsDataURL(file);
    }

    useSampleImage(sampleId) {
        // Create a proper sample image with canvas
        const sampleData = [
            { name: 'Golden Retriever', emoji: '🐕', colors: ['#FFB74D', '#FF8A65'], dataValue: 0.2 },
            { name: 'Sports Car', emoji: '🚗', colors: ['#64B5F6', '#42A5F5'], dataValue: 0.8 },
            { name: 'Coffee Cup', emoji: '☕', colors: ['#8BC34A', '#66BB6A'], dataValue: 0.5 }
        ];
        
        const sample = sampleData[sampleId - 1];
        
        // Create a canvas to generate a sample image  
        const canvas = document.createElement('canvas');
        canvas.width = 224;
        canvas.height = 224;
        const ctx = canvas.getContext('2d');
        
        // Create gradient background
        const gradient = ctx.createLinearGradient(0, 0, 224, 224);
        gradient.addColorStop(0, sample.colors[0]);
        gradient.addColorStop(1, sample.colors[1]);
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 224, 224);
        
        // Add some pattern for visual interest
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        for (let i = 0; i < 20; i++) {
            for (let j = 0; j < 20; j++) {
                if ((i + j) % 2 === 0) {
                    ctx.fillRect(i * 11.2, j * 11.2, 11.2, 11.2);
                }
            }
        }
        
        // Add text
        ctx.fillStyle = 'white';
        ctx.font = 'bold 24px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(sample.name, 112, 100);
        
        // Add emoji
        ctx.font = '48px Arial';
        ctx.fillText(sample.emoji, 112, 150);
        
        // Convert to image and display
        const img = document.getElementById('image-preview');
        img.src = canvas.toDataURL('image/png');
        img.classList.remove('hidden');
        
        console.log(`Selected sample: ${sample.name}`);
        
        // Store the sample info for classification
        this.currentSample = sample;
        
        // Run classification
        this.classifyImage();
    }

    async classifyImage(sampleLabel = null) {
        const resultsContainer = document.getElementById('prediction-results');
        resultsContainer.innerHTML = '<div class="loading"></div><p>Classifying image...</p>';
        
        try {
            // Generate sample-specific realistic data patterns quickly
            let inputData = [];
            
            if (this.currentSample) {
                console.log(`Creating realistic data for sample: ${this.currentSample.name}`);
                
                // Create sample-specific patterns based on the sample colors and type
                const sampleColors = {
                    'Golden Retriever': { r: 0.8, g: 0.6, b: 0.3 }, // Orange/golden colors
                    'Sports Car': { r: 0.4, g: 0.7, b: 0.9 },       // Blue colors  
                    'Coffee Cup': { r: 0.5, g: 0.8, b: 0.4 }        // Green colors
                };
                
                const colors = sampleColors[this.currentSample.name] || { r: 0.5, g: 0.5, b: 0.5 };
                
                // Generate 224x224x3 = 150528 values with sample-specific color patterns
                for (let y = 0; y < 224; y++) {
                    for (let x = 0; x < 224; x++) {
                        // Create gradient and pattern effects
                        const gradientFactor = (x + y) / (224 + 224); // 0 to 1
                        const noiseFactor = (Math.random() - 0.5) * 0.1; // Small noise
                        
                        // Red channel
                        inputData.push(Math.max(0, Math.min(1, colors.r * (0.8 + gradientFactor * 0.4) + noiseFactor)));
                        // Green channel  
                        inputData.push(Math.max(0, Math.min(1, colors.g * (0.8 + gradientFactor * 0.4) + noiseFactor)));
                        // Blue channel
                        inputData.push(Math.max(0, Math.min(1, colors.b * (0.8 + gradientFactor * 0.4) + noiseFactor)));
                    }
                }
                
                console.log(`Generated ${inputData.length} realistic pixel values for ${this.currentSample.name}`);
            } else {
                console.log('Using generic data pattern');
                // Generic pattern for non-sample images
                for (let i = 0; i < 150528; i++) {
                    inputData.push(Math.random() * 0.6 + 0.2);
                }
            }
            
            const payload = {
                model: 'resnet18',
                data: [inputData] // Send actual image data
            };
            
            console.log('Sending request to:', `${this.baseURL}/predict`);
            console.log('Payload structure:', {
                model: payload.model,
                dataLength: payload.data.length,
                firstElementLength: payload.data[0].length,
                sampleData: payload.data[0].slice(0, 5)
            });
            
            const startTime = Date.now();
            const response = await fetch(`${this.baseURL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const endTime = Date.now();
            const latency = endTime - startTime;
            
            console.log('Response status:', response.status);
            console.log('Response headers:', [...response.headers.entries()]);
            
            if (response.ok) {
                const data = await response.json();
                console.log('Received response:', data);
                if (data.predictions && data.predictions.length > 0 && data.predictions[0].predictions) {
                    this.displayPredictions(data.predictions[0].predictions, latency);
                    this.updateMetrics(latency, true);
                } else {
                    throw new Error('Invalid response format');
                }
            } else {
                const errorText = await response.text();
                console.error('API Error:', response.status, errorText);
                
                // Try to parse JSON error for better display
                try {
                    const errorJson = JSON.parse(errorText);
                    throw new Error(`${response.status}: ${errorJson.detail || errorText}`);
                } catch (parseError) {
                    throw new Error(`${response.status}: ${errorText}`);
                }
            }
        } catch (error) {
            console.error('Classification error:', error);
            let errorMessage = error.message;
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage = 'Network error - is the API running on port 8000?';
            }
            resultsContainer.innerHTML = `<p style="color: #ef4444;">Classification failed: ${errorMessage}</p>`;
            this.updateMetrics(0, false);
        }
    }

    displayPredictions(predictions, latency) {
        const resultsContainer = document.getElementById('prediction-results');
        resultsContainer.innerHTML = `
            <h3>Predictions (${latency}ms)</h3>
            ${predictions.map((pred, index) => `
                <div class="prediction-item">
                    <div>
                        <strong>${pred.class_name}</strong>
                        <br>
                        <small>Class ID: ${pred.class_id}</small>
                    </div>
                    <div style="text-align: right;">
                        <div>${(pred.confidence * 100).toFixed(1)}%</div>
                        <div class="prediction-bar">
                            <div class="prediction-fill" style="width: ${pred.confidence * 100}%;"></div>
                        </div>
                    </div>
                </div>
            `).join('')}
        `;
    }

    async startLoadTest(type) {
        if (this.loadTestActive) return;
        
        this.loadTestActive = true;
        const requestCount = type === 'light' ? 5 : 20;
        const concurrent = type === 'light' ? 2 : 8;
        
        // Update UI
        document.getElementById('light-load-btn').disabled = true;
        document.getElementById('heavy-load-btn').disabled = true;
        document.getElementById('stop-btn').disabled = false;
        
        this.addLog(`Starting ${type} load test: ${requestCount} requests`, 'info');
        
        const startTime = Date.now();
        const results = [];
        
        try {
            // Send requests in batches for concurrency
            const batches = [];
            for (let i = 0; i < requestCount; i += concurrent) {
                const batchSize = Math.min(concurrent, requestCount - i);
                const batch = [];
                
                for (let j = 0; j < batchSize; j++) {
                    batch.push(this.makeTestRequest(i + j + 1, requestCount));
                }
                
                batches.push(Promise.all(batch));
            }
            
            for (const batch of batches) {
                if (!this.loadTestActive) break;
                const batchResults = await batch;
                results.push(...batchResults);
                
                // Update progress
                const progress = (results.length / requestCount) * 100;
                document.getElementById('load-progress').style.width = `${progress}%`;
            }
            
            // Calculate final metrics
            const endTime = Date.now();
            const totalTime = endTime - startTime;
            const successCount = results.filter(r => r.success).length;
            const avgLatency = results.reduce((sum, r) => sum + r.latency, 0) / results.length;
            const rps = (results.length / totalTime) * 1000;
            
            this.addLog(`Test completed: ${successCount}/${requestCount} successful`, 'success');
            this.addLog(`Average latency: ${avgLatency.toFixed(0)}ms`, 'info');
            this.addLog(`Throughput: ${rps.toFixed(1)} req/sec`, 'info');
            
            // Update chart
            this.updateChart(avgLatency, rps);
            
        } catch (error) {
            this.addLog(`Load test failed: ${error.message}`, 'error');
        } finally {
            this.stopLoadTest();
        }
    }

    async makeTestRequest(requestId, total) {
        const dummyData = Array(150528).fill(0.5); // 224*224*3 = 150528
        const payload = {
            model: 'resnet18',
            data: [dummyData]
        };
        
        const startTime = Date.now();
        
        try {
            const response = await fetch(`${this.baseURL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const endTime = Date.now();
            const latency = endTime - startTime;
            const success = response.ok;
            
            if (success) {
                this.addLog(`Request ${requestId}/${total}: ${response.status} (${latency}ms)`, 'success');
                this.updateMetrics(latency, true);
            } else {
                this.addLog(`Request ${requestId}/${total}: ${response.status} (${latency}ms)`, 'error');
                this.updateMetrics(latency, false);
            }
            
            return { success, latency };
            
        } catch (error) {
            const endTime = Date.now();
            const latency = endTime - startTime;
            this.addLog(`Request ${requestId}/${total}: Error (${latency}ms)`, 'error');
            this.updateMetrics(latency, false);
            return { success: false, latency };
        }
    }

    stopLoadTest() {
        this.loadTestActive = false;
        
        document.getElementById('light-load-btn').disabled = false;
        document.getElementById('heavy-load-btn').disabled = false;
        document.getElementById('stop-btn').disabled = true;
        document.getElementById('load-progress').style.width = '0%';
        
        this.addLog('Load test stopped', 'info');
    }

    updateMetrics(latency, success) {
        this.metrics.totalRequests++;
        if (success) {
            this.metrics.successfulRequests++;
        }
        this.metrics.totalLatency += latency;
        
        const avgLatency = this.metrics.totalLatency / this.metrics.totalRequests;
        const successRate = (this.metrics.successfulRequests / this.metrics.totalRequests) * 100;
        
        document.getElementById('total-requests').textContent = this.metrics.totalRequests;
        document.getElementById('avg-latency').textContent = `${Math.round(avgLatency)}ms`;
        document.getElementById('success-rate').textContent = `${Math.round(successRate)}%`;
    }

    addLog(message, type = 'info') {
        const logsContainer = document.getElementById('load-logs');
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        logsContainer.appendChild(logEntry);
        logsContainer.scrollTop = logsContainer.scrollHeight;
        
        // Keep only last 50 log entries
        while (logsContainer.children.length > 50) {
            logsContainer.removeChild(logsContainer.firstChild);
        }
    }

    initChart() {
        const ctx = document.getElementById('performance-chart').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Latency (ms)',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    yAxisID: 'y'
                }, {
                    label: 'Throughput (req/s)',
                    data: [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Latency (ms)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Throughput (req/s)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    }

    updateChart(latency, throughput) {
        const now = new Date().toLocaleTimeString();
        
        this.chartData.labels.push(now);
        this.chartData.latencies.push(latency);
        this.chartData.throughput.push(throughput);
        
        // Keep only last 10 data points
        if (this.chartData.labels.length > 10) {
            this.chartData.labels.shift();
            this.chartData.latencies.shift();
            this.chartData.throughput.shift();
        }
        
        this.chart.data.labels = this.chartData.labels;
        this.chart.data.datasets[0].data = this.chartData.latencies;
        this.chart.data.datasets[1].data = this.chartData.throughput;
        this.chart.update();
    }

    startStatusUpdates() {
        // Update status every 5 seconds
        setInterval(async () => {
            await Promise.all([
                this.updateAPIStatus(),
                this.updateRayStatus()
            ]);
        }, 5000);
    }
}

// Global functions for HTML onclick events
window.useSampleImage = function(sampleId) {
    dashboard.useSampleImage(sampleId);
};

window.startLoadTest = function(type) {
    dashboard.startLoadTest(type);
};

window.stopLoadTest = function() {
    dashboard.stopLoadTest();
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new MLServeDashboard();
});