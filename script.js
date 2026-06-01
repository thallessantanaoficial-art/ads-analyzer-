// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const resetBtn = document.getElementById('resetBtn');
const errorMessage = document.getElementById('errorMessage');

let performanceChart = null;

// File Upload Handling
uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragging');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragging');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragging');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileUpload();
    }
});

fileInput.addEventListener('change', handleFileUpload);

function handleFileUpload() {
    const file = fileInput.files[0];
    
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
        showError('Please upload a CSV file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showError('File size exceeds 10MB limit');
        return;
    }
    
    analyzeFile(file);
}

function analyzeFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred during analysis');
        }
    })
    .catch(error => {
        showError('Error uploading file: ' + error.message);
    });
}

function displayResults(data) {
    // Hide loading and error sections
    hideLoading();
    hideError();
    
    // Display metrics
    displayMetrics(data.metrics);
    
    // Display insights
    displayInsights(data.insights);
    
    // Display charts
    displayCharts(data.daily_performance);
    
    // Display table
    displayTable(data.daily_performance);
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayMetrics(metrics) {
    const metricsGrid = document.getElementById('metricsGrid');
    metricsGrid.innerHTML = '';
    
    const metricsList = [
        {
            label: 'Total Impressions',
            value: metrics.total_impressions,
            unit: '',
            key: 'total_impressions'
        },
        {
            label: 'Total Clicks',
            value: metrics.total_clicks,
            unit: '',
            key: 'total_clicks'
        },
        {
            label: 'Total Spend',
            value: metrics.total_cost ? '$' + metrics.total_cost.toFixed(2) : 'N/A',
            unit: '',
            key: 'total_cost'
        },
        {
            label: 'Total Conversions',
            value: metrics.total_conversions,
            unit: '',
            key: 'total_conversions'
        },
        {
            label: 'Click-Through Rate',
            value: metrics.ctr ? metrics.ctr.toFixed(2) : 'N/A',
            unit: '%',
            key: 'ctr'
        },
        {
            label: 'Cost Per Click',
            value: metrics.cpc ? '$' + metrics.cpc.toFixed(2) : 'N/A',
            unit: '',
            key: 'cpc'
        },
        {
            label: 'Cost Per Mille',
            value: metrics.cpm ? '$' + metrics.cpm.toFixed(2) : 'N/A',
            unit: '',
            key: 'cpm'
        },
        {
            label: 'Cost Per Conversion',
            value: metrics.cpa ? '$' + metrics.cpa.toFixed(2) : 'N/A',
            unit: '',
            key: 'cpa'
        },
        {
            label: 'Conversion Rate',
            value: metrics.conversion_rate ? metrics.conversion_rate.toFixed(2) : 'N/A',
            unit: '%',
            key: 'conversion_rate'
        },
        {
            label: 'Return On Ad Spend',
            value: metrics.roas ? metrics.roas.toFixed(2) : 'N/A',
            unit: 'x',
            key: 'roas'
        },
        {
            label: 'Total Revenue',
            value: metrics.total_revenue ? '$' + metrics.total_revenue.toFixed(2) : 'N/A',
            unit: '',
            key: 'total_revenue'
        },
        {
            label: 'Avg Daily Spend',
            value: metrics.avg_daily_cost ? '$' + metrics.avg_daily_cost.toFixed(2) : 'N/A',
            unit: '',
            key: 'avg_daily_cost'
        }
    ];
    
    metricsList.forEach(metric => {
        if (metric.value !== undefined && metric.value !== 'N/A') {
            const card = document.createElement('div');
            card.className = 'metric-card';
            card.innerHTML = `
                <div class="metric-label">${metric.label}</div>
                <div class="metric-value">
                    ${metric.value}
                    <span class="metric-unit">${metric.unit}</span>
                </div>
            `;
            metricsGrid.appendChild(card);
        }
    });
}

function displayInsights(insights) {
    const insightsList = document.getElementById('insightsList');
    insightsList.innerHTML = '';
    
    if (insights.length === 0) {
        insightsList.innerHTML = '<p>No specific insights available at this time.</p>';
        return;
    }
    
    insights.forEach(insight => {
        const insightItem = document.createElement('div');
        insightItem.className = `insight-item ${insight.type}`;
        insightItem.innerHTML = `
            <div class="insight-title">${insight.title}</div>
            <div class="insight-message">${insight.message}</div>
        `;
        insightsList.appendChild(insightItem);
    });
}

function displayCharts(dailyPerformance) {
    if (!dailyPerformance || dailyPerformance.length === 0) {
        document.getElementById('chartsSection').style.display = 'none';
        return;
    }
    
    // Prepare data for charts
    const dates = dailyPerformance.map(d => d.date);
    const impressions = dailyPerformance.map(d => d.impressions || 0);
    const clicks = dailyPerformance.map(d => d.clicks || 0);
    const cost = dailyPerformance.map(d => d.cost || 0);
    const conversions = dailyPerformance.map(d => d.conversions || 0);
    
    // Destroy existing chart if it exists
    if (performanceChart) {
        performanceChart.destroy();
    }
    
    // Create new chart
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;
    
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Clicks',
                    data: clicks,
                    borderColor: '#4F46E5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    tension: 0.3,
                    yAxisID: 'y',
                    borderWidth: 2,
                    fill: true
                },
                {
                    label: 'Impressions',
                    data: impressions,
                    borderColor: '#06B6D4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    tension: 0.3,
                    yAxisID: 'y1',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Conversions',
                    data: conversions,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.3,
                    yAxisID: 'y',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13,
                            weight: '500'
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Clicks / Conversions',
                        font: { weight: 'bold' }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Impressions',
                        font: { weight: 'bold' }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function displayTable(dailyPerformance) {
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    if (!dailyPerformance || dailyPerformance.length === 0) {
        return;
    }
    
    // Get all keys from first item
    const firstItem = dailyPerformance[0];
    const headers = Object.keys(firstItem);
    
    // Create header
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header.charAt(0).toUpperCase() + header.slice(1);
        tableHeader.appendChild(th);
    });
    
    // Create rows
    dailyPerformance.forEach(item => {
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            let value = item[header];
            
            // Format numeric values
            if (typeof value === 'number') {
                if (header.includes('cost') || header.includes('revenue')) {
                    value = '$' + value.toFixed(2);
                } else if (!Number.isInteger(value)) {
                    value = value.toFixed(2);
                }
            }
            
            td.textContent = value || '-';
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

function showLoading() {
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

function hideLoading() {
    loadingSection.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorSection.style.display = 'none';
}

function resetAnalysis() {
    fileInput.value = '';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loadingSection.style.display = 'none';
    if (performanceChart) {
        performanceChart.destroy();
        performanceChart = null;
    }
    document.getElementById('metricsGrid').innerHTML = '';
    document.getElementById('insightsList').innerHTML = '';
    document.getElementById('tableBody').innerHTML = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

resetBtn.addEventListener('click', resetAnalysis);

// Prevent default drag and drop on document
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});
