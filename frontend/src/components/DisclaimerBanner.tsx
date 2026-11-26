import React, { useState } from 'react';
import { AlertTriangle, Info, X } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  const [minimized, setMinimized] = useState(false);

  if (minimized) {
    return (
      <div className="bg-amber-50 border-b border-amber-200 px-4 py-1 text-xs text-amber-800 flex justify-between items-center">
        <span className="flex items-center gap-1.5 font-medium">
          <Info className="w-3.5 h-3.5 text-amber-600" />
          KTU Activity Points Advisory Tool (Unofficial Student Aid)
        </span>
        <button
          onClick={() => setMinimized(false)}
          className="text-amber-700 underline text-xs hover:text-amber-900"
        >
          View Full Statutory Disclaimer
        </button>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-b border-amber-200 px-4 py-2.5 text-xs text-amber-900 shadow-sm relative">
      <div className="max-w-7xl mx-auto flex items-start gap-3">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-0.5 flex-1 pr-6">
          <p className="font-semibold text-amber-950">
            MANDATORY NOTICE & STATUTORY DISCLAIMER (agent.md §1.2 & docs/SPEC.md §12.2)
          </p>
          <p className="text-amber-800 leading-relaxed">
            This tool is an <strong>independent student aid</strong> and is NOT an official portal of APJ Abdul Kalam Technological University (KTU).
            Points calculations, group totals, and credit determinations are <strong>advisory estimates</strong> based on the 2024 Scheme Handbook.
            Official credit eligibility is subject to the physical Activity Points File verified by your <strong>Senior Faculty Advisor (SFA)</strong> and endorsed by the Head of Department (HoD).
            Never present an unverified estimate as an official university entitlement.
          </p>
        </div>
        <button
          onClick={() => setMinimized(true)}
          className="text-amber-500 hover:text-amber-800 p-1"
          title="Minimize disclaimer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
