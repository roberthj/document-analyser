from typing import List, Optional
from pydantic import BaseModel


class BoardMember(BaseModel):
    name: str
    role: str


class Loan(BaseModel):
    lender: str
    amount: Optional[float] = None
    currency: Optional[str] = None
    interest_rate: Optional[str] = None
    maturity_date: Optional[str] = None


class AssociationFacts(BaseModel):
    name: str
    organization_number: Optional[str] = None
    address: Optional[str] = None
    num_apartments: Optional[int] = None
    board_members: List[BoardMember] = []


class AnnualReportAnalysis(BaseModel):
    association: AssociationFacts
    loans: List[Loan] = []
    summary: str
    notes: List[str] = []
