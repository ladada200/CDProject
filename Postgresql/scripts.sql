-- Create user table first and primarily.

GRANT CONNECT ON DATABASE retrievr TO retrievr;

-- VIEWS

-- TBR
drop trigger if exists chk_usr on private.auth_users;
drop trigger if exists chk_song on public.song;
drop trigger if exists chk_album on public.album;
drop trigger if exists chk_artist on public.artist;

drop trigger if exists chk_usr_upd on private.auth_users;
drop trigger if exists chk_song_upd on public.song;
drop trigger if exists chk_album_upd on public.album;
drop trigger if exists chk_artist_upd on public.artist;
drop trigger if exists chk_usr_ins on private.auth_users;
drop trigger if exists chk_song_ins on public.song;
drop trigger if exists chk_album_ins on public.album;
drop trigger if exists chk_artist_ins on public.artist;


drop function if exists private.update_write();
drop function if exists public.update_write();
drop function if exists private.update_create();
drop function if exists public.update_create();

DROP TABLE IF EXISTS public.song,
					 public.album,
					 public.artist,
					 public.streams;

DROP TABLE IF EXISTS private.auth_users;

drop extension if exists "uuid-ossp";

DROP SCHEMA IF EXISTS public;
DROP SCHEMA IF EXISTS private;


CREATE SCHEMA public;
CREATE SCHEMA private;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

GRANT USAGE ON SCHEMA public TO retrievr;
GRANT USAGE ON SCHEMA private TO retrievr;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO retrievr;
GRANT SELECT, INSERT, update, DELETE ON ALL TABLES IN SCHEMA private TO retrievr;

--- function

CREATE OR REPLACE FUNCTION public.song_total_listens(songid uuid)
 RETURNS TABLE(song_id uuid, unique_streams integer, the_total_listens integer)
 LANGUAGE plpgsql
AS $function$
	begin
		return query select song_uuid as song_id,
			   count(*)::integer as unique_streams,
			   sum("total_listens")::integer as the_total_listens
		  FROM public.streams
		 WHERE song_uuid = songid
		group by song_uuid;
	end;
	$function$
;

-- select public.song_total_listens('5dd4aef3-695e-4734-b225-ac27ffce8b39'::uuid); -- for testing

create or replace function public.update_write() 
	returns trigger as $$
	begin 
		new.write_date := now();
		return new;
	end;
	$$ language plpgsql volatile;

create or replace function private.update_write() 
	returns trigger as $$
	begin 
		new.write_date := now();
		return new;
	end;
	$$ language plpgsql volatile;

create or replace function public.update_create() 
	returns trigger as $$
	begin 
		new.write_date := now();
		new.create_date := now();
		return new;
	end;
	$$ language plpgsql volatile;

create or replace function private.update_create() 
	returns trigger as $$
	begin 
		new.write_date := now();
		new.create_date := now();
		return new;
	end;
	$$ language plpgsql volatile;

CREATE TABLE private.auth_users (
	id serial NOT NULL,
	uuid uuid NOT null default uuid_generate_v4(),
	login varchar NOT NULL,
    email varchar NOT NULL,
	"password" varchar NOT NULL,
	lastactive timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	active boolean NULL DEFAULT False,
	accepted_invite bool NULL DEFAULT False,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT user_uuid_pk PRIMARY KEY (uuid)
);
CREATE INDEX user_id_idx ON private.auth_users (id);
grant all on sequence private.auth_users_id_seq to retrievr;

create trigger chk_usr_upd
	before UPDATE of login, email, "password", active, accepted_invite, lastactive
	on private.auth_users
	for each row 
	execute procedure update_write();

create trigger chk_usr_ins
	before INSERT
	on private.auth_users
	for each row 
	execute procedure update_create();

-- Column comments

COMMENT ON COLUMN private.auth_users.uuid IS 'primary';

-- Create artist table for artists.

CREATE TABLE public.artist (
	uuid uuid NOT null default uuid_generate_v4(),
	"name" varchar NOT NULL,
	create_uid uuid NOT NULL,
    active boolean NOT NULL DEFAULT True,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT artist_pk PRIMARY KEY (uuid),
	CONSTRAINT artist_create_uid_fk FOREIGN KEY (create_uid) REFERENCES private.auth_users(uuid),
	CONSTRAINT artist_write_uid_fk FOREIGN KEY (write_uid) REFERENCES private.auth_users(uuid)
);
CREATE INDEX artist_uuid_idx ON public.artist (uuid);
CREATE INDEX artist_name_idx ON public.artist ("name");

