// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table Users {
  id integer [primary key]
  name string
  email string
  password string
}

Table Bills {
  id integer [primary key]
  user_id integer
  type string
  coins_diff integer
  description string
  time string
}

Table Predictions {
  id integer [primary key]
  user_id integer
  model_id string
  input_path string
  status string
  result float
}

Table Models {
  id integer [primary key]
  type string
  name string
  version int
  prediction_cost int
}


Ref: Users.id > Bills.user_id // many-to-one
Ref: Users.id > Predictions.user_id
Ref: Models.id > Predictions.model_id
