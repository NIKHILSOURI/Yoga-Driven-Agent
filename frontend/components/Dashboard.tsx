'use client';

import { useState, useEffect } from 'react';
import { getDashboardOverview, getTrends, getTopItems, getWeeklyReport } from '@/lib/api';
import { TrendingUp, TrendingDown, Activity, Apple, Heart, Target } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DashboardProps {
  userId: number;
}

export default function Dashboard({ userId }: DashboardProps) {
  const [overview, setOverview] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);
  const [topItems, setTopItems] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [userId]);

  const loadData = async () => {
    try {
      const [overviewData, trendsData, topItemsData] = await Promise.all([
        getDashboardOverview(userId),
        getTrends(userId, 30),
        getTopItems(userId),
      ]);
      setOverview(overviewData);
      setTrends(trendsData);
      setTopItems(topItemsData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
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

  if (!overview) {
    return <div className="text-center text-gray-500">No data available</div>;
  }

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Dashboard</h1>
        <p className="text-gray-600">Your wellness journey at a glance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Yoga Consistency"
          value={`${overview.yoga?.consistency_percentage || 0}%`}
          icon={Activity}
          trend={overview.yoga?.consistency_percentage > 70 ? 'up' : 'down'}
          color="green"
        />
        <StatCard
          title="Protein Intake"
          value={`${overview.nutrition?.protein_total || 0}g`}
          icon={Apple}
          trend="up"
          color="blue"
        />
        <StatCard
          title="Stress Reduction"
          value={`${overview.wellness?.stress_reduction || 0}%`}
          icon={Heart}
          trend={overview.wellness?.stress_reduction > 50 ? 'up' : 'down'}
          color="purple"
        />
        <StatCard
          title="Adherence"
          value={`${overview.wellness?.adherence_avg || 0}%`}
          icon={Target}
          trend={overview.wellness?.adherence_improvement > 0 ? 'up' : 'down'}
          color="orange"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Adherence Trend</h2>
          {trends?.adherence && trends.adherence.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trends.adherence.map((item: any) => ({
                ...item,
                date: new Date(item.date).toLocaleDateString()
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  angle={-45} 
                  textAnchor="end" 
                  height={60}
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <YAxis 
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', color: '#1f2937' }}
                  labelStyle={{ color: '#1f2937' }}
                />
                <Legend wrapperStyle={{ color: '#1f2937' }} />
                <Line type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              <p>No adherence data available yet. Complete check-ins to see trends.</p>
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Stress & Motivation</h2>
          {trends?.stress && trends.stress.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trends.stress.map((s: any, i: number) => ({
                date: new Date(s.date).toLocaleDateString(),
                stress: s.value,
                motivation: trends.motivation?.[i]?.value || 0
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  angle={-45} 
                  textAnchor="end" 
                  height={60}
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <YAxis 
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', color: '#1f2937' }}
                  labelStyle={{ color: '#1f2937' }}
                />
                <Legend wrapperStyle={{ color: '#1f2937' }} />
                <Line type="monotone" dataKey="stress" stroke="#ef4444" strokeWidth={2} />
                <Line type="monotone" dataKey="motivation" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              <p>No quiz data available yet. Take mental health quizzes to see trends.</p>
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Nutrition Trends</h2>
          {trends?.protein && trends.protein.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={trends.protein.slice(-7).map((item: any) => ({
                ...item,
                date: new Date(item.date).toLocaleDateString()
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  angle={-45} 
                  textAnchor="end" 
                  height={60}
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <YAxis 
                  stroke="#374151"
                  tick={{ fill: '#374151', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', color: '#1f2937' }}
                  labelStyle={{ color: '#1f2937' }}
                />
                <Legend wrapperStyle={{ color: '#1f2937' }} />
                <Bar dataKey="value" fill="#22c55e" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              <p>No nutrition data available yet. Submit check-ins with ingredients to see trends.</p>
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Top Meals & Videos</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Favorite Meals</h3>
              <div className="space-y-2">
                {topItems?.top_meals?.slice(0, 3).map((meal: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                    <span className="text-sm">{meal.name}</span>
                    <span className="text-xs text-gray-500">{meal.count}x</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Recent Videos</h3>
              <div className="space-y-2">
                {topItems?.recent_videos?.slice(0, 3).map((video: any, idx: number) => (
                  <div key={idx} className="p-2 bg-gray-50 rounded">
                    <p className="text-sm font-medium">{video.title}</p>
                    <p className="text-xs text-gray-500">{video.session_type}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, trend, color }: any) {
  const colorClasses = {
    green: 'bg-green-100 text-green-600',
    blue: 'bg-blue-100 text-blue-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600',
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`${colorClasses[color as keyof typeof colorClasses]} p-3 rounded-lg`}>
          <Icon size={24} />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center text-sm">
          {trend === 'up' ? (
            <TrendingUp className="text-green-500 mr-1" size={16} />
          ) : (
            <TrendingDown className="text-red-500 mr-1" size={16} />
          )}
          <span className={trend === 'up' ? 'text-green-500' : 'text-red-500'}>
            {trend === 'up' ? 'Improving' : 'Needs attention'}
          </span>
        </div>
      )}
    </div>
  );
}

