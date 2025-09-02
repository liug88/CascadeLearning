'use client';

import { useState } from 'react';
import { api, QueryResponse } from '../lib/api';
import { MetricCard } from './MetricCard';

export function QueryInterface() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    setResponse(null);
    
    try {
      const result = await api.query({ query });
      setResponse(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to process query';
      setError(errorMessage);
      console.error('Query error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResponse(null);
    setError(null);
  };
  
  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything... (e.g., 'What is 2+2?', 'Explain recursion in Python')"
            className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                Processing...
              </span>
            ) : (
              'Send Query'
            )}
          </button>
          {(query || response || error) && (
            <button
              type="button"
              onClick={handleClear}
              className="px-4 py-3 text-gray-600 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-all"
              disabled={loading}
            >
              Clear
            </button>
          )}
        </div>
      </form>
      
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-4 flex items-center gap-2">
          <span className="text-red-500 text-xl">⚠️</span>
          <div>
            <p className="font-medium">Error processing your query</p>
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}

      {loading && !response && (
        <div className="p-6 bg-blue-50 border border-blue-200 rounded-lg mb-4">
          <div className="flex items-center gap-3">
            <div className="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            <div>
              <p className="text-blue-800 font-medium">Processing your query...</p>
              <p className="text-blue-600 text-sm">The cascade system is selecting the optimal model</p>
            </div>
          </div>
        </div>
      )}
      
      {response && (
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Response:</h3>
            <p className="whitespace-pre-wrap">{response.response}</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard
              title="Model Used"
              value={response.model_used}
              subtitle={response.model_size}
              color="blue"
            />
            <MetricCard
              title="Cost"
              value={`$${response.cost.toFixed(4)}`}
              subtitle={`${response.tokens} tokens`}
              color="green"
            />
            <MetricCard
              title="Saved"
              value={`$${response.savings.toFixed(4)}`}
              subtitle={`${((response.savings / (response.cost + response.savings)) * 100).toFixed(1)}% savings`}
              color="yellow"
            />
            <MetricCard
              title="Response Time"
              value={`${response.response_time.toFixed(2)}s`}
              subtitle={`Confidence: ${(response.confidence * 100).toFixed(1)}%`}
              color="red"
            />
          </div>
          
          <div className="p-3 bg-gray-100 rounded text-sm">
            <p><strong>Routing Reason:</strong> {response.routing_reason}</p>
          </div>
        </div>
      )}
    </div>
  );
}