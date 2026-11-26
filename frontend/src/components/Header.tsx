import React from 'react';
import { Award, BookOpen, Download, FileText, PlusCircle, User, RefreshCw, UploadCloud, ShieldCheck } from 'lucide-react';
import { getExportUrl } from '../api';

interface HeaderProps {
  activeTab: 'dashboard' | 'rules';
  setActiveTab: (tab: 'dashboard' | 'rules') => void;
  onOpenAddModal: () => void;
  onOpenProfileModal: () => void;
  onOpenUploadModal: () => void;
  onOpenSfaModal: () => void;
  onLoadSample: () => void;
  isLoadingSample: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  onOpenAddModal,
  onOpenProfileModal,
  onOpenUploadModal,
  onOpenSfaModal,
  onLoadSample,
  isLoadingSample,
}) => {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo & Scheme Badge */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-900 text-base sm:text-lg tracking-tight">
                  KTU Activity Points
                </span>
                <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                  2024 Scheme
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                Deterministic Advisory Engine (Groups I, II, III)
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-white text-slate-900 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('rules')}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                activeTab === 'rules'
                  ? 'bg-white text-slate-900 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <BookOpen className="w-4 h-4 text-slate-500" />
              <span>Rules Explorer</span>
            </button>
          </nav>

          {/* Actions & Utilities */}
          <div className="flex items-center gap-2">
            <button
              onClick={onLoadSample}
              disabled={isLoadingSample}
              title="Load synthetic sample activity portfolio (Groups I, II, III)"
              className="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors border border-slate-300"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoadingSample ? 'animate-spin' : ''}`} />
              <span>Sample Batch</span>
            </button>

            {/* Export Dropdown / Buttons */}
            <div className="flex items-center gap-1">
              <a
                href={getExportUrl('csv')}
                download="ktu_activity_points.csv"
                title="Download Activity Points CSV"
                className="p-2 text-slate-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors border border-slate-200"
              >
                <FileText className="w-4 h-4" />
              </a>
              <a
                href={getExportUrl('pdf')}
                download="ktu_activity_points.pdf"
                title="Download Endorsed Activity Points PDF (SFA Signature Block)"
                className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 rounded-lg transition-colors border border-slate-200 shadow-2xs"
              >
                <Download className="w-3.5 h-3.5 text-blue-600" />
                <span className="hidden sm:inline">PDF</span>
              </a>
            </div>

            {/* Profile Button */}
            <button
              onClick={onOpenProfileModal}
              title="Student Profile & Scheme Thresholds"
              className="p-2 text-slate-700 hover:text-blue-600 hover:bg-slate-100 rounded-lg transition-colors border border-slate-200"
            >
              <User className="w-4 h-4" />
            </button>

            {/* SFA Workspace Button */}
            <button
              onClick={onOpenSfaModal}
              title="Staff Advisor (SFA) Review Workspace"
              className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors border border-indigo-200"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
              <span className="hidden md:inline">SFA Review</span>
            </button>

            {/* Upload Certificate Button */}
            <button
              onClick={onOpenUploadModal}
              title="Upload Certificate (PDF, PNG, JPG) with Automatic Fact Extraction"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs sm:text-sm font-medium shadow-sm transition-all"
            >
              <UploadCloud className="w-4 h-4" />
              <span className="hidden sm:inline">Upload</span>
            </button>

            {/* Add Activity Button */}
            <button
              onClick={onOpenAddModal}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs sm:text-sm font-medium shadow-sm transition-all"
            >
              <PlusCircle className="w-4 h-4" />
              <span className="hidden sm:inline">Manual Entry</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
