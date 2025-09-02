'use client';

import { useState, useEffect } from 'react';
import { api, StatsResponse } from '../lib/api';
import { MetricCard } from './MetricCard';

export function StatsDashboard() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.getStats();
      setStats(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch statistics';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const runDemo = async () => {
    setLoading(true);
    setError(null);
    
    try {
      await api.runDemo();
      await fetchStats(); // Refresh stats after demo
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to run demo';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading && !stats) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-800">System Statistics</h2>
        <div className="flex gap-2">
          <button
            onClick={fetchStats}
            disabled={loading}
            className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 disabled:opacity-50 transition-all"
          >
            Refresh
          </button>
          <button
            onClick={runDemo}
            disabled={loading}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-all"
          >
            {loading ? 'Running...' : 'Run Demo'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-4">
          <p className="font-medium">Error: {error}</p>
        </div>
      )}

      {stats && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricCard
              title="Total Queries"
              value={stats.total_queries.toLocaleString()}
              subtitle="Processed"
              color="blue"
            />
            <MetricCard
              title="Total Cost"
              value={`$${stats.total_cost.toFixed(4)}`}
              subtitle="Spent"
              color="red"
            />
            <MetricCard
              title="Total Saved"
              value={`$${stats.total_saved.toFixed(4)}`}
              subtitle={`${stats.savings_percentage.toFixed(1)}% savings`}
              color="green"
            />
            <MetricCard
              title="Avg Response Time"
              value={`${stats.avg_response_time.toFixed(2)}s`}
              subtitle="Per query"
              color="yellow"
            />
          </div>

          {Object.keys(stats.model_distribution).length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Model Usage Distribution</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(stats.model_distribution).map(([modelSize, count]) => (
                  <div key={modelSize} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="font-medium capitalize">{modelSize} Model</span>
                      <span className="text-2xl font-bold">{count}</span>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            modelSize === 'tiny' 
                              ? 'bg-green-500' 
                              : modelSize === 'medium'
                              ? 'bg-yellow-500'
                              : 'bg-red-500'
                          }`}
                          style={{
                            width: `${((count / stats.total_queries) * 100).toFixed(1)}%`
                          }}
                        ></div>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {((count / stats.total_queries) * 100).toFixed(1)}% of queries
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}