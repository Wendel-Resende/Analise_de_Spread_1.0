import axios from 'axios';
import { PairAnalysis } from '../types/stock';

const API_URL = 'https://your-backend-api.com'; // You'll need to replace this with your actual API endpoint

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