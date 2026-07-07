-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.


CREATE TABLE public.students (
  is_laptop boolean NOT NULL DEFAULT false,
  regno bigint NOT NULL UNIQUE,
  name text NOT NULL,
  branch text NOT NULL,
  reminder_time timestamp without time zone,
  password text,
  email text,
  is_admin boolean NOT NULL DEFAULT false,
  box_no bigint,
  preferred_box bigint,
  CONSTRAINT students_pkey PRIMARY KEY (regno)
);
CREATE TABLE public.entries (
  regno bigint NOT NULL,
  box_no bigint,
  out_time timestamp with time zone,
  in_time timestamp with time zone NOT NULL DEFAULT now(),
  session_id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  branch text NOT NULL,
  name text,
  CONSTRAINT entries_pkey PRIMARY KEY (session_id),
  CONSTRAINT entries_regno_fkey FOREIGN KEY (regno) REFERENCES public.students(regno)
);
CREATE TABLE public.boxes (
  room_no smallint,
  name text,
  is_laptop boolean NOT NULL DEFAULT false,
  regno bigint NOT NULL DEFAULT '1'::bigint,
  box_no integer NOT NULL,
  id integer NOT NULL,
  x_coordinate bigint,
  y_coordinate bigint,
  CONSTRAINT boxes_pkey PRIMARY KEY (id)
);