schema = """
type Query {
  hero(episode: Episode): Character
  droid(id: ID!): Droid
  version: String
}

type Character {
  name: String!
  appearsIn: [Episode!]!
}

type Droid {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  primaryFunction: String
}

enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}"""