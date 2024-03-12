schema = """
enum Episode { NEW_HOPE, EMPIRE, JEDI }

interface Character {
  id: String!
  name: String
  friends: [Character]
  appearsIn: [Episode]
}

type Human implements Character {
  id: String!
  name: String
  friends: [Character]
  appearsIn: [Episode]
  homePlanet: String
}

type Droid implements Character {
  id: String!
  name: String
  friends (first: Int, after: Int): [Character]
  appearsIn: [Episode]
  primaryFunction: String
}

type Query {
  version: String
  hero(episode: Episode): Character
  human(id: String!): Human
  droid(id: String!): Droid
}
"""
