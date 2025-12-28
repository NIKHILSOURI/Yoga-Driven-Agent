'use client';

import { useState, useEffect } from 'react';
import { getQuizQuestions, submitQuiz } from '@/lib/api';
import { Brain, CheckCircle } from 'lucide-react';

interface MentalHealthQuizProps {
  userId: number;
  onComplete?: (results: any) => void;
}

export default function MentalHealthQuiz({ userId, onComplete }: MentalHealthQuizProps) {
  const [questions, setQuestions] = useState<any[]>([]);
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await getQuizQuestions();
      setQuestions(data.questions || []);
      // Initialize responses
      const initialResponses: Record<string, number> = {};
      data.questions?.forEach((q: any) => {
        initialResponses[q.id] = 5; // Default to middle value
      });
      setResponses(initialResponses);
    } catch (error) {
      console.error('Failed to load questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = (questionId: string, value: number) => {
    setResponses({ ...responses, [questionId]: value });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      handleSubmit();
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const result = await submitQuiz(userId, { responses });
      setResults(result);
      setCompleted(true);
      if (onComplete) {
        onComplete(result);
      }
    } catch (error: any) {
      alert('Failed to submit quiz: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  if (completed && results) {
    return (
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-6">
          <CheckCircle className="mx-auto text-green-500 mb-4" size={48} />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz Completed!</h2>
          <p className="text-gray-600">Here are your wellness scores</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
          {Object.entries(results.scores).map(([key, value]: [string, any]) => (
            <div key={key} className="bg-gray-50 rounded-lg p-4 text-center">
              <p className="text-sm text-gray-600 mb-1">{key.replace('_', ' ').toUpperCase()}</p>
              <p className="text-2xl font-bold text-gray-800">{value}/10</p>
            </div>
          ))}
        </div>

        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            These scores will help personalize your wellness plan. The AI will use this information
            to recommend appropriate yoga sessions, nutrition plans, and stress management strategies.
          </p>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return <div className="text-center text-gray-500">No questions available</div>;
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Brain className="text-purple-500" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Mental Health & Wellness Quiz</h2>
          </div>
          <span className="text-sm text-gray-500">
            {currentQuestion + 1} of {questions.length}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-green-500 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-800 mb-4">{question.question}</h3>
        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Low</span>
              <span className="text-sm text-gray-600">High</span>
            </div>
            <input
              type="range"
              min="1"
              max="10"
              value={responses[question.id] || 5}
              onChange={(e) => handleResponse(question.id, parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex items-center justify-center mt-2">
              <span className="text-2xl font-bold text-green-600">
                {responses[question.id] || 5}
              </span>
              <span className="text-gray-500 ml-2">/ 10</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-between">
        <button
          onClick={handlePrevious}
          disabled={currentQuestion === 0}
          className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          disabled={submitting}
          className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition disabled:opacity-50"
        >
          {currentQuestion === questions.length - 1
            ? submitting
              ? 'Submitting...'
              : 'Submit'
            : 'Next'}
        </button>
      </div>
    </div>
  );
}

