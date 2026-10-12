--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

-- Started on 2024-01-25 13:12:44 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2483 (class 1262 OID 712803)
-- Name: employees; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE employees WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.UTF-8' LC_CTYPE = 'ru_RU.UTF-8';


\connect employees

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2484 (class 1262 OID 712803)
-- Dependencies: 2483
-- Name: DATABASE employees; Type: MAC LABEL; Schema: -; Owner: -
--

MAC LABEL ON DATABASE CURRENT_CATALOG IS '{2,0}';


--
-- TOC entry 2485 (class 1262 OID 712803)
-- Dependencies: 2483
-- Name: DATABASE employees; Type: MAC CCR; Schema: -; Owner: -
--

MAC CCR ON DATABASE CURRENT_CATALOG IS ON;


--
-- TOC entry 2487 (class 2615 OID 2200)
-- Dependencies: 3
-- Name: SCHEMA public; Type: MAC LABEL; Schema: -; Owner: -
--

MAC LABEL ON SCHEMA public IS '{2,0}';


--
-- TOC entry 2488 (class 2615 OID 2200)
-- Dependencies: 3
-- Name: SCHEMA public; Type: MAC CCR; Schema: -; Owner: -
--

MAC CCR ON SCHEMA public IS ON;


--
-- TOC entry 1 (class 3079 OID 12411)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2489 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 2490 (class 3079 OID 12411)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: MAC LABEL; Schema: pg_catalog; Owner: -
--

MAC LABEL ON EXTENSION plpgsql IS '{0,0}';


--
-- TOC entry 2491 (class 2612 OID 12415)
-- Dependencies: 759
-- Name: LANGUAGE plpgsql; Type: MAC LABEL; Schema: -; Owner: -
--

MAC LABEL ON LANGUAGE plpgsql IS '{0,0}';


--
-- TOC entry 185 (class 1259 OID 712804)
-- Name: !_Виды взысканий_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Виды взысканий_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2492 (class 1259 OID 712804)
-- Dependencies: 185
-- Name: SEQUENCE "!_Виды взысканий_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Виды взысканий_ID_seq" IS '{2,0}';


--
-- TOC entry 2493 (class 1259 OID 712804)
-- Dependencies: 185
-- Name: SEQUENCE "!_Виды взысканий_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Виды взысканий_ID_seq" IS ON;


SET default_with_oids = false;

--
-- TOC entry 186 (class 1259 OID 712806)
-- Name: !_Виды взысканий; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Виды взысканий" (
    "ID" integer DEFAULT nextval('public."!_Виды взысканий_ID_seq"'::regclass) NOT NULL,
    "Название" character varying(30)
)
WITH (MACS=FALSE);


--
-- TOC entry 2494 (class 1259 OID 712806)
-- Dependencies: 186
-- Name: TABLE "!_Виды взысканий"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Виды взысканий" IS '{2,0}';


--
-- TOC entry 2495 (class 1259 OID 712806)
-- Dependencies: 186
-- Name: TABLE "!_Виды взысканий"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Виды взысканий" IS ON;


--
-- TOC entry 187 (class 1259 OID 712810)
-- Name: !_Виды поощерений_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Виды поощерений_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2496 (class 1259 OID 712810)
-- Dependencies: 187
-- Name: SEQUENCE "!_Виды поощерений_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Виды поощерений_ID_seq" IS '{2,0}';


--
-- TOC entry 2497 (class 1259 OID 712810)
-- Dependencies: 187
-- Name: SEQUENCE "!_Виды поощерений_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Виды поощерений_ID_seq" IS ON;


--
-- TOC entry 188 (class 1259 OID 712812)
-- Name: !_Виды поощерений; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Виды поощерений" (
    "ID" integer DEFAULT nextval('public."!_Виды поощерений_ID_seq"'::regclass) NOT NULL,
    "Название" character varying(30)
)
WITH (MACS=FALSE);


--
-- TOC entry 2498 (class 1259 OID 712812)
-- Dependencies: 188
-- Name: TABLE "!_Виды поощерений"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Виды поощерений" IS '{2,0}';


--
-- TOC entry 2499 (class 1259 OID 712812)
-- Dependencies: 188
-- Name: TABLE "!_Виды поощерений"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Виды поощерений" IS ON;


--
-- TOC entry 189 (class 1259 OID 712816)
-- Name: _Воинские звания_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Воинские звания_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2500 (class 1259 OID 712816)
-- Dependencies: 189
-- Name: SEQUENCE "_Воинские звания_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Воинские звания_ID_seq" IS '{2,0}';


--
-- TOC entry 2501 (class 1259 OID 712816)
-- Dependencies: 189
-- Name: SEQUENCE "_Воинские звания_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Воинские звания_ID_seq" IS ON;


--
-- TOC entry 190 (class 1259 OID 712818)
-- Name: !_Воинские звания; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Воинские звания" (
    "ID" integer DEFAULT nextval('public."_Воинские звания_ID_seq"'::regclass) NOT NULL,
    "Звание полностью" character varying(30),
    "Звание сокращенно" character varying(20),
    "Категория" character varying(20),
    "Тип" character varying(20)
)
WITH (MACS=FALSE);


--
-- TOC entry 2502 (class 1259 OID 712818)
-- Dependencies: 190
-- Name: TABLE "!_Воинские звания"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Воинские звания" IS '{2,0}';


--
-- TOC entry 2503 (class 1259 OID 712818)
-- Dependencies: 190
-- Name: TABLE "!_Воинские звания"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Воинские звания" IS ON;


--
-- TOC entry 191 (class 1259 OID 712822)
-- Name: _Данные по войскам_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Данные по войскам_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2504 (class 1259 OID 712822)
-- Dependencies: 191
-- Name: SEQUENCE "_Данные по войскам_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Данные по войскам_ID_seq" IS '{2,0}';


--
-- TOC entry 2505 (class 1259 OID 712822)
-- Dependencies: 191
-- Name: SEQUENCE "_Данные по войскам_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Данные по войскам_ID_seq" IS ON;


--
-- TOC entry 192 (class 1259 OID 712824)
-- Name: !_Данные по войскам; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Данные по войскам" (
    "ID" integer DEFAULT nextval('public."_Данные по войскам_ID_seq"'::regclass) NOT NULL,
    "Условное наименование" character varying(100),
    "Действительное наименование" character varying(100),
    "Округ" character varying(100),
    "Адрес" character varying(100),
    "ID_Коефициент" integer,
    "Центр" boolean,
    "ЧНП" boolean,
    "Актуально" boolean DEFAULT true
)
WITH (MACS=FALSE);


--
-- TOC entry 2506 (class 1259 OID 712824)
-- Dependencies: 192
-- Name: TABLE "!_Данные по войскам"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Данные по войскам" IS '{2,0}';


--
-- TOC entry 2507 (class 1259 OID 712824)
-- Dependencies: 192
-- Name: TABLE "!_Данные по войскам"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Данные по войскам" IS ON;


--
-- TOC entry 193 (class 1259 OID 712831)
-- Name: !_Награды_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Награды_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2508 (class 1259 OID 712831)
-- Dependencies: 193
-- Name: SEQUENCE "!_Награды_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Награды_ID_seq" IS '{2,0}';


--
-- TOC entry 2509 (class 1259 OID 712831)
-- Dependencies: 193
-- Name: SEQUENCE "!_Награды_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Награды_ID_seq" IS ON;


