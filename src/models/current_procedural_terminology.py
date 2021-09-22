from webapp import db

class CurrentProceduralTerminologyModel(db.Model):

    __tablename__ = 'cpts'

    hcpcs = db.Column(db.String(5), nullable=True, primary_key=True)
    mod = db.Column(db.String(2), nullable=True)
    description = db.Column(db.String(28), nullable=True)
    status_code = db.Column(db.String(1), nullable=True)
    not_used_for_mcare_pmt = db.Column(db.String(1), nullable=True)
    wrvu = db.Column(db.String(5), nullable=True)
    non_fac_pe_rvu = db.Column(db.String(5), nullable=True)
    non_fac_na_indicator = db.Column(db.String(2), nullable=True)
    fac_pe_rvu = db.Column(db.String(4), nullable=True)
    fac_na_indicator = db.Column(db.String(2), nullable=True)
    mp_rvu = db.Column(db.String(4), nullable=True)
    non_fac_total = db.Column(db.String(5), nullable=True)
    fac_total = db.Column(db.String(5), nullable=True)
    pctc_ind = db.Column(db.String(1), nullable=True)
    global_period = db.Column(db.String(3), nullable=True)
    preop = db.Column(db.String(3), nullable=True)
    intraop = db.Column(db.String(3), nullable=True)
    postop = db.Column(db.String(3), nullable=True)
    mult_proc = db.Column(db.String(1), nullable=True)
    bilat_surg = db.Column(db.String(1), nullable=True)
    asst_surg = db.Column(db.String(1), nullable=True)
    co_surg = db.Column(db.String(1), nullable=True)
    team_surg = db.Column(db.String(1), nullable=True)
    endo_base = db.Column(db.String(5), nullable=True)
    conv_factor = db.Column(db.String(6), nullable=True)
    physician_supervision_of_diagnostic_procedures = db.Column(db.String(2), nullable=True)
    calculation_flag = db.Column(db.String(1), nullable=True)
    diagnostic_imaging_family_indicator = db.Column(db.String(2), nullable=True)
    non_fac_pe_used_for_opps_pmt_amt = db.Column(db.String(5), nullable=True)
    fac_pe_used_for_opps_pmt_amt = db.Column(db.String(5), nullable=True)
    for_opps_pmt_amt = db.Column(db.String(3), nullable=True)

    def __init__(self,
                 hcpcs=None,
                 mod=None,
                 description=None,
                 status_code=None,
                 not_used_for_mcare_pmt=None,
                 wrvu=None,
                 non_fac_pe_rvu=None,
                 non_fac_na_indicator=None,
                 fac_pe_rvu=None,
                 fac_na_indicator=None,
                 mp_rvu=None,
                 non_fac_total=None,
                 fac_total=None,
                 pctc_ind=None,
                 global_period=None,
                 preop=None,
                 intraop=None,
                 postop=None,
                 mult_proc=None,
                 bilat_surg=None,
                 asst_surg=None,
                 co_surg=None,
                 team_surg=None,
                 endo_base=None,
                 conv_factor=None,
                 physician_supervision_of_diagnostic_procedures=None,
                 calculation_flag=None,
                 diagnostic_imaging_family_indicator=None,
                 non_fac_pe_used_for_opps_pmt_amt=None,
                 fac_pe_used_for_opps_pmt_amt=None,
                 for_opps_pmt_amt=None
                 ):
        self.hcpcs = hcpcs
        self.mod = mod
        self.description = description
        self.status_code = status_code
        self.not_used_for_mcare_pmt = not_used_for_mcare_pmt
        self.wrvu = wrvu
        self.non_fac_pe_rvu = non_fac_pe_rvu
        self.non_fac_na_indicator = non_fac_na_indicator
        self.fac_pe_rvu = fac_pe_rvu
        self.fac_na_indicator = fac_na_indicator
        self.mp_rvu = mp_rvu
        self.non_fac_total = non_fac_total
        self.fac_total = fac_total
        self.pctc_ind = pctc_ind
        self.global_period = global_period
        self.preop = preop
        self.intraop = intraop
        self.postop = postop
        self.mult_proc = mult_proc
        self.bilat_surg = bilat_surg
        self.asst_surg = asst_surg
        self.co_surg = co_surg
        self.team_surg = team_surg
        self.endo_base = endo_base
        self.conv_factor = conv_factor
        self.physician_supervision_of_diagnostic_procedures = physician_supervision_of_diagnostic_procedures
        self.calculation_flag = calculation_flag
        self.diagnostic_imaging_family_indicator = diagnostic_imaging_family_indicator
        self.non_fac_pe_used_for_opps_pmt_amt = non_fac_pe_used_for_opps_pmt_amt
        self.fac_pe_used_for_opps_pmt_amt = fac_pe_used_for_opps_pmt_amt
        self.for_opps_pmt_amt = for_opps_pmt_amt


    @classmethod
    def find_by_code(cls, hcpcs):
        return cls.query.filter_by(hcpcs=hcpcs).first()

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_hcpcs_codes(cls):
        """
        Note that this does not return a list of codes, but a db object that we can extract the codes from to add to a
        list.
        :return: flask_sqlalchemy.BaseQuery
        """
        return db.session.query(cls.hcpcs).order_by(cls.hcpcs.asc())

    @staticmethod
    def validate_hcpcs_code(message_body):
        # get all hcpcs codes from database and store in a list
        db_codes = CurrentProceduralTerminologyModel.get_all_hcpcs_codes()
        all_codes = []
        for code in db_codes:
            if len(code['hcpcs']) == 5:
                all_codes.append(code['hcpcs'])
        for code in all_codes:
            lowered_code = code.lower()
            if lowered_code in message_body.lower():
                return code
        return False

    @staticmethod
    def formatted_found_code_response(code):
        code_base = CurrentProceduralTerminologyModel.find_by_code(code)
        code_result = '{0} is the HCPCS code for "{1}". It has a global period of {2} days and is valued at {3} wRVU.'.format(code_base.hcpcs,
                                                                                                                                  code_base.description,
                                                                                                                                  code_base.global_period,
                                                                                                                                  code_base.wrvu)
        response_string = code_result
        return response_string

    def json(self):
        return {
            'hcpcs': self.hcpcs,
            'mod': self.mod,
            'description': self.description,
            'status_code': self.status_code,
            'not_used_for_mcare_pmt': self.not_used_for_mcare_pmt,
            'wrvu': self.wrvu,
            'non_fac_pe_rvu': self.non_fac_pe_rvu,
            'non_fac_na_indicator': self.non_fac_na_indicator,
            'fac_pe_rvu': self.fac_pe_rvu,
            'fac_na_indicator': self.fac_na_indicator,
            'mp_rvu': self.mp_rvu,
            'non_fac_total': self.non_fac_total,
            'fac_total': self.fac_total,
            'pctc_ind': self.pctc_ind,
            'global_period': self.global_period,
            'preop': self.preop,
            'intraop': self.intraop,
            'postop': self.postop,
            'mult_proc': self.mult_proc,
            'bilat_surg': self.bilat_surg,
            'asst_surg': self.asst_surg,
            'co_surg': self.co_surg,
            'team_surg': self.team_surg,
            'endo_base': self.endo_base,
            'conv_factor': self.conv_factor,
            'physician_supervision_of_diagnostic_procedures': self.physician_supervision_of_diagnostic_procedures,
            'calculation_flag': self.calculation_flag,
            'diagnostic_imaging_family_indicator': self.diagnostic_imaging_family_indicator,
            'non_fac_pe_used_for_opps_pmt_amt': self.non_fac_pe_used_for_opps_pmt_amt,
            'fac_pe_used_for_opps_pmt_amt': self.fac_pe_used_for_opps_pmt_amt,
            'for_opps_pmt_amt': self.for_opps_pmt_amt
        }
