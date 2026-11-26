import React, { useState } from 'react';
import { X, UserCheck, CheckCircle2 } from 'lucide-react';
import { StudentProfile } from '../types';

interface ProfileModalProps {
  profile: StudentProfile;
  isOpen: boolean;
  onClose: () => void;
  onSave: (updated: StudentProfile) => Promise<void>;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  profile,
  isOpen,
  onClose,
  onSave,
}) => {
  const [formData, setFormData] = useState<StudentProfile>({ ...profile });
  const [saving, setSaving] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await onSave(formData);
      onClose();
    } finally {
      setSaving(false);
    }
  };

  const getRequirements = () => {
    if (formData.is_pwd) return { total: 60, perGroup: 20, desc: 'PwD Category: 60 points total, min. 20 per group' };
    if (formData.entry_type === 'lateral') return { total: 90, perGroup: 30, desc: 'Lateral Entry (3-Year): 90 points total, min. 30 per group' };
    return { total: 120, perGroup: 40, desc: 'Regular 4-Year B.Tech: 120 points total, min. 40 per group' };
  };

  const req = getRequirements();

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
              <UserCheck className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Student Profile & Thresholds</h2>
              <p className="text-xs text-slate-500">Configures KTU scheme requirement boundaries</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Student ID / Roll No</label>
              <input
                type="text"
                value={formData.student_id}
                onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
                required
                className="w-full text-xs font-mono px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Degree Programme</label>
            <input
              type="text"
              value={formData.programme}
              onChange={(e) => setFormData({ ...formData, programme: e.target.value })}
              required
              className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Admission Date (Rule vi)</label>
              <input
                type="date"
                value={formData.admission_date}
                onChange={(e) => setFormData({ ...formData, admission_date: e.target.value })}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Programme End Date</label>
              <input
                type="date"
                value={formData.programme_end_date}
                onChange={(e) => setFormData({ ...formData, programme_end_date: e.target.value })}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
          </div>

          {/* Admission Type Selection */}
          <div className="space-y-2 pt-2 border-t border-slate-100">
            <label className="block text-xs font-semibold text-slate-700">Curriculum Entry Path</label>
            <div className="grid grid-cols-2 gap-2">
              <label
                className={`flex items-center gap-2 p-2.5 rounded-xl border text-xs cursor-pointer transition-all ${
                  formData.entry_type === 'regular'
                    ? 'border-blue-500 bg-blue-50/50 text-blue-900 font-medium'
                    : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                }`}
              >
                <input
                  type="radio"
                  name="entry_type"
                  value="regular"
                  checked={formData.entry_type === 'regular'}
                  onChange={() => setFormData({ ...formData, entry_type: 'regular' })}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span>Regular (120 pts)</span>
              </label>

              <label
                className={`flex items-center gap-2 p-2.5 rounded-xl border text-xs cursor-pointer transition-all ${
                  formData.entry_type === 'lateral'
                    ? 'border-blue-500 bg-blue-50/50 text-blue-900 font-medium'
                    : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                }`}
              >
                <input
                  type="radio"
                  name="entry_type"
                  value="lateral"
                  checked={formData.entry_type === 'lateral'}
                  onChange={() => setFormData({ ...formData, entry_type: 'lateral' })}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span>Lateral Entry (90 pts)</span>
              </label>
            </div>
          </div>

          {/* PwD Toggle */}
          <label className="flex items-center gap-2.5 p-3 rounded-xl border border-slate-200 bg-slate-50 cursor-pointer">
            <input
              type="checkbox"
              checked={formData.is_pwd}
              onChange={(e) => setFormData({ ...formData, is_pwd: e.target.checked })}
              className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800">Person with Benchmark Disability (PwD)</span>
              <p className="text-[11px] text-slate-500">Applies 60 total / 20 per group handbook threshold</p>
            </div>
          </label>

          {/* Threshold summary callout */}
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
            <div className="text-xs text-blue-900">
              <span className="font-semibold">Threshold Target: </span>
              {req.desc} (3 mandatory degree credits).
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg text-xs font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium shadow-sm transition-all"
            >
              {saving ? 'Saving...' : 'Apply Thresholds'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