--
-- TOC entry 194 (class 1259 OID 712833)
-- Name: !_Награды; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Награды" (
    "ID" integer DEFAULT nextval('public."!_Награды_ID_seq"'::regclass) NOT NULL,
    "Название" character varying(30)
)
WITH (MACS=FALSE);


--
-- TOC entry 2510 (class 1259 OID 712833)
-- Dependencies: 194
-- Name: TABLE "!_Награды"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Награды" IS '{2,0}';


--
-- TOC entry 2511 (class 1259 OID 712833)
-- Dependencies: 194
-- Name: TABLE "!_Награды"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Награды" IS ON;


--
-- TOC entry 195 (class 1259 OID 712837)
-- Name: !_ОШС_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_ОШС_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2512 (class 1259 OID 712837)
-- Dependencies: 195
-- Name: SEQUENCE "!_ОШС_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_ОШС_ID_seq" IS '{2,0}';


--
-- TOC entry 2513 (class 1259 OID 712837)
-- Dependencies: 195
-- Name: SEQUENCE "!_ОШС_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_ОШС_ID_seq" IS ON;


--
-- TOC entry 196 (class 1259 OID 712839)
-- Name: !_ОШС; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_ОШС" (
    "ID" integer DEFAULT nextval('public."!_ОШС_ID_seq"'::regclass) NOT NULL,
    "ID_подразделения" integer,
    "Название должности" character varying(50),
    "Название сокращенно" character varying(20),
    "ВУС" character varying(10),
    "Тарифный разряд" integer,
    "Штатная категория (ID_взв)" integer
)
WITH (MACS=FALSE);


--
-- TOC entry 2514 (class 1259 OID 712839)
-- Dependencies: 196
-- Name: TABLE "!_ОШС"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_ОШС" IS '{2,0}';


--
-- TOC entry 2515 (class 1259 OID 712839)
-- Dependencies: 196
-- Name: TABLE "!_ОШС"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_ОШС" IS ON;


--
-- TOC entry 197 (class 1259 OID 712843)
-- Name: !_Подразделения_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Подразделения_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2516 (class 1259 OID 712843)
-- Dependencies: 197
-- Name: SEQUENCE "!_Подразделения_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Подразделения_ID_seq" IS '{2,0}';


--
-- TOC entry 2517 (class 1259 OID 712843)
-- Dependencies: 197
-- Name: SEQUENCE "!_Подразделения_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Подразделения_ID_seq" IS ON;


--
-- TOC entry 198 (class 1259 OID 712845)
-- Name: !_Подразделения; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Подразделения" (
    "ID" integer DEFAULT nextval('public."!_Подразделения_ID_seq"'::regclass) NOT NULL,
    "ID_вч" integer,
    "Наименование" character varying(100),
    "ПЗГТ" boolean,
    "ШР" boolean,
    "Наименование сокращенно" character varying(20)
)
WITH (MACS=FALSE);


--
-- TOC entry 2518 (class 1259 OID 712845)
-- Dependencies: 198
-- Name: TABLE "!_Подразделения"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Подразделения" IS '{2,0}';


--
-- TOC entry 2519 (class 1259 OID 712845)
-- Dependencies: 198
-- Name: TABLE "!_Подразделения"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Подразделения" IS ON;


--
-- TOC entry 199 (class 1259 OID 712849)
-- Name: !_Семейное положение; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Семейное положение" (
    "ID" integer NOT NULL,
    "Семейное положение" character varying(50),
    "Пол" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2520 (class 1259 OID 712849)
-- Dependencies: 199
-- Name: TABLE "!_Семейное положение"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Семейное положение" IS '{2,0}';


--
-- TOC entry 2521 (class 1259 OID 712849)
-- Dependencies: 199
-- Name: TABLE "!_Семейное положение"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Семейное положение" IS ON;


--
-- TOC entry 200 (class 1259 OID 712852)
-- Name: !_Семейное положение_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Семейное положение_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2522 (class 0 OID 0)
-- Dependencies: 200
-- Name: !_Семейное положение_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."!_Семейное положение_ID_seq" OWNED BY public."!_Семейное положение"."ID";


--
-- TOC entry 2523 (class 1259 OID 712852)
-- Dependencies: 200
-- Name: SEQUENCE "!_Семейное положение_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Семейное положение_ID_seq" IS '{2,0}';


--
-- TOC entry 2524 (class 1259 OID 712852)
-- Dependencies: 200
-- Name: SEQUENCE "!_Семейное положение_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Семейное положение_ID_seq" IS ON;


--
-- TOC entry 201 (class 1259 OID 712854)
-- Name: !_Специальности_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Специальности_ID_seq"
    START WITH 100002
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2525 (class 1259 OID 712854)
-- Dependencies: 201
-- Name: SEQUENCE "!_Специальности_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Специальности_ID_seq" IS '{2,0}';


--
-- TOC entry 2526 (class 1259 OID 712854)
-- Dependencies: 201
-- Name: SEQUENCE "!_Специальности_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Специальности_ID_seq" IS ON;


--
-- TOC entry 202 (class 1259 OID 712856)
-- Name: !_Специальности; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Специальности" (
    "ID" integer DEFAULT nextval('public."!_Специальности_ID_seq"'::regclass) NOT NULL,
    "ID_ВУЗа" integer,
    "Специальность" character varying(150),
    "Квалификация" character varying(100),
    "Тип образования" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2527 (class 1259 OID 712856)
-- Dependencies: 202
-- Name: TABLE "!_Специальности"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Специальности" IS '{2,0}';


--
-- TOC entry 2528 (class 1259 OID 712856)
-- Dependencies: 202
-- Name: TABLE "!_Специальности"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Специальности" IS ON;


--
-- TOC entry 203 (class 1259 OID 712860)
-- Name: !_Сроки контрактов_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Сроки контрактов_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2529 (class 1259 OID 712860)
-- Dependencies: 203
-- Name: SEQUENCE "!_Сроки контрактов_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Сроки контрактов_ID_seq" IS '{2,0}';


--
-- TOC entry 2530 (class 1259 OID 712860)
-- Dependencies: 203
-- Name: SEQUENCE "!_Сроки контрактов_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Сроки контрактов_ID_seq" IS ON;


--
-- TOC entry 204 (class 1259 OID 712862)
-- Name: !_Сроки контрактов; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Сроки контрактов" (
    "ID" integer DEFAULT nextval('public."!_Сроки контрактов_ID_seq"'::regclass) NOT NULL,
    "Наименование" character varying(50),
    "Количество лет" integer
)
WITH (MACS=FALSE);


--
-- TOC entry 2531 (class 1259 OID 712862)
-- Dependencies: 204
-- Name: TABLE "!_Сроки контрактов"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Сроки контрактов" IS '{2,0}';


--
-- TOC entry 2532 (class 1259 OID 712862)
-- Dependencies: 204
-- Name: TABLE "!_Сроки контрактов"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Сроки контрактов" IS ON;


--
-- TOC entry 205 (class 1259 OID 712866)
-- Name: _Типы коэффициентов_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Типы коэффициентов_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2533 (class 1259 OID 712866)
-- Dependencies: 205
-- Name: SEQUENCE "_Типы коэффициентов_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Типы коэффициентов_ID_seq" IS '{2,0}';


--
-- TOC entry 2534 (class 1259 OID 712866)
-- Dependencies: 205
-- Name: SEQUENCE "_Типы коэффициентов_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Типы коэффициентов_ID_seq" IS ON;


