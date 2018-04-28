import sqlalchemy
from sqlalchemy.ext.orderinglist import ordering_list

from webpage.data.modelbase import SqlAlchemyBase

class Album(SqlAlchemyBase):
    __tablename__ = 'Album'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    url = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, index=True)
    album_image = sqlalchemy.Column(sqlalchemy.String)
    has_preview = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    #  One to many relationship with tracks
    tracks = sqlalchemy.orm.relationship('Track', back_populates='album',
                                         order_by='Track.display_order',
                                         collection_class=ordering_list('display_order'),
                                         cascade='all')

    #  order_by sets default order to display order in Tracks table
    #  collection_class, if something (track) is inserted to the object before it has been saved to the database,
    #  this will include that track in the order_by as well.
    #  The tracks should not exist without an album, if an album is deleted, the tracks should be deleted as well,
    #  cascade handle this.