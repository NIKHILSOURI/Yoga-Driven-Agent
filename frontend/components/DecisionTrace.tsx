'use client';

import { useState, useEffect } from 'react';
import { getTodayTraces, getRecentTraces } from '@/lib/api';
import { GitBranch, Clock, Lightbulb, Database, Zap } from 'lucide-react';

interface DecisionTraceProps {
  userId: number;
}

export default function DecisionTrace({ userId }: DecisionTraceProps) {
  const [traces, setTraces] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'today' | 'recent'>('today');

  useEffect(() => {
    loadTraces();
  }, [userId, viewMode]);

  const loadTraces = async () => {
    try {
      const data = viewMode === 'today' 
        ? await getTodayTraces(userId)
        : await getRecentTraces(userId, 10);
      setTraces(data);
    } catch (error) {
      console.error('Failed to load traces:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Decision Trace Viewer</h1>
          <p className="text-gray-600">See how the AI makes decisions for your wellness</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setViewMode('today')}
            className={`px-4 py-2 rounded-lg transition ${
              viewMode === 'today'
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Today
          </button>
          <button
            onClick={() => setViewMode('recent')}
            className={`px-4 py-2 rounded-lg transition ${
              viewMode === 'recent'
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Recent
          </button>
        </div>
      </div>

      {traces.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
          <GitBranch className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No decision traces available yet</p>
          <p className="text-sm text-gray-500 mt-2">Complete a check-in to see AI reasoning</p>
        </div>
      ) : (
        <div className="space-y-4">
          {traces.map((trace) => (
            <div key={trace.id} className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Zap className="text-green-500" size={20} />
                    <h3 className="text-lg font-semibold text-gray-800">{trace.agent_name}</h3>
                  </div>
                  <p className="text-sm text-gray-500">
                    <Clock size={14} className="inline mr-1" />
                    {new Date(trace.date).toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Explanation */}
              <div className="bg-blue-50 rounded-lg p-4 mb-4">
                <div className="flex items-start space-x-2">
                  <Lightbulb className="text-blue-500 flex-shrink-0 mt-1" size={18} />
                  <div>
                    <h4 className="font-semibold text-blue-900 mb-1">Decision Explanation</h4>
                    <p className="text-sm text-blue-800">{trace.explanation}</p>
                  </div>
                </div>
              </div>

              {/* Triggered Rules */}
              {trace.triggered_rules && trace.triggered_rules.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-800 mb-2">Triggered Rules</h4>
                  <div className="space-y-2">
                    {trace.triggered_rules.map((rule: any, idx: number) => (
                      <div key={idx} className="bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded">
                        <p className="text-sm font-medium text-yellow-900">{rule.rule_id}</p>
                        <p className="text-xs text-yellow-700 mt-1">Condition: {rule.condition}</p>
                        <p className="text-xs text-yellow-700">Action: {rule.action}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Memory Retrieved */}
              {trace.memory_retrieved && trace.memory_retrieved.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-800 mb-2">Memory Retrieved</h4>
                  <div className="flex items-start space-x-2">
                    <Database className="text-purple-500 flex-shrink-0 mt-1" size={18} />
                    <div className="flex-1 space-y-1">
                      {trace.memory_retrieved.slice(0, 3).map((mem: any, idx: number) => (
                        <div key={idx} className="bg-purple-50 rounded p-2">
                          <p className="text-xs font-medium text-purple-900">{mem.type}</p>
                          <p className="text-xs text-purple-700">{JSON.stringify(mem.content).substring(0, 100)}...</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Plan Chosen */}
              {trace.plan_chosen && (
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Plan Chosen</h4>
                  <div className="bg-green-50 rounded-lg p-4">
                    <pre className="text-xs text-gray-800 overflow-x-auto bg-gray-50 p-3 rounded">
                      {JSON.stringify(trace.plan_chosen, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Tools Called */}
              {trace.tools_called && (
                <div className="mt-4 pt-4 border-t">
                  <h4 className="font-semibold text-gray-800 mb-2">External Tools Used</h4>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(trace.tools_called).map(([tool, used]: [string, any]) => (
                      <span
                        key={tool}
                        className={`px-3 py-1 rounded-full text-xs ${
                          used
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-500'
                        }`}
                      >
                        {tool}: {used ? '✓' : '✗'}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