--
-- TOC entry 206 (class 1259 OID 712868)
-- Name: !_Типы коэффициентов; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Типы коэффициентов" (
    "ID" integer DEFAULT nextval('public."_Типы коэффициентов_ID_seq"'::regclass) NOT NULL,
    "Множитель" real,
    "Наименование" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2535 (class 1259 OID 712868)
-- Dependencies: 206
-- Name: TABLE "!_Типы коэффициентов"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Типы коэффициентов" IS '{2,0}';


--
-- TOC entry 2536 (class 1259 OID 712868)
-- Dependencies: 206
-- Name: TABLE "!_Типы коэффициентов"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Типы коэффициентов" IS ON;


--
-- TOC entry 207 (class 1259 OID 712872)
-- Name: !_Участки ЗРА; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Участки ЗРА" (
    "ID" integer NOT NULL,
    "Страна" character varying(50),
    "Город" character varying(50),
    "Росзагранпредставительство" character varying(50),
    "ID_коэффициент" integer
)
WITH (MACS=FALSE);


--
-- TOC entry 2537 (class 1259 OID 712872)
-- Dependencies: 207
-- Name: TABLE "!_Участки ЗРА"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Участки ЗРА" IS '{2,0}';


--
-- TOC entry 2538 (class 1259 OID 712872)
-- Dependencies: 207
-- Name: TABLE "!_Участки ЗРА"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Участки ЗРА" IS ON;


--
-- TOC entry 208 (class 1259 OID 712875)
-- Name: !_Участки ЗРА_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Участки ЗРА_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2539 (class 0 OID 0)
-- Dependencies: 208
-- Name: !_Участки ЗРА_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."!_Участки ЗРА_ID_seq" OWNED BY public."!_Участки ЗРА"."ID";


--
-- TOC entry 2540 (class 1259 OID 712875)
-- Dependencies: 208
-- Name: SEQUENCE "!_Участки ЗРА_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Участки ЗРА_ID_seq" IS '{2,0}';


--
-- TOC entry 2541 (class 1259 OID 712875)
-- Dependencies: 208
-- Name: SEQUENCE "!_Участки ЗРА_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Участки ЗРА_ID_seq" IS ON;


--
-- TOC entry 209 (class 1259 OID 712877)
-- Name: !_Учебные заведения_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."!_Учебные заведения_ID_seq"
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2542 (class 1259 OID 712877)
-- Dependencies: 209
-- Name: SEQUENCE "!_Учебные заведения_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."!_Учебные заведения_ID_seq" IS '{2,0}';


--
-- TOC entry 2543 (class 1259 OID 712877)
-- Dependencies: 209
-- Name: SEQUENCE "!_Учебные заведения_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."!_Учебные заведения_ID_seq" IS ON;


--
-- TOC entry 210 (class 1259 OID 712879)
-- Name: !_Учебные заведения; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."!_Учебные заведения" (
    "ID" integer DEFAULT nextval('public."!_Учебные заведения_ID_seq"'::regclass) NOT NULL,
    "Название" character varying(70),
    "Название сокращенно" character varying(20),
    "Адрес" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2544 (class 1259 OID 712879)
-- Dependencies: 210
-- Name: TABLE "!_Учебные заведения"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."!_Учебные заведения" IS '{2,0}';


--
-- TOC entry 2545 (class 1259 OID 712879)
-- Dependencies: 210
-- Name: TABLE "!_Учебные заведения"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."!_Учебные заведения" IS ON;


--
-- TOC entry 211 (class 1259 OID 712883)
-- Name: _Адреса_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Адреса_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2546 (class 1259 OID 712883)
-- Dependencies: 211
-- Name: SEQUENCE "_Адреса_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Адреса_ID_seq" IS '{2,0}';


--
-- TOC entry 2547 (class 1259 OID 712883)
-- Dependencies: 211
-- Name: SEQUENCE "_Адреса_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Адреса_ID_seq" IS ON;


--
-- TOC entry 212 (class 1259 OID 712885)
-- Name: _Адреса; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Адреса" (
    "ID" integer DEFAULT nextval('public."_Адреса_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Тип адреса" character varying(30),
    "Область" character varying(70),
    "Населенный пункт" character varying(70),
    "Улица" character varying(70),
    "Дом" character varying(10),
    "Квартира" character varying(10),
    "Телефон" character varying(20)
)
WITH (MACS=FALSE);


--
-- TOC entry 2548 (class 1259 OID 712885)
-- Dependencies: 212
-- Name: TABLE "_Адреса"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Адреса" IS '{2,0}';


--
-- TOC entry 2549 (class 1259 OID 712885)
-- Dependencies: 212
-- Name: TABLE "_Адреса"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Адреса" IS ON;


--
-- TOC entry 246 (class 1259 OID 742424)
-- Name: _Аттестация; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Аттестация" (
    "ID" integer NOT NULL,
    "Личный номер" character varying(30),
    "Дата проведения" date,
    "Номер протокола" character varying(30),
    "Кем утвержден" character varying(50),
    "Дата утверждения" date,
    "Выводы" character varying(300)
)
WITH (MACS=FALSE);


--
-- TOC entry 2550 (class 1259 OID 742424)
-- Dependencies: 246
-- Name: TABLE "_Аттестация"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Аттестация" IS '{0,0}';


--
-- TOC entry 2551 (class 1259 OID 742424)
-- Dependencies: 246
-- Name: TABLE "_Аттестация"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Аттестация" IS ON;


--
-- TOC entry 245 (class 1259 OID 742422)
-- Name: _Аттестация_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Аттестация_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2552 (class 0 OID 0)
-- Dependencies: 245
-- Name: _Аттестация_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_Аттестация_ID_seq" OWNED BY public."_Аттестация"."ID";


--
-- TOC entry 2553 (class 1259 OID 742422)
-- Dependencies: 245
-- Name: SEQUENCE "_Аттестация_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Аттестация_ID_seq" IS '{0,0}';


--
-- TOC entry 2554 (class 1259 OID 742422)
-- Dependencies: 245
-- Name: SEQUENCE "_Аттестация_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Аттестация_ID_seq" IS ON;


--
-- TOC entry 213 (class 1259 OID 712889)
-- Name: _БД_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_БД_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2555 (class 1259 OID 712889)
-- Dependencies: 213
-- Name: SEQUENCE "_БД_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_БД_ID_seq" IS '{2,0}';


--
-- TOC entry 2556 (class 1259 OID 712889)
-- Dependencies: 213
-- Name: SEQUENCE "_БД_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_БД_ID_seq" IS ON;


--
-- TOC entry 214 (class 1259 OID 712891)
-- Name: _БД; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_БД" (
    "ID" integer DEFAULT nextval('public."_БД_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Район БД" character varying(30),
    "Дата прибытия" date,
    "Дата убытия" date,
    "Номер льготного удостоверения" character varying(30)
)
WITH (MACS=FALSE);


--
-- TOC entry 2557 (class 1259 OID 712891)
-- Dependencies: 214
-- Name: TABLE "_БД"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_БД" IS '{2,0}';


--
-- TOC entry 2558 (class 1259 OID 712891)
-- Dependencies: 214
-- Name: TABLE "_БД"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_БД" IS ON;


--
-- TOC entry 215 (class 1259 OID 712895)
-- Name: _Взыскания_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Взыскания_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2559 (class 1259 OID 712895)
-- Dependencies: 215
-- Name: SEQUENCE "_Взыскания_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Взыскания_ID_seq" IS '{2,0}';


