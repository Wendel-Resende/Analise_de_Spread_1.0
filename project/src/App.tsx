import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StockPairAnalyzer } from './components/StockPairAnalyzer';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Stock Spread Analyzer
            </h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <StockPairAnalyzer />
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;