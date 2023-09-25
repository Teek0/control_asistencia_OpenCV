-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema attend_bd
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema attend_bd
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `attend_bd` DEFAULT CHARACTER SET utf8 ;
USE `attend_bd` ;

-- -----------------------------------------------------
-- Table `attend_bd`.`cursos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attend_bd`.`cursos` (
  `idcurso` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `codigo` VARCHAR(45) NOT NULL,
  `seccion` VARCHAR(45) NOT NULL,
  `creado` DATETIME NOT NULL DEFAULT NOW(),
  `editado` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`idcurso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `attend_bd`.`alumnos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attend_bd`.`alumnos` (
  `idalumno` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `rut` INT(9) NOT NULL,
  `digito_verificador` CHAR(1) NOT NULL,
  `ruta_archivo` VARCHAR(500) NOT NULL,
  `creado` DATETIME NOT NULL DEFAULT NOW(),
  `editado` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`idalumno`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `attend_bd`.`listado_asistencias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attend_bd`.`listado_asistencias` (
  `curso_idcurso` INT NOT NULL,
  `alumno_idalumno` INT NOT NULL,
  `fecha` DATETIME NOT NULL,
  `asiste` TINYINT NOT NULL,
  PRIMARY KEY (`curso_idcurso`, `alumno_idalumno`),
  INDEX `fk_curso_has_alumno_alumno1_idx` (`alumno_idalumno` ASC) VISIBLE,
  INDEX `fk_curso_has_alumno_curso_idx` (`curso_idcurso` ASC) VISIBLE,
  CONSTRAINT `fk_curso_has_alumno_curso`
    FOREIGN KEY (`curso_idcurso`)
    REFERENCES `attend_bd`.`cursos` (`idcurso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_curso_has_alumno_alumno1`
    FOREIGN KEY (`alumno_idalumno`)
    REFERENCES `attend_bd`.`alumnos` (`idalumno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `attend_bd`.`docentes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attend_bd`.`docentes` (
  `idprofesor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `usuario` VARCHAR(30) NOT NULL,
  `password` VARCHAR(30) NOT NULL,
  `creado` DATETIME NOT NULL DEFAULT NOW(),
  `editado` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `cursos_idcurso` INT NOT NULL,
  PRIMARY KEY (`idprofesor`),
  INDEX `fk_docentes_cursos1_idx` (`cursos_idcurso` ASC) VISIBLE,
  CONSTRAINT `fk_docentes_cursos1`
    FOREIGN KEY (`cursos_idcurso`)
    REFERENCES `attend_bd`.`cursos` (`idcurso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `attend_bd`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attend_bd`.`admin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(30) NOT NULL,
  `password` VARCHAR(30) NOT NULL,
  `creado` DATETIME NOT NULL DEFAULT NOW(),
  `editado` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;