export interface BoardMember {
  name: string;
  role: string;
}

export interface Loan {
  lender: string;
  amount: number | null;
  currency: string | null;
  interest_rate: string | null;
  maturity_date: string | null;
}

export interface AssociationFacts {
  name: string;
  organization_number: string | null;
  address: string | null;
  num_apartments: number | null;
  board_members: BoardMember[];
}

export interface ReportAnalysis {
  association: AssociationFacts;
  loans: Loan[];
  summary: string;
}
