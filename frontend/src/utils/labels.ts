const VIOLATION_TYPE_LABELS: Record<string, string> = {
  'NO-Hardhat': 'No Helmet',
  'NO-Mask': 'No Mask',
  'NO-Safety Vest': 'No Vest',
};

export function formatViolationType(violationType: string): string {
  return VIOLATION_TYPE_LABELS[violationType] ?? violationType;
}
