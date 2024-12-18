from sqlalchemy import Column, BigInteger, String, ForeignKey, Index, TIMESTAMP, text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner = Column(String, nullable=False)
    balance = Column(BigInteger, nullable=False)
    currency = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    entries = relationship("Entry", back_populates="account")
    outgoing_transfers = relationship("Transfer", foreign_keys="Transfer.from_account_id", back_populates="from_account")
    incoming_transfers = relationship("Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account")

    __table_args__ = (
        Index("idx_accounts_owner", "owner"),
    )

class Entry(Base):
    __tablename__ = "entries"

    entry_id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_id = Column(BigInteger, ForeignKey("accounts.account_id"), nullable=True)
    amount = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    account = relationship("Account", back_populates="entries")

    __table_args__ = (
        Index("idx_entries_account_id", "account_id"),
    )

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    from_account_id = Column(BigInteger, ForeignKey("accounts.account_id"), nullable=True)
    to_account_id = Column(BigInteger, ForeignKey("accounts.account_id"), nullable=True)
    amount = Column(BigInteger, nullable=False, comment="It must be positive")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="outgoing_transfers")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="incoming_transfers")

    __table_args__ = (
        Index("idx_transfers_from_account_id", "from_account_id"),
        Index("idx_transfers_to_account_id", "to_account_id"),
        Index("idx_transfers_from_to_account_id", "from_account_id", "to_account_id"),
    )
