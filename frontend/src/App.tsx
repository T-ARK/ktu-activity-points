import React, { useEffect, useState } from 'react';
import {
  fetchDashboard,
  fetchProfile,
  fetchRules,
  updateProfile,
  addActivity,
  deleteActivity,
  loadSampleActivities,
} from './api';
import { DashboardResponse, Rule, StudentProfile } from './types';
import { Header } from './components/Header';
import { DisclaimerBanner } from './components/DisclaimerBanner';
import { DashboardView } from './components/DashboardView';
import { RulesExplorerView } from './components/RulesExplorerView';
import { ManualEntryModal } from './components/ManualEntryModal';
import { ProfileModal } from './components/ProfileModal';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'rules'>('dashboard');
  const [dashboardData, setDashboardData] = useState<DashboardResponse | null>(null);
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState<boolean>(false);
  const [isLoadingSample, setIsLoadingSample] = useState<boolean>(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [dash, prof, rulesRes] = await Promise.all([
        fetchDashboard(),
        fetchProfile(),
        fetchRules(),
      ]);
      setDashboardData(dash);
      setProfile(prof);
      setRules(rulesRes.rules);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend engine');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUpdateProfile = async (updated: StudentProfile) => {
    const newProf = await updateProfile(updated);
    setProfile(newProf);
    const newDash = await fetchDashboard();
    setDashboardData(newDash);
  };

  const handleAddActivity = async (payload: any) => {
    await addActivity(payload);
    const newDash = await fetchDashboard();
    setDashboardData(newDash);
  };

  const handleDeleteActivity = async (certId: string) => {
    await deleteActivity(certId);
    const newDash = await fetchDashboard();
    setDashboardData(newDash);
  };

  const handleLoadSample = async () => {
    try {
      setIsLoadingSample(true);
      await loadSampleActivities();
      const newDash = await fetchDashboard();
      setDashboardData(newDash);
    } finally {
      setIsLoadingSample(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Statutory Disclaimer Banner */}
      <DisclaimerBanner />

      {/* App Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenAddModal={() => setIsAddModalOpen(true)}
        onOpenProfileModal={() => setIsProfileModalOpen(true)}
        onLoadSample={handleLoadSample}
        isLoadingSample={isLoadingSample}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <div className="py-24 text-center space-y-3">
            <div className="w-10 h-10 border-3 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="text-sm font-medium text-slate-600">
              Evaluating KTU 2024 Scheme Rules Engine...
            </p>
          </div>
        ) : error ? (
          <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl max-w-lg mx-auto text-center space-y-3">
            <h3 className="font-bold text-rose-900 text-base">Backend Connection Error</h3>
            <p className="text-xs text-rose-700">{error}</p>
            <button
              onClick={loadData}
              className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold"
            >
              Retry Connection
            </button>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && dashboardData && (
              <DashboardView
                data={dashboardData}
                onDeleteActivity={handleDeleteActivity}
                onOpenAddModal={() => setIsAddModalOpen(true)}
              />
            )}

            {activeTab === 'rules' && <RulesExplorerView rules={rules} />}
          </>
        )}
      </main>

      {/* Modals */}
      {profile && (
        <ProfileModal
          profile={profile}
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
          onSave={handleUpdateProfile}
        />
      )}

      <ManualEntryModal
        rules={rules}
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAdd={handleAddActivity}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        <p>
          APJ Abdul Kalam Technological University Activity Points Advisory Aid &bull; KTU 2024
          Scheme &bull; Deterministic Engine v1.0
        </p>
      </footer>
    </div>
  );
};
