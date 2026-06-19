"use client";

import { useSimulationStore } from '../lib/store';
import { advanceEpoch } from '../lib/api';

export default function ControlPanel() {
  const store = useSimulationStore();

  const handleAdvance = async () => {
    try {
      store.setLoading(true);
      const response = await advanceEpoch(
        store.activeWords,
        store.isolation,
        store.density,
        store.literacy,
        store.climate,
        store.customEventText
      );
      store.setActiveWords(response.active_words);
      store.incrementEpoch();
    } catch (error) {
      console.error("Failed to advance epoch:", error);
    } finally {
      store.setLoading(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl p-6 rounded-2xl shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] border border-white/20 w-full md:w-80 flex-shrink-0 flex flex-col gap-6 text-gray-200">
      <div>
        <h3 className="font-bold text-white text-xl mb-1 tracking-wide">Evolutionary Pressures</h3>
        <p className="text-xs text-blue-200/70 mb-4">Dial in vector mutation weights to shape linguistic drift.</p>
      </div>

      <div className="space-y-4 max-h-[40vh] overflow-y-auto pr-2 custom-scrollbar">
        <div>
          <label className="block text-sm font-medium text-blue-100 mb-2">
            Geographical Isolation <span className="float-right text-blue-400 font-mono">{(store.isolation * 100).toFixed(0)}%</span>
          </label>
          <input 
            type="range" min="0" max="1" step="0.05" 
            value={store.isolation} 
            onChange={(e) => store.setParameters(parseFloat(e.target.value), store.density, store.literacy, store.climate, store.customEventText)}
            className="w-full h-2 bg-gray-700/50 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
          <div className="flex justify-between text-[10px] text-gray-400 mt-2 uppercase tracking-wider font-semibold">
            <span>High Contact</span><span>High Altitude</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-blue-100 mb-2">
            Population Density <span className="float-right text-purple-400 font-mono">{(store.density * 100).toFixed(0)}%</span>
          </label>
          <input 
            type="range" min="0" max="1" step="0.05" 
            value={store.density} 
            onChange={(e) => store.setParameters(store.isolation, parseFloat(e.target.value), store.literacy, store.climate, store.customEventText)}
            className="w-full h-2 bg-gray-700/50 rounded-lg appearance-none cursor-pointer accent-purple-500"
          />
          <div className="flex justify-between text-[10px] text-gray-400 mt-2 uppercase tracking-wider font-semibold">
            <span>Nomadic</span><span>Urbanized</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-blue-100 mb-2">
            Literacy & Standardization <span className="float-right text-green-400 font-mono">{(store.literacy * 100).toFixed(0)}%</span>
          </label>
          <input 
            type="range" min="0" max="1" step="0.05" 
            value={store.literacy} 
            onChange={(e) => store.setParameters(store.isolation, store.density, parseFloat(e.target.value), store.climate, store.customEventText)}
            className="w-full h-2 bg-gray-700/50 rounded-lg appearance-none cursor-pointer accent-green-500"
          />
          <div className="flex justify-between text-[10px] text-gray-400 mt-2 uppercase tracking-wider font-semibold">
            <span>Oral Tradition</span><span>Written Standard</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-blue-100 mb-2">
            Climate Humidity <span className="float-right text-amber-400 font-mono">{(store.climate * 100).toFixed(0)}%</span>
          </label>
          <input 
            type="range" min="0" max="1" step="0.05" 
            value={store.climate} 
            onChange={(e) => store.setParameters(store.isolation, store.density, store.literacy, parseFloat(e.target.value), store.customEventText)}
            className="w-full h-2 bg-gray-700/50 rounded-lg appearance-none cursor-pointer accent-amber-500"
          />
          <div className="flex justify-between text-[10px] text-gray-400 mt-2 uppercase tracking-wider font-semibold">
            <span>Cold & Dry</span><span>Hot & Humid</span>
          </div>
        </div>
      </div>

      <div className="mt-2">
        <label className="block text-sm font-medium text-blue-100 mb-2">Historical Shock Event</label>
        <textarea 
          value={store.customEventText}
          onChange={(e) => store.setParameters(store.isolation, store.density, store.literacy, store.climate, e.target.value)}
          placeholder="e.g., A massive volcanic eruption isolated the tribes in the deep mountains..."
          className="w-full p-3 h-24 border border-white/10 rounded-xl text-sm bg-black/40 text-gray-200 placeholder-gray-500 outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all resize-none shadow-inner"
        />
        <p className="text-[10px] text-blue-300/50 mt-2 leading-tight">
          Describe a natural disaster, invasion, or cultural shift. The RAG engine will semantically match it to a known evolutionary pressure profile.
        </p>
      </div>

      <button 
        onClick={handleAdvance}
        disabled={store.isLoading}
        className="relative group w-full mt-auto bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-4 px-4 rounded-xl transition-all duration-300 disabled:opacity-50 overflow-hidden shadow-[0_0_20px_rgba(59,130,246,0.4)]"
      >
        <span className="relative z-10 flex items-center justify-center gap-2">
          {store.isLoading ? (
            <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            `Advance to Epoch ${store.currentEpoch + 1}`
          )}
        </span>
        <div className="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-[100%] group-hover:animate-shimmer" />
      </button>
    </div>
  );
}