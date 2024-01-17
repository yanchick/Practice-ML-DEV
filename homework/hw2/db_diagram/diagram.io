Table User {
  id integer [primary key]
  username string
  hashed_password string
  name string
  surname string
}

Table Bill {
  id integer [primary key]
  User_id integer
  money number
}

Table PredictRow {
  id integer [primary key]
  age_group integer
  gender integer
  sport_days integer
  bmi float
  glucose float
  diabetes_degree float
  hemoglobin float
  insulin float
  result float
}

Ref: Bill.User_id - User.id // many-to-one

Ref: PredictRow.id < User.id
