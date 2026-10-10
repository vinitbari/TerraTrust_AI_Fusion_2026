"""Deterministic seed data for local development and integration tests."""

import uuid
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from app.models.assessment import CreditAssessment, YieldPrediction, RiskExplanation, ScenarioRun
from app.models.borrower import Borrower
from app.models.crop_cycle import CropCycle
from app.models.farm import Farm, Plot
from app.models.governance import DataSource, ModelVersion
from app.models.institution import Branch, Institution, UserBranch
from app.models.loan import Loan, LoanApplication, RepaymentSchedule
from app.models.user import Permission, Role, User
from app.models.observation import ClimateObservation, SatelliteObservation, SoilMoisture
from app.models.job import Job
from app.core.security import hash_password


def seed_database(db: Session) -> dict:
    """Populate database with deterministic initial data if empty."""
    institution = db.query(Institution).filter_by(id=uuid.UUID("11111111-1111-1111-1111-111111111111")).first()
    if institution:
        return {"status": "already_seeded", "institution_id": str(institution.id)}

    # 1. Institution & Branches
    institution = Institution(
        id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
        name="Apex Rural Development Bank",
        status="ACTIVE",
    )
    db.add(institution)
    db.flush()

    branch_solapur = db.query(Branch).filter_by(id=uuid.UUID("22222222-2222-2222-2222-222222222221")).first()
    if not branch_solapur:
        branch_solapur = Branch(
            id=uuid.UUID("22222222-2222-2222-2222-222222222221"),
            institution=institution,
            name="Solapur South Branch",
            code="BR-SOL-01",
        )
        db.add(branch_solapur)

    branch_nashik = db.query(Branch).filter_by(id=uuid.UUID("22222222-2222-2222-2222-222222222222")).first()
    if not branch_nashik:
        branch_nashik = Branch(
            id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
            institution=institution,
            name="Nashik Central Branch",
            code="BR-NSK-01",
        )
        db.add(branch_nashik)
    db.flush()

    # 2. Roles & Permissions
    roles_map = {
        "LOAN_OFFICER": (uuid.UUID("33333333-3333-3333-3333-333333333331"), "Frontline loan origination, farm profiling, and review report generation"),
        "RISK_ANALYST": (uuid.UUID("33333333-3333-3333-3333-333333333332"), "Credit risk underwriting, scenario evaluation, and model validation"),
        "INSTITUTION_ADMIN": (uuid.UUID("33333333-3333-3333-3333-333333333333"), "Branch and user management, data import health oversight"),
        "PLATFORM_OPERATOR": (uuid.UUID("33333333-3333-3333-3333-333333333334"), "Infrastructure, model deployment, and system observability"),
    }
    roles = {}
    for code, (rid, desc) in roles_map.items():
        role = db.query(Role).filter_by(code=code).first()
        if not role:
            role = Role(id=rid, code=code, description=desc)
            db.add(role)
        roles[code] = role
    db.flush()

    # 3. Default Users
    default_password_hash = hash_password("password123")

    user_officer = db.query(User).filter_by(email="officer@fin03.local").first()
    if not user_officer:
        user_officer = User(
            id=uuid.UUID("44444444-4444-4444-4444-444444444441"),
            institution=institution,
            email="officer@fin03.local",
            full_name="Rajesh Sharma (Loan Officer)",
            hashed_password=default_password_hash,
            status="ACTIVE",
            roles=[roles["LOAN_OFFICER"]],
        )
        db.add(user_officer)

    user_analyst = db.query(User).filter_by(email="analyst@fin03.local").first()
    if not user_analyst:
        user_analyst = User(
            id=uuid.UUID("44444444-4444-4444-4444-444444444442"),
            institution=institution,
            email="analyst@fin03.local",
            full_name="Priya Deshmukh (Risk Analyst)",
            hashed_password=default_password_hash,
            status="ACTIVE",
            roles=[roles["RISK_ANALYST"]],
        )
        db.add(user_analyst)

    user_admin = db.query(User).filter_by(email="admin@fin03.local").first()
    if not user_admin:
        user_admin = User(
            id=uuid.UUID("44444444-4444-4444-4444-444444444443"),
            institution=institution,
            email="admin@fin03.local",
            full_name="Vikram Joshi (Admin)",
            hashed_password=default_password_hash,
            status="ACTIVE",
            roles=[roles["INSTITUTION_ADMIN"]],
        )
        db.add(user_admin)
    db.flush()

    # Assign branch scope
    ub1 = db.query(UserBranch).filter_by(user_id=user_officer.id, branch_id=branch_solapur.id).first()
    if not ub1:
        ub1 = UserBranch(
            id=uuid.uuid4(),
            user=user_officer,
            branch=branch_solapur,
            scope="BRANCH_READ_WRITE",
        )
        db.add(ub1)

    # 4. Registered Data Sources
    source_weather = db.query(DataSource).filter_by(id=uuid.UUID("55555555-5555-5555-5555-555555555551")).first()
    if not source_weather:
        source_weather = DataSource(
            id=uuid.UUID("55555555-5555-5555-5555-555555555551"),
            name="IMD Weather Observations",
            type="WEATHER",
            terms_uri="https://mausam.imd.gov.in/",
            license_ref="Government Open Data License - India",
            status="ACTIVE",
            owner="India Meteorological Department",
        )
        db.add(source_weather)

    source_sentinel = db.query(DataSource).filter_by(id=uuid.UUID("55555555-5555-5555-5555-555555555552")).first()
    if not source_sentinel:
        source_sentinel = DataSource(
            id=uuid.UUID("55555555-5555-5555-5555-555555555552"),
            name="Copernicus Sentinel-2 MSI",
            type="SATELLITE",
            terms_uri="https://dataspace.copernicus.eu/",
            license_ref="Copernicus Open Access License",
            status="ACTIVE",
            owner="European Space Agency",
        )
        db.add(source_sentinel)

    source_market = db.query(DataSource).filter_by(id=uuid.UUID("55555555-5555-5555-5555-555555555553")).first()
    if not source_market:
        source_market = DataSource(
            id=uuid.UUID("55555555-5555-5555-5555-555555555553"),
            name="AGMARKNET Mandi Portal",
            type="MARKET",
            terms_uri="https://agmarknet.gov.in/",
            license_ref="Ministry of Agriculture & Farmers Welfare",
            status="ACTIVE",
            owner="Directorate of Marketing & Inspection",
        )
        db.add(source_market)
    db.flush()

    # 5. Model Version
    model_baseline = db.query(ModelVersion).filter_by(id=uuid.UUID("66666666-6666-6666-6666-666666666661")).first()
    if not model_baseline:
        model_baseline = ModelVersion(
            id=uuid.UUID("66666666-6666-6666-6666-666666666661"),
            name="crop-yield-baseline",
            version="0.1.0-demo",
            artifact_uri="./artifacts/demo-model.joblib",
            checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            feature_schema_version="1.0",
            metrics_json={"mae": 142.5, "rmse": 185.0, "unit": "kg/hectare"},
            status="PROMOTED",
            approved_at=datetime.now(timezone.utc),
        )
        db.add(model_baseline)
    db.flush()

    # 6. Sample Borrower
    borrower = db.query(Borrower).filter_by(id=uuid.UUID("77777777-7777-7777-7777-777777777771")).first()
    if not borrower:
        borrower = Borrower(
            id=uuid.UUID("77777777-7777-7777-7777-777777777771"),
            institution=institution,
            branch=branch_solapur,
            external_ref="CUST-MH-2026-001",
            display_name="Ramesh Patil",
            contact_phone="+91-9822012345",
            contact_email="ramesh.patil@example.farm",
            status="ACTIVE",
        )
        db.add(borrower)
    db.flush()

    # 7. Sample Farm & Plot
    farm = db.query(Farm).filter_by(id=uuid.UUID("88888888-8888-8888-8888-888888888881")).first()
    if not farm:
        farm = Farm(
            id=uuid.UUID("88888888-8888-8888-8888-888888888881"),
            institution=institution,
            borrower=borrower,
            name="Patil Farmholding",
            latitude=17.6599,
            longitude=75.9064,
            area_value=2.5,
            area_unit="hectare",
            village="Kumbhari",
            district="Solapur",
            state="Maharashtra",
            status="ACTIVE",
        )
        db.add(farm)
    db.flush()

    plot = db.query(Plot).filter_by(id=uuid.UUID("99999999-9999-9999-9999-999999999991")).first()
    if not plot:
        plot = Plot(
            id=uuid.UUID("99999999-9999-9999-9999-999999999991"),
            farm=farm,
            name="Plot A - North Field",
            area_value=1.5,
            area_unit="hectare",
            soil_type="Medium Black Soil",
        )
        db.add(plot)
    db.flush()

    # 8. Sample Crop Cycle
    crop_cycle = db.query(CropCycle).filter_by(id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")).first()
    if not crop_cycle:
        crop_cycle = CropCycle(
            id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            plot=plot,
            crop_code="WHEAT",
            variety="Lokwan",
            season="RABI",
            sowing_date=date(2026, 11, 1),
            expected_harvest_date=date(2027, 3, 15),
            area_value=1.5,
            area_unit="hectare",
            irrigation_type="CANAL",
            irrigation_reliability="HIGH",
            status="GROWING",
        )
        db.add(crop_cycle)
    db.flush()

    # 9. Sample Loan Application & Loan
    loan_app = db.query(LoanApplication).filter_by(id=uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")).first()
    if not loan_app:
        loan_app = LoanApplication(
            id=uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
            institution=institution,
            borrower=borrower,
            branch=branch_solapur,
            amount=150000.00,
            currency="INR",
            purpose="Crop cultivation inputs (seeds, fertilizer, diesel)",
            status="APPROVED",
        )
        db.add(loan_app)
    db.flush()

    loan = db.query(Loan).filter_by(id=uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")).first()
    if not loan:
        loan = Loan(
            id=uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),
            application=loan_app,
            institution=institution,
            borrower=borrower,
            principal=150000.00,
            currency="INR",
            interest_rate=0.0700,
            start_date=date(2026, 11, 1),
            end_date=date(2027, 4, 30),
            repayment_frequency="BULLET_HARVEST",
            status="ACTIVE",
        )
        db.add(loan)
    db.flush()

    # 11. Credit Assessment
    assessment = db.query(CreditAssessment).filter_by(id=uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")).first()
    if not assessment:
        assessment = CreditAssessment(
            id=uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"),
            institution_id=institution.id,
            borrower_id=borrower.id,
            loan_id=loan.id,
            model_version_id=model_baseline.id,
            status="COMPLETED",
            risk_band="LOW",
            dscr=1.68,
            pd_status="NOT_AVAILABLE",
            completed_at=datetime.now(timezone.utc),
            snapshot_json={
                "assessment_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
                "borrower": {
                    "id": str(borrower.id),
                    "display_name": borrower.display_name,
                    "external_ref": borrower.external_ref,
                },
                "farm": {
                    "id": str(farm.id),
                    "name": farm.name,
                    "area_value": farm.area_value,
                    "area_unit": farm.area_unit,
                },
                "crop_cycle": {
                    "id": str(crop_cycle.id),
                    "crop_code": crop_cycle.crop_code,
                    "season": crop_cycle.season,
                    "area_value": crop_cycle.area_value,
                },
                "yield_prediction": {
                    "value": 3850.0,
                    "unit": "kg/hectare",
                    "model_version_id": "v1.0.0",
                    "quality_status": "VALID",
                    "uncertainty": {"lower_bound": 3465.0, "upper_bound": 4235.0, "confidence_level": 0.90},
                },
                "income_estimate": {
                    "gross_revenue": 308000.0,
                    "production_costs": 125000.0,
                    "net_farm_income": 183000.0,
                    "iads": 155000.0,
                    "debt_service": 60000.0,
                    "repayment_capacity_ratio": 1.68,
                    "currency": "INR",
                },
                "risk_score": 78,
                "risk_band": "LOW",
                "dscr": 1.68,
                "pd_regulatory_status": "PD_UNAVAILABLE",
            },
        )
        db.add(assessment)
    db.flush()

    # 12. Risk Explanations
    exp = db.query(RiskExplanation).filter_by(assessment_id=assessment.id).first()
    if not exp:
        exp1 = RiskExplanation(
            id=uuid.uuid4(),
            assessment=assessment,
            factor_code="AGRI-YLD-01",
            contribution_value=12.5,
            direction="POSITIVE",
            explanation_type="MODEL_FEATURE",
            unit="pts",
            caveat="Yield model trained on historical regional agro-climatic distributions.",
        )
        exp2 = RiskExplanation(
            id=uuid.uuid4(),
            assessment=assessment,
            factor_code="FIN-DSCR-02",
            contribution_value=15.0,
            direction="POSITIVE",
            explanation_type="MODEL_FEATURE",
            unit="pts",
            caveat="Assuming MSP statutory procurement price benchmarks.",
        )
        exp3 = RiskExplanation(
            id=uuid.uuid4(),
            assessment=assessment,
            factor_code="EO-NDVI-03",
            contribution_value=8.0,
            direction="POSITIVE",
            explanation_type="OBSERVED_FACT",
            unit="pts",
            caveat="Clear satellite pass with <5% cloud occlusion.",
        )
        db.add_all([exp1, exp2, exp3])
    db.flush()

    # 13. Scenario Runs
    sc = db.query(ScenarioRun).filter_by(assessment_id=assessment.id).first()
    if not sc:
        sc1 = ScenarioRun(
            id=uuid.uuid4(),
            assessment=assessment,
            scenario_code="DROUGHT_SEVERE",
            assumptions_json={"yield_change_pct": -20.0, "rainfall_factor_pct": -30.0, "price_change_pct": 5.0},
            yield_delta_pct=-20.0,
            income_delta_pct=-24.5,
            result_json={
                "name": "Severe Monsoon Drought Scenario",
                "description": "30% rainfall deficit stress test with compensatory mandi price firming.",
                "baseline": {"yield_val": 3.85, "gross_revenue": 308000, "net_income": 183000, "iads": 155000, "risk_classification": "LOW"},
                "projected": {"yield_val": 3.08, "gross_revenue": 258720, "net_income": 133720, "iads": 105720, "delta_net_income": -49280, "delta_iads": -49280, "repayment_ratio": 1.25, "risk_classification": "MEDIUM"},
                "assumptions": {"yield_change_pct": -20.0, "price_change_pct": 5.0, "cost_change_pct": 0.0, "rainfall_factor_pct": -30.0, "tenor_extension_months": 0},
                "created_by": "System Stress Benchmark",
                "evidence_status": "ILLUSTRATIVE",
            },
            evidence_status="ILLUSTRATIVE_ASSUMPTION",
        )
        db.add(sc1)
    db.flush()

    # 14. Report Job
    job_report = db.query(Job).filter_by(id=uuid.UUID("99999999-9999-9999-9999-999999999999")).first()
    if not job_report:
        job_report = Job(
            id=uuid.UUID("99999999-9999-9999-9999-999999999999"),
            institution_id=institution.id,
            type="REPORT_GENERATION",
            status="COMPLETED",
            payload_json={"assessment_id": str(assessment.id), "export_format": "PDF"},
            result_json={
                "assessment_id": str(assessment.id),
                "format": "PDF",
                "download_url": f"/api/v1/reports/99999999-9999-9999-9999-999999999999/download",
                "summary": {
                    "title": "Credit Assessment Memorandum",
                    "description": "Credit Assessment Memorandum for Ramesh Patil (CUST-MH-2026-001) - Score 78, DSCR 1.68x",
                    "borrower_name": "Ramesh Patil",
                    "external_ref": "CUST-MH-2026-001",
                    "repayment_probability_status": "NOT_AVAILABLE",
                    "disclaimer": "Agricultural credit risk analysis decision support.",
                },
                "content": "# Credit Assessment Report\n**Borrower:** Ramesh Patil\n**Status:** Approved",
            },
        )
        db.add(job_report)

    db.commit()
    return {
        "status": "seeded",
        "institution_id": str(institution.id),
        "borrower_id": str(borrower.id),
        "farm_id": str(farm.id),
        "crop_cycle_id": str(crop_cycle.id),
        "loan_id": str(loan.id),
        "assessment_id": str(assessment.id),
    }


if __name__ == "__main__":
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        res = seed_database(db)
        print("Seed finished:", res)
    finally:
        db.close()
