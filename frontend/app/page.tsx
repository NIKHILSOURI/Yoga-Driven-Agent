'use client';

import { useState, useEffect } from 'react';
import Dashboard from '@/components/Dashboard';
import TodaysPlan from '@/components/TodaysPlan';
import CheckInPanel from '@/components/CheckInPanel';
import Chatbot from '@/components/Chatbot';
import DecisionTrace from '@/components/DecisionTrace';
import Navigation from '@/components/Navigation';
import Onboarding from '@/components/Onboarding';
import MentalHealthQuiz from '@/components/MentalHealthQuiz';

export default function Home() {
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);

  useEffect(() => {
    // Check for existing user in localStorage
    const savedUser = localStorage.getItem('wellness_user');
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    } else {
      setShowOnboarding(true);
    }
  }, []);

  const handleUserCreated = (user: any) => {
    setCurrentUser(user);
    localStorage.setItem('wellness_user', JSON.stringify(user));
    setShowOnboarding(false);
  };

  if (showOnboarding || !currentUser) {
    return <Onboarding onComplete={handleUserCreated} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="container mx-auto px-4 py-8">
        {showQuiz ? (
          <MentalHealthQuiz
            userId={currentUser.id}
            onComplete={() => setShowQuiz(false)}
          />
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <div className="space-y-4">
                <button
                  onClick={() => setShowQuiz(true)}
                  className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition"
                >
                  Take Mental Health Quiz
                </button>
                <Dashboard userId={currentUser.id} />
              </div>
            )}
            {activeTab === 'todaysplan' && <TodaysPlan userId={currentUser.id} />}
            {activeTab === 'checkin' && <CheckInPanel userId={currentUser.id} />}
            {activeTab === 'chatbot' && <Chatbot userId={currentUser.id} />}
            {activeTab === 'trace' && <DecisionTrace userId={currentUser.id} />}
          </>
        )}
      </main>
    </div>
  );
}

