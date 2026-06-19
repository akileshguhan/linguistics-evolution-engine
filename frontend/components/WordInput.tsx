"use client";

import { useState } from 'react';
import { useSimulationStore } from '../lib/store';
import { initSimulation } from '../lib/api';

export default function WordInput() {
  const [words, setWords] = useState<string[]>(['']);
  const { setActiveWords, setLoading, isLoading } = useSimulationStore();

  const handleStart = async () => {
    try {
      setLoading(true);
      const validWords = words.filter(w => w.trim().length > 0);
      if (validWords.length === 0) return;
      const response = await initSimulation(validWords);
      setActiveWords(response.active_words);
    } catch (error) {
      console.error("Failed to initialize:", error);
      alert("Make sure your Python backend is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-8 bg-white/5 backdrop-blur-2xl rounded-3xl shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] border border-white/10 relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <h2 className="text-3xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
        Initialize Proto-Language
      </h2>
      <p className="text-sm text-blue-200/60 mb-8 leading-relaxed font-medium">
        Enter base words using standard characters to begin the evolutionary simulation.
      </p>
      
      <div className="space-y-4 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
        {words.map((word, index) => (
          <div key={index} className="relative flex items-center gap-2">
            <input
              type="text"
              value={word}
              onChange={(e) => {
                const newWords = [...words];
                newWords[index] = e.target.value.toLowerCase();
                setWords(newWords);
              }}
              className="w-full p-4 pl-5 bg-black/40 border border-white/10 rounded-xl text-gray-200 focus:ring-2 focus:ring-blue-500/50 outline-none transition-all placeholder-gray-600 shadow-inner"
              placeholder={`Proto-word ${index + 1}`}
            />
            {words.length > 1 && (
              <button
                onClick={() => {
                  const newWords = [...words];
                  newWords.splice(index, 1);
                  setWords(newWords);
                }}
                className="p-3 text-red-400/70 hover:text-red-400 hover:bg-red-400/10 rounded-xl transition-colors"
                title="Remove word"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path></svg>
              </button>
            )}
          </div>
        ))}
      </div>
      
      <button
        onClick={() => setWords([...words, ''])}
        className="mt-4 text-sm font-medium text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors px-2 py-1 rounded-lg hover:bg-blue-400/10"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        Add Word
      </button>

      <button
        onClick={handleStart}
        disabled={isLoading || words.filter(w => w.trim().length > 0).length === 0}
        className="w-full mt-8 relative group overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-4 px-4 rounded-xl transition-all duration-300 disabled:opacity-50 shadow-[0_0_20px_rgba(79,70,229,0.3)]"
      >
        <span className="relative z-10 flex items-center justify-center gap-2">
          {isLoading ? (
            <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            'Generate Epoch 0'
          )}
        </span>
        <div className="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-[100%] group-hover:animate-shimmer" />
      </button>
    </div>
  );
}