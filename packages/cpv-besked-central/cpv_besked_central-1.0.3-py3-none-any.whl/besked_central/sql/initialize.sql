INSERT INTO roles (id) VALUES ('admin');
INSERT INTO roles (id) VALUES ('controller');
INSERT INTO roles (id) VALUES ('user');
INSERT INTO roles (id) VALUES ('api');

INSERT INTO departments (id, department_name) VALUES ('CPV', 'CP Viborg');
INSERT INTO departments (id, department_name) VALUES ('CPS', 'CP Silkeborg');
INSERT INTO departments (id, department_name) VALUES ('CPB', 'CP Bjerringbro');

INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', '_Gargamel_',
    'Kanon og katapult - kugle starter fra mindstorms kran');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Esge',
    'Simpel postkasse til HTML workshop - forår 2024');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Rasmus',
    'Simpel postkasse til HTML workshop - forår 2024');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Magnus',
    'Simpel postkasse til HTML workshop - forår 2024');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Paola',
    'Simpel postkasse til HTML workshop - forår 2024');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Holger',
    'Simpel postkasse til HTML workshop - forår 2024');
INSERT INTO tracks(department_id, track_name, description) VALUES ('CPV', 'Anton',
    'Simpel postkasse til HTML workshop - forår 2024');

INSERT INTO tracks(department_id, track_name, description) VALUES ('CPB', '_Gammelsmølf_',
    'Rundt på NVH - kugle starter fra 3. sal');

INSERT INTO tracks(department_id, track_name, description) VALUES ('CPS', '_Astrosmølf_',
    'Månebanen - kuglen skubbes igang af en rover');

INSERT INTO commands(id, command_name) VALUES ('START', 'Start kugle');
INSERT INTO commands(id, command_name) VALUES ('FORTRYD', 'Glem alle tidligere sende kommandoer');
INSERT INTO commands(id, command_name) VALUES ('BESKED', 'Brug events som en simpel postbesked (HTML workshop forår 2024)');

-- 'pbkdf2:sha256:260000$AcUv89QijOGpiHUx$522ee04209932020830214d70bc2775e1e5a80b95793a27b3f3826f0a3d40897'

-- admin
INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Esge', 'pbkdf2:sha256:260000$ru6pGUZMg3zU4uKm$5539ac9686ea7f35b1cf20eb48f190f5ca77620e96d4ffc7701a2e124d6faa40', 
'admin', 
'CPV');

-- CPV

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cpv', 'pbkdf2:sha256:260000$v9DFCaf3Ut0Wz7fX$af259509cd0b312fc54d0759b95eceb8450a80f181988d6c8bd99d88e53192ee', 
'controller', 
'CPV');

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cpv pirat', 'pbkdf2:sha256:260000$AcUv89QijOGpiHUx$522ee04209932020830214d70bc2775e1e5a80b95793a27b3f3826f0a3d40897', 
'user', 
'CPV');

-- CPB

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cpb', 'pbkdf2:sha256:260000$ZrelelkxyRRZ2A58$c4a5e4059b72093064956eab027c1075e48ecce9ec2a8172383a180b26e8f425', 
'controller', 
'CPB');

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cpb pirat', 'pbkdf2:sha256:260000$AcUv89QijOGpiHUx$522ee04209932020830214d70bc2775e1e5a80b95793a27b3f3826f0a3d40897', 
'user', 
'CPB');

-- CPS

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cps', 'pbkdf2:sha256:260000$JFPGUcGHKAwaw6mW$bf5e9d409388a5d5bd8f25356a1f37c39650640f390337c31afa817f185b8f9b', 
'controller', 
'CPS');

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('Cps pirat', 'pbkdf2:sha256:260000$AcUv89QijOGpiHUx$522ee04209932020830214d70bc2775e1e5a80b95793a27b3f3826f0a3d40897', 
'user', 
'CPS');

-- API Users
INSERT INTO users (username, password, role_id, department_id) 
VALUES ('CpvApi', 'pbkdf2:sha256:260000$sx8aADuLmbBe3txV$4c1092ca16da3dc8620f6b11210d9feabad1c494f69433f6a9cda5abb3d5f346', 
'api', 
'CPV');

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('CpbApi', 'pbkdf2:sha256:260000$JP5GVm9AF2z3K4Un$a5fefd0c75f314bb5ad0f17e22b86b6d68f02de381f2044b7af74aa82e2ed7ed', 
'api', 
'CPB');

INSERT INTO users (username, password, role_id, department_id) 
VALUES ('CpsApi', 'pbkdf2:sha256:260000$j0DGGZ8HCHm4jucu$c8d2833ab65ab620490185f9c948748aee34427c9480aa62b0088f340b4c2ee2', 
'api', 
'CPS');

