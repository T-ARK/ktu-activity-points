import React, { useState } from 'react';
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  Trash2,
  ChevronDown,
  ChevronUp,
  FileCheck,
} from 'lucide-react';
import { DashboardResponse } from '../types';
import { PointDisplay } from './PointDisplay';

interface DashboardViewProps {
  data: DashboardResponse;
  onDeleteActivity: (id: string) => Promise<void>;
  onOpenAddModal: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  data,
  onDeleteActivity,
  onOpenAddModal,
}) => {
  const { engine_result, doubt_catalog } = data;
  const [expandedDoubts, setExpandedDoubts] = useState<Record<string, boolean>>({});

  const toggleDoubt = (certId: string) => {
    setExpandedDoubts((prev) => ({ ...prev, [certId]: !prev[certId] }));
  };

  const getStatusBadge = () => {
    switch (engine_result.credit_status) {
      case 'ACHIEVED':
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-100 text-emerald-900 border border-emerald-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span className="font-bold text-xs sm:text-sm">3 Credits Fully Confirmed</span>
          </div>
        );
      case 'ACHIEVABLE_WITH_PENDING':
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-100 text-amber-900 border border-amber-200">
            <Clock className="w-4 h-4 text-amber-600" />
            <span className="font-bold text-xs sm:text-sm">3 Credits Achievable With Pending</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-100 text-rose-900 border border-rose-200">
            <AlertTriangle className="w-4 h-4 text-rose-600" />
            <span className="font-bold text-xs sm:text-sm">Credit Deficit (Pending Points Needed)</span>
          </div>
        );
    }
  };

  const groupThemes: Record<string, { title: string; subtitle: string }> = {
    I: {
      title: 'Group I: Sports, Arts & Social Service',
      subtitle: 'Sports, Cultural, NSS, NCC, Community Service, Clean Campus',
    },
    II: {
      title: 'Group II: Technical & Professional',
      subtitle: 'Tech Fests, Paper Presentations, Hackathons, Professional Societies, Internships',
    },
    III: {
      title: 'Group III: Innovation & Leadership',
      subtitle: 'Startups, Patents, Student Council, Incubation, Tech Transfer',
    },
  };

  return (
    <div className="space-y-6">
      {/* 1. Degree Requirement Status Overview Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm relative overflow-hidden">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Curriculum Requirement Overview
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900">
              Total Points: Confirmed vs Upper Bound
            </h2>
            <p className="text-xs sm:text-sm text-slate-500">
              Degree Requirement: <strong>{engine_result.required_total} points</strong> (min.{' '}
              {engine_result.groups.I.required_points} per group) for 3 mandatory non-GPA credits.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            {getStatusBadge()}
          </div>
        </div>

        {/* Big Overall 3-Number Display */}
        <div className="mt-6 pt-6 border-t border-slate-100 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
            <PointDisplay bracket={engine_result.total_bracket} size="lg" />
            <p className="text-[11px] text-slate-500 mt-2 font-mono">
              Target: {engine_result.required_total} pts &bull; Confirmed:{' '}
              {engine_result.credits_earned_confirmed}/3 credits
            </p>
          </div>

          <div className="md:col-span-2 grid grid-cols-3 gap-2 sm:gap-4 text-center">
            <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-100">
              <span className="text-xs text-emerald-800 font-medium block">Credits Confirmed</span>
              <span className="text-2xl font-bold font-mono text-emerald-700">
                {engine_result.credits_earned_confirmed} / 3
              </span>
            </div>
            <div className="p-3 rounded-xl bg-amber-50/60 border border-amber-100">
              <span className="text-xs text-amber-800 font-medium block">Credits Upper Bound</span>
              <span className="text-2xl font-bold font-mono text-amber-700">
                {engine_result.credits_earned_upper} / 3
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-xs text-slate-600 font-medium block">Activities Logged</span>
              <span className="text-2xl font-bold font-mono text-slate-800">
                {engine_result.activities.length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Group Breakdown Cards (Groups I, II, III) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {(['I', 'II', 'III'] as const).map((gid) => {
          const grp = engine_result.groups[gid];
          const theme = groupThemes[gid];

          return (
            <div
              key={gid}
              className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-800">
                    Group {gid}
                  </span>
                  <span
                    className={`text-[11px] px-2 py-0.5 rounded-full font-semibold ${
                      grp.is_credit_achieved_confirmed
                        ? 'bg-emerald-100 text-emerald-800'
                        : grp.is_credit_achievable_upper
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}
                  >
                    {grp.is_credit_achieved_confirmed
                      ? '1 Credit Confirmed'
                      : grp.is_credit_achievable_upper
                      ? '1 Credit Pending'
                      : 'Credit Deficit'}
                  </span>
                </div>

                <h3 className="font-bold text-slate-900 text-sm sm:text-base mt-2">
                  {theme.title}
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">{theme.subtitle}</p>

                {/* Group Bracket Display */}
                <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <PointDisplay bracket={grp.bracket} size="md" />
                  <div className="flex justify-between text-[11px] text-slate-500 font-mono mt-2">
                    <span>Target: {grp.required_points} pts</span>
                    <span>
                      {grp.bracket.confirmed >= grp.required_points
                        ? 'Met Target'
                        : `Need ${grp.required_points - grp.bracket.confirmed} pts`}
                    </span>
                  </div>
                </div>
              </div>

              {/* Activity count */}
              <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center text-xs text-slate-500 font-mono">
                <span>{grp.activities.length} Activities Recorded</span>
                <span className="font-semibold text-slate-700">
                  {grp.bracket.upper_bound} pts max
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 3. Activity Ledger Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <div>
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <FileCheck className="w-4 h-4 text-blue-600" />
              Activity Ledger & Verification Status
            </h3>
            <p className="text-xs text-slate-500">
              Evaluated with Rule i deduplication and handbook cap sequence
            </p>
          </div>
          <button
            onClick={onOpenAddModal}
            className="text-xs font-semibold text-blue-600 hover:text-blue-800"
          >
            + Add Another Activity
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Rule</th>
                <th className="py-3 px-4">Group</th>
                <th className="py-3 px-4">Activity Description</th>
                <th className="py-3 px-4 text-center">Verdict</th>
                <th className="py-3 px-4 text-center">Confirmed</th>
                <th className="py-3 px-4 text-center">Upper Bound</th>
                <th className="py-3 px-4 text-center">Doubt Flags</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {engine_result.activities.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-slate-500">
                    No activities recorded yet. Click &quot;Add Activity&quot; or &quot;Sample Batch&quot; to begin.
                  </td>
                </tr>
              ) : (
                engine_result.activities.map((act) => {
                  const hasDoubts = act.doubt_codes.length > 0;
                  const isExpanded = expandedDoubts[act.certificate_id];

                  return (
                    <React.Fragment key={act.certificate_id}>
                      <tr className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-4 font-mono font-bold text-blue-700">
                          {act.rule_id}
                        </td>
                        <td className="py-3 px-4 font-mono text-slate-700">
                          Group {act.group}
                        </td>
                        <td className="py-3 px-4 font-medium text-slate-900 max-w-xs truncate">
                          {act.activity_title || `Activity ${act.certificate_id}`}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {act.verdict === 'VERIFIED' ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
                              <CheckCircle2 className="w-3 h-3" />
                              VERIFIED
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800">
                              <AlertTriangle className="w-3 h-3" />
                              DOUBT
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4 font-mono font-bold text-center text-emerald-700">
                          {act.counted_points_pessimistic}
                        </td>
                        <td className="py-3 px-4 font-mono font-semibold text-center text-slate-800">
                          {act.counted_points_optimistic}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {hasDoubts ? (
                            <button
                              onClick={() => toggleDoubt(act.certificate_id)}
                              className="inline-flex items-center gap-1 text-[11px] font-mono font-semibold text-amber-700 bg-amber-50 hover:bg-amber-100 px-2 py-0.5 rounded border border-amber-200 transition-colors"
                            >
                              <span>{act.doubt_codes.join(', ')}</span>
                              {isExpanded ? (
                                <ChevronUp className="w-3 h-3" />
                              ) : (
                                <ChevronDown className="w-3 h-3" />
                              )}
                            </button>
                          ) : (
                            <span className="text-slate-400 font-mono text-[11px]">None</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <button
                            onClick={() => onDeleteActivity(act.certificate_id)}
                            className="p-1 text-slate-400 hover:text-rose-600 rounded transition-colors"
                            title="Remove activity"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>

                      {/* Expandable Doubt Explanations Drawer */}
                      {hasDoubts && isExpanded && (
                        <tr className="bg-amber-50/50">
                          <td colSpan={8} className="py-3 px-6 border-y border-amber-100">
                            <div className="space-y-2">
                              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-900 block">
                                Doubt Details & Resolution Actions:
                              </span>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                {act.doubt_codes.map((code) => {
                                  const detail = doubt_catalog[code];
                                  return (
                                    <div
                                      key={code}
                                      className="p-2.5 bg-white rounded-lg border border-amber-200 text-xs space-y-1 shadow-2xs"
                                    >
                                      <div className="flex justify-between items-center">
                                        <span className="font-mono font-bold text-amber-800">
                                          [{code}] {detail?.category || 'Verification'}
                                        </span>
                                        <span className="text-[10px] uppercase font-bold text-amber-700 bg-amber-100 px-1.5 py-0.2 rounded">
                                          {detail?.severity || 'warning'}
                                        </span>
                                      </div>
                                      <p className="text-slate-700">{detail?.message}</p>
                                      <div className="text-[11px] text-blue-800 font-medium pt-1 border-t border-slate-100">
                                        <strong>How to Resolve: </strong>
                                        {detail?.how_to_resolve}
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
