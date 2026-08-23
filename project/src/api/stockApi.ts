import axios from 'axios';
import { PairAnalysis } from '../types/stock';

const API_URL = import.meta.env.VITE_API_URL ?? '/api';

export const analyzePair = async (
  stockA: string,
  stockB: string,
  startDate: string,
  endDate: string,
  minSpread: number,
  operationalCost: number
): Promise<PairAnalysis> => {
  const response = await axios.get(`${API_URL}/analyze-pair`, {
    params: {
      stockA,
      stockB,
      startDate,
      endDate,
      minSpread,
      operationalCost
    }
  });
  return response.data;
};