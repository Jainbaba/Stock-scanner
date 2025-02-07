import { API_BASE_URL } from '../config';

export interface Stock {
  yearweek: string;
  created_date: string;
  symbols: string[];
  count: number;
}

export interface NewStocks {
  current_yearweek: string;
  previous_yearweek: string;
  new_symbols_count: number;
  new_symbols: string[];
}

export interface Log {
  timestamp: string;
  yearweek: string;
  success: boolean;
  message: string;
  symbols_count: number;
  source: string;
}

export async function getCurrentStocks(): Promise<Stock> {
  const response = await fetch(`${API_BASE_URL}/api/stocks/current`);
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch current stocks');
  }
  return data.data;
}

export async function getNewStocks(): Promise<NewStocks> {
  const response = await fetch(`${API_BASE_URL}/api/stocks/new`);
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch new stocks');
  }
  return data.data;
}

export async function getLogs(): Promise<Log[]> {
  const response = await fetch(`${API_BASE_URL}/api/logs`);
  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch logs');
  }
  return data.data;
}
