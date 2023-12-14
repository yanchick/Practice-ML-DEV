CREATE TABLE "Users" (
  "id_user" INT GENERATED BY DEFAULT AS IDENTITY UNIQUE PRIMARY KEY,
  "created_at" timestamp,
  "username" varchar(255),
  "email" varchar(255),
  "password_hash" varchar(255),
  "updated_at" timestamp,
  "balance" FLOAT
);

CREATE TABLE "Billing_Accounts" (
  "id_user" int PRIMARY KEY,
  "update_at" timestamp,
  "balance" FLOAT
);

CREATE TABLE "Inference_server" (
  "id_user" int PRIMARY KEY,
  "created_at" timestamp,
  "update_at" timestamp,
  "current_port" int,
  "current_post" varchar
);

CREATE TABLE "Billing_history" (
  "id_user" int PRIMARY KEY,
  "id_billing" int,
  "balance_changed" FLOAT,
  "changed_at" timestamp
);

CREATE TABLE "Model_info" (
  "model_name" varchar PRIMARY KEY,
  "description" varchar,
  "model_file" varchar,
  "created_at" timestamp,
  "user_id" int,
  "status" varchar
);

CREATE TABLE "Prediction" (
  "id_user" int PRIMARY KEY,
  "created_at" timestamp,
  "model_used" varchar,
  "input_data" json,
  "output_data" json,
  "predicted_at" timestamp
);

COMMENT ON COLUMN "Users"."updated_at" IS 'When order created';

COMMENT ON COLUMN "Billing_Accounts"."update_at" IS 'When order created';

COMMENT ON COLUMN "Billing_history"."changed_at" IS 'When order created';

ALTER TABLE "Users" ADD FOREIGN KEY ("id_user") REFERENCES "Billing_Accounts" ("id_user");

ALTER TABLE "Users" ADD FOREIGN KEY ("id_user") REFERENCES "Billing_history" ("id_user");

ALTER TABLE "Billing_Accounts" ADD FOREIGN KEY ("id_user") REFERENCES "Billing_history" ("id_user");

ALTER TABLE "Inference_server" ADD FOREIGN KEY ("id_user") REFERENCES "Prediction" ("id_user");

ALTER TABLE "Inference_server" ADD FOREIGN KEY ("id_user") REFERENCES "Billing_Accounts" ("id_user");

ALTER TABLE "Model_info" ADD FOREIGN KEY ("model_name") REFERENCES "Prediction" ("model_used");

ALTER TABLE "Prediction" ADD FOREIGN KEY ("id_user") REFERENCES "Users" ("id_user");

ALTER TABLE "Users" ADD FOREIGN KEY ("updated_at") REFERENCES "Users" ("password_hash");