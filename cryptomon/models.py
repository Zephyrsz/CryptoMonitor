from datetime import datetime
from config import db, ma


## columns columns = ['id','name','symbol','tag','date_added']
class CMCCrypotMeta(db.Model):
    __tablename__ = "CMCCrypotMeta"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    symbol = db.Column(db.String(50))
    tag = db.Column(db.String(5120))
    date_added = db.Column(db.DateTime)

class CMCCrypotMetaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CMCCrypotMeta
        load_instance = True

class CMCRank(db.Model):
    __tablename__ = "CMCRank"
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cmcid = db.Column(db.Integer)
    cmcrank = db.Column(db.Integer)
    symbol = db.Column(db.String(50))
    rank_date = db.Column(db.DateTime)

class CMCRankSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CMCRank
        load_instance = True


##columns
# class HistoryPrize(db.Model):
#     __tablename__ = "CMCRank"
#     tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id = db.Column(db.Integer)
#     rank = db.Column(db.Integer)
#     symbol = db.Column(db.String(50))
#     rank_date = db.Column(db.DateTime)
#
# class HistoryPrizeSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = HistoryPrize
#         load_instance = True