export interface StockData {
  date: string;
  high: number;
}

export interface SpreadAnalysis {
  spreadMean: number;
  spreadMax: number;
  totalOpportunities: number;
  averageReturn: number;
  totalReturn: number;
  correlation: number;
}

export interface PairAnalysis {
  pair: string;
  analysis: SpreadAnalysis;
  opportunities: Array<{
    date: string;
    difference: number;
    grossReturn: number;
    netReturn: number;
    returnPercentage: number;
  }>;
}