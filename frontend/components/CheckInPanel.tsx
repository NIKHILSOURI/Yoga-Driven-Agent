'use client';

import { useState } from 'react';
import { submitCheckIn } from '@/lib/api';
import { CheckCircle, Loader } from 'lucide-react';

interface CheckInPanelProps {
  userId: number;
}

export default function CheckInPanel({ userId }: CheckInPanelProps) {
  const [formData, setFormData] = useState({
    mood: 'neutral',
    mood_score: 5,
    appetite: 5,
    energy: 5,
    sleep_hours: 7,
    adherence: 50,
    ingredients: '',
    notes: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await submitCheckIn(userId, formData);
      setResult(response);
    } catch (error: any) {
      alert('Check-in failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Daily Check-in</h1>
        <p className="text-gray-600">Share how you're feeling today</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8 space-y-6">
        {/* Mood */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Mood</label>
          <div className="flex space-x-4">
            {['happy', 'neutral', 'sad', 'stressed'].map((mood) => (
              <button
                key={mood}
                type="button"
                onClick={() => setFormData({ ...formData, mood })}
                className={`px-6 py-3 rounded-lg border-2 transition ${
                  formData.mood === mood
                    ? 'border-green-500 bg-green-50 text-green-700'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {mood.charAt(0).toUpperCase() + mood.slice(1)}
              </button>
            ))}
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Mood Score: {formData.mood_score}/10
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.mood_score}
              onChange={(e) => setFormData({ ...formData, mood_score: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>
        </div>

        {/* Appetite */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Appetite: {formData.appetite}/10
          </label>
          <input
            type="range"
            min="0"
            max="10"
            step="0.5"
            value={formData.appetite}
            onChange={(e) => setFormData({ ...formData, appetite: parseFloat(e.target.value) })}
            className="w-full"
          />
        </div>

        {/* Energy */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Energy Level: {formData.energy}/10
          </label>
          <input
            type="range"
            min="0"
            max="10"
            step="0.5"
            value={formData.energy}
            onChange={(e) => setFormData({ ...formData, energy: parseFloat(e.target.value) })}
            className="w-full"
          />
        </div>

        {/* Sleep */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Sleep Hours</label>
          <input
            type="number"
            min="0"
            max="24"
            step="0.5"
            value={formData.sleep_hours}
            onChange={(e) => setFormData({ ...formData, sleep_hours: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 bg-white text-gray-900"
          />
        </div>

        {/* Adherence */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Yesterday's Plan Adherence: {formData.adherence}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={formData.adherence}
            onChange={(e) => setFormData({ ...formData, adherence: parseInt(e.target.value) })}
            className="w-full"
          />
        </div>

        {/* Ingredients */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Available Ingredients (comma-separated)
            <span className="text-xs text-gray-500 ml-2">We'll create breakfast, lunch, dinner & snacks for the day</span>
          </label>
          <input
            type="text"
            value={formData.ingredients}
            onChange={(e) => setFormData({ ...formData, ingredients: e.target.value })}
            placeholder="e.g., rice, lentils, vegetables, spices, fruits, nuts, yogurt, oats"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 bg-white text-gray-900 placeholder-gray-400"
          />
          <p className="text-xs text-gray-500 mt-1">
            💡 Tip: List all ingredients you have. The AI will create a complete daily meal plan using them!
          </p>
        </div>

        {/* Notes */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Additional Notes</label>
          <textarea
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 bg-white text-gray-900 placeholder-gray-400"
            placeholder="Any additional information..."
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-500 text-white py-3 rounded-lg font-semibold hover:bg-green-600 transition disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader className="animate-spin" size={20} />
              <span>Processing...</span>
            </>
          ) : (
            <>
              <CheckCircle size={20} />
              <span>Submit Check-in</span>
            </>
          )}
        </button>
      </form>

      {/* Results */}
      {result && (
        <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold text-gray-800">Your Personalized Plan</h2>
          
          {result.reasoning && (
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-gray-800">AI Reasoning</h3>
              <p className="text-sm text-gray-700">{result.reasoning.explanation}</p>
              <div className="mt-2">
                <p className="text-xs text-gray-600">
                  Energy Trend: <span className="font-semibold text-gray-800">{result.reasoning.energy_trend}</span> | 
                  Appetite Trend: <span className="font-semibold text-gray-800">{result.reasoning.appetite_trend}</span>
                </p>
              </div>
            </div>
          )}

          {result.plans?.yoga && (
            <div className="bg-green-50 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-gray-800">Today's Yoga Plan</h3>
              <p className="text-sm text-gray-700">{result.plans.yoga.description}</p>
              <a
                href={result.plans.yoga.youtube_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-green-600 hover:underline text-sm mt-2 inline-block"
              >
                Watch: {result.plans.yoga.youtube_title}
              </a>
            </div>
          )}

          {result.plans?.nutrition && result.plans.nutrition.length > 0 && (
            <div className="bg-purple-50 rounded-lg p-4">
              <h3 className="font-semibold mb-3 text-gray-800 text-lg">Complete Daily Meal Plan</h3>
              <p className="text-sm text-gray-600 mb-4">
                Your personalized meals for the day using your available ingredients
              </p>
              <div className="space-y-3">
                {result.plans.nutrition.map((meal: any, idx: number) => (
                  <div key={idx} className="bg-white rounded-lg p-4 border border-purple-200 shadow-sm">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <p className="font-semibold text-gray-800 capitalize text-base">
                          {meal.meal_type}: {meal.recipe_name}
                        </p>
                        {meal.sattvic_score && (
                          <p className="text-xs text-green-600 mt-1">
                            Sattvic Score: {meal.sattvic_score}/10 | 
                            Simplicity: {meal.simplicity_index}/10
                          </p>
                        )}
                      </div>
                    </div>
                    
                    {meal.ingredients && Array.isArray(meal.ingredients) && meal.ingredients.length > 0 && (
                      <div className="mb-2">
                        <p className="text-xs font-medium text-gray-600 mb-1">Ingredients:</p>
                        <p className="text-xs text-gray-700">
                          {meal.ingredients.slice(0, 6).join(", ")}
                          {meal.ingredients.length > 6 ? "..." : ""}
                        </p>
                      </div>
                    )}
                    
                    {meal.nutrients && (
                      <div className="mb-2 flex flex-wrap gap-3 text-xs">
                        <span className="text-gray-600">
                          Calories: <span className="font-semibold text-gray-800">{Math.round(meal.nutrients.calories || 0)}</span>
                        </span>
                        <span className="text-gray-600">
                          Protein: <span className="font-semibold text-gray-800">{meal.nutrients.protein?.toFixed(1) || 0}g</span>
                        </span>
                        <span className="text-gray-600">
                          Fiber: <span className="font-semibold text-gray-800">{meal.nutrients.fiber?.toFixed(1) || 0}g</span>
                        </span>
                      </div>
                    )}
                    
                    <details className="mt-2">
                      <summary className="text-xs text-purple-600 cursor-pointer hover:text-purple-700 font-medium">
                        View Full Instructions
                      </summary>
                      <p className="text-xs text-gray-700 mt-2 whitespace-pre-wrap bg-gray-50 p-2 rounded">
                        {meal.instructions || "No instructions available."}
                      </p>
                    </details>
                  </div>
                ))}
                
                {/* Daily Nutrition Summary */}
                {result.plans.nutrition.length > 0 && (
                  <div className="mt-4 bg-white rounded-lg p-4 border-2 border-purple-300 shadow-md">
                    <p className="text-sm font-semibold text-gray-800 mb-3">📊 Daily Nutrition Summary</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                      <div className="bg-green-50 rounded p-2">
                        <p className="text-xs text-gray-600">Total Calories</p>
                        <p className="text-lg font-bold text-gray-800">
                          {Math.round(result.plans.nutrition.reduce((sum: number, m: any) => sum + (m.nutrients?.calories || 0), 0))}
                        </p>
                      </div>
                      <div className="bg-blue-50 rounded p-2">
                        <p className="text-xs text-gray-600">Total Protein</p>
                        <p className="text-lg font-bold text-gray-800">
                          {result.plans.nutrition.reduce((sum: number, m: any) => sum + (m.nutrients?.protein || 0), 0).toFixed(1)}g
                        </p>
                      </div>
                      <div className="bg-orange-50 rounded p-2">
                        <p className="text-xs text-gray-600">Total Fiber</p>
                        <p className="text-lg font-bold text-gray-800">
                          {result.plans.nutrition.reduce((sum: number, m: any) => sum + (m.nutrients?.fiber || 0), 0).toFixed(1)}g
                        </p>
                      </div>
                      <div className="bg-purple-50 rounded p-2">
                        <p className="text-xs text-gray-600">Total Meals</p>
                        <p className="text-lg font-bold text-gray-800">
                          {result.plans.nutrition.length}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

