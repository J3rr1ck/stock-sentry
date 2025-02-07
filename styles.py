# CSS styles for the application
STYLES = """
<style>
.stDownloadButton button {
    width: 100%;
    margin-top: 1rem;
}

.stock-metrics {
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}

.loading-spinner {
    text-align: center;
    padding: 2rem;
}

.error-message {
    color: red;
    padding: 1rem;
    border: 1px solid red;
    border-radius: 5px;
    margin: 1rem 0;
}

/* News Feed Styles */
.news-card {
    padding: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    margin-bottom: 1rem;
    background-color: white;
}

.news-title {
    font-weight: bold;
    color: #1f77b4;
    margin-bottom: 0.5rem;
}

.news-meta {
    font-size: 0.8rem;
    color: #666;
    margin-bottom: 0.5rem;
}

.news-summary {
    font-size: 0.9rem;
    color: #333;
}

/* Stock Insight Card Styles */
.insight-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.card-header h2 {
    margin: 0;
    color: #1f77b4;
    font-size: 1.5rem;
}

.price-change {
    font-size: 1.2rem;
    font-weight: bold;
}

.card-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}

.metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.metric .label {
    font-size: 0.8rem;
    color: #666;
    margin-bottom: 0.25rem;
}

.metric .value {
    font-size: 1.1rem;
    font-weight: bold;
    color: #333;
}

.card-footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
    text-align: right;
}

.card-footer .timestamp {
    font-size: 0.8rem;
    color: #999;
}

/* AI Chat Styles */
.ai-chat-container {
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.ai-response {
    background: #f8f9fa;
    border-left: 4px solid #1f77b4;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 0 4px 4px 0;
}
</style>
"""