create trigger chk_artist_upd
	before UPDATE of "name", active
	on public.artist
	for each row 
	execute procedure update_write();

create trigger chk_artist_ins
	before INSERT
	on public.artist
	for each row 
	execute procedure update_create();

-- Column comments

COMMENT ON COLUMN public.artist.name IS 'Artist''s Name';
COMMENT ON COLUMN public.artist.create_uid IS 'Created by';

CREATE TABLE public.album (
	uuid uuid NOT null DEFAULT uuid_generate_v4(),
	active bool NULL DEFAULT true,
	album_artist uuid NOT NULL,
	create_uid uuid NOT NULL,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"name" varchar NOT NULL,
    CONSTRAINT album_pk PRIMARY KEY (uuid),
	CONSTRAINT album_artist_fk FOREIGN KEY (album_artist) REFERENCES public.artist(uuid),
	CONSTRAINT album_create_uid_fk FOREIGN KEY (create_uid) REFERENCES private.auth_users(uuid),
	CONSTRAINT album_write_uid_fk FOREIGN KEY (write_uid) REFERENCES private.auth_users(uuid)
);
CREATE INDEX album_uuid_idx ON public.album (uuid);
CREATE INDEX album_name_idx ON public.album ("name");

create trigger chk_album_upd
	before UPDATE of active, album_artist, "name"
	on public.album
	for each row 
	execute procedure update_write();

create trigger chk_album_ins
	before INSERT
	on public.album
	for each row 
	execute procedure update_create();


CREATE TABLE public.song (
	uuid uuid NOT null default uuid_generate_v4(),
	"name" varchar NOT NULL,
	artist uuid NOT NULL,
	album uuid NULL,
	"data" bytea NOT null,
	"length" integer NOT NULL,
	release_date date NULL,
	favorites integer NOT NULL DEFAULT 0,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	create_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	CONSTRAINT song_pk PRIMARY KEY (uuid),
	CONSTRAINT song_create_uid_fk FOREIGN KEY (create_uid) REFERENCES private.auth_users(uuid),
	CONSTRAINT song_write_uid_fk FOREIGN KEY (write_uid) REFERENCES private.auth_users(uuid),
	CONSTRAINT song_artist_fk FOREIGN KEY (artist) REFERENCES public.artist(uuid),
	CONSTRAINT song_album_fk FOREIGN KEY (album) REFERENCES public.album(uuid) ON DELETE SET NULL
);
CREATE INDEX song_uuid_idx ON public.song (uuid);
CREATE INDEX song_artist_idx ON public.song (artist);
CREATE INDEX song_album_idx ON public.song (album);
COMMENT ON TABLE public.song IS 'currently this is a list of all songs for the db';

create trigger chk_song_upd
	before UPDATE of "name", artist, album, "data", "length", release_date, favorites
	on public.song
	for each row 
	execute procedure update_write();

create trigger chk_song_ins
	before INSERT
	on public.song
	for each row 
	execute procedure update_create();

-- Column comments

COMMENT ON COLUMN public.song.album IS 'songs can be created without an album';

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.album, public.artist, public.song TO retrievr;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE private.auth_users TO retrievr;
grant all on sequence public.album_id_seq to retrievr;
grant all on sequence public.artist_id_seq to retrievr;
grant all on sequence public.song_id_seq to retrievr;


CREATE TABLE public.streams (
	id serial NOT NULL,
	user_uuid uuid NOT NULL,
	song_uuid uuid NOT NULL,
	total_listens int NOT NULL DEFAULT 1,
	CONSTRAINT pk_streams_user_uuid PRIMARY KEY (id),
	CONSTRAINT fk_streams_user_uuid FOREIGN KEY (user_uuid) REFERENCES private.auth_users(uuid),
	CONSTRAINT fk_streams_song_uuid FOREIGN KEY (song_uuid) REFERENCES public.song(uuid)
);

GRANT SELECT, UPDATE, INSERT ON TABLE public.streams TO retrievr;


-- Views

DROP VIEW IF EXISTS public.artist_songs;
CREATE OR REPLACE VIEW public.artist_songs AS
	SELECT t1."name" AS "song_name", 
		   t3."name" AS "album_name"
	  FROM public.song t1
	  JOIN public.artist t2 ON t1.artist = t2.uuid
	  JOIN public.album t3 ON t1.album = t3.uuid;