-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.boxes (
  box_no bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  is_laptop boolean NOT NULL DEFAULT false,
  regno bigint,
  name text,
  x_coordinate bigint,
  y_coordinate bigint,
  CONSTRAINT boxes_pkey PRIMARY KEY (box_no),
  CONSTRAINT boxes_regno_fkey FOREIGN KEY (regno) REFERENCES public.students(regno)
);
CREATE TABLE public.entries (
  session_id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  regno bigint NOT NULL,
  box_no bigint,
  in_time timestamp with time zone NOT NULL DEFAULT now(),
  out_time timestamp with time zone,
  branch text NOT NULL,
  name text,
  CONSTRAINT entries_pkey PRIMARY KEY (session_id),
  CONSTRAINT entries_regno_fkey FOREIGN KEY (regno) REFERENCES public.students(regno)
);
CREATE TABLE public.students (
  regno bigint NOT NULL UNIQUE,
  name text NOT NULL,
  branch text NOT NULL,
  password text,
  email text,
  is_admin boolean NOT NULL DEFAULT false,
  is_checkedin boolean NOT NULL DEFAULT false,
  box_no bigint,
  is_laptop boolean NOT NULL DEFAULT false,
  preferred_box bigint,
  CONSTRAINT students_pkey PRIMARY KEY (regno)
);