--
-- TOC entry 2560 (class 1259 OID 712895)
-- Dependencies: 215
-- Name: SEQUENCE "_Взыскания_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Взыскания_ID_seq" IS ON;


--
-- TOC entry 216 (class 1259 OID 712897)
-- Name: _Взыскания; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Взыскания" (
    "ID" integer DEFAULT nextval('public."_Взыскания_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "ID_Взыскания" integer,
    "Дата обьявления" date,
    "Приказ" character varying(50),
    "Дата приказа" date,
    "Дата снятия" date,
    "Кем снято" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2561 (class 1259 OID 712897)
-- Dependencies: 216
-- Name: TABLE "_Взыскания"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Взыскания" IS '{2,0}';


--
-- TOC entry 2562 (class 1259 OID 712897)
-- Dependencies: 216
-- Name: TABLE "_Взыскания"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Взыскания" IS ON;


--
-- TOC entry 217 (class 1259 OID 712901)
-- Name: _Документы_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Документы_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2563 (class 1259 OID 712901)
-- Dependencies: 217
-- Name: SEQUENCE "_Документы_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Документы_ID_seq" IS '{2,0}';


--
-- TOC entry 2564 (class 1259 OID 712901)
-- Dependencies: 217
-- Name: SEQUENCE "_Документы_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Документы_ID_seq" IS ON;


--
-- TOC entry 218 (class 1259 OID 712903)
-- Name: _Документы; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Документы" (
    "ID" integer DEFAULT nextval('public."_Документы_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Тип документа" character varying(50),
    "Серия" character varying(20),
    "Номер" character varying(20),
    "Кем выдан" character varying(70),
    "Дата выдачи" date
)
WITH (MACS=FALSE);


--
-- TOC entry 2565 (class 1259 OID 712903)
-- Dependencies: 218
-- Name: TABLE "_Документы"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Документы" IS '{2,0}';


--
-- TOC entry 2566 (class 1259 OID 712903)
-- Dependencies: 218
-- Name: TABLE "_Документы"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Документы" IS ON;


--
-- TOC entry 219 (class 1259 OID 712907)
-- Name: _Допуска; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Допуска" (
    "ID" integer NOT NULL,
    "Личный номер" character varying(20),
    "Номер допуска" character varying(30),
    "Дата выдачи" date,
    "Кем выдан" character varying(70)
)
WITH (MACS=FALSE);


--
-- TOC entry 2567 (class 1259 OID 712907)
-- Dependencies: 219
-- Name: TABLE "_Допуска"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Допуска" IS '{2,0}';


--
-- TOC entry 2568 (class 1259 OID 712907)
-- Dependencies: 219
-- Name: TABLE "_Допуска"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Допуска" IS ON;


--
-- TOC entry 220 (class 1259 OID 712910)
-- Name: _Допуска_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Допуска_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2569 (class 0 OID 0)
-- Dependencies: 220
-- Name: _Допуска_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_Допуска_ID_seq" OWNED BY public."_Допуска"."ID";


--
-- TOC entry 2570 (class 1259 OID 712910)
-- Dependencies: 220
-- Name: SEQUENCE "_Допуска_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Допуска_ID_seq" IS '{2,0}';


--
-- TOC entry 2571 (class 1259 OID 712910)
-- Dependencies: 220
-- Name: SEQUENCE "_Допуска_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Допуска_ID_seq" IS ON;


--
-- TOC entry 221 (class 1259 OID 712912)
-- Name: _Классность_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Классность_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2572 (class 1259 OID 712912)
-- Dependencies: 221
-- Name: SEQUENCE "_Классность_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Классность_ID_seq" IS '{2,0}';


--
-- TOC entry 2573 (class 1259 OID 712912)
-- Dependencies: 221
-- Name: SEQUENCE "_Классность_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Классность_ID_seq" IS ON;


--
-- TOC entry 222 (class 1259 OID 712914)
-- Name: _Классность; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Классность" (
    "ID" integer DEFAULT nextval('public."_Классность_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Классность" character varying(30),
    "Приказ" character varying(50),
    "Дата приказа" date
)
WITH (MACS=FALSE);


--
-- TOC entry 2574 (class 1259 OID 712914)
-- Dependencies: 222
-- Name: TABLE "_Классность"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Классность" IS '{2,0}';


--
-- TOC entry 2575 (class 1259 OID 712914)
-- Dependencies: 222
-- Name: TABLE "_Классность"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Классность" IS ON;


--
-- TOC entry 223 (class 1259 OID 712918)
-- Name: _Контракты_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Контракты_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2576 (class 1259 OID 712918)
-- Dependencies: 223
-- Name: SEQUENCE "_Контракты_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Контракты_ID_seq" IS '{2,0}';


--
-- TOC entry 2577 (class 1259 OID 712918)
-- Dependencies: 223
-- Name: SEQUENCE "_Контракты_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Контракты_ID_seq" IS ON;


--
-- TOC entry 224 (class 1259 OID 712920)
-- Name: _Контракты; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Контракты" (
    "ID" integer DEFAULT nextval('public."_Контракты_ID_seq"'::regclass) NOT NULL,
    "Приказ" character varying(20),
    "Дата приказа" date,
    "С какого числа" date,
    "ID_срок" integer,
    "Личный номер" character varying(20)
)
WITH (MACS=FALSE);


--
-- TOC entry 2578 (class 1259 OID 712920)
-- Dependencies: 224
-- Name: TABLE "_Контракты"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Контракты" IS '{2,0}';


--
-- TOC entry 2579 (class 1259 OID 712920)
-- Dependencies: 224
-- Name: TABLE "_Контракты"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Контракты" IS ON;


--
-- TOC entry 225 (class 1259 OID 712924)
-- Name: _Награждения_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Награждения_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2580 (class 1259 OID 712924)
-- Dependencies: 225
-- Name: SEQUENCE "_Награждения_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Награждения_ID_seq" IS '{2,0}';


--
-- TOC entry 2581 (class 1259 OID 712924)
-- Dependencies: 225
-- Name: SEQUENCE "_Награждения_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Награждения_ID_seq" IS ON;


--
-- TOC entry 226 (class 1259 OID 712926)
-- Name: _Награждения; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Награждения" (
    "ID" integer DEFAULT nextval('public."_Награждения_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "ID_Награды" integer,
    "Приказ" character varying(50),
    "Дата приказа" date
)
WITH (MACS=FALSE);


--
-- TOC entry 2582 (class 1259 OID 712926)
-- Dependencies: 226
-- Name: TABLE "_Награждения"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Награждения" IS '{2,0}';


--
-- TOC entry 2583 (class 1259 OID 712926)
-- Dependencies: 226
-- Name: TABLE "_Награждения"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Награждения" IS ON;


--
-- TOC entry 227 (class 1259 OID 712930)
-- Name: _Образования_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Образования_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2584 (class 1259 OID 712930)
-- Dependencies: 227
-- Name: SEQUENCE "_Образования_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Образования_ID_seq" IS '{2,0}';


--
-- TOC entry 2585 (class 1259 OID 712930)
-- Dependencies: 227
-- Name: SEQUENCE "_Образования_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Образования_ID_seq" IS ON;


--
-- TOC entry 228 (class 1259 OID 712932)
-- Name: _Образования; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Образования" (
    "ID" integer DEFAULT nextval('public."_Образования_ID_seq"'::regclass) NOT NULL,
    "ID_специальности" integer,
    "Дата окончания" date,
    "Диплом с отличаем" boolean,
    "Золотая медаль" boolean,
    "Примечание" character varying(50),
    "Личный номер" character varying(20),
    "Особые отметки" integer DEFAULT 0
)
WITH (MACS=FALSE);


