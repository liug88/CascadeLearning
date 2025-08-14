// frontend/components/QueryInterface.tsx
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
    
    try {
      const result = await api.query({ query });
      setResponse(result);
    } catch (err) {
      setError('Failed to process query');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Send'}
          </button>
        </div>
      </form>
      
      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-lg mb-4">
          {error}
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