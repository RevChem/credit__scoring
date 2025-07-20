import re
from typing import Optional
from app.users.sql_enums import JobType
from pydantic import BaseModel, Field, field_validator


class SUser(BaseModel):
    Amt: float = Field(..., description="Сумма кредита")
    Trm: int = Field(..., description="Срок кредита в месяцах")

    YngAcntAge: Optional[float] = Field(None, description="Возраст самого молодого счёта")
    CntActv: Optional[int] = Field(None, description="Количество активных счетов")
    CntCls12: Optional[int] = Field(None, description="Количество закрытых за последние 12 месяцев")
    CntOpn12: Optional[int] = Field(None, description="Количество открытых за последние 12 месяцев")
    CntSttl: Optional[int] = Field(None, description="Количество погашенных счетов")
    AvgAcntAge: Optional[float] = Field(None, description="Средний возраст счетов")

    OutBal: Optional[float] = Field(None, description="Общая сумма текущих обязательств")
    OutBalNoMtg: Optional[float] = Field(None, description="Обязательства без ипотеки")
    WorstPayStat: Optional[int] = Field(None, description="Худший статус платежей по активным счетам")

    EmpPT: Optional[JobType] 
    EmpRtrd: Optional[int] = Field(None, description="На пенсии (0/1)")
    EmpSelf: Optional[int] = Field(None, description="Самозанятый (0/1)")

    LoanPurpose: Optional[str] = Field(None, description="Цель кредита")

    @field_validator("Trm")
    @classmethod
    def validate_Trm(cls, value: int) -> int:
        if value < 3:
            raise ValueError('Срок кредита не может быть меньше 3 месяцев')
        return value



