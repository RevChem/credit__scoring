from sqlalchemy import Float, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk
from app.users.sql_enums import JobType, Risk_Category


class User(Base):
    id: Mapped[int_pk] 

    Amt: Mapped[float] = mapped_column(Float)
    Trm: Mapped[int] = mapped_column(Integer)

    YngAcntAge: Mapped[float] = mapped_column(Float, nullable=True)
    CntActv: Mapped[int] = mapped_column(Integer, nullable=True)
    CntCls12: Mapped[int] = mapped_column(Integer, nullable=True)
    CntOpn12: Mapped[int] = mapped_column(Integer, nullable=True)
    CntSttl: Mapped[int] = mapped_column(Integer, nullable=True)
    AvgAcntAge: Mapped[float] = mapped_column(Float, nullable=True)

    OutBal: Mapped[float] = mapped_column(Float, nullable=True)
    OutBalNoMtg: Mapped[float] = mapped_column(Float, nullable=True)
    WorstPayStat: Mapped[int] = mapped_column(Integer, nullable=True)

    EmpPT: Mapped[JobType] 
    EmpRtrd: Mapped[int] = mapped_column(Integer, nullable=True)
    EmpSelf: Mapped[int] = mapped_column(Integer, nullable=True)
    LoanPurpose: Mapped[str] = mapped_column(String, nullable=False)

    Probability: Mapped[float] = mapped_column(Float, nullable=True)
    Risk_Category: Mapped[Risk_Category] 

    extend_existing = True

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, Amt={self.Amt})"

    def __repr__(self):
        return str(self)


    def to_dict(self):
        return {
            "id": self.id,
            "Amt": self.Amt,
            "Trm": self.Trm,
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
            "Probability": self.Probability,
            "Risk_Category": self.Risk_Category
        }