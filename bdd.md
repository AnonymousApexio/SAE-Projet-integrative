Etapes de créations de la BDD sur la machine Windows 11.

1. Installation de MySQL : 

https://dev.mysql.com/downloads/installer/

Suivre le processus d'installation puis lancer MySQL -> mysqlsh.exe 

2. Création de la BDD : 

CREATE DATABASE sae24
Table des capteurs : 

CREATE TABLE capteurs (
    id_capteur VARCHAR(20) PRIMARY KEY,
    nom_capteur VARCHAR(50) UNIQUE NOT NULL,
    piece VARCHAR(50),
    emplacement VARCHAR(100)
);

Table des données : 

CREATE TABLE donnees (
    id_donnee INT AUTO_INCREMENT PRIMARY KEY,
    id_capteur VARCHAR(20),
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_capteur) REFERENCES capteurs(id_capteur) ON DELETE CASCADE
);


Index pour les filtres : 

CREATE INDEX idx_timestamp ON donnees(timestamp);
CREATE INDEX idx_id_capteur ON donnees(id_capteur);

Lien 1 <> N : un capteur peut avoir plusieurs données.


Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
