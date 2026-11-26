import React from 'react';
import { PointBracket } from '../types';

interface PointDisplayProps {
  bracket: PointBracket;
  size?: 'sm' | 'md' | 'lg';
  showLabels?: boolean;
}

export const PointDisplay: React.FC<PointDisplayProps> = ({
  bracket,
  size = 'md',
  showLabels = true,
}) => {
  const isLg = size === 'lg';
  const isSm = size === 'sm';

  return (
    <div className="flex items-baseline gap-2 font-mono">
      {/* Confirmed Points (Green) */}
      <div className="flex flex-col items-start">
        {showLabels && (
          <span className="text-[10px] font-sans font-medium uppercase tracking-wider text-emerald-700">
            Confirmed
          </span>
        )}
        <span
          className={`font-bold text-emerald-700 ${
            isLg ? 'text-3xl' : isSm ? 'text-sm' : 'text-xl'
          }`}
          title="Definitive points earned from VERIFIED certificates"
        >
          {bracket.confirmed}
        </span>
      </div>

      {/* Pending Indicator */}
      <span className={`text-slate-400 font-semibold ${isLg ? 'text-xl' : 'text-sm'}`}>
        +
      </span>

      {/* Pending Points (Amber) */}
      <div className="flex flex-col items-start">
        {showLabels && (
          <span className="text-[10px] font-sans font-medium uppercase tracking-wider text-amber-700">
            Pending
          </span>
        )}
        <span
          className={`font-semibold text-amber-600 ${
            isLg ? 'text-2xl' : isSm ? 'text-sm' : 'text-lg'
          }`}
          title="Possible additional points from DOUBT certificates"
        >
          {bracket.pending}
        </span>
      </div>

      <span className={`text-slate-300 ${isLg ? 'text-xl' : 'text-sm'}`}>/</span>

      {/* Upper Bound Points (Slate / Blue) */}
      <div className="flex flex-col items-start">
        {showLabels && (
          <span className="text-[10px] font-sans font-medium uppercase tracking-wider text-slate-500">
            Upper Bound
          </span>
        )}
        <span
          className={`font-semibold text-slate-700 ${
            isLg ? 'text-2xl' : isSm ? 'text-sm' : 'text-lg'
          }`}
          title="Maximum possible outcome if all DOUBT items are approved"
        >
          {bracket.upper_bound}
        </span>
      </div>
    </div>
  );
};
