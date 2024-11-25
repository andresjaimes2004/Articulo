import sqlite3 from 'sqlite3'
import { DATABASE_URL } from '../../config/config.js'
const { Database } = sqlite3
const conexionDB = new Database(DATABASE_URL)

class UserModel {
  static async searchUserById ({ NumeroDocumento }) {
    return new Promise((resolve, reject) => {
      const query = 'SELECT * FROM usuario WHERE id = ?'
      conexionDB.get(query, [NumeroDocumento], (err, row) => {
        if (err) {
          reject(err)
        } else {
          resolve(row || null)
        }
      })
    })
  }

  static async listUsers () {
    return new Promise((resolve, reject) => {
      const query = 'SELECT * FROM usuario'
      conexionDB.all(query, [], (err, rows) => {
        if (err) {
          reject(err)
        } else {
          resolve(rows)
        }
      })
    })
  }

  static async insertUser ({
    tipoDocumento,
    nombres,
    apellidos,
    municipio,
    departamento,
    antecedentes
  }) {
    return new Promise((resolve, reject) => {
      const query = `
        INSERT INTO usuario (tipo_documento, nombre, apellidos, municipio, departamento, antecedentes)
        VALUES (?, ?, ?, ?, ?, ?)
      `
      conexionDB.run(
        query,
        [tipoDocumento, nombres, apellidos, municipio, departamento, antecedentes],
        function (err) {
          if (err) {
            reject(err)
          } else {
            resolve(this.lastID)
          }
        }
      )
    })
  }
}

export default UserModel
