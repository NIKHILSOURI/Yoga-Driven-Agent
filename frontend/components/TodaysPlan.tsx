'use client';

import { useState, useEffect } from 'react';
import { getTodayYogaPlan, getTodayNutritionPlans, getTodayTraces } from '@/lib/api';
import { Play, Clock, UtensilsCrossed, Activity, Sparkles, TrendingUp, Brain } from 'lucide-react';

interface TodaysPlanProps {
  userId: number;
}

export default function TodaysPlan({ userId }: TodaysPlanProps) {
  const [yogaPlan, setYogaPlan] = useState<any>(null);
  const [nutritionPlans, setNutritionPlans] = useState<any[]>([]);
  const [aiReasoning, setAiReasoning] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTodaysPlan();
  }, [userId]);

  const loadTodaysPlan = async () => {
    try {
      const [yogaData, nutritionData, tracesData] = await Promise.all([
        getTodayYogaPlan(userId),
        getTodayNutritionPlans(userId),
        getTodayTraces(userId),
      ]);
      
      if (yogaData && !yogaData.message) {
        setYogaPlan(yogaData);
      }
      
      if (Array.isArray(nutritionData)) {
        setNutritionPlans(nutritionData);
      }
      
      if (Array.isArray(tracesData)) {
        setAiReasoning(tracesData);
      }
    } catch (error) {
      console.error('Failed to load today\'s plan:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get YouTube thumbnail URL
  const getYouTubeThumbnail = (videoId: string) => {
    if (!videoId) return null;
    return `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
  };

  // Get exercises based on session type
  const getExercisesForSession = (sessionType: string) => {
    const exercises: Record<string, string[]> = {
      stress_relief: [
        'Child\'s Pose (Balasana) - 2 min',
        'Cat-Cow Stretch - 1 min',
        'Seated Forward Fold - 2 min',
        'Legs Up the Wall - 5 min',
        'Corpse Pose (Savasana) - 5 min',
        'Alternate Nostril Breathing - 3 min'
      ],
      energizing: [
        'Sun Salutation (Surya Namaskar) - 5 rounds',
        'Warrior I & II - 1 min each',
        'Triangle Pose (Trikonasana) - 1 min',
        'Downward Dog - 1 min',
        'Cobra Pose - 30 sec',
        'Bridge Pose - 1 min'
      ],
      flexibility: [
        'Standing Forward Fold - 1 min',
        'Seated Forward Fold - 2 min',
        'Pigeon Pose - 2 min each side',
        'Butterfly Pose - 2 min',
        'Reclining Hand-to-Big-Toe - 1 min each',
        'Twisted Triangle - 1 min each side'
      ],
      strength: [
        'Plank Pose - 30-60 sec',
        'Warrior III - 30 sec each',
        'Side Plank - 30 sec each',
        'Chair Pose - 1 min',
        'Boat Pose - 30 sec',
        'Crow Pose - 30 sec'
      ],
      recovery: [
        'Gentle Twists - 1 min each',
        'Supported Bridge - 3 min',
        'Legs Up the Wall - 5 min',
        'Reclining Bound Angle - 3 min',
        'Supine Spinal Twist - 2 min each',
        'Corpse Pose (Savasana) - 5 min'
      ],
    };
    
    return exercises[sessionType] || [
      'Mountain Pose - 1 min',
      'Downward Dog - 1 min',
      'Warrior I - 1 min',
      'Child\'s Pose - 2 min',
      'Corpse Pose - 3 min'
    ];
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  const hasPlan = yogaPlan || nutritionPlans.length > 0;

  if (!hasPlan) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
          <Sparkles className="mx-auto text-gray-400 mb-4" size={48} />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">No Plan for Today</h2>
          <p className="text-gray-600 mb-4">
            Complete a check-in to get your personalized plan for today!
          </p>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              window.location.hash = 'checkin';
            }}
            className="inline-block bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition"
          >
            Go to Check-in
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Today's Plan</h1>
        <p className="text-gray-600 text-lg">Your personalized wellness plan for today</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Yoga Plan - Left Column (2/3 width on large screens) */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Reasoning Card */}
          {aiReasoning.length > 0 && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl shadow-lg p-6 border border-blue-200">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <Brain size={24} className="mr-2 text-blue-600" />
                AI Reasoning
              </h2>
              {aiReasoning.map((trace, idx) => (
                <div key={trace.id || idx} className="mb-4 last:mb-0">
                  {trace.explanation && (
                    <p className="text-sm text-gray-700 mb-2 whitespace-pre-wrap">
                      {trace.explanation}
                    </p>
                  )}
                  {trace.triggered_rules && Array.isArray(trace.triggered_rules) && trace.triggered_rules.length > 0 && (
                    <div className="bg-white bg-opacity-60 rounded-lg p-3 text-xs">
                      <p className="font-semibold text-gray-700 mb-2">Triggered Rules:</p>
                      <div className="space-y-2">
                        {trace.triggered_rules.map((rule: any, i: number) => (
                          <div key={i} className="bg-yellow-50 border-l-4 border-yellow-400 p-2 rounded">
                            {typeof rule === 'object' ? (
                              <>
                                <p className="text-xs font-medium text-yellow-900">
                                  {rule.rule_id || `Rule ${i + 1}`}
                                </p>
                                {rule.condition && (
                                  <p className="text-xs text-yellow-700 mt-1">
                                    Condition: {rule.condition}
                                  </p>
                                )}
                                {rule.action && (
                                  <p className="text-xs text-yellow-700">
                                    Action: {rule.action}
                                  </p>
                                )}
                              </>
                            ) : (
                              <p className="text-xs text-yellow-700">{String(rule)}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          {/* Yoga Session Card */}
          {yogaPlan && (
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-green-500 to-blue-500 p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">Today's Yoga Session</h2>
                    <p className="text-green-50">{yogaPlan.description}</p>
                  </div>
                  <Activity size={40} className="opacity-80" />
                </div>
              </div>
              
              <div className="p-6">
                {/* YouTube Video Thumbnail */}
                {yogaPlan.youtube_video_id && (
                  <div className="mb-6">
                    <a
                      href={yogaPlan.youtube_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block relative group"
                    >
                      <img
                        src={getYouTubeThumbnail(yogaPlan.youtube_video_id)}
                        alt={yogaPlan.youtube_title}
                        className="w-full rounded-lg shadow-md group-hover:shadow-xl transition"
                        onError={(e) => {
                          // Fallback to default thumbnail
                          (e.target as HTMLImageElement).src = `https://img.youtube.com/vi/${yogaPlan.youtube_video_id}/hqdefault.jpg`;
                        }}
                      />
                      <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 group-hover:bg-opacity-40 rounded-lg transition">
                        <div className="bg-red-600 rounded-full p-4 group-hover:scale-110 transition">
                          <Play size={32} className="text-white ml-1" fill="white" />
                        </div>
                      </div>
                    </a>
                    <p className="text-sm text-gray-600 mt-2 text-center">
                      {yogaPlan.youtube_title}
                    </p>
                  </div>
                )}

                {/* Session Details */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-green-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600 mb-1">Session Type</p>
                    <p className="text-lg font-semibold text-gray-800 capitalize">
                      {yogaPlan.session_type?.replace('_', ' ')}
                    </p>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600 mb-1">Duration</p>
                    <p className="text-lg font-semibold text-gray-800 flex items-center">
                      <Clock size={18} className="mr-1" />
                      {yogaPlan.duration_minutes} minutes
                    </p>
                  </div>
                </div>

                {/* Exercises */}
                <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-lg p-4 border border-green-200">
                  <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
                    <Activity size={20} className="mr-2 text-green-600" />
                    Today's Exercises & Poses
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {getExercisesForSession(yogaPlan.session_type).map((exercise, idx) => (
                      <div
                        key={idx}
                        className="bg-white rounded-lg p-3 text-sm text-gray-700 border border-green-200 hover:shadow-md transition flex items-center"
                      >
                        <span className="bg-green-100 text-green-700 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2 flex-shrink-0">
                          {idx + 1}
                        </span>
                        <span className="flex-1">{exercise}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Nutrition Plans */}
          {nutritionPlans.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800 flex items-center">
                  <UtensilsCrossed size={28} className="mr-2 text-purple-600" />
                  Today's Meals
                </h2>
                <div className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-semibold">
                  {nutritionPlans.length} Meals
                </div>
              </div>

              <div className="space-y-4">
                {nutritionPlans.map((meal, idx) => (
                  <div
                    key={meal.id || idx}
                    className="border border-purple-200 rounded-lg p-4 hover:shadow-md transition"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-semibold capitalize">
                            {meal.meal_type}
                          </span>
                          {meal.sattvic_score && (
                            <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">
                              Sattvic: {meal.sattvic_score}/10
                            </span>
                          )}
                        </div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-1">
                          {meal.recipe_name}
                        </h3>
                      </div>
                    </div>

                    {meal.ingredients && Array.isArray(meal.ingredients) && meal.ingredients.length > 0 && (
                      <div className="mb-3">
                        <p className="text-xs font-medium text-gray-600 mb-1">Ingredients:</p>
                        <p className="text-sm text-gray-700">
                          {meal.ingredients.slice(0, 8).join(', ')}
                          {meal.ingredients.length > 8 ? '...' : ''}
                        </p>
                      </div>
                    )}

                    {meal.nutrients && (
                      <div className="flex gap-4 text-xs mb-3">
                        <span className="text-gray-600">
                          Calories: <span className="font-semibold text-gray-800">
                            {Math.round(meal.nutrients.calories || 0)}
                          </span>
                        </span>
                        <span className="text-gray-600">
                          Protein: <span className="font-semibold text-gray-800">
                            {meal.nutrients.protein?.toFixed(1) || 0}g
                          </span>
                        </span>
                        <span className="text-gray-600">
                          Fiber: <span className="font-semibold text-gray-800">
                            {meal.nutrients.fiber?.toFixed(1) || 0}g
                          </span>
                        </span>
                      </div>
                    )}

                    <details className="mt-2">
                      <summary className="text-sm text-purple-600 cursor-pointer hover:text-purple-700 font-medium">
                        View Recipe Instructions
                      </summary>
                      <p className="text-sm text-gray-700 mt-2 whitespace-pre-wrap bg-gray-50 p-3 rounded">
                        {meal.recipe_instructions || 'No instructions available.'}
                      </p>
                    </details>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Sidebar - Summary & Stats */}
        <div className="space-y-6">
          {/* Daily Summary Card */}
          <div className="bg-gradient-to-br from-green-500 to-blue-500 rounded-xl shadow-lg p-6 text-white">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <Sparkles size={24} className="mr-2" />
              Daily Summary
            </h3>
            
            <div className="space-y-3">
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <p className="text-sm opacity-90">Yoga Session</p>
                <p className="text-lg font-semibold">
                  {yogaPlan ? `${yogaPlan.duration_minutes} min` : 'Not scheduled'}
                </p>
              </div>
              
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <p className="text-sm opacity-90">Total Meals</p>
                <p className="text-lg font-semibold">{nutritionPlans.length}</p>
              </div>
              
              {nutritionPlans.length > 0 && (
                <div className="bg-white bg-opacity-20 rounded-lg p-3">
                  <p className="text-sm opacity-90">Total Calories</p>
                  <p className="text-lg font-semibold">
                    {Math.round(
                      nutritionPlans.reduce(
                        (sum, m) => sum + (m.nutrients?.calories || 0),
                        0
                      )
                    )}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Quick Stats */}
          {nutritionPlans.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                <TrendingUp size={20} className="mr-2 text-green-600" />
                Nutrition Stats
              </h3>
              <div className="space-y-3">
                <div>
                  <p className="text-xs text-gray-600 mb-1">Total Protein</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {nutritionPlans
                      .reduce((sum, m) => sum + (m.nutrients?.protein || 0), 0)
                      .toFixed(1)}g
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 mb-1">Total Fiber</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {nutritionPlans
                      .reduce((sum, m) => sum + (m.nutrients?.fiber || 0), 0)
                      .toFixed(1)}g
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 mb-1">Avg Sattvic Score</p>
                  <p className="text-2xl font-bold text-green-600">
                    {(
                      nutritionPlans
                        .filter((m) => m.sattvic_score)
                        .reduce((sum, m) => sum + (m.sattvic_score || 0), 0) /
                      nutritionPlans.filter((m) => m.sattvic_score).length || 0
                    ).toFixed(1)}/10
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Tips Card */}
          <div className="bg-blue-50 rounded-xl shadow-lg p-6 border border-blue-200">
            <h3 className="font-semibold text-gray-800 mb-3">💡 Wellness Tips</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start">
                <span className="text-green-600 mr-2">•</span>
                Practice yoga on an empty stomach or 2-3 hours after meals
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">•</span>
                Stay hydrated throughout the day
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">•</span>
                Eat mindfully and chew your food well
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">•</span>
                Take breaks between meals for better digestion
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

