from databases.domains.settings import Settings
from sqlalchemy.orm import sessionmaker

class SettingsRepository:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        
    def getRunnerNumber(self, session):
        return session.query(Settings.state).filter(Settings.data == "RunnerNumber").scalar()
    
    def setRunnerNumber(self, session, value):
        session.query(Settings).filter(Settings.data == "RunnerNumber").update({Settings.state: value})
        session.commit()
        
    def getRewardsNumber(self, session):
        return session.query(Settings.state).filter(Settings.data == "RewardsNumber").scalar()
    
    def setRewardsNumber(self, session, value):
        session.query(Settings).filter(Settings.data == "RewardsNumber").update({Settings.state: value})
        session.commit()