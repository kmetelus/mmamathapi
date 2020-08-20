import py2neo.ogm

class Fighter(GraphObject):
  __primarykey__ = "name"

  name = Property()
  nickname = Property()
  has_beaten = RelatedTo(Fighter)