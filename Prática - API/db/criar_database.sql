CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT(200) NOT NULL,
    telefone TEXT(11) NOT NULL UNIQUE,
    data_criado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modificado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emails (
    id_email INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_cliente INTEGER NOT NULL,
    email TEXT(120) NOT NULL,
    is_main BOOLEAN DEFAULT FALSE,
    data_criado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modificado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
);

CREATE TABLE enderecos (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tipo_logradouro TEXT(120) NOT NULL,
    nome_logradouro TEXT(255) NOT NULL,
    numero INTEGER,
    complemento TEXT(120),
    bairro TEXT(120) NOT NULL,
    cep TEXT(8) NOT NULL,
    cidade TEXT(120) NOT NULL,
    sigla_UF TEXT(2) NOT NULL,
    país TEXT(120) NOT NULL,
    is_main BOOLEAN DEFAULT FALSE,
    data_criado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modificado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cliente_endereco (
    id_cliente INTEGER NOT NULL,
    id_endereco INTEGER NOT NULL,
    PRIMARY KEY (id_cliente, id_endereco),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_endereco) REFERENCES enderecos(id_endereco) ON DELETE RESTRICT
);