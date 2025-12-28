'use client';

import { useState } from 'react';
import { registerUser } from '@/lib/api';
import { Sparkles } from 'lucide-react';

interface OnboardingProps {
  onComplete: (user: any) => void;
}

export default function Onboarding({ onComplete }: OnboardingProps) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    age: 25,
    gender: 'other',
    yoga_experience: 'beginner',
    dietary_preferences: [] as string[],
    allergies: [] as string[],
    goals: [] as string[],
    activity_level: 'moderate',
  });
  const [loading, setLoading] = useState(false);

  const dietaryOptions = ['vegetarian', 'vegan', 'omnivore', 'pescatarian'];
  const goalOptions = ['weight_loss', 'muscle_gain', 'stress_relief', 'flexibility', 'general_wellness'];
  const activityLevels = ['sedentary', 'light', 'moderate', 'active', 'very_active'];

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const user = await registerUser(formData);
      onComplete(user);
    } catch (error: any) {
      alert('Registration failed: ' + (error.response?.data?.detail || error.message));
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-blue-500 rounded-full mb-4">
            <Sparkles className="text-white" size={40} />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome to Yoga Wellness Coach</h1>
          <p className="text-gray-600">Let's set up your personalized wellness journey</p>
        </div>

        {step === 1 && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Basic Information</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900 placeholder-gray-400"
                placeholder="Your name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900 placeholder-gray-400"
                placeholder="your@email.com"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <button
              onClick={() => setStep(2)}
              className="w-full bg-green-500 text-white py-3 rounded-lg font-semibold hover:bg-green-600 transition"
            >
              Next
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Yoga & Wellness</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Yoga Experience</label>
              <select
                value={formData.yoga_experience}
                onChange={(e) => setFormData({ ...formData, yoga_experience: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Activity Level</label>
              <select
                value={formData.activity_level}
                onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white text-gray-900"
              >
                {activityLevels.map(level => (
                  <option key={level} value={level}>{level.replace('_', ' ').toUpperCase()}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Dietary Preferences</label>
              <div className="flex flex-wrap gap-2">
                {dietaryOptions.map(option => (
                  <button
                    key={option}
                    onClick={() => {
                      const newPrefs = formData.dietary_preferences.includes(option)
                        ? formData.dietary_preferences.filter(p => p !== option)
                        : [...formData.dietary_preferences, option];
                      setFormData({ ...formData, dietary_preferences: newPrefs });
                    }}
                    className={`px-4 py-2 rounded-lg border transition ${
                      formData.dietary_preferences.includes(option)
                        ? 'bg-green-500 text-white border-green-500'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Wellness Goals</label>
              <div className="flex flex-wrap gap-2">
                {goalOptions.map(goal => (
                  <button
                    key={goal}
                    onClick={() => {
                      const newGoals = formData.goals.includes(goal)
                        ? formData.goals.filter(g => g !== goal)
                        : [...formData.goals, goal];
                      setFormData({ ...formData, goals: newGoals });
                    }}
                    className={`px-4 py-2 rounded-lg border transition ${
                      formData.goals.includes(goal)
                        ? 'bg-green-500 text-white border-green-500'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                    }`}
                  >
                    {goal.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setStep(1)}
                className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
              >
                Back
              </button>
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 bg-green-500 text-white py-3 rounded-lg font-semibold hover:bg-green-600 transition disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Complete Setup'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

