from app.users.sql_enums import JobType

class RBUser:
    def __init__(
        self,
        id: int | None = None,
        Amt: float | None = None,
        Trm: int | None = None,
        Suc: int | None = None,
        YngAcntAge: float | None = None,
        CntActv: int | None = None,
        CntCls12: int | None = None,
        CntOpn12: int | None = None,
        CntSttl: int | None = None,
        AvgAcntAge: float | None = None,
        OutBal: float | None = None,
        OutBalNoMtg: float | None = None,
        WorstPayStat: int | None = None,
        EmpPT: JobType | None = None,
        EmpRtrd: int | None = None,
        EmpSelf: int | None = None,
        LoanPurpose: str | None = None,
    ):
        self.id = id
        self.Amt = Amt
        self.Trm = Trm
        self.Suc = Suc
        self.YngAcntAge = YngAcntAge
        self.CntActv = CntActv
        self.CntCls12 = CntCls12
        self.CntOpn12 = CntOpn12
        self.CntSttl = CntSttl
        self.AvgAcntAge = AvgAcntAge
        self.OutBal = OutBal
        self.OutBalNoMtg = OutBalNoMtg
        self.WorstPayStat = WorstPayStat
        self.EmpPT = EmpPT
        self.EmpRtrd = EmpRtrd
        self.EmpSelf = EmpSelf
        self.LoanPurpose = LoanPurpose

    def to_dict(self) -> dict:
        return {
            key: value
            for key, value in {
                "id": self.id,
                "Amt": self.Amt,
                "Trm": self.Trm,
                "Suc": self.Suc,
                "YngAcntAge": self.YngAcntAge,
                "CntActv": self.CntActv,
                "CntCls12": self.CntCls12,
                "CntOpn12": self.CntOpn12,
                "CntSttl": self.CntSttl,
                "AvgAcntAge": self.AvgAcntAge,
                "OutBal": self.OutBal,
                "OutBalNoMtg": self.OutBalNoMtg,
                "WorstPayStat": self.WorstPayStat,
                "EmpPT": self.EmpPT,
                "EmpRtrd": self.EmpRtrd,
                "EmpSelf": self.EmpSelf,
                "LoanPurpose": self.LoanPurpose,
            }.items()
            if value is not None
        }