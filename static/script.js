document.getElementById('finance-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const goals = document.getElementById('financial_goals').value.trim();
    const situation = document.getElementById('current_situation').value.trim();
    const provider = document.getElementById('provider').value;
    const apiKey = document.getElementById('api_key').value.trim();

    const btn = document.getElementById('submit-btn');
    const spinner = document.getElementById('spinner');
    const btnText = document.querySelector('.btn-text');
    const resultsDiv = document.getElementById('results');
    const markdownContainer = document.getElementById('markdown-content');

    // UI Loading State
    btn.disabled = true;
    spinner.classList.remove('hidden');
    btnText.textContent = "Analyzing & Generating Strategy...";
    resultsDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                financial_goals: goals,
                current_situation: situation,
                provider: provider,
                api_key: apiKey
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "An error occurred while generating the plan.");
        }

        // Parse markdown and inject into UI
        markdownContainer.innerHTML = marked.parse(data.plan);
        resultsDiv.classList.remove('hidden');

        // Optional smooth scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        // Reset UI State
        btn.disabled = false;
        spinner.classList.add('hidden');
        btnText.textContent = "Generate Financial Plan";
    }
});

document.getElementById('export-btn').addEventListener('click', () => {
    // Find the table within the markdown content
    const table = document.querySelector('#markdown-content table');
    if (!table) {
        alert("No table found to export! Please generate a plan first.");
        return;
    }

    // Convert the HTML table to a SheetJS workbook
    const wb = XLSX.utils.table_to_book(table, {sheet: "Financial Plan"});
    
    // Export the workbook to an Excel file
    XLSX.writeFile(wb, 'AI_Financial_Plan.xlsx');
});

// Dynamic API Key Link Logic
const providerUrls = {
    'gemini': {
        name: 'Google AI Studio',
        url: 'https://aistudio.google.com/app/apikey'
    },
    'openai': {
        name: 'OpenAI Dashboard',
        url: 'https://platform.openai.com/api-keys'
    },
    'groq': {
        name: 'Groq Cloud',
        url: 'https://console.groq.com/keys'
    }
};

const providerSelect = document.getElementById('provider');
const apiKeyHelper = document.getElementById('api-key-helper');

function updateApiKeyLink() {
    const selected = providerSelect.value;
    const info = providerUrls[selected];
    if (info) {
        apiKeyHelper.innerHTML = `<a href="${info.url}" target="_blank" rel="noopener noreferrer">Get your ${info.name} API Key</a>`;
    } else {
        apiKeyHelper.innerHTML = '';
    }
}

// Listen for changes
providerSelect.addEventListener('change', updateApiKeyLink);

// Initialize on load
updateApiKeyLink();
