export type EntryType = 'regular' | 'lateral';

export interface StudentProfile {
  student_id: string;
  full_name: string;
  programme: string;
  admission_date: string;
  programme_end_date: string;
  entry_type: EntryType;
  is_pwd: boolean;
  scheme: string;
  aliases: string[];
}

export type Level = 'college' | 'zonal' | 'state' | 'national' | 'international';
export type Verdict = 'VERIFIED' | 'DOUBT' | 'NOT_ELIGIBLE' | 'MANUAL_ONLY';

export interface CertificateFacts {
  certificate_id: string;
  rule_id: string;
  activity_title: string;
  event_name?: string | null;
  organiser?: string | null;
  level?: Level | null;
  position?: string | null;
  event_type?: string | null;
  activity_date?: string | null;
  academic_year?: string | null;
  semester?: string | null;
  duration_days?: number | null;
  duration_hours?: number | null;
  duration_weeks?: number | null;
  duration_months?: string | null;
  score_value?: string | number | null;
  verdict: Verdict;
  doubt_codes: string[];
  student_asserted: boolean;
}

export interface PointBracket {
  confirmed: number;
  pending: number;
  upper_bound: number;
}

export interface ActivityOutcome {
  certificate_id: string;
  rule_id: string;
  group: 'I' | 'II' | 'III';
  activity_title?: string | null;
  raw_points: number;
  counted_points_pessimistic: number;
  counted_points_optimistic: number;
  verdict: string;
  doubt_codes: string[];
  notes: string[];
}

export interface GroupResult {
  group_id: 'I' | 'II' | 'III';
  required_points: number;
  bracket: PointBracket;
  is_credit_achieved_confirmed: boolean;
  is_credit_achievable_upper: boolean;
  activities: ActivityOutcome[];
}

export interface EngineResult {
  total_bracket: PointBracket;
  required_total: number;
  groups: {
    I: GroupResult;
    II: GroupResult;
    III: GroupResult;
  };
  credit_status: 'ACHIEVED' | 'ACHIEVABLE_WITH_PENDING' | 'DEFICIT';
  credits_earned_confirmed: number;
  credits_earned_upper: number;
  activities: ActivityOutcome[];
  ambiguity_flags: string[];
}

export interface DoubtDetail {
  code: string;
  category: string;
  severity: string;
  message: string;
  how_to_resolve: string;
  points_impact: string;
}

export interface DashboardResponse {
  engine_result: EngineResult;
  doubt_catalog: Record<string, DoubtDetail>;
  disclaimer: string;
}

export interface Rule {
  id: string;
  group: 'I' | 'II' | 'III';
  major_head: string;
  sub_activity_head: string;
  kind: string;
  handbook_page: number;
  handbook_page_pdf: number;
  points: any;
  documentary_evidence: string;
  evidence_issuers: string[];
  cap_subhead: number | null;
  cap_category: number | null;
  shared_cap_id: string | null;
  shared_cap_max: number | null;
  remarks: string | null;
}
