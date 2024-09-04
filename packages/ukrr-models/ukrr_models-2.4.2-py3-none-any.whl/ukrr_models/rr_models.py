from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

from typing import List

Base = declarative_base()


class UKRRPatient(Base):
    __tablename__ = "patients"

    # This is (probably) the last centre for which a file was
    # loaded and not neccesarily the latest/main unit they
    # attend.
    hosp_centre = Column(String)

    rr_no = Column(Integer, primary_key=True)
    surname = Column(String)
    forename = Column(String)
    sex = Column(String)

    nhs_no = Column("new_nhs_no", Integer)
    chi_no = Column(Integer)
    hsc_no = Column(Integer)
    uktssa_no = Column(Integer)

    date_birth = Column(Date)
    date_death = Column(Date)

    ethnicity = Column("ethgr_code", String)

    blood_group = Column(String)
    blood_rhesus = Column("blood_group_rhesus", String)

    cod_read = Column(String)
    # TODO: [GIT-18] These should be updated to String in the DB.
    cod_edta1 = Column(Integer)
    cod_edta2 = Column(Integer)
    cod_text = Column(String)

    # This is the date the patient was
    # first loaded into the UKRR database
    date_registered = Column(Date)

    first_seen_date = Column(Date)

    patient_demographics: Mapped[List["Patient_Demographics"]] = relationship(
        back_populates="ukrr_patient"
    )

    opt_out_flag = Column(String)


class Patient_Demographics(Base):
    __tablename__ = "patient_demog"

    rr_no = Column(Integer, ForeignKey("patients.rr_no"), primary_key=True)
    hosp_centre = Column(String, primary_key=True)

    surname = Column(String)
    forename = Column(String)
    birth_name = Column(String)
    alias_name = Column(String)
    date_birth = Column(Date)
    date_death = Column(Date)

    nhs_no = Column("new_nhs_no", Integer)
    chi_no = Column(Integer)
    hsc_no = Column(Integer)
    uktssa_no = Column(Integer)
    local_hosp_no = Column(String)

    first_seen_date = Column(Date)

    ukrr_patient: Mapped["UKRRPatient"] = relationship(
        back_populates="patient_demographics"
    )


class UKRR_Deleted_Patient(Base):
    __tablename__ = "deleted_patients"

    rr_no = Column(Integer, primary_key=True)
    surname = Column(String)
    forename = Column(String)
    sex = Column(String)

    nhs_no = Column("new_nhs_no", Integer)
    chi_no = Column(Integer)
    hsc_no = Column(Integer)
    uktssa_no = Column(Integer)

    local_hosp_no = Column(String)

    date_birth = Column(Date)
    date_death = Column(Date)


class QuarterlyTreatment(Base):
    __tablename__ = "quarterly_treatment"

    rr_no = Column(Integer, primary_key=True)
    date_start = Column(DateTime, primary_key=True)
    treatment_modality = Column(String, primary_key=True)
    treatment_centre = Column(String, primary_key=True)
    hosp_centre = Column(String, primary_key=True)
    date_end = Column(DateTime)
    add_haemo_on_pd = Column(String)
    creatinine = Column(Numeric(38, 4))
    urea = Column(Numeric(38, 4))
    haemoglobin = Column(Numeric(38, 4))
    ferretin = Column(Numeric(38, 4))
    albumin = Column(Numeric(38, 4))
    aluminium = Column(Numeric(38, 4))
    hba1c = Column(Numeric(38, 4))
    cholesterol = Column(Numeric(38, 4))
    ipth = Column(Numeric(38, 4))
    calcium_uncorr = Column(Numeric(38, 4))
    calcium_corr = Column(Numeric(38, 4))
    phosphate = Column(Numeric(38, 4))
    bicarbonate = Column(Numeric(38, 4))
    systolic_bp = Column(Numeric(20, 0))
    diastolic_bp = Column(Numeric(20, 0))
    weight = Column(Numeric(38, 4))
    urea_reduction_ratio = Column(Numeric(38, 4))
    epo_use = Column(String)
    hd_supervison = Column(String)
    dialyser_used = Column(String)
    flow_rate = Column(Numeric(20, 0))
    dial_reuse = Column(String)
    times_per_week = Column(Numeric(20, 0))
    dial_time = Column(Numeric(38, 4))
    bicarb_dial = Column(String)
    weekly_fluid_vol = Column(Numeric(38, 4))
    bag_size = Column(Numeric(38, 4))
    centre_pri = Column(String)
    post_systolic_bp = Column(Numeric(20, 0))
    post_diastolic_bp = Column(Numeric(20, 0))
    sodium = Column(Numeric(38, 4))
    pd_dialysate_ktv = Column(Numeric(38, 4))
    pd_urine_ktv = Column(Numeric(38, 4))
    pd_npcr = Column(Numeric(38, 4))
    crp = Column(Numeric(38, 4))
    ldl_cholesterol = Column(Numeric(38, 4))
    hdl_cholesterol = Column(Numeric(38, 4))
    triglycerides = Column(Numeric(38, 4))
    waiting_list_status = Column(String)
    creatinine_first_month = Column(Numeric(38, 4))
    creatinine_second_month = Column(Numeric(38, 4))
    percent_hypochromic = Column(Numeric(38, 4))
    mch = Column(Numeric(38, 4))
    b12 = Column(Numeric(38, 4))
    red_cell_folate = Column(Numeric(38, 4))
    transferrin_saturation = Column(Numeric(38, 4))
    serum_potassium = Column(Numeric(38, 4))
    protein_creatinine_ratio = Column(Numeric(38, 4))
    albumin_creatinine_ratio = Column(Numeric(38, 4))
    serum_cell_folate = Column(Numeric(38, 4))
    ace_inhibitor = Column(String)
    renagel = Column(String)
    lanthanum = Column(String)
    cinacalcet = Column(String)
    calcium_based_binder = Column(String)
    alucaps = Column(String)
    serum_urate = Column(Numeric(38, 4))
    statin_drug_use = Column(String)
    hba1c_mmol = Column(Numeric(3, 0))
    alkaline_phosphatase = Column(Numeric(38, 4))
