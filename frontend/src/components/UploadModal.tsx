import React, { useState } from 'react';
import { UploadCloud, CheckCircle2, AlertTriangle, X, FileText, Loader2 } from 'lucide-react';
import { uploadDocument } from '../api';
import { CertificateFacts } from '../types';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: (fact: CertificateFacts) => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onUploadSuccess,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<CertificateFacts | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = (selectedFile: File) => {
    setErrorMsg(null);
    setUploadResult(null);

    const allowed = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
    if (!allowed.includes(selectedFile.type) && !selectedFile.name.endsWith('.pdf')) {
      setErrorMsg('Invalid file format. Only PDF, PNG, and JPG files are accepted.');
      return;
    }

    if (selectedFile.size > 15 * 1024 * 1024) {
      setErrorMsg('File exceeds 15 MB maximum size limit.');
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      setIsUploading(true);
      setErrorMsg(null);
      const fact = await uploadDocument(file);
      setUploadResult(fact);
      onUploadSuccess(fact);
    } catch (err: any) {
      setErrorMsg(err.message || 'Upload and fact extraction failed.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-xl w-full shadow-2xl border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <UploadCloud className="w-6 h-6 text-emerald-400" />
            <h2 className="text-lg font-bold">Upload Activity Certificate</h2>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Dropzone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
              dragActive
                ? 'border-emerald-500 bg-emerald-50/50'
                : 'border-slate-300 hover:border-slate-400 bg-slate-50'
            }`}
          >
            <input
              type="file"
              id="cert-file-input"
              className="hidden"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={handleFileInput}
            />
            <label htmlFor="cert-file-input" className="cursor-pointer block">
              <UploadCloud className="w-12 h-12 text-slate-400 mx-auto mb-3" />
              <p className="text-sm font-semibold text-slate-700">
                Click to browse or drag and drop certificate here
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Accepted: Native PDF, PNG, JPG (Max 15 MB, up to 10 pages)
              </p>
            </label>
          </div>

          {/* Selected File Display */}
          {file && (
            <div className="bg-slate-100 rounded-lg p-3 flex items-center justify-between border border-slate-200">
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-indigo-600" />
                <div>
                  <p className="text-sm font-medium text-slate-800">{file.name}</p>
                  <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors disabled:opacity-50"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Extracting Facts...
                  </>
                ) : (
                  'Process Certificate'
                )}
              </button>
            </div>
          )}

          {/* Error Message */}
          {errorMsg && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-sm flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Upload & Extraction Result */}
          {uploadResult && (
            <div
              className={`p-4 rounded-xl border ${
                uploadResult.verdict === 'VERIFIED'
                  ? 'bg-emerald-50 border-emerald-200'
                  : 'bg-amber-50 border-amber-200'
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                {uploadResult.verdict === 'VERIFIED' ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-amber-600" />
                )}
                <h4
                  className={`text-sm font-bold ${
                    uploadResult.verdict === 'VERIFIED' ? 'text-emerald-900' : 'text-amber-900'
                  }`}
                >
                  Extraction Verdict: {uploadResult.verdict}
                </h4>
              </div>

              <div className="text-xs space-y-1 text-slate-700">
                <p>
                  <span className="font-semibold">Mapped Rule:</span> {uploadResult.rule_id}
                </p>
                <p>
                  <span className="font-semibold">Title:</span> {uploadResult.activity_title}
                </p>
                {uploadResult.activity_date && (
                  <p>
                    <span className="font-semibold">Date:</span> {uploadResult.activity_date}
                  </p>
                )}
                {uploadResult.level && (
                  <p>
                    <span className="font-semibold">Level:</span> {uploadResult.level}
                  </p>
                )}
              </div>

              {uploadResult.doubt_codes.length > 0 && (
                <div className="mt-3 pt-3 border-t border-amber-200">
                  <p className="text-xs font-semibold text-amber-800 mb-1">
                    Triggered Doubt Codes (Pending SFA Review):
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {uploadResult.doubt_codes.map((code) => (
                      <span
                        key={code}
                        className="px-2 py-0.5 bg-amber-200 text-amber-900 font-mono text-[11px] rounded"
                      >
                        {code}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-50 border-t border-slate-200 flex justify-end">
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
