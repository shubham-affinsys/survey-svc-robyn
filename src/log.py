

import logging

logger = logging.getLogger('survey-svc')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False




# from sqlalchemy import create_engine, Column, Integer, String, CHAR, DateTime, ForeignKey, JSON, Date, Identity, CheckConstraint, UUID, TEXT
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from uuid import uuid4

# Base = declarative_base()

# class TransactionMaster(Base):
#     __tablename__ = 'transaction_master'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, nullable=False, primary_key=True)
#     transaction_code = Column(String(50), primary_key=True)
#     transaction_desc = Column(String(200), nullable=False)


# class BranchMaster(Base):
#     __tablename__ = 'branch_master'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, primary_key=True)
#     branch_name = Column(String(50), nullable=False)
#     branch_type = Column(String(200))


# class SessionMaster(Base):
#     __tablename__ = 'session_master'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     sessionid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     customer_rep = Column(CHAR(1), CheckConstraint("customer_rep IN ('C', 'R')"), nullable=False)
#     authentication_method = Column(String(20), CheckConstraint("authentication_method IN ('Card', 'CIF', 'Account number', 'NID', 'Passport', 'DL')"))
#     cif = Column(String(50), nullable=False)
#     account_no = Column(JSON)
#     session_start = Column(DateTime(timezone=True))
#     session_end = Column(DateTime(timezone=True))
#     userid = Column(Integer)
#     provider_name = Column(String(50))
#     username = Column(String(100))
#     id_type = Column(String(20))
#     id_no = Column(String(50))
#     first_name = Column(String(50))
#     last_name = Column(String(50))
#     dob = Column(Date)
#     gender = Column(CHAR(1), CheckConstraint("gender IN ('M', 'F', 'O')"))

# class CurrencyMaster(Base):
#     __tablename__ = 'currency_master'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False, primary_key=True)
#     currency_code = Column(String(5), primary_key=True)
#     currency_name = Column(String(50))


# class DenominationMaster(Base):
#     __tablename__ = 'denomination_master'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     currency_code = Column(String(5), ForeignKey('currency_master.currency_code'), nullable=False)
#     denomination_code = Column(Integer, primary_key=True, autoincrement=True)  # Use auto increment
#     denomination_label = Column(String(50))
#     denomination_value = Column(Integer, nullable=False)

# class Transaction(Base):
#     __tablename__ = 'transactions'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     transaction_id = Column(String(50), primary_key=True)
#     transaction_code = Column(String(100), ForeignKey('transaction_master.transaction_code'), nullable=False)
#     transaction_status = Column(CHAR(1), CheckConstraint("transaction_status IN ('D', 'I', 'B', 'S', 'F', 'R')"), primary_key=True)
#     auth_status = Column(CHAR(1), CheckConstraint("auth_status IN ('A', 'U', 'R')"))
#     sessionid = Column(UUID(as_uuid=True), ForeignKey('session_master.sessionid'))
#     created_by = Column(String(50))
#     created_by_user_id = Column(Integer)
#     created_by_provider = Column(String(50))
#     create_timestamp = Column(DateTime(timezone=True))
#     last_updated_user = Column(String(50))
#     last_updated_user_id = Column(Integer)
#     last_updated_user_provider = Column(String(50))
#     last_updated_timestamp = Column(DateTime(timezone=True))
#     comments = Column(CHAR(1), CheckConstraint("comments IN ('Y', 'N')"))
#     data_table = Column(JSONB)
#     callback_done = Column(CHAR(1), CheckConstraint("callback_done IN ('Y', 'N')"))