--
-- TOC entry 2586 (class 1259 OID 712932)
-- Dependencies: 228
-- Name: TABLE "_Образования"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Образования" IS '{2,0}';


--
-- TOC entry 2587 (class 1259 OID 712932)
-- Dependencies: 228
-- Name: TABLE "_Образования"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Образования" IS ON;


--
-- TOC entry 229 (class 1259 OID 712937)
-- Name: _Поощерения_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Поощерения_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2588 (class 1259 OID 712937)
-- Dependencies: 229
-- Name: SEQUENCE "_Поощерения_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Поощерения_ID_seq" IS '{2,0}';


--
-- TOC entry 2589 (class 1259 OID 712937)
-- Dependencies: 229
-- Name: SEQUENCE "_Поощерения_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Поощерения_ID_seq" IS ON;


--
-- TOC entry 230 (class 1259 OID 712939)
-- Name: _Поощерения; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Поощерения" (
    "ID" integer DEFAULT nextval('public."_Поощерения_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "ID_Поощерения" integer,
    "Дата обьявления" date,
    "Приказ" character varying(50),
    "Дата приказа" date
)
WITH (MACS=FALSE);


--
-- TOC entry 2590 (class 1259 OID 712939)
-- Dependencies: 230
-- Name: TABLE "_Поощерения"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Поощерения" IS '{2,0}';


--
-- TOC entry 2591 (class 1259 OID 712939)
-- Dependencies: 230
-- Name: TABLE "_Поощерения"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Поощерения" IS ON;


--
-- TOC entry 231 (class 1259 OID 712943)
-- Name: _Посещение ЗРА; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Посещение ЗРА" (
    "ID" integer NOT NULL,
    "ID_Участок" integer,
    "Личный номер" character varying(20),
    "Должность" character varying(50),
    "Цель пребывания" character varying(100),
    "Дата убытия" date,
    "Дата возвращения" date
)
WITH (MACS=FALSE);


--
-- TOC entry 2592 (class 1259 OID 712943)
-- Dependencies: 231
-- Name: TABLE "_Посещение ЗРА"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Посещение ЗРА" IS '{2,0}';


--
-- TOC entry 2593 (class 1259 OID 712943)
-- Dependencies: 231
-- Name: TABLE "_Посещение ЗРА"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Посещение ЗРА" IS ON;


--
-- TOC entry 232 (class 1259 OID 712946)
-- Name: _Посещение ЗРА_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Посещение ЗРА_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2594 (class 0 OID 0)
-- Dependencies: 232
-- Name: _Посещение ЗРА_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_Посещение ЗРА_ID_seq" OWNED BY public."_Посещение ЗРА"."ID";


--
-- TOC entry 2595 (class 1259 OID 712946)
-- Dependencies: 232
-- Name: SEQUENCE "_Посещение ЗРА_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Посещение ЗРА_ID_seq" IS '{2,0}';


--
-- TOC entry 2596 (class 1259 OID 712946)
-- Dependencies: 232
-- Name: SEQUENCE "_Посещение ЗРА_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Посещение ЗРА_ID_seq" IS ON;


--
-- TOC entry 233 (class 1259 OID 712948)
-- Name: _Присвоения воинских званий_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Присвоения воинских званий_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2597 (class 1259 OID 712948)
-- Dependencies: 233
-- Name: SEQUENCE "_Присвоения воинских званий_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Присвоения воинских званий_ID_seq" IS '{2,0}';


--
-- TOC entry 2598 (class 1259 OID 712948)
-- Dependencies: 233
-- Name: SEQUENCE "_Присвоения воинских званий_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Присвоения воинских званий_ID_seq" IS ON;


--
-- TOC entry 234 (class 1259 OID 712950)
-- Name: _Присвоения воинских званий; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Присвоения воинских званий" (
    "ID" integer DEFAULT nextval('public."_Присвоения воинских званий_ID_seq"'::regclass) NOT NULL,
    "ID_зв" integer,
    "Дата присвоения" date,
    "Приказ" character varying(20),
    "Дата приказа" date,
    "Личный номер" character varying(20),
    "Примечание" character varying(256)
)
WITH (MACS=FALSE);


--
-- TOC entry 2599 (class 1259 OID 712950)
-- Dependencies: 234
-- Name: TABLE "_Присвоения воинских званий"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Присвоения воинских званий" IS '{2,0}';


--
-- TOC entry 2600 (class 1259 OID 712950)
-- Dependencies: 234
-- Name: TABLE "_Присвоения воинских званий"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Присвоения воинских званий" IS ON;


--
-- TOC entry 235 (class 1259 OID 712954)
-- Name: _Прохождение службы_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Прохождение службы_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2601 (class 1259 OID 712954)
-- Dependencies: 235
-- Name: SEQUENCE "_Прохождение службы_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Прохождение службы_ID_seq" IS '{2,0}';


--
-- TOC entry 2602 (class 1259 OID 712954)
-- Dependencies: 235
-- Name: SEQUENCE "_Прохождение службы_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Прохождение службы_ID_seq" IS ON;


--
-- TOC entry 236 (class 1259 OID 712956)
-- Name: _Прохождение службы; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Прохождение службы" (
    "ID" integer DEFAULT nextval('public."_Прохождение службы_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Приказ" character varying(20),
    "Дата приказа" date,
    "ID_должности" integer,
    "Примечание" character varying(100)
)
WITH (MACS=FALSE);


--
-- TOC entry 2603 (class 1259 OID 712956)
-- Dependencies: 236
-- Name: TABLE "_Прохождение службы"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Прохождение службы" IS '{2,0}';


--
-- TOC entry 2604 (class 1259 OID 712956)
-- Dependencies: 236
-- Name: TABLE "_Прохождение службы"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Прохождение службы" IS ON;


--
-- TOC entry 248 (class 1259 OID 742443)
-- Name: _СПФО; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_СПФО" (
    "ID" integer NOT NULL,
    "Личный номер" character varying(30),
    "Место проведения" character varying(50),
    "Дата проведения" date,
    "Примечание" character varying(200)
)
WITH (MACS=FALSE);


--
-- TOC entry 2605 (class 1259 OID 742443)
-- Dependencies: 248
-- Name: TABLE "_СПФО"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_СПФО" IS '{0,0}';


--
-- TOC entry 2606 (class 1259 OID 742443)
-- Dependencies: 248
-- Name: TABLE "_СПФО"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_СПФО" IS ON;


--
-- TOC entry 247 (class 1259 OID 742441)
-- Name: _СПФО_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_СПФО_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2607 (class 0 OID 0)
-- Dependencies: 247
-- Name: _СПФО_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_СПФО_ID_seq" OWNED BY public."_СПФО"."ID";


--
-- TOC entry 2608 (class 1259 OID 742441)
-- Dependencies: 247
-- Name: SEQUENCE "_СПФО_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_СПФО_ID_seq" IS '{0,0}';


--
-- TOC entry 2609 (class 1259 OID 742441)
-- Dependencies: 247
-- Name: SEQUENCE "_СПФО_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_СПФО_ID_seq" IS ON;


