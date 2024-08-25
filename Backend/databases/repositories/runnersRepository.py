from databases.domains.runners import Runners
from sqlalchemy.orm import sessionmaker

class RunnersRepository:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        
    # GETTERS
    def getIdByNameAndSurname(self, session, name, surname):
        return session.query(Runners.id).filter(Runners.name == name, Runners.surname == surname).scalar()
    
    def getRewardInScratch(self, session, ranking, sex):
        return session.query(Runners.sex, Runners.ranking, Runners.name, Runners.surname, Runners.bib_number, Runners.time).filter(Runners.sex_ranking == ranking, Runners.sex == sex).first()
    
    def getRewardInCategoryM(self, session, category):
        return session.query(Runners.sex, Runners.ranking, Runners.name, Runners.surname, Runners.bib_number, Runners.time).filter(Runners.sex == "M", Runners.category == category, Runners.sex_ranking > 5 ).order_by(Runners.category_ranking).first()
    
    def getRewardInCategoryF(self, session, category):
        return session.query(Runners.sex, Runners.ranking, Runners.name, Runners.surname, Runners.bib_number, Runners.time).filter(Runners.sex == "F", Runners.category == category, Runners.sex_ranking > 3 ).order_by(Runners.category_ranking).first()
    
    def getFirstOriolM(self, session, bibNumberRewarded):
        return session.query(Runners.sex, Runners.ranking, Runners.name, Runners.surname, Runners.bib_number, Runners.time).filter(Runners.sex == "M", Runners.oriol == 1, Runners.bib_number.not_in(bibNumberRewarded)).order_by(Runners.sex_ranking).first()
    
    def getFirstOriolF(self, session, bibNumberRewarded):
        return session.query(Runners.sex, Runners.ranking, Runners.name, Runners.surname, Runners.bib_number, Runners.time).filter(Runners.sex == "F", Runners.oriol == 1, Runners.bib_number.not_in(bibNumberRewarded)).order_by(Runners.sex_ranking).first()
    
    # INSERT
    def insertRunner(self, session, name, surname, sex, ranking, category, category_ranking, sex_ranking, bib_number, time, oriol):
        newRunner = Runners(name=name, surname=surname, sex=sex, ranking=ranking, category=category, category_ranking=category_ranking, sex_ranking=sex_ranking, bib_number=bib_number, time=time, oriol=oriol)
        session.add(newRunner)
        session.commit()
        
    # UPDATE
    def updateRunner(self, session, id, name, surname, sex, ranking, category, category_ranking, sex_ranking, bib_number, time):
        session.query(Runners).filter(Runners.id == id).update({Runners.name: name, Runners.surname: surname, Runners.sex: sex, Runners.ranking: ranking, Runners.category: category, Runners.category_ranking: category_ranking, Runners.sex_ranking: sex_ranking, Runners.bib_number: bib_number, Runners.time: time})
        session.commit()
        
    # COUNT
    def count(self, session):
        return session.query(Runners).count()

    # DELETE
    def deleteAll(self, session):
        session.query(Runners).delete()
        session.commit()