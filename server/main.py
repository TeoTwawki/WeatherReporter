from flask import Flask, request
import sqlite3
import hashlib
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

get_data = []


def update_get_data():
    connection = sqlite3.connect("db.sqlite", isolation_level=None)
    cursor = connection.cursor()

    print("Updating get_data")

    results = []
    cursor.execute("""
        SELECT zone_names.name, weather_names.name, DATETIME(weather_data.timestamp, 'unixepoch'), SUBSTR(weather_data.submitter, 0, 5)
        FROM weather_data
        LEFT JOIN zone_names on zone_names.zone = weather_data.zone
        LEFT JOIN weather_names on weather_names.weather = weather_data.weather
        ORDER BY weather_data.timestamp DESC
        LIMIT 10
    """)
    for entry in cursor.fetchall():
        results.append(entry)

    global get_data
    get_data = results

    cursor.close()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_get_data, trigger="interval", seconds=60)
scheduler.start()


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def execute(query):
    connection = sqlite3.connect("db.sqlite", isolation_level=None)
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()


def insert_weather(zone, weather, timestamp, submitter):
    execute(f"INSERT INTO weather_data VALUES ({zone}, {weather}, {timestamp}, '{submitter}')")


def insert_static_data():
    connection = sqlite3.connect("db.sqlite", isolation_level=None)
    cursor = connection.cursor()

    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (0, 'NONE')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (1, 'SUNSHINE')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (2, 'CLOUDS')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (3, 'FOG')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (4, 'HOT_SPELL')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (5, 'HEAT_WAVE')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (6, 'RAIN')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (7, 'SQUALL')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (8, 'DUST_STORM')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (9, 'SAND_STORM')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (10, 'WIND')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (11, 'GALES')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (12, 'SNOW')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (13, 'BLIZZARDS')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (14, 'THUNDER')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (15, 'THUNDERSTORMS')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (16, 'AURORAS')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (17, 'STELLAR_GLARE')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (18, 'GLOOM')")
    cursor.execute("INSERT OR REPLACE INTO weather_names VALUES (19, 'DARKNESS')")

    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (1, 'PHANAUET_CHANNEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (2, 'CARPENTERS_LANDING')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (3, 'MANACLIPPER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (4, 'BIBIKI_BAY')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (5, 'ULEGUERAND_RANGE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (6, 'BEARCLAW_PINNACLE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (7, 'ATTOHWA_CHASM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (8, 'BONEYARD_GULLY')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (9, 'PSOXJA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (10, 'THE_SHROUDED_MAW')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (11, 'OLDTON_MOVALPOLOS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (12, 'NEWTON_MOVALPOLOS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (13, 'MINE_SHAFT_2716')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (14, 'HALL_OF_TRANSFERENCE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (15, 'ABYSSEA_KONSCHTAT')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (16, 'PROMYVION_HOLLA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (17, 'SPIRE_OF_HOLLA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (18, 'PROMYVION_DEM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (19, 'SPIRE_OF_DEM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (20, 'PROMYVION_MEA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (21, 'SPIRE_OF_MEA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (22, 'PROMYVION_VAHZL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (23, 'SPIRE_OF_VAHZL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (24, 'LUFAISE_MEADOWS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (25, 'MISAREAUX_COAST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (26, 'TAVNAZIAN_SAFEHOLD')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (27, 'PHOMIUNA_AQUEDUCTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (28, 'SACRARIUM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (29, 'RIVERNE_SITE_B01')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (30, 'RIVERNE_SITE_A01')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (31, 'MONARCH_LINN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (32, 'SEALIONS_DEN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (33, 'ALTAIEU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (34, 'GRAND_PALACE_OF_HUXZOI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (35, 'THE_GARDEN_OF_RUHMET')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (36, 'EMPYREAL_PARADOX')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (37, 'TEMENOS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (38, 'APOLLYON')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (39, 'DYNAMIS_VALKURM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (40, 'DYNAMIS_BUBURIMU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (41, 'DYNAMIS_QUFIM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (42, 'DYNAMIS_TAVNAZIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (43, 'DIORAMA_ABDHALJS_GHELSBA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (44, 'ABDHALJS_ISLE_PURGONORGO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (45, 'ABYSSEA_TAHRONGI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (46, 'OPEN_SEA_ROUTE_TO_AL_ZAHBI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (47, 'OPEN_SEA_ROUTE_TO_MHAURA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (48, 'AL_ZAHBI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (49, '49')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (50, 'AHT_URHGAN_WHITEGATE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (51, 'WAJAOM_WOODLANDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (52, 'BHAFLAU_THICKETS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (53, 'NASHMAU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (54, 'ARRAPAGO_REEF')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (55, 'ILRUSI_ATOLL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (56, 'PERIQIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (57, 'TALACCA_COVE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (58, 'SILVER_SEA_ROUTE_TO_NASHMAU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (59, 'SILVER_SEA_ROUTE_TO_AL_ZAHBI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (60, 'THE_ASHU_TALIF')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (61, 'MOUNT_ZHAYOLM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (62, 'HALVUNG')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (63, 'LEBROS_CAVERN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (64, 'NAVUKGO_EXECUTION_CHAMBER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (65, 'MAMOOK')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (66, 'MAMOOL_JA_TRAINING_GROUNDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (67, 'JADE_SEPULCHER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (68, 'AYDEEWA_SUBTERRANE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (69, 'LEUJAOAM_SANCTUM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (70, 'CHOCOBO_CIRCUIT')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (71, 'THE_COLOSSEUM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (72, 'ALZADAAL_UNDERSEA_RUINS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (73, 'ZHAYOLM_REMNANTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (74, 'ARRAPAGO_REMNANTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (75, 'BHAFLAU_REMNANTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (76, 'SILVER_SEA_REMNANTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (77, 'NYZUL_ISLE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (78, 'HAZHALM_TESTING_GROUNDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (79, 'CAEDARVA_MIRE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (80, 'SOUTHERN_SAN_DORIA_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (81, 'EAST_RONFAURE_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (82, 'JUGNER_FOREST_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (83, 'VUNKERL_INLET_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (84, 'BATALLIA_DOWNS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (85, 'LA_VAULE_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (86, 'EVERBLOOM_HOLLOW')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (87, 'BASTOK_MARKETS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (88, 'NORTH_GUSTABERG_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (89, 'GRAUBERG_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (90, 'PASHHOW_MARSHLANDS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (91, 'ROLANBERRY_FIELDS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (92, 'BEADEAUX_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (93, 'RUHOTZ_SILVERMINES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (94, 'WINDURST_WATERS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (95, 'WEST_SARUTABARUTA_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (96, 'FORT_KARUGO_NARUGO_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (97, 'MERIPHATAUD_MOUNTAINS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (98, 'SAUROMUGUE_CHAMPAIGN_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (99, 'CASTLE_OZTROJA_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (100, 'WEST_RONFAURE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (101, 'EAST_RONFAURE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (102, 'LA_THEINE_PLATEAU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (103, 'VALKURM_DUNES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (104, 'JUGNER_FOREST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (105, 'BATALLIA_DOWNS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (106, 'NORTH_GUSTABERG')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (107, 'SOUTH_GUSTABERG')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (108, 'KONSCHTAT_HIGHLANDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (109, 'PASHHOW_MARSHLANDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (110, 'ROLANBERRY_FIELDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (111, 'BEAUCEDINE_GLACIER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (112, 'XARCABARD')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (113, 'CAPE_TERIGGAN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (114, 'EASTERN_ALTEPA_DESERT')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (115, 'WEST_SARUTABARUTA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (116, 'EAST_SARUTABARUTA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (117, 'TAHRONGI_CANYON')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (118, 'BUBURIMU_PENINSULA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (119, 'MERIPHATAUD_MOUNTAINS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (120, 'SAUROMUGUE_CHAMPAIGN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (121, 'THE_SANCTUARY_OF_ZITAH')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (122, 'ROMAEVE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (123, 'YUHTUNGA_JUNGLE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (124, 'YHOATOR_JUNGLE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (125, 'WESTERN_ALTEPA_DESERT')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (126, 'QUFIM_ISLAND')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (127, 'BEHEMOTHS_DOMINION')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (128, 'VALLEY_OF_SORROWS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (129, 'GHOYUS_REVERIE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (130, 'RUAUN_GARDENS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (131, 'MORDION_GAOL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (132, 'ABYSSEA_LA_THEINE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (133, 'OUTER_RAKAZNAR_U2')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (134, 'DYNAMIS_BEAUCEDINE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (135, 'DYNAMIS_XARCABARD')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (136, 'BEAUCEDINE_GLACIER_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (137, 'XARCABARD_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (138, 'CASTLE_ZVAHL_BAILEYS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (139, 'HORLAIS_PEAK')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (140, 'GHELSBA_OUTPOST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (141, 'FORT_GHELSBA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (142, 'YUGHOTT_GROTTO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (143, 'PALBOROUGH_MINES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (144, 'WAUGHROON_SHRINE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (145, 'GIDDEUS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (146, 'BALGAS_DAIS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (147, 'BEADEAUX')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (148, 'QULUN_DOME')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (149, 'DAVOI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (150, 'MONASTIC_CAVERN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (151, 'CASTLE_OZTROJA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (152, 'ALTAR_ROOM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (153, 'THE_BOYAHDA_TREE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (154, 'DRAGONS_AERY')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (155, 'CASTLE_ZVAHL_KEEP_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (156, 'THRONE_ROOM_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (157, 'MIDDLE_DELKFUTTS_TOWER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (158, 'UPPER_DELKFUTTS_TOWER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (159, 'TEMPLE_OF_UGGALEPIH')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (160, 'DEN_OF_RANCOR')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (161, 'CASTLE_ZVAHL_BAILEYS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (162, 'CASTLE_ZVAHL_KEEP')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (163, 'SACRIFICIAL_CHAMBER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (164, 'GARLAIGE_CITADEL_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (165, 'THRONE_ROOM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (166, 'RANGUEMONT_PASS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (167, 'BOSTAUNIEUX_OUBLIETTE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (168, 'CHAMBER_OF_ORACLES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (169, 'TORAIMARAI_CANAL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (170, 'FULL_MOON_FOUNTAIN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (171, 'CRAWLERS_NEST_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (172, 'ZERUHN_MINES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (173, 'KORROLOKA_TUNNEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (174, 'KUFTAL_TUNNEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (175, 'THE_ELDIEME_NECROPOLIS_S')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (176, 'SEA_SERPENT_GROTTO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (177, 'VELUGANNON_PALACE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (178, 'THE_SHRINE_OF_RUAVITAU')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (179, 'STELLAR_FULCRUM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (180, 'LALOFF_AMPHITHEATER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (181, 'THE_CELESTIAL_NEXUS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (182, 'WALK_OF_ECHOES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (183, 'MAQUETTE_ABDHALJS_LEGION_A')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (184, 'LOWER_DELKFUTTS_TOWER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (185, 'DYNAMIS_SAN_DORIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (186, 'DYNAMIS_BASTOK')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (187, 'DYNAMIS_WINDURST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (188, 'DYNAMIS_JEUNO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (189, '189')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (190, 'KING_RANPERRES_TOMB')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (191, 'DANGRUF_WADI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (192, 'INNER_HORUTOTO_RUINS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (193, 'ORDELLES_CAVES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (194, 'OUTER_HORUTOTO_RUINS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (195, 'THE_ELDIEME_NECROPOLIS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (196, 'GUSGEN_MINES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (197, 'CRAWLERS_NEST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (198, 'MAZE_OF_SHAKHRAMI')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (199, '199')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (200, 'GARLAIGE_CITADEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (201, 'CLOISTER_OF_GALES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (202, 'CLOISTER_OF_STORMS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (203, 'CLOISTER_OF_FROST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (204, 'FEIYIN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (205, 'IFRITS_CAULDRON')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (206, 'QUBIA_ARENA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (207, 'CLOISTER_OF_FLAMES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (208, 'QUICKSAND_CAVES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (209, 'CLOISTER_OF_TREMORS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (210, 'GM_HOME')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (211, 'CLOISTER_OF_TIDES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (212, 'GUSTAV_TUNNEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (213, 'LABYRINTH_OF_ONZOZO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (214, '214')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (215, 'ABYSSEA_ATTOHWA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (216, 'ABYSSEA_MISAREAUX')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (217, 'ABYSSEA_VUNKERL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (218, 'ABYSSEA_ALTEPA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (219, '219')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (220, 'SHIP_BOUND_FOR_SELBINA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (221, 'SHIP_BOUND_FOR_MHAURA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (222, 'PROVENANCE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (223, 'SAN_DORIA_JEUNO_AIRSHIP')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (224, 'BASTOK_JEUNO_AIRSHIP')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (225, 'WINDURST_JEUNO_AIRSHIP')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (226, 'KAZHAM_JEUNO_AIRSHIP')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (227, 'SHIP_BOUND_FOR_SELBINA_PIRATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (228, 'SHIP_BOUND_FOR_MHAURA_PIRATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (229, 'THRONE_ROOM_V')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (230, 'SOUTHERN_SANDORIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (231, 'NORTHERN_SANDORIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (232, 'PORT_SANDORIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (233, 'CHATEAU_DORAGUILLE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (234, 'BASTOK_MINES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (235, 'BASTOK_MARKETS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (236, 'PORT_BASTOK')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (237, 'METALWORKS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (238, 'WINDURST_WATERS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (239, 'WINDURST_WALLS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (240, 'PORT_WINDURST')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (241, 'WINDURST_WOODS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (242, 'HEAVENS_TOWER')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (243, 'RULUDE_GARDENS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (244, 'UPPER_JEUNO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (245, 'LOWER_JEUNO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (246, 'PORT_JEUNO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (247, 'RABAO')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (248, 'SELBINA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (249, 'MHAURA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (250, 'KAZHAM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (251, 'HALL_OF_THE_GODS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (252, 'NORG')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (253, 'ABYSSEA_ULEGUERAND')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (254, 'ABYSSEA_GRAUBERG')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (255, 'ABYSSEA_EMPYREAL_PARADOX')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (256, 'WESTERN_ADOULIN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (257, 'EASTERN_ADOULIN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (258, 'RALA_WATERWAYS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (259, 'RALA_WATERWAYS_U')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (260, 'YAHSE_HUNTING_GROUNDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (261, 'CEIZAK_BATTLEGROUNDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (262, 'FORET_DE_HENNETIEL')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (263, 'YORCIA_WEALD')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (264, 'YORCIA_WEALD_U')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (265, 'MORIMAR_BASALT_FIELDS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (266, 'MARJAMI_RAVINE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (267, 'KAMIHR_DRIFTS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (268, 'SIH_GATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (269, 'MOH_GATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (270, 'CIRDAS_CAVERNS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (271, 'CIRDAS_CAVERNS_U')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (272, 'DHO_GATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (273, 'WOH_GATES')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (274, 'OUTER_RAKAZNAR')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (275, 'OUTER_RAKAZNAR_U1')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (276, 'RAKAZNAR_INNER_COURT')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (277, 'RAKAZNAR_TURRIS')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (278, 'GWORA_CORRIDOR')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (279, 'WALK_OF_ECHOES_P2')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (280, 'MOG_GARDEN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (281, 'LEAFALLIA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (282, 'MOUNT_KAMIHR')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (283, 'SILVER_KNIFE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (284, 'CELENNIA_MEMORIAL_LIBRARY')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (285, 'FERETORY')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (286, '286')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (287, 'MAQUETTE_ABDHALJS_LEGION_B')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (288, 'ESCHA_ZITAH')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (289, 'ESCHA_RUAUN')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (290, 'DESUETIA_EMPYREAL_PARADOX')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (291, 'REISENJIMA')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (292, 'REISENJIMA_HENGE')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (293, 'REISENJIMA_SANCTORIUM')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (294, 'DYNAMIS_SAN_DORIA_D')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (295, 'DYNAMIS_BASTOK_D')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (296, 'DYNAMIS_WINDURST_D')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (297, 'DYNAMIS_JEUNO_D')")
    cursor.execute("INSERT OR REPLACE INTO zone_names VALUES (298, 'WALK_OF_ECHOES_P1')")

    print("Testing weather_names:")
    cursor.execute("SELECT * FROM weather_names LIMIT 5")
    for entry in cursor.fetchall():
        print(entry)
    print("")

    print("Testing zone_names:")
    cursor.execute("SELECT * FROM zone_names LIMIT 5")
    for entry in cursor.fetchall():
        print(entry)
    print("")

    print("Testing weather_data:")
    cursor.execute("""
        SELECT zone_names.name, weather_names.name, DATETIME(weather_data.timestamp, 'unixepoch'), weather_data.submitter
        FROM weather_data
        LEFT JOIN zone_names on zone_names.zone = weather_data.zone
        LEFT JOIN weather_names on weather_names.weather = weather_data.weather
        ORDER BY weather_data.timestamp DESC
        LIMIT 5
    """)
    for entry in cursor.fetchall():
        print(entry)
    print("")

    cursor.close()


@app.route("/weather", methods=["PUT","POST"])
def weather_put_post_handler():
    data = request.data.decode("utf-8")
    parts = data.split(",")

    zone = int(parts[0])
    weather = int(parts[1])
    timestamp = int(parts[2])

    sha = hashlib.sha256()
    sha.update(str(hash(request.access_route[-1])).encode('utf-8'))
    submitter = sha.digest().hex()

    insert_weather(zone, weather, timestamp, submitter)

    return "WeatherReporter::Success", 200


@app.route("/weather", methods=["GET"])
def weather_get_handler():
    global get_data
    return get_data, 200


@app.route("/", methods=["GET"])
def main_get_handler():
    return "Success", 200


if __name__ == "__main__":
    connection = sqlite3.connect("db.sqlite", isolation_level=None)
    connection.execute('pragma journal_mode=wal;') # Only needs to be specified once per sqlite db file

    execute("CREATE TABLE IF NOT EXISTS weather_data (zone SMALLINT, weather TINYINT, timestamp BIGINT, submitter TEXT)")
    execute("DROP INDEX IF EXISTS idx_weather_data_zone")
    execute("CREATE UNIQUE INDEX idx_weather_data_zone ON weather_data(zone)")

    execute("CREATE TABLE IF NOT EXISTS weather_names (weather TINYINT, name TEXT)")
    execute("DROP INDEX IF EXISTS idx_weather_names_weather")
    execute("CREATE UNIQUE INDEX idx_weather_names_weather ON weather_names(weather)")

    execute("CREATE TABLE IF NOT EXISTS zone_names (zone SMALLINT, name TEXT)")
    execute("DROP INDEX IF EXISTS idx_zone_names_zone")
    execute("CREATE UNIQUE INDEX idx_zone_names_zone ON zone_names(zone)")

    insert_static_data()

    update_get_data()

    app.run(port=80, host="0.0.0.0")
