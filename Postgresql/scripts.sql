-- Create user table first and primarily.

CREATE TABLE public."user" (
	id serial NOT NULL,
	uuid uuid NOT NULL,
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
CREATE INDEX user_id_idx ON public."user" (id);
CREATE INDEX user_uuid_idx ON public."user" (uuid);

-- Column comments

COMMENT ON COLUMN public."user".uuid IS 'primary';

-- Create artist table for artists.

CREATE TABLE public.artist (
	id serial NOT NULL,
	uuid uuid NOT NULL,
	name varchar NOT NULL,
	create_uid uuid NOT NULL,
    active boolean NULL DEFAULT True,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT artist_pk PRIMARY KEY (uuid),
	CONSTRAINT artist_create_uid_fk FOREIGN KEY (create_uid) REFERENCES public."user"(uuid),
	CONSTRAINT artist_write_uid_fk FOREIGN KEY (write_uid) REFERENCES public."user"(uuid)
);
CREATE INDEX artist_uuid_idx ON public.artist (uuid);
CREATE INDEX artist_name_idx ON public.artist (name);

-- Column comments

COMMENT ON COLUMN public.artist.name IS 'Artist''s Name';
COMMENT ON COLUMN public.artist.create_uid IS 'Created by';

CREATE TABLE public.album (
	id serial NOT NULL,
	uuid uuid NOT NULL,
	active bool NULL DEFAULT true,
	album_artist uuid NOT NULL,
	create_uid uuid NOT NULL,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"name" varchar NOT NULL,
    CONSTRAINT album_pk PRIMARY KEY (uuid),
	CONSTRAINT album_artist_fk FOREIGN KEY (album_artist) REFERENCES public.artist(uuid),
	CONSTRAINT album_create_uid_fk FOREIGN KEY (create_uid) REFERENCES public."user"(uuid),
	CONSTRAINT album_write_uid_fk FOREIGN KEY (write_uid) REFERENCES public."user"(uuid)
);
CREATE INDEX album_uuid_idx ON public.album (uuid);
CREATE INDEX album_name_idx ON public.album ("name");


CREATE TABLE public.song (
	id serial NOT NULL,
	uuid uuid NOT NULL,
	"name" varchar NOT NULL,
	artist uuid NOT NULL,
	album uuid NULL,
	"data" bytea NOT NULL
	length integer NOT NULL,
	release_date date NULL,
	favorites integer NOT NULL DEFAULT 0,
	create_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	create_uid uuid NOT NULL,
	write_date timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
	write_uid uuid NOT NULL,
	CONSTRAINT song_pk PRIMARY KEY (uuid),
	CONSTRAINT song_create_uid_fk FOREIGN KEY (create_uid) REFERENCES public."user"(uuid),
	CONSTRAINT song_write_uid_fk FOREIGN KEY (write_uid) REFERENCES public."user"(uuid),
	CONSTRAINT song_artist_fk FOREIGN KEY (artist) REFERENCES public.artist(uuid),
	CONSTRAINT song_album_fk FOREIGN KEY (album) REFERENCES public.album(uuid)
);
CREATE INDEX song_uuid_idx ON public.song (uuid);
CREATE INDEX song_artist_idx ON public.song (artist);
CREATE INDEX song_album_idx ON public.song (album);
COMMENT ON TABLE public.song IS 'currently this is a list of all songs for the db';

-- Column comments

COMMENT ON COLUMN public.song.album IS 'songs can be created without an album';

GRANT SELECT ON TABLE public.album TO retrievr;
GRANT UPDATE ON TABLE public.album TO retrievr;
GRANT INSERT ON TABLE public.album TO retrievr;
GRANT SELECT ON TABLE public.artist TO retrievr;
GRANT INSERT ON TABLE public.artist TO retrievr;
GRANT UPDATE ON TABLE public.artist TO retrievr;
GRANT SELECT ON TABLE public.song TO retrievr;
GRANT INSERT ON TABLE public.song TO retrievr;
GRANT UPDATE ON TABLE public.song TO retrievr;
GRANT SELECT ON TABLE public."user" TO retrievr;
GRANT INSERT ON TABLE public."user" TO retrievr;
GRANT UPDATE ON TABLE public."user" TO retrievr;
