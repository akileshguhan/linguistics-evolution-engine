import axios from 'axios';

// Automatically uses localhost during dev, and your Render URL in production
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface WordState {
  text: string;
  epoch: number;
  root_word: string;
}

export const initSimulation = async (words: string[]) => {
  const response = await apiClient.post('/simulation/init', { words });
  return response.data;
};

export const advanceEpoch = async (
  words: WordState[],
  geography_isolation: number,
  population_density: number,
  literacy_rate: number,
  climate_humidity: number,
  custom_event_text: string
) => {
  const response = await apiClient.post('/simulation/advance', {
    words,
    geography_isolation,
    population_density,
    literacy_rate,
    climate_humidity,
    custom_event_text,
  });
  return response.data;
};

export const fetchTreeData = async () => {
  const response = await apiClient.get('/simulation/tree');
  return response.data;
};

export const fetchEpochState = async (epoch: number) => {
  const response = await apiClient.get(`/simulation/state/${epoch}`);
  return response.data;
};