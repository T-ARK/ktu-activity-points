import React, { useState } from 'react';
import { X, Plus, AlertCircle } from 'lucide-react';
import { Level, Rule } from '../types';

interface ManualEntryModalProps {
  rules: Rule[];
  isOpen: boolean;
  onClose: () => void;
  onAdd: (payload: any) => Promise<void>;
}

export const ManualEntryModal: React.FC<ManualEntryModalProps> = ({
  rules,
  isOpen,
  onClose,
  onAdd,
}) => {
  const [selectedRuleId, setSelectedRuleId] = useState<string>('1.1');
  const [activityTitle, setActivityTitle] = useState<string>('');
  const [eventName, setEventName] = useState<string>('');
  const [organiser, setOrganiser] = useState<string>('');
  const [level, setLevel] = useState<Level>('college');
  const [position, setPosition] = useState<string>('Participation');
  const [activityDate, setActivityDate] = useState<string>('2025-02-15');
  const [academicYear, setAcademicYear] = useState<string>('2024-2025');
  const [semester, setSemester] = useState<string>('S2');
  const [scoreValue, setScoreValue] = useState<string>('');
  const [durationWeeks, setDurationWeeks] = useState<string>('');
  const [isVerifiedBySfa, setIsVerifiedBySfa] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [searchFilter, setSearchFilter] = useState<string>('');

  if (!isOpen) return null;

  const currentRule = rules.find((r) => r.id === selectedRuleId) || rules[0];

  const filteredRules = rules.filter(
    (r) =>
      r.id.toLowerCase().includes(searchFilter.toLowerCase()) ||
      r.sub_activity_head.toLowerCase().includes(searchFilter.toLowerCase()) ||
      r.major_head.toLowerCase().includes(searchFilter.toLowerCase())
  );

  // Compute live estimated points
  const calculateEstimatedPoints = (): number => {
    if (!currentRule) return 0;
    if (currentRule.kind === 'flat') {
      return typeof currentRule.points === 'number' ? currentRule.points : 0;
    }
    if (currentRule.kind === 'leveled' && typeof currentRule.points === 'object') {
      return currentRule.points[level] || 0;
    }
    if (currentRule.kind === 'per_unit' && typeof currentRule.points === 'object') {
      const unit = currentRule.points.unit;
      if (unit === 'per_week' && durationWeeks) {
        return Math.min(Number(durationWeeks) * (currentRule.points.points_per_unit || 0), currentRule.cap_subhead || 999);
      }
      return currentRule.points.points_per_unit || 0;
    }
    if (currentRule.kind === 'tiered_score' && scoreValue) {
      const val = parseFloat(scoreValue);
      if (!isNaN(val) && currentRule.points.tiers) {
        for (const tier of currentRule.points.tiers) {
          if (val >= tier.min && (tier.max === null || val <= tier.max)) {
            return tier.points;
          }
        }
      }
    }
    return 0;
  };

  const estimatedPoints = calculateEstimatedPoints();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onAdd({
        rule_id: selectedRuleId,
        activity_title: activityTitle,
        event_name: eventName || null,
        organiser: organiser || null,
        level: currentRule.kind === 'leveled' ? level : null,
        position: position || null,
        activity_date: activityDate,
        academic_year: academicYear,
        semester: semester,
        score_value: scoreValue ? scoreValue : null,
        duration_weeks: durationWeeks ? parseInt(durationWeeks, 10) : null,
        is_verified_by_sfa: isVerifiedBySfa,
      });
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden max-h-[92vh] flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
              <Plus className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Add Student Activity</h2>
              <p className="text-xs text-slate-500">Maps certificate to Table 2 handbook rule deterministically</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto flex-1">
          {/* Rule Selector with Filter */}
          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="text-xs font-semibold text-slate-700">Handbook Rule (Table 2)</label>
              <input
                type="text"
                placeholder="Search rule ID or topic..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                className="text-[11px] px-2 py-0.5 border border-slate-300 rounded focus:outline-hidden"
              />
            </div>
            <select
              value={selectedRuleId}
              onChange={(e) => setSelectedRuleId(e.target.value)}
              className="w-full text-xs font-mono px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden bg-white"
            >
              {filteredRules.map((r) => (
                <option key={r.id} value={r.id}>
                  [{r.id}] Group {r.group} - {r.sub_activity_head.substring(0, 75)}... (p. {r.handbook_page})
                </option>
              ))}
            </select>
          </div>

          {/* Rule Details Summary Card */}
          {currentRule && (
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
              <div className="flex justify-between">
                <span className="font-semibold text-slate-800">
                  Group {currentRule.group} &bull; {currentRule.major_head}
                </span>
                <span className="font-mono text-slate-500">Handbook p. {currentRule.handbook_page}</span>
              </div>
              <p className="text-slate-600">{currentRule.sub_activity_head}</p>
              {currentRule.remarks && (
                <p className="text-amber-700 text-[11px] font-medium pt-1 border-t border-slate-200">
                  Rule Note: {currentRule.remarks}
                </p>
              )}
            </div>
          )}

          {/* Title, Event, and Organiser */}
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Activity Title</label>
              <input
                type="text"
                placeholder="e.g. State Badminton Tournament"
                value={activityTitle}
                onChange={(e) => setActivityTitle(e.target.value)}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Event Name</label>
              <input
                type="text"
                placeholder="e.g. KTU Sports Meet"
                value={eventName}
                onChange={(e) => setEventName(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Organiser / Host</label>
              <input
                type="text"
                placeholder="e.g. Host College / University"
                value={organiser}
                onChange={(e) => setOrganiser(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
          </div>

          {/* Duration in Weeks (if per_unit) */}
          {currentRule?.kind === 'per_unit' && (
            <div className="p-3 bg-blue-50/50 rounded-xl border border-blue-100">
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Duration (Weeks)
              </label>
              <input
                type="number"
                min="1"
                max="52"
                placeholder="e.g. 4"
                value={durationWeeks}
                onChange={(e) => setDurationWeeks(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
          )}

          {/* Level & Position (if leveled) */}
          {currentRule?.kind === 'leveled' && (
            <div className="grid grid-cols-2 gap-3 p-3 bg-blue-50/40 rounded-xl border border-blue-100">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Handbook Level (§4.3)</label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value as Level)}
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden bg-white"
                >
                  <option value="college">Level 1 - College</option>
                  <option value="zonal">Level 2 - Zonal</option>
                  <option value="state">Level 3 - State</option>
                  <option value="national">Level 4 - National</option>
                  <option value="international">Level 5 - International</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Achievement / Position</label>
                <input
                  type="text"
                  placeholder="1st Prize / Participation"
                  value={position}
                  onChange={(e) => setPosition(e.target.value)}
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                />
              </div>
            </div>
          )}

          {/* Tiered Score (if tiered_score e.g. IELTS/GATE) */}
          {currentRule?.kind === 'tiered_score' && (
            <div className="p-3 bg-indigo-50/50 rounded-xl border border-indigo-100">
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Examination Score / Band / Rank
              </label>
              <input
                type="text"
                placeholder="e.g. 7.5 (IELTS) or 105 (TOEFL) or AIR 4500 (GATE)"
                value={scoreValue}
                onChange={(e) => setScoreValue(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Tiers: {JSON.stringify(currentRule.points.tiers?.map((t: any) => `${t.min}+ -> ${t.points} pts`))}
              </p>
            </div>
          )}

          {/* Dates & Academic Period */}
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Activity Date</label>
              <input
                type="date"
                value={activityDate}
                onChange={(e) => setActivityDate(e.target.value)}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Academic Year</label>
              <input
                type="text"
                placeholder="2024-2025"
                value={academicYear}
                onChange={(e) => setAcademicYear(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Semester</label>
              <input
                type="text"
                placeholder="S1, S2..."
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
              />
            </div>
          </div>

          {/* SFA Verification Toggle */}
          <label className="flex items-start gap-2.5 p-3 rounded-xl border border-slate-200 bg-slate-50 cursor-pointer">
            <input
              type="checkbox"
              checked={isVerifiedBySfa}
              onChange={(e) => setIsVerifiedBySfa(e.target.checked)}
              className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500 mt-0.5"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800">
                Staff Advisor (SFA) Endorsed / Pre-Verified
              </span>
              <p className="text-[11px] text-slate-500">
                Under G2, student-asserted entries default to <strong>DOUBT</strong> (Pending) until SFA review.
                Check this only if signed proof is held.
              </p>
            </div>
          </label>

          {/* Point Preview Callout */}
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-medium text-emerald-900">
                Calculated Potential Points:
              </span>
            </div>
            <div className="font-mono text-base font-bold text-emerald-800">
              {estimatedPoints} pts
            </div>
          </div>

          {/* Footer Actions */}
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
              disabled={submitting}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium shadow-sm transition-all"
            >
              {submitting ? 'Recording...' : 'Record Activity'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
