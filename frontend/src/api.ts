import {
  CertificateFacts,
  DashboardResponse,
  Rule,
  StudentProfile,
} from './types';

const API_BASE = '/api';

export async function fetchProfile(): Promise<StudentProfile> {
  const res = await fetch(`${API_BASE}/profile`);
  if (!res.ok) throw new Error('Failed to fetch profile');
  return res.json();
}

export async function updateProfile(profile: StudentProfile): Promise<StudentProfile> {
  const res = await fetch(`${API_BASE}/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  });
  if (!res.ok) throw new Error('Failed to update profile');
  return res.json();
}

export async function fetchRules(): Promise<{ rules: Rule[] }> {
  const res = await fetch(`${API_BASE}/rules`);
  if (!res.ok) throw new Error('Failed to fetch rules');
  return res.json();
}

export async function fetchActivities(): Promise<CertificateFacts[]> {
  const res = await fetch(`${API_BASE}/activities`);
  if (!res.ok) throw new Error('Failed to fetch activities');
  return res.json();
}

export async function addActivity(payload: any): Promise<CertificateFacts> {
  const res = await fetch(`${API_BASE}/activities`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to add activity' }));
    throw new Error(err.detail || 'Failed to add activity');
  }
  return res.json();
}

export async function deleteActivity(certId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/activities/${certId}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete activity');
}

export async function loadSampleActivities(): Promise<CertificateFacts[]> {
  const res = await fetch(`${API_BASE}/activities/load-sample`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to load sample activities');
  return res.json();
}

export async function fetchDashboard(): Promise<DashboardResponse> {
  const res = await fetch(`${API_BASE}/dashboard`);
  if (!res.ok) throw new Error('Failed to fetch dashboard results');
  return res.json();
}

export function getExportUrl(format: 'csv' | 'pdf'): string {
  return `${API_BASE}/export?format=${format}`;
}
