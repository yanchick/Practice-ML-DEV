CREATE TABLE "Users" (
  "id_user" SERIAL PRIMARY KEY,
  "created_at" timestamptz,
  "username" varchar(255) UNIQUE,
  "password_hash" varchar(255),
  "balance" NUMERIC
);

CREATE TABLE "Prediction" (
  "id_prediction" SERIAL PRIMARY KEY,
  "id_user" SERIAL REFERENCES "Users" ("id_user"),
  "model_used" varchar(255),
  "input_data" varchar(255),
  "output_data" varchar(255),
  "predicted_at" timestamptz,
  "price" NUMERIC,
  FOREIGN KEY ("id_user") REFERENCES "Users" ("id_user")
);

CREATE TABLE "Billing_updating" (
  "id_user" SERIAL REFERENCES "Users" ("id_user") PRIMARY KEY,
  "balance" NUMERIC,
  "updated_at" timestamptz,
  FOREIGN KEY ("id_user") REFERENCES "Users" ("id_user")
);

CREATE TABLE "Billing_history" (
  "operation_id" SERIAL PRIMARY KEY,
  "id_user" SERIAL REFERENCES "Users" ("id_user"),
  "balance_changed" NUMERIC,
  "operation_type" VARCHAR(10),
  "final_balance" NUMERIC,
  "changed_at" timestamptz,
  FOREIGN KEY ("id_user") REFERENCES "Users" ("id_user")
);