# class FinancialTransaction(Base):
#     __tablename__ = 'financial_transactions'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     sessionid = Column(UUID(as_uuid=True), ForeignKey('session_master.sessionid'))
#     transaction_id = Column(String(50), ForeignKey('transactions.transaction_id'), primary_key=True)
#     denom_tracking = Column(CHAR(1), CheckConstraint("Denom_tracking IN ('Y', 'N')"))
#     from_account = Column(String(50))
#     to_account = Column(String(50))
#     from_currency = Column(String(50), nullable=False)
#     to_currency = Column(String(50), nullable=False)
#     from_amount = Column(Integer, nullable=False)
#     to_amount = Column(Integer, nullable=False)
#     source_of_funds = Column(String(100))
#     purpose = Column(String(100))
#     remarks1 = Column(String(200))
#     remarks2 = Column(String(200))
#     exchange_rate_type = Column(String(50))
#     exchange_rate = Column(String(50))
#     special_rate = Column(CHAR(1), CheckConstraint("special_rate IN ('Y', 'N')"))
#     treasury_remarks = Column(String(50))
#     treasury_approved = Column(CHAR(1), CheckConstraint("treasury_approved IN ('Y', 'N')"))
#     treasury_approved_date = Column(DateTime(timezone=True))
#     instrument_type = Column(String(50))
#     instrument_date = Column(DateTime(timezone=True))
#     instrument_number = Column(String(50))
#     value_date = Column(DateTime(timezone=True))


# class Comment(Base):
#     __tablename__ = 'comments'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     sessionid = Column(UUID(as_uuid=True), ForeignKey('session_master.sessionid'), nullable=False)
#     transaction_id = Column(String(50), ForeignKey('transactions.transaction_id'), nullable=False)
#     sequence_number = Column(Integer, primary_key=True)
#     user_provider = Column(String(50))
#     username = Column(String(100), nullable=False)
#     userid = Column(Integer, nullable=False)
#     comments = Column(String(200), nullable=False)
#     comments_date = Column(DateTime(timezone=True), nullable=False)

# class TillMaster(Base):
#     __tablename__ = 'till_master'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False, primary_key=True)
#     till_id = Column(Integer, primary_key=True)
#     till_status = Column(CHAR(1), CheckConstraint("till_status IN ('O', 'C')"))
#     till_type = Column(String(20), CheckConstraint("till_type IN ('Till', 'vault', 'chief teller', 'cash centre')"))
#     currency_code = Column(String(5), ForeignKey('currency_master.currency_code'), nullable=False, primary_key=True)
#     denominations = Column(JSONB)
#     amount = Column(Integer)


# class UserTillMaster(Base):
#     __tablename__ = 'user_till_master'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False, primary_key=True)
#     user_provider = Column(String(50))
#     username = Column(String(100), nullable=False)
#     userid = Column(Integer, nullable=False, primary_key=True)
#     till_id = Column(Integer, unique=True)
#     aprover_provider = Column(String(20))
#     aprover_id = Column(Integer, nullable=False)
#     aprover_name = Column(String(20))

# class AuditLogTxn(Base):
#     __tablename__ = 'audit_log_txns'

#     tenant = Column(String(50), nullable=False)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False)
#     audit_id = Column(Integer, primary_key=True)
#     transaction_id = Column(String(50), ForeignKey('transactions.transaction_id'), nullable=False)
#     till_id = Column(Integer, nullable=False)
#     currency_code = Column(String(50), nullable=False)
#     amount = Column(Integer, nullable=False)
#     updated_denominations = Column(JSONB, nullable=False)
#     update_date = Column(DateTime(timezone=True))
#     userid = Column(Integer, nullable=False)
#     username = Column(String(50), nullable=False)

# class TransactionDenomination(Base):
#     __tablename__ = 'transaction_denomination'

#     tenant = Column(String(50), nullable=False, primary_key=True)
#     branch_id = Column(Integer, ForeignKey('branch_master.branch_id'), nullable=False, primary_key=True)
#     transaction_id = Column(String(50), ForeignKey('transactions.transaction_id'), unique=True)
#     till_id = Column(Integer, nullable=False)
#     currency_code = Column(String(50), nullable=False)
#     related_account = Column(String(50))
#     amount = Column(Integer, nullable=False)
#     denominations = Column(JSONB, nullable=False)

