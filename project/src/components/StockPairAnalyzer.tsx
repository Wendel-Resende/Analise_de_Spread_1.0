import React, { lazy, Suspense, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { PairAnalysis } from '../types/stock';
import { analyzePair } from '../api/stockApi';

const Plot = lazy(() => import('react-plotly.js'));

export const StockPairAnalyzer: React.FC = () => {
  const [stockA, setStockA] = useState('PETR3');
  const [stockB, setStockB] = useState('PETR4');
  const [minSpread, setMinSpread] = useState(1.0);
  const [operationalCost, setOperationalCost] = useState(5.0);

  const startDate = format(new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd');
  const endDate = format(new Date(), 'yyyy-MM-dd');

  const { data, isLoading, error, refetch } = useQuery<PairAnalysis>({
    queryKey: ['pairAnalysis', stockA, stockB, minSpread, operationalCost],
    queryFn: () => analyzePair(stockA, stockB, startDate, endDate, minSpread, operationalCost),
    enabled: false,
  });

  return (
    <div className="p-4">
      <div className="grid grid-cols-2 gap-4 mb-4">
        <input
          type="text"
          value={stockA}
          onChange={(e) => setStockA(e.target.value.toUpperCase())}
          className="border p-2 rounded"
          placeholder="Stock A (e.g. PETR3)"
        />
        <input
          type="text"
          value={stockB}
          onChange={(e) => setStockB(e.target.value.toUpperCase())}
          className="border p-2 rounded"
          placeholder="Stock B (e.g. PETR4)"
        />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <input
          type="number"
          value={minSpread}
          onChange={(e) => setMinSpread(Number(e.target.value))}
          className="border p-2 rounded"
          placeholder="Minimum Spread"
        />
        <input
          type="number"
          value={operationalCost}
          onChange={(e) => setOperationalCost(Number(e.target.value))}
          className="border p-2 rounded"
          placeholder="Operational Cost"
        />
      </div>

      <button
        type="button"
        onClick={() => void refetch()}
        disabled={isLoading || stockA === stockB}
        className="rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading ? 'Analisando...' : 'Analisar par'}
      </button>

      {stockA === stockB && (
        <p className="mt-2 text-sm text-red-600">Informe duas ações diferentes.</p>
      )}

      {error && (
        <p className="mt-4 rounded bg-red-50 p-3 text-red-700">
          Não foi possível consultar a API: {(error as Error).message}
        </p>
      )}

      {data && (
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold">Average Spread</h3>
              <p className="text-2xl">R$ {data.analysis.spreadMean.toFixed(2)}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold">Total Opportunities</h3>
              <p className="text-2xl">{data.analysis.totalOpportunities}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold">Total Return</h3>
              <p className="text-2xl">R$ {data.analysis.totalReturn.toFixed(2)}</p>
            </div>
          </div>

          {data.opportunities.length > 0 && (
            <Suspense fallback={<div className="rounded bg-white p-4">Carregando gráfico...</div>}>
              <Plot
                data={[
                  {
                    x: data.opportunities.map(o => o.date),
                    y: data.opportunities.map(o => o.difference),
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Spread'
                  }
                ]}
                layout={{
                  title: `Spread ${stockA}/${stockB}`,
                  xaxis: { title: 'Date' },
                  yaxis: { title: 'Spread (R$)' }
                }}
                style={{ width: '100%', height: '400px' }}
              />
            </Suspense>
          )}
        </div>
      )}
    </div>
  );
};