--
-- TOC entry 250 (class 1259 OID 742509)
-- Name: _Сдачи; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Сдачи" (
    "ID" integer NOT NULL,
    "Наименование" character varying(50),
    "1_М" character varying(200),
    "2_М" character varying(200),
    "3_М" character varying(150),
    "4_М" character varying(150),
    "5_М" character varying(150),
    "6_М" character varying(150),
    "7_М" character varying(150),
    "8_М" character varying(150),
    "1_Ж" character varying(150),
    "2_Ж" character varying(150),
    "3_Ж" character varying(150),
    "4_Ж" character varying(150),
    "5_Ж" character varying(150),
    "6_Ж" character varying(150)
)
WITH (MACS=FALSE);


--
-- TOC entry 2610 (class 1259 OID 742509)
-- Dependencies: 250
-- Name: TABLE "_Сдачи"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Сдачи" IS '{0,0}';


--
-- TOC entry 2611 (class 1259 OID 742509)
-- Dependencies: 250
-- Name: TABLE "_Сдачи"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Сдачи" IS ON;


--
-- TOC entry 249 (class 1259 OID 742507)
-- Name: _Сдачи_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Сдачи_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2612 (class 0 OID 0)
-- Dependencies: 249
-- Name: _Сдачи_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_Сдачи_ID_seq" OWNED BY public."_Сдачи"."ID";


--
-- TOC entry 2613 (class 1259 OID 742507)
-- Dependencies: 249
-- Name: SEQUENCE "_Сдачи_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Сдачи_ID_seq" IS '{0,0}';


--
-- TOC entry 2614 (class 1259 OID 742507)
-- Dependencies: 249
-- Name: SEQUENCE "_Сдачи_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Сдачи_ID_seq" IS ON;


--
-- TOC entry 244 (class 1259 OID 742411)
-- Name: _Увольнение; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Увольнение" (
    "Личный номер" character varying(30),
    "Приказ" character varying(30),
    "Причина увольнения" character varying(50),
    "Примечание" character varying(100),
    "ID" integer NOT NULL
)
WITH (MACS=FALSE);


--
-- TOC entry 2615 (class 1259 OID 742411)
-- Dependencies: 244
-- Name: TABLE "_Увольнение"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Увольнение" IS '{0,0}';


--
-- TOC entry 2616 (class 1259 OID 742411)
-- Dependencies: 244
-- Name: TABLE "_Увольнение"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Увольнение" IS ON;


--
-- TOC entry 243 (class 1259 OID 742409)
-- Name: _Увольнение_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Увольнение_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2617 (class 0 OID 0)
-- Dependencies: 243
-- Name: _Увольнение_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."_Увольнение_ID_seq" OWNED BY public."_Увольнение"."ID";


--
-- TOC entry 2618 (class 1259 OID 742409)
-- Dependencies: 243
-- Name: SEQUENCE "_Увольнение_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Увольнение_ID_seq" IS '{0,0}';


--
-- TOC entry 2619 (class 1259 OID 742409)
-- Dependencies: 243
-- Name: SEQUENCE "_Увольнение_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Увольнение_ID_seq" IS ON;


--
-- TOC entry 237 (class 1259 OID 712960)
-- Name: _Члены семьи_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_Члены семьи_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2620 (class 1259 OID 712960)
-- Dependencies: 237
-- Name: SEQUENCE "_Члены семьи_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_Члены семьи_ID_seq" IS '{2,0}';


--
-- TOC entry 2621 (class 1259 OID 712960)
-- Dependencies: 237
-- Name: SEQUENCE "_Члены семьи_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_Члены семьи_ID_seq" IS ON;


--
-- TOC entry 238 (class 1259 OID 712962)
-- Name: _Члены семьи; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_Члены семьи" (
    "ID" integer DEFAULT nextval('public."_Члены семьи_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Степень родства" character varying(70),
    "Дата рождения" date,
    "Фамилия" character varying(70),
    "Имя" character varying(50),
    "Отчество" character varying(50)
)
WITH (MACS=FALSE);


--
-- TOC entry 2622 (class 1259 OID 712962)
-- Dependencies: 238
-- Name: TABLE "_Члены семьи"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_Члены семьи" IS '{2,0}';


--
-- TOC entry 2623 (class 1259 OID 712962)
-- Dependencies: 238
-- Name: TABLE "_Члены семьи"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_Члены семьи" IS ON;


--
-- TOC entry 239 (class 1259 OID 712966)
-- Name: _ШР_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."_ШР_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2624 (class 1259 OID 712966)
-- Dependencies: 239
-- Name: SEQUENCE "_ШР_ID_seq"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON SEQUENCE public."_ШР_ID_seq" IS '{2,0}';


--
-- TOC entry 2625 (class 1259 OID 712966)
-- Dependencies: 239
-- Name: SEQUENCE "_ШР_ID_seq"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON SEQUENCE public."_ШР_ID_seq" IS ON;


--
-- TOC entry 240 (class 1259 OID 712968)
-- Name: _ШР; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ШР" (
    "ID" integer DEFAULT nextval('public."_ШР_ID_seq"'::regclass) NOT NULL,
    "Личный номер" character varying(20),
    "Дата допуска" date,
    "Документ" character varying(70)
)
WITH (MACS=FALSE);


--
-- TOC entry 2626 (class 1259 OID 712968)
-- Dependencies: 240
-- Name: TABLE "_ШР"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."_ШР" IS '{2,0}';


--
-- TOC entry 2627 (class 1259 OID 712968)
-- Dependencies: 240
-- Name: TABLE "_ШР"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."_ШР" IS ON;


--
-- TOC entry 241 (class 1259 OID 712972)
-- Name: Сотрудники; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Сотрудники" (
    "Личный номер" character varying(50) NOT NULL,
    "Фамилия" character varying(50),
    "Имя" character varying(50),
    "Отчество" character varying(50),
    "Дата рождения" timestamp with time zone,
    "Место рождения" character varying(255),
    "Национальность" character varying(50),
    "Номер спецдела" character varying(10),
    "Номер личного дела в УК" character varying(10),
    "Пол" character varying(50),
    "Фотография" bytea,
    "Сотовый телефон" character varying(50),
    "Семейное положение" character varying(50) DEFAULT 1,
    "Центр" boolean,
    "Действующий" boolean,
    CONSTRAINT "Личный номер - Только русский алфавит" CHECK ((("Личный номер")::text ~ similar_escape('[А-ЯЁ]%'::text, NULL::text)))
)
WITH (MACS=FALSE);


--
-- TOC entry 2628 (class 1259 OID 712972)
-- Dependencies: 241
-- Name: TABLE "Сотрудники"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."Сотрудники" IS '{2,0}';


--
-- TOC entry 2629 (class 1259 OID 712972)
-- Dependencies: 241
-- Name: TABLE "Сотрудники"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."Сотрудники" IS ON;


--
-- TOC entry 242 (class 1259 OID 712980)
-- Name: Учетные записи; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Учетные записи" (
    "Учетная запись" character varying(20) NOT NULL,
    "Личный номер" character varying(20)
)
WITH (MACS=FALSE);


--
-- TOC entry 2630 (class 1259 OID 712980)
-- Dependencies: 242
-- Name: TABLE "Учетные записи"; Type: MAC LABEL; Schema: public; Owner: -
--

MAC LABEL ON TABLE public."Учетные записи" IS '{2,0}';


--
-- TOC entry 2631 (class 1259 OID 712980)
-- Dependencies: 242
-- Name: TABLE "Учетные записи"; Type: MAC CCR; Schema: public; Owner: -
--

MAC CCR ON TABLE public."Учетные записи" IS ON;


