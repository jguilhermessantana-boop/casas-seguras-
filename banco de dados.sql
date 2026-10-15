CREATE DATABASE casa_segura;

USE casa_segura;

CREATE TABLE morador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    localizacao VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE deteccao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    descricao VARCHAR(100),
    FOREIGN KEY (id_sensor) REFERENCES sensor(id)
);

CREATE TABLE alerta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_morador INT,
    id_deteccao INT,
    mensagem VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (id_morador) REFERENCES morador(id),
    FOREIGN KEY (id_deteccao) REFERENCES deteccao(id)
);


INSERT INTO morador (nome, telefone) VALUES
('Carlos', '64999990001'),
('Mariana', '64999990002');

INSERT INTO sensor (tipo, localizacao, status) VALUES
('Movimento', 'Sala', 'Ativo'),
('Magnetico', 'Porta', 'Ativo'),
('Magnetico', 'Janela', 'Ativo');

INSERT INTO deteccao (id_sensor, descricao) VALUES
(1, 'Movimento na sala'),
(2, 'Porta aberta'),
(3, 'Janela aberta');

INSERT INTO alerta (id_morador, id_deteccao, mensagem, status) VALUES
(1, 1, 'Movimento detectado', 'Enviado'),
(1, 2, 'Porta aberta', 'Enviado'),
(2, 3, 'Janela aberta', 'Pendente');

SELECT * FROM morador;
SELECT * FROM sensor;
SELECT * FROM deteccao;
SELECT * FROM alerta;



