"use client";

import { useSimulationStore } from '../lib/store';
import WordInput from '../components/WordInput';
import ControlPanel from '../components/ControlPanel';
import PhylogeneticTree from '../components/PhylogeneticTree';

export default function Home() {
  const { activeWords, resetSimulation } = useSimulationStore();

  const isStarted = activeWords.length > 0;

  return (
    <main className="min-h-screen p-4 md:p-8 font-sans bg-transparent">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <header className="mb-8 flex justify-between items-end border-b border-white/10 pb-6">
          <div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400 pb-1">
              Linguistic Evolution Engine
            </h1>
            <p className="text-blue-200/60 mt-2 font-medium tracking-wide text-sm md:text-base">
              RAG-Augmented Phonetic State Simulation
            </p>
          </div>
          {isStarted && (
            <button 
              onClick={resetSimulation}
              className="text-sm px-4 py-2 rounded-full border border-red-500/30 text-red-400 hover:bg-red-500/10 font-medium transition-all shadow-[0_0_15px_rgba(239,68,68,0.15)] hover:shadow-[0_0_20px_rgba(239,68,68,0.3)]"
            >
              Reset Simulation
            </button>
          )}
        </header>

        {/* Dynamic App Layout */}
        {!isStarted ? (
          <div className="pt-20">
            <WordInput />
          </div>
        ) : (
          <div className="flex flex-col md:flex-row gap-6 h-[calc(100vh-180px)]">
            <ControlPanel />
            <PhylogeneticTree />
          </div>
        )}

      </div>
    </main>
  );
}