from fastapi import APIRouter

from packages.domain.models import ApprovalDecision, ApprovalRequest, ApprovalResult


router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.post("/{document_version_id}", response_model=ApprovalResult)
def decide_approval(document_version_id: str, payload: ApprovalRequest) -> ApprovalResult:
    return ApprovalResult(
        document_version_id=document_version_id,
        decision=payload.decision,
        published=payload.decision == ApprovalDecision.APPROVE,
    )

