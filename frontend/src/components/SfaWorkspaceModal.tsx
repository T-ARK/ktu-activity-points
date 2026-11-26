import React, { useState, useEffect } from 'react';
import { ShieldCheck, CheckCircle2, XCircle, AlertCircle, RefreshCw, X, History } from 'lucide-react';
import { fetchSfaQueue, adjudicateActivity, fetchSfaAuditLog } from '../api';
import { CertificateFacts, SfaAuditEntry } from '../types';

interface SfaWorkspaceModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAdjudicationComplete: () => void;
}

export const SfaWorkspaceModal: React.FC<SfaWorkspaceModalProps> = ({
  isOpen,
  onClose,
  onAdjudicationComplete,
}) => {
  const [queue, setQueue] = useState<CertificateFacts[]>([]);
  const [auditLog, setAuditLog] = useState<SfaAuditEntry[]>([]);
  const [activeTab, setActiveTab] = useState<'queue' | 'audit'>('queue');
  const [selectedCert, setSelectedCert] = useState<CertificateFacts | null>(null);
  const [sfaName, setSfaName] = useState('Dr. S. Nair (Staff Advisor)');
  const [reason, setReason] = useState('');
  const [overrideRuleId, setOverrideRuleId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const q = await fetchSfaQueue();
      setQueue(q);
      const logs = await fetchSfaAuditLog();
      setAuditLog(logs);
      if (q.length > 0 && !selectedCert) {
        setSelectedCert(q[0]);
      }
    } catch (err: any) {
      setErrorMsg('Failed to load SFA queue');
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleAdjudicate = async (action: 'verify' | 'reject' | 'override') => {
    if (!selectedCert) return;
    if (!reason.trim()) {
      setErrorMsg('Mandatory audit requirement: enter a formal reason for this decision.');
      return;
    }

    try {
      setIsSubmitting(true);
      setErrorMsg(null);
      await adjudicateActivity({
        certificate_id: selectedCert.certificate_id,
        action,
        sfa_name: sfaName,
        reason: reason.trim(),
        override_rule_id: action === 'override' && overrideRuleId.trim() ? overrideRuleId.trim() : undefined,
      });

      setReason('');
      setOverrideRuleId('');
      await loadData();
      onAdjudicationComplete();
      setSelectedCert(null);
    } catch (err: any) {
      setErrorMsg(err.message || 'Adjudication failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-4xl w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-900 text-white flex items-center justify-between flex-shrink-0">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-indigo-400" />
            <div>
              <h2 className="text-lg font-bold">Staff Advisor (SFA) Review Workspace</h2>
              <p className="text-xs text-slate-400">Formal Adjudication & Audit Log for Doubtful Certificates</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Controls */}
        <div className="bg-slate-100 border-b border-slate-200 px-6 flex gap-4 flex-shrink-0">
          <button
            onClick={() => setActiveTab('queue')}
            className={`py-3 text-sm font-semibold border-b-2 flex items-center gap-2 transition-colors ${
              activeTab === 'queue'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <AlertCircle className="w-4 h-4" />
            Pending Doubt Queue ({queue.length})
          </button>
          <button
            onClick={() => setActiveTab('audit')}
            className={`py-3 text-sm font-semibold border-b-2 flex items-center gap-2 transition-colors ${
              activeTab === 'audit'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <History className="w-4 h-4" />
            Adjudication Audit Trail ({auditLog.length})
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6">
          {errorMsg && (
            <div className="mb-4 p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-sm flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {activeTab === 'queue' ? (
            queue.length === 0 ? (
              <div className="text-center py-12">
                <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
                <h3 className="text-base font-semibold text-slate-800">Review Queue Empty</h3>
                <p className="text-sm text-slate-500 mt-1">All student certificate submissions have been adjudicated.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* List Column */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Certificates Awaiting Review
                  </h3>
                  {queue.map((cert) => (
                    <div
                      key={cert.certificate_id}
                      onClick={() => setSelectedCert(cert)}
                      className={`p-4 rounded-xl border cursor-pointer transition-all ${
                        selectedCert?.certificate_id === cert.certificate_id
                          ? 'border-indigo-600 bg-indigo-50/40 shadow-sm'
                          : 'border-slate-200 bg-slate-50 hover:bg-slate-100'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <span className="px-2 py-0.5 bg-slate-200 font-mono text-[11px] font-semibold text-slate-700 rounded">
                            Rule {cert.rule_id}
                          </span>
                          <h4 className="text-sm font-semibold text-slate-900 mt-1">{cert.activity_title}</h4>
                        </div>
                        <span className="px-2 py-0.5 bg-amber-100 text-amber-800 text-[11px] font-bold rounded">
                          DOUBT
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-2">
                        {cert.doubt_codes.map((c) => (
                          <span key={c} className="px-1.5 py-0.5 bg-amber-200 text-amber-900 font-mono text-[10px] rounded">
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Adjudication Panel Column */}
                {selectedCert && (
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
                    <h3 className="text-sm font-bold text-slate-800 border-b pb-2">
                      Adjudicate: {selectedCert.certificate_id}
                    </h3>

                    <div className="text-xs space-y-1.5 text-slate-600 bg-white p-3 rounded-lg border border-slate-200">
                      <p><span className="font-semibold text-slate-700">Activity:</span> {selectedCert.activity_title}</p>
                      <p><span className="font-semibold text-slate-700">Mapped Rule:</span> {selectedCert.rule_id}</p>
                      {selectedCert.activity_date && <p><span className="font-semibold text-slate-700">Date:</span> {selectedCert.activity_date}</p>}
                      <p><span className="font-semibold text-slate-700">Flagged Doubts:</span> {selectedCert.doubt_codes.join(', ')}</p>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Staff Advisor (SFA) Identity
                      </label>
                      <input
                        type="text"
                        value={sfaName}
                        onChange={(e) => setSfaName(e.target.value)}
                        className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-lg text-xs"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Rule Override (Optional ID)
                      </label>
                      <input
                        type="text"
                        placeholder="e.g. 1.2 or 2.2"
                        value={overrideRuleId}
                        onChange={(e) => setOverrideRuleId(e.target.value)}
                        className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-lg text-xs font-mono"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Mandatory Audit Justification *
                      </label>
                      <textarea
                        rows={3}
                        placeholder="Enter the justification / verification evidence found..."
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg text-xs"
                      />
                    </div>

                    <div className="grid grid-cols-3 gap-2 pt-2">
                      <button
                        onClick={() => handleAdjudicate('verify')}
                        disabled={isSubmitting}
                        className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        Verify
                      </button>
                      <button
                        onClick={() => handleAdjudicate('override')}
                        disabled={isSubmitting}
                        className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        Override
                      </button>
                      <button
                        onClick={() => handleAdjudicate('reject')}
                        disabled={isSubmitting}
                        className="px-3 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1"
                      >
                        <XCircle className="w-3.5 h-3.5" />
                        Reject
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )
          ) : (
            /* Audit Trail Tab */
            <div className="space-y-3">
              {auditLog.length === 0 ? (
                <p className="text-sm text-slate-500 py-8 text-center">No audit records recorded yet.</p>
              ) : (
                <div className="overflow-x-auto border border-slate-200 rounded-xl">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-100 text-slate-700 border-b">
                      <tr>
                        <th className="px-4 py-2.5 font-bold">Audit ID</th>
                        <th className="px-4 py-2.5 font-bold">Certificate</th>
                        <th className="px-4 py-2.5 font-bold">Action</th>
                        <th className="px-4 py-2.5 font-bold">Verdict</th>
                        <th className="px-4 py-2.5 font-bold">SFA</th>
                        <th className="px-4 py-2.5 font-bold">Reason</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {auditLog.map((log) => (
                        <tr key={log.audit_id} className="hover:bg-slate-50">
                          <td className="px-4 py-2 font-mono text-slate-500">{log.audit_id}</td>
                          <td className="px-4 py-2 font-mono">{log.certificate_id}</td>
                          <td className="px-4 py-2 uppercase font-bold text-[10px]">{log.action}</td>
                          <td className="px-4 py-2 font-semibold text-emerald-700">{log.new_verdict}</td>
                          <td className="px-4 py-2 text-slate-600">{log.sfa_name}</td>
                          <td className="px-4 py-2 text-slate-800">{log.reason}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-50 border-t border-slate-200 flex justify-end flex-shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-lg text-sm font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