--
-- TOC entry 2232 (class 2604 OID 742142)
-- Name: !_Семейное положение ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Семейное положение" ALTER COLUMN "ID" SET DEFAULT nextval('public."!_Семейное положение_ID_seq"'::regclass);


--
-- TOC entry 2236 (class 2604 OID 742143)
-- Name: !_Участки ЗРА ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Участки ЗРА" ALTER COLUMN "ID" SET DEFAULT nextval('public."!_Участки ЗРА_ID_seq"'::regclass);


--
-- TOC entry 2257 (class 2604 OID 742427)
-- Name: _Аттестация ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Аттестация" ALTER COLUMN "ID" SET DEFAULT nextval('public."_Аттестация_ID_seq"'::regclass);


--
-- TOC entry 2242 (class 2604 OID 742144)
-- Name: _Допуска ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Допуска" ALTER COLUMN "ID" SET DEFAULT nextval('public."_Допуска_ID_seq"'::regclass);


--
-- TOC entry 2249 (class 2604 OID 742145)
-- Name: _Посещение ЗРА ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Посещение ЗРА" ALTER COLUMN "ID" SET DEFAULT nextval('public."_Посещение ЗРА_ID_seq"'::regclass);


--
-- TOC entry 2258 (class 2604 OID 742446)
-- Name: _СПФО ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_СПФО" ALTER COLUMN "ID" SET DEFAULT nextval('public."_СПФО_ID_seq"'::regclass);


--
-- TOC entry 2259 (class 2604 OID 742512)
-- Name: _Сдачи ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Сдачи" ALTER COLUMN "ID" SET DEFAULT nextval('public."_Сдачи_ID_seq"'::regclass);


--
-- TOC entry 2256 (class 2604 OID 742414)
-- Name: _Увольнение ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Увольнение" ALTER COLUMN "ID" SET DEFAULT nextval('public."_Увольнение_ID_seq"'::regclass);


--
-- TOC entry 2323 (class 2606 OID 742429)
-- Name: _Аттестация ID; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Аттестация"
    ADD CONSTRAINT "ID" PRIMARY KEY ("ID");


--
-- TOC entry 2261 (class 2606 OID 712988)
-- Name: !_Виды взысканий ID!_Виды взысканий; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Виды взысканий"
    ADD CONSTRAINT "ID!_Виды взысканий" PRIMARY KEY ("ID");


--
-- TOC entry 2263 (class 2606 OID 712990)
-- Name: !_Виды поощерений ID!_Виды поощерений; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Виды поощерений"
    ADD CONSTRAINT "ID!_Виды поощерений" PRIMARY KEY ("ID");


--
-- TOC entry 2287 (class 2606 OID 712992)
-- Name: _Адреса ID_Адреса; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Адреса"
    ADD CONSTRAINT "ID_Адреса" PRIMARY KEY ("ID");


--
-- TOC entry 2289 (class 2606 OID 712994)
-- Name: _БД ID_БД; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_БД"
    ADD CONSTRAINT "ID_БД" PRIMARY KEY ("ID");


--
-- TOC entry 2285 (class 2606 OID 712996)
-- Name: !_Учебные заведения ID_ВУЗа; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Учебные заведения"
    ADD CONSTRAINT "ID_ВУЗа" PRIMARY KEY ("ID");


--
-- TOC entry 2291 (class 2606 OID 712998)
-- Name: _Взыскания ID_Взыскания; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Взыскания"
    ADD CONSTRAINT "ID_Взыскания" PRIMARY KEY ("ID");


--
-- TOC entry 2293 (class 2606 OID 713000)
-- Name: _Документы ID_Документы; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Документы"
    ADD CONSTRAINT "ID_Документы" PRIMARY KEY ("ID");


--
-- TOC entry 2283 (class 2606 OID 713002)
-- Name: !_Участки ЗРА ID_ЗРА; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Участки ЗРА"
    ADD CONSTRAINT "ID_ЗРА" PRIMARY KEY ("ID");


--
-- TOC entry 2307 (class 2606 OID 713004)
-- Name: _Посещение ЗРА ID_К; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Посещение ЗРА"
    ADD CONSTRAINT "ID_К" PRIMARY KEY ("ID");


--
-- TOC entry 2297 (class 2606 OID 713006)
-- Name: _Классность ID_Классность; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Классность"
    ADD CONSTRAINT "ID_Классность" PRIMARY KEY ("ID");


--
-- TOC entry 2269 (class 2606 OID 713008)
-- Name: !_Награды ID_Награды; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Награды"
    ADD CONSTRAINT "ID_Награды" PRIMARY KEY ("ID");


--
-- TOC entry 2301 (class 2606 OID 713010)
-- Name: _Награждения ID_Награждения; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Награждения"
    ADD CONSTRAINT "ID_Награждения" PRIMARY KEY ("ID");


--
-- TOC entry 2305 (class 2606 OID 713012)
-- Name: _Поощерения ID_Поощерения; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Поощерения"
    ADD CONSTRAINT "ID_Поощерения" PRIMARY KEY ("ID");


--
-- TOC entry 2325 (class 2606 OID 742448)
-- Name: _СПФО ID_СПФО; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_СПФО"
    ADD CONSTRAINT "ID_СПФО" PRIMARY KEY ("ID");


--
-- TOC entry 2327 (class 2606 OID 742517)
-- Name: _Сдачи ID_Сдача; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Сдачи"
    ADD CONSTRAINT "ID_Сдача" PRIMARY KEY ("ID");


--
-- TOC entry 2275 (class 2606 OID 713014)
-- Name: !_Семейное положение ID_Семейное положение; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Семейное положение"
    ADD CONSTRAINT "ID_Семейное положение" PRIMARY KEY ("ID");


--
-- TOC entry 2321 (class 2606 OID 742416)
-- Name: _Увольнение ID_Увольнения; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Увольнение"
    ADD CONSTRAINT "ID_Увольнения" PRIMARY KEY ("ID");


--
-- TOC entry 2319 (class 2606 OID 713016)
-- Name: Учетные записи ID_Учетная запись; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Учетные записи"
    ADD CONSTRAINT "ID_Учетная запись" PRIMARY KEY ("Учетная запись");


--
-- TOC entry 2313 (class 2606 OID 713018)
-- Name: _Члены семьи ID_Члены семьи; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Члены семьи"
    ADD CONSTRAINT "ID_Члены семьи" PRIMARY KEY ("ID");


--
-- TOC entry 2315 (class 2606 OID 713020)
-- Name: _ШР ID_ШР; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ШР"
    ADD CONSTRAINT "ID_ШР" PRIMARY KEY ("ID");


--
-- TOC entry 2281 (class 2606 OID 713022)
-- Name: !_Типы коэффициентов ID_вид_коэф; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Типы коэффициентов"
    ADD CONSTRAINT "ID_вид_коэф" PRIMARY KEY ("ID");


--
-- TOC entry 2267 (class 2606 OID 713024)
-- Name: !_Данные по войскам ID_войска; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Данные по войскам"
    ADD CONSTRAINT "ID_войска" PRIMARY KEY ("ID");


--
-- TOC entry 2271 (class 2606 OID 713026)
-- Name: !_ОШС ID_должности; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_ОШС"
    ADD CONSTRAINT "ID_должности" PRIMARY KEY ("ID");


--
-- TOC entry 2295 (class 2606 OID 713028)
-- Name: _Допуска ID_допуска; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Допуска"
    ADD CONSTRAINT "ID_допуска" PRIMARY KEY ("ID");


