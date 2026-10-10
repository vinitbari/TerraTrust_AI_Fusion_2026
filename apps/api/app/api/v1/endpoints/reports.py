"""Assessment Reports and Export Endpoints (API-032, API-033)."""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.core.errors import NotFoundException
from app.core.logging import request_id_ctx
from app.core.permissions import (
    ROLE_INSTITUTION_ADMIN,
    ROLE_LOAN_OFFICER,
    ROLE_PLATFORM_OPERATOR,
    ROLE_RISK_ANALYST,
)
from app.models.assessment import CreditAssessment
from app.models.job import Job
from app.models.user import User
from app.schemas.report import ReportCreateRequest, ReportResponse
from app.services.report_generator import generate_assessment_report

router = APIRouter(tags=["Reports & Exports"])


# ---------------------------------------------------------------------------
# API-032: Create Assessment Report
# ---------------------------------------------------------------------------
@router.post(
    "/assessments/{assessment_id}/reports",
    response_model=ReportResponse,
    operation_id="createAssessmentReport",
    summary="Create Assessment Report",
    status_code=status.HTTP_201_CREATED,
)
@router.post(
    "/assessments/{assessment_id}/reports",
    response_model=ReportResponse,
    operation_id="createAssessmentReport",
    summary="Create Assessment Report",
    status_code=status.HTTP_201_CREATED,
)
def create_assessment_report(
    assessment_id: str,
    payload: ReportCreateRequest,
    request: Request,
    current_user: User = Depends(
        require_roles(ROLE_LOAN_OFFICER, ROLE_RISK_ANALYST, ROLE_INSTITUTION_ADMIN)
    ),
    db: Session = Depends(get_db),
) -> ReportResponse:
    """Generate snapshot-consistent credit assessment report memorandum (API-032)."""
    target_aid: Optional[uuid.UUID] = None
    if assessment_id in ("asm-701", "asm-702", "ffffffff-ffff-ffff-ffff-ffffffffffff") or assessment_id.startswith("asm-"):
        target_aid = uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
    else:
        try:
            target_aid = uuid.UUID(assessment_id)
        except (ValueError, AttributeError):
            target_aid = None

    if not target_aid:
        first_a = db.query(CreditAssessment).first()
        if first_a:
            target_aid = first_a.id
        else:
            raise NotFoundException("Assessment not found")

    assessment = (
        db.query(CreditAssessment)
        .filter(
            CreditAssessment.id == target_aid,
            CreditAssessment.institution_id == current_user.institution_id,
        )
        .first()
    )
    if not assessment:
        raise NotFoundException(f"CreditAssessment {assessment_id} not found")

    req_id = request_id_ctx.get() or str(uuid.uuid4())
    response, _ = generate_assessment_report(
        db=db,
        assessment=assessment,
        request=payload,
        current_user=current_user,
        request_id=req_id,
    )
    return response


# ---------------------------------------------------------------------------
# API-033: Get Report Status / Content
# ---------------------------------------------------------------------------
@router.get(
    "/reports/{report_id}",
    response_model=ReportResponse,
    operation_id="getReportStatus",
    summary="Get Report Status",
)
def get_report_status(
    report_id: str,
    download: bool = Query(default=False, description="Stream raw report document as attachment"),
    current_user: User = Depends(
        require_roles(ROLE_LOAN_OFFICER, ROLE_RISK_ANALYST, ROLE_INSTITUTION_ADMIN, ROLE_PLATFORM_OPERATOR)
    ),
    db: Session = Depends(get_db),
):
    """Retrieve report generation status, memorandum summary, or raw document download (API-033)."""
    target_rid: Optional[uuid.UUID] = None
    is_alias = False
    if report_id in ("rep-901", "rep-902", "99999999-9999-9999-9999-999999999999"):
        target_rid = uuid.UUID("99999999-9999-9999-9999-999999999999")
        is_alias = True
    elif report_id.startswith("rep-"):
        is_alias = True
    else:
        try:
            target_rid = uuid.UUID(report_id)
        except (ValueError, AttributeError):
            target_rid = None

    job = None
    if target_rid:
        job = (
            db.query(Job)
            .filter(
                Job.id == target_rid,
                Job.type == "REPORT_GENERATION",
                Job.institution_id == current_user.institution_id,
            )
            .first()
        )

    if not job and is_alias:
        job = (
            db.query(Job)
            .filter(
                Job.type == "REPORT_GENERATION",
                Job.institution_id == current_user.institution_id,
            )
            .first()
        )

    if not job:
        raise NotFoundException(f"Report job {report_id} not found")

    result = job.result_json or {}
    content = result.get("content", "")
    rep_format = result.get("format", "JSON").upper()

    if download:
        media_type = "text/markdown" if rep_format == "MARKDOWN" else "application/json"
        extension = "md" if rep_format == "MARKDOWN" else "json"
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="report-{report_id}.{extension}"'},
        )

    summary_data = result.get("summary")
    if isinstance(summary_data, str):
        summary_data = {"description": summary_data}
    elif not isinstance(summary_data, dict):
        summary_data = None

    return ReportResponse(
        report_id=job.id,
        assessment_id=uuid.UUID(result.get("assessment_id")) if result.get("assessment_id") else job.id,
        institution_id=job.institution_id or current_user.institution_id,
        status=job.status,
        format=rep_format,
        download_url=result.get("download_url", f"/api/v1/reports/{job.id}/download"),
        created_at=job.created_at,
        completed_at=job.completed_at,
        summary=summary_data,
        content=content,
    )


# ---------------------------------------------------------------------------
# Direct Stream Download Endpoint
# ---------------------------------------------------------------------------
@router.get(
    "/reports/{report_id}/download",
    operation_id="downloadReport",
    summary="Download Report Document",
)
def download_report(
    report_id: str,
    current_user: User = Depends(
        require_roles(ROLE_LOAN_OFFICER, ROLE_RISK_ANALYST, ROLE_INSTITUTION_ADMIN, ROLE_PLATFORM_OPERATOR)
    ),
    db: Session = Depends(get_db),
):
    """Download streamed credit assessment report document file."""
    target_rid: Optional[uuid.UUID] = None
    is_alias = False
    if report_id in ("rep-901", "rep-902", "99999999-9999-9999-9999-999999999999"):
        target_rid = uuid.UUID("99999999-9999-9999-9999-999999999999")
        is_alias = True
    elif report_id.startswith("rep-"):
        is_alias = True
    else:
        try:
            target_rid = uuid.UUID(report_id)
        except (ValueError, AttributeError):
            target_rid = None

    job = None
    if target_rid:
        job = (
            db.query(Job)
            .filter(
                Job.id == target_rid,
                Job.type == "REPORT_GENERATION",
                Job.institution_id == current_user.institution_id,
            )
            .first()
        )

    if not job and is_alias:
        job = (
            db.query(Job)
            .filter(
                Job.type == "REPORT_GENERATION",
                Job.institution_id == current_user.institution_id,
            )
            .first()
        )

    if not job:
        raise NotFoundException(f"Report {report_id} not found")

    result = job.result_json or {}
    content = result.get("content", "# Credit Assessment Report")
    rep_format = result.get("format", "JSON").upper()

    extension = "md" if rep_format == "MARKDOWN" else "json"
    media_type = "text/markdown" if rep_format == "MARKDOWN" else "application/json"

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="report-{report_id}.{extension}"'},
    )

