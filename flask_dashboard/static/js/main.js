// Chart instances
let costChart = null;
let netWorthChart = null;
let finalChart = null;

// Format functions
function formatCurrency(value) {
    if (value >= 10000000) {
        return '₹' + (value / 10000000).toFixed(2) + ' Cr';
    } else if (value >= 100000) {
        return '₹' + (value / 100000).toFixed(2) + ' L';
    } else {
        return '₹' + value.toLocaleString('en-IN', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });
    }
}

function formatPercentage(value) {
    return value.toFixed(1) + '%';
}

function formatYears(value) {
    return value + ' year' + (value === 1 ? '' : 's');
}

// Update slider values
function updateSliderDisplays() {
    const sliders = {
        'prop_price': { display: 'prop_price_display', format: formatCurrency },
        'monthly_rent_input': { display: 'monthly_rent_input_display', format: formatCurrency },
        'dp_pct': { display: 'dp_pct_display', format: (v) => v.toFixed(0) + '%' },
        'loan_rate': { display: 'loan_rate_display', format: (v) => v.toFixed(1) + '%' },
        'tenure': { display: 'tenure_display', format: (v) => v.toFixed(0) + ' years' },
        'prop_appr': { display: 'prop_appr_display', format: formatPercentage },
        'rent_appr': { display: 'rent_appr_display', format: formatPercentage },
        'inv_ret': { display: 'inv_ret_display', format: formatPercentage },
        'horizon': { display: 'horizon_display', format: (v) => v.toFixed(0) + ' years' }
    };

    Object.entries(sliders).forEach(([sliderId, config]) => {
        const input = document.getElementById(sliderId);
        if (input) {
            const value = parseFloat(input.value);
            const display = document.getElementById(config.display);
            if (display) {
                display.textContent = config.format(value);
            }
            // Update range gradient
            const percentage = (value - input.min) / (input.max - input.min) * 100;
            input.style.setProperty('--value', percentage + '%');
        }
    });
}

// Attach event listeners to sliders
function initializeSliders() {
    document.querySelectorAll('input[type="range"]').forEach(slider => {
        slider.addEventListener('input', function () {
            updateSliderDisplays();
        });
    });
    updateSliderDisplays();
}

// Get current parameters
function getParameters() {
    return {
        prop_price: parseFloat(document.getElementById('prop_price').value),
        monthly_rent_input: parseFloat(document.getElementById('monthly_rent_input').value),
        dp_pct: parseFloat(document.getElementById('dp_pct').value),
        loan_rate: parseFloat(document.getElementById('loan_rate').value),
        tenure: parseFloat(document.getElementById('tenure').value),
        prop_appr: parseFloat(document.getElementById('prop_appr').value),
        rent_appr: parseFloat(document.getElementById('rent_appr').value),
        inv_ret: parseFloat(document.getElementById('inv_ret').value),
        horizon: parseFloat(document.getElementById('horizon').value)
    };
}

// Calculate DCF
async function calculateDCF() {
    const calculateBtn = document.getElementById('calculateBtn');
    calculateBtn.disabled = true;
    calculateBtn.textContent = 'Calculating...';

    try {
        const params = getParameters();
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error('Calculation failed');
        }

        const data = await response.json();
        updateResults(data);
        updateCharts(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error calculating DCF. Please try again.');
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.textContent = 'Calculate Analysis';
    }
}

// Update Results
function updateResults(data) {
    document.getElementById('emi_display').textContent = formatCurrency(data.emi);
    document.getElementById('dp_display').textContent = formatCurrency(data.dp_amount);

    if (data.breakeven_yr) {
        document.getElementById('breakeven_display').textContent = 'Year ' + data.breakeven_yr;
    } else {
        document.getElementById('breakeven_display').textContent = 'Never';
    }

    const verdictElement = document.getElementById('verdict_display');
    verdictElement.textContent = data.verdict;
    verdictElement.parentElement.classList.remove('text-success', 'text-warning');
    if (data.verdict === 'BUYING') {
        verdictElement.style.color = '#10b981';
    } else {
        verdictElement.style.color = '#f59e0b';
    }
}

// Update Charts
function updateCharts(data) {
    updateCostChart(data);
    updateNetWorthChart(data);
    updateFinalChart(data);
}

// Cost Comparison Chart
function updateCostChart(data) {
    const ctx = document.getElementById('costChart').getContext('2d');

    if (costChart) {
        costChart.destroy();
    }

    costChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.years.map(y => 'Year ' + y),
            datasets: [
                {
                    label: 'Buying Cost',
                    data: data.buy_costs,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#fff'
                },
                {
                    label: 'Renting Cost',
                    data: data.rent_costs,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#f59e0b',
                    pointBorderColor: '#fff'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 500
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Net Worth Chart
function updateNetWorthChart(data) {
    const ctx = document.getElementById('netWorthChart').getContext('2d');

    if (netWorthChart) {
        netWorthChart.destroy();
    }

    netWorthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.years.map(y => 'Year ' + y),
            datasets: [
                {
                    label: 'Buying Net Worth',
                    data: data.buy_nw,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff'
                },
                {
                    label: 'Renting Net Worth',
                    data: data.rent_nw,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: '#fff'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 500
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Final Net Worth Comparison
function updateFinalChart(data) {
    const ctx = document.getElementById('finalChart').getContext('2d');

    if (finalChart) {
        finalChart.destroy();
    }

    finalChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Final Net Worth'],
            datasets: [
                {
                    label: 'Buying',
                    data: [data.final_buy_nw],
                    backgroundColor: '#3b82f6',
                    borderRadius: 6,
                    borderSkipped: false
                },
                {
                    label: 'Renting',
                    data: [data.final_rent_nw],
                    backgroundColor: '#8b5cf6',
                    borderRadius: 6,
                    borderSkipped: false
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 500
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    initializeSliders();

    const calculateBtn = document.getElementById('calculateBtn');
    calculateBtn.addEventListener('click', calculateDCF);

    // Load defaults and calculate initially
    calculateDCF();
});

// Real-time calculation (optional - uncomment to enable)
// document.addEventListener('change', function(e) {
//     if (e.target.type === 'range') {
//         calculateDCF();
//     }
// });
