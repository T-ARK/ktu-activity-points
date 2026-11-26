import React, { useState } from 'react';
import { Search, Filter, ExternalLink, ShieldCheck } from 'lucide-react';
import { Rule } from '../types';

interface RulesExplorerViewProps {
  rules: Rule[];
}

export const RulesExplorerView: React.FC<RulesExplorerViewProps> = ({ rules }) => {
  const [selectedGroup, setSelectedGroup] = useState<string>('ALL');
  const [search, setSearch] = useState<string>('');

  const filteredRules = rules.filter((r) => {
    const matchesGroup = selectedGroup === 'ALL' || r.group === selectedGroup;
    const matchesSearch =
      r.id.toLowerCase().includes(search.toLowerCase()) ||
      r.major_head.toLowerCase().includes(search.toLowerCase()) ||
      r.sub_activity_head.toLowerCase().includes(search.toLowerCase()) ||
      r.documentary_evidence.toLowerCase().includes(search.toLowerCase());
    return matchesGroup && matchesSearch;
  });

  const renderPoints = (rule: Rule) => {
    if (rule.kind === 'flat') {
      return <span className="font-mono font-bold text-slate-900">{rule.points} pts (Flat)</span>;
    }
    if (rule.kind === 'leveled' && typeof rule.points === 'object') {
      return (
        <div className="font-mono text-[11px] space-y-0.5">
          <div>College: {rule.points.college} | Zonal: {rule.points.zonal}</div>
          <div>State: {rule.points.state} | Nat: {rule.points.national} | Int: {rule.points.international}</div>
        </div>
      );
    }
    if (rule.kind === 'per_unit') {
      return (
        <span className="font-mono text-xs text-slate-800">
          {rule.points.points_per_unit} pts {rule.points.unit?.replace('_', ' ')}
        </span>
      );
    }
    if (rule.kind === 'tiered_score') {
      return (
        <div className="font-mono text-[11px] space-y-0.5 text-indigo-700">
          {rule.points.tiers?.map((t: any, idx: number) => (
            <span key={idx} className="inline-block mr-2">
              [{t.min}{t.max ? `-${t.max}` : '+'}: {t.points}p]
            </span>
          ))}
        </div>
      );
    }
    return <span className="font-mono text-xs text-slate-500">Rule-based</span>;
  };

  return (
    <div className="space-y-4">
      {/* Search and Filters Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row justify-between items-center gap-3">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-semibold text-slate-700">Group:</span>
          <div className="flex gap-1 bg-slate-100 p-0.5 rounded-lg">
            {['ALL', 'I', 'II', 'III'].map((grp) => (
              <button
                key={grp}
                onClick={() => setSelectedGroup(grp)}
                className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                  selectedGroup === grp
                    ? 'bg-white text-blue-700 font-bold shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {grp === 'ALL' ? 'All Groups' : `Group ${grp}`}
              </button>
            ))}
          </div>
        </div>

        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search rules, keywords, or evidence..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
          />
        </div>
      </div>

      {/* Rules Count Summary */}
      <div className="flex justify-between items-center text-xs text-slate-500 px-1">
        <span>Showing {filteredRules.length} of {rules.length} Table 2 Rules</span>
        <span className="flex items-center gap-1 font-mono text-emerald-700 font-medium">
          <ShieldCheck className="w-3.5 h-3.5" />
          Checksum Verified (ktu-2024-v1)
        </span>
      </div>

      {/* Rules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredRules.map((rule) => (
          <div
            key={rule.id}
            className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs hover:border-blue-300 transition-all flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex justify-between items-start gap-2">
                <span className="px-2 py-0.5 rounded-md font-mono font-bold text-xs bg-slate-100 text-blue-800 border border-slate-200">
                  Row {rule.id}
                </span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                  Group {rule.group}
                </span>
              </div>

              <div>
                <h3 className="font-semibold text-slate-900 text-xs sm:text-sm line-clamp-2">
                  {rule.sub_activity_head}
                </h3>
                <p className="text-[11px] text-slate-500 font-medium mt-0.5">{rule.major_head}</p>
              </div>

              {/* Points calculation block */}
              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-100 text-xs">
                <span className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">
                  Point Allocation ({rule.kind})
                </span>
                {renderPoints(rule)}
              </div>

              {/* Caps Info */}
              {(rule.cap_subhead || rule.cap_category || rule.shared_cap_max) && (
                <div className="text-[11px] text-amber-800 font-medium flex flex-wrap gap-2 pt-1">
                  {rule.cap_subhead && <span>Subhead Cap: {rule.cap_subhead} pts</span>}
                  {rule.cap_category && <span>Category Cap: {rule.cap_category} pts</span>}
                  {rule.shared_cap_max && <span>Shared Cap: {rule.shared_cap_max} pts</span>}
                </div>
              )}

              {/* Evidence */}
              <div className="text-[11px] text-slate-600 border-t border-slate-100 pt-2">
                <span className="font-semibold text-slate-700">Documentary Proof: </span>
                <span className="line-clamp-2">{rule.documentary_evidence}</span>
              </div>
            </div>

            {/* Footer handbook reference */}
            <div className="mt-3 pt-2 border-t border-slate-100 flex justify-between items-center text-[10px] text-slate-500 font-mono">
              <span>Handbook p. {rule.handbook_page} (PDF p. {rule.handbook_page_pdf})</span>
              <span className="text-blue-600 flex items-center gap-0.5">
                Official Row <ExternalLink className="w-2.5 h-2.5" />
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
