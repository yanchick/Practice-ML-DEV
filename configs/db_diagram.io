// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table Users {
  id integer [primary key]
  name string
  email string
  password string
  balance int
}

Table Predictions {
  id integer [primary key]
  user_id integer
  model_id string
  prediction_date string
  is_success boolean
  is_finished boolean
  error_info string
  output float
}

Table Models {
  id integer [primary key]
  model_type string
  name string
  cost int
}


Ref: Users.id > Bills.user_id // many-to-one
Ref: Users.id > Predictions.user_id
Ref: Models.id > Predictions.model_id
