import { QueryInterface } from "../../components/QueryInterface";
import { StatsDashboard } from "../../components/StatsDashboard";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Cascade Learning Platform
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            An intelligent query routing system that automatically selects the most 
            cost-effective AI model for your requests while maintaining quality.
          </p>
        </header>

        <main className="max-w-6xl mx-auto space-y-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">
              Try the Cascade Query System
            </h2>
            <QueryInterface />
          </div>

          <StatsDashboard />

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                🎯 Smart Routing
              </h3>
              <p className="text-gray-600">
                Automatically routes queries to the most appropriate model based on complexity and cost.
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                💰 Cost Optimization
              </h3>
              <p className="text-gray-600">
                Reduces AI costs by up to 70% while maintaining response quality.
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                ⚡ Fast Response
              </h3>
              <p className="text-gray-600">
                Optimized for speed with intelligent caching and model selection.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