--
-- TOC entry 2265 (class 2606 OID 713030)
-- Name: !_Воинские звания ID_звания; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Воинские звания"
    ADD CONSTRAINT "ID_звания" PRIMARY KEY ("ID");


--
-- TOC entry 2299 (class 2606 OID 713032)
-- Name: _Контракты ID_контракт; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Контракты"
    ADD CONSTRAINT "ID_контракт" PRIMARY KEY ("ID");


--
-- TOC entry 2303 (class 2606 OID 713034)
-- Name: _Образования ID_образования; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Образования"
    ADD CONSTRAINT "ID_образования" PRIMARY KEY ("ID");


--
-- TOC entry 2273 (class 2606 OID 713036)
-- Name: !_Подразделения ID_подразделения; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Подразделения"
    ADD CONSTRAINT "ID_подразделения" PRIMARY KEY ("ID");


--
-- TOC entry 2309 (class 2606 OID 713038)
-- Name: _Присвоения воинских званий ID_присвоения_званий; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Присвоения воинских званий"
    ADD CONSTRAINT "ID_присвоения_званий" PRIMARY KEY ("ID");


--
-- TOC entry 2311 (class 2606 OID 713040)
-- Name: _Прохождение службы ID_прохождение_службы; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Прохождение службы"
    ADD CONSTRAINT "ID_прохождение_службы" PRIMARY KEY ("ID");


--
-- TOC entry 2277 (class 2606 OID 713042)
-- Name: !_Специальности ID_специальности; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Специальности"
    ADD CONSTRAINT "ID_специальности" PRIMARY KEY ("ID");


--
-- TOC entry 2279 (class 2606 OID 713044)
-- Name: !_Сроки контрактов ID_сроки_контрактов; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Сроки контрактов"
    ADD CONSTRAINT "ID_сроки_контрактов" PRIMARY KEY ("ID");


--
-- TOC entry 2329 (class 2606 OID 742519)
-- Name: _Сдачи Uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Сдачи"
    ADD CONSTRAINT "Uniq" UNIQUE ("Наименование");


--
-- TOC entry 2317 (class 2606 OID 713046)
-- Name: Сотрудники Сотрудники_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Сотрудники"
    ADD CONSTRAINT "Сотрудники_pkey" PRIMARY KEY ("Личный номер");


--
-- TOC entry 2350 (class 2606 OID 713047)
-- Name: _Посещение ЗРА ID_Участок; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Посещение ЗРА"
    ADD CONSTRAINT "ID_Участок" FOREIGN KEY ("ID_Участок") REFERENCES public."!_Участки ЗРА"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2335 (class 2606 OID 713052)
-- Name: !_Участки ЗРА ID_коэф; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Участки ЗРА"
    ADD CONSTRAINT "ID_коэф" FOREIGN KEY ("ID_коэффициент") REFERENCES public."!_Типы коэффициентов"("ID") ON UPDATE CASCADE;


--
-- TOC entry 2334 (class 2606 OID 713057)
-- Name: !_Специальности ВУЗ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Специальности"
    ADD CONSTRAINT "ВУЗ" FOREIGN KEY ("ID_ВУЗа") REFERENCES public."!_Учебные заведения"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2333 (class 2606 OID 713062)
-- Name: !_Подразделения Воинская часть; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Подразделения"
    ADD CONSTRAINT "Воинская часть" FOREIGN KEY ("ID_вч") REFERENCES public."!_Данные по войскам"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2354 (class 2606 OID 713067)
-- Name: _Прохождение службы Должность; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Прохождение службы"
    ADD CONSTRAINT "Должность" FOREIGN KEY ("ID_должности") REFERENCES public."!_ОШС"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2352 (class 2606 OID 713072)
-- Name: _Присвоения воинских званий Звание; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Присвоения воинских званий"
    ADD CONSTRAINT "Звание" FOREIGN KEY ("ID_зв") REFERENCES public."!_Воинские звания"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2330 (class 2606 OID 713077)
-- Name: !_Данные по войскам Коефициент; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_Данные по войскам"
    ADD CONSTRAINT "Коефициент" FOREIGN KEY ("ID_Коефициент") REFERENCES public."!_Типы коэффициентов"("ID") ON DELETE CASCADE;


--
-- TOC entry 2336 (class 2606 OID 713082)
-- Name: _Адреса Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Адреса"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2337 (class 2606 OID 713087)
-- Name: _БД Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_БД"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2338 (class 2606 OID 713092)
-- Name: _Документы Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Документы"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2339 (class 2606 OID 713097)
-- Name: _Допуска Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Допуска"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2340 (class 2606 OID 713102)
-- Name: _Классность Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Классность"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2342 (class 2606 OID 713107)
-- Name: _Контракты Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Контракты"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2344 (class 2606 OID 713112)
-- Name: _Награждения Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Награждения"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2346 (class 2606 OID 713117)
-- Name: _Образования Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Образования"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2348 (class 2606 OID 713122)
-- Name: _Поощерения Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Поощерения"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2351 (class 2606 OID 713127)
-- Name: _Присвоения воинских званий Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Присвоения воинских званий"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2353 (class 2606 OID 713132)
-- Name: _Прохождение службы Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Прохождение службы"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2355 (class 2606 OID 713137)
-- Name: _Члены семьи Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Члены семьи"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2356 (class 2606 OID 713142)
-- Name: _ШР Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ШР"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2349 (class 2606 OID 713147)
-- Name: _Посещение ЗРА Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Посещение ЗРА"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2357 (class 2606 OID 713152)
-- Name: Учетные записи Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Учетные записи"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2358 (class 2606 OID 742417)
-- Name: _Увольнение Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Увольнение"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2359 (class 2606 OID 742430)
-- Name: _Аттестация Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Аттестация"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2360 (class 2606 OID 742449)
-- Name: _СПФО Личный номер; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_СПФО"
    ADD CONSTRAINT "Личный номер" FOREIGN KEY ("Личный номер") REFERENCES public."Сотрудники"("Личный номер") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2343 (class 2606 OID 713157)
-- Name: _Награждения Награда; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Награждения"
    ADD CONSTRAINT "Награда" FOREIGN KEY ("ID_Награды") REFERENCES public."!_Награды"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2332 (class 2606 OID 713162)
-- Name: !_ОШС Подразделение; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_ОШС"
    ADD CONSTRAINT "Подразделение" FOREIGN KEY ("ID_подразделения") REFERENCES public."!_Подразделения"("ID") ON DELETE CASCADE;


--
-- TOC entry 2347 (class 2606 OID 713167)
-- Name: _Поощерения Поощерение; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Поощерения"
    ADD CONSTRAINT "Поощерение" FOREIGN KEY ("ID_Поощерения") REFERENCES public."!_Виды поощерений"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2345 (class 2606 OID 713172)
-- Name: _Образования Специальность; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Образования"
    ADD CONSTRAINT "Специальность" FOREIGN KEY ("ID_специальности") REFERENCES public."!_Специальности"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2341 (class 2606 OID 713177)
-- Name: _Контракты Сроки контракта; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_Контракты"
    ADD CONSTRAINT "Сроки контракта" FOREIGN KEY ("ID_срок") REFERENCES public."!_Сроки контрактов"("ID") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 2331 (class 2606 OID 713182)
-- Name: !_ОШС Штатная категория; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."!_ОШС"
    ADD CONSTRAINT "Штатная категория" FOREIGN KEY ("Штатная категория (ID_взв)") REFERENCES public."!_Воинские звания"("ID") ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-01-25 13:12:44 MSK

--
-- PostgreSQL database dump complete
--

