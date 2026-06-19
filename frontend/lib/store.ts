import { create } from 'zustand';
import { WordState } from './api';

interface SimulationState {
  // Game State
  activeWords: WordState[];
  currentEpoch: number;
  isLoading: boolean;
  
  // Environment Parameters
  isolation: number;
  density: number;
  literacy: number;
  climate: number;
  customEventText: string;

  // Actions
  setActiveWords: (words: WordState[]) => void;
  incrementEpoch: () => void;
  setEpoch: (epoch: number) => void;
  setLoading: (status: boolean) => void;
  setParameters: (isolation: number, density: number, literacy: number, climate: number, event: string) => void;
  resetSimulation: () => void;
}

export const useSimulationStore = create<SimulationState>((set) => ({
  activeWords: [],
  currentEpoch: 0,
  isLoading: false,
  
  isolation: 0.5,
  density: 0.5,
  literacy: 0.5,
  climate: 0.5,
  customEventText: '',

  setActiveWords: (words) => set({ activeWords: words }),
  
  incrementEpoch: () => set((state) => ({ currentEpoch: state.currentEpoch + 1 })),

  setEpoch: (epoch) => set({ currentEpoch: epoch }),
  
  setLoading: (status) => set({ isLoading: status }),
  
  setParameters: (isolation, density, literacy, climate, event) => 
    set({ isolation, density, literacy, climate, customEventText: event }),
    
  resetSimulation: () => set({ 
    activeWords: [], 
    currentEpoch: 0, 
    isolation: 0.5, 
    density: 0.5, 
    literacy: 0.5,
    climate: 0.5,
    customEventText: '' 
  }),
